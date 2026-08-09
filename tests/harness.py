"""Shared helpers for the harness test suites.

Two kinds of check live here.

Structural checks are deterministic and free: does the repo have the files a
plugin needs, is the JSON valid, is the skill registered with the harness.

Behavioural checks drive a real agent, so they are slow, cost tokens, and
cannot assert on exact wording. They assert on the things that are actually
deterministic: which files got written, which files did not, whether the source
survived, and whether the mode banner and group headings appear at all.

Behavioural checks are skipped unless SKILL_AGENT_TESTS=1 is set.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "remove-ai-writing-indicators"
SKILL_DIR = REPO_ROOT / "skills" / SKILL_NAME
FIXTURE = REPO_ROOT / "examples" / "slop-draft.md"

GROUP_NAMES = ["Surface", "Structure", "Voice", "Substance"]

# One agent run can take several minutes on a slow provider.
AGENT_TIMEOUT = 600

PROMPT = (
    "Use the {skill} skill in {mode} mode on slop-draft.md. "
    "Read only that file."
)

agent_tests = unittest.skipUnless(
    os.environ.get("SKILL_AGENT_TESTS") == "1",
    "set SKILL_AGENT_TESTS=1 to run agent-driven tests (slow, costs tokens)",
)


def needs_harness(binary):
    """Skip when the harness is absent rather than failing.

    "Is the skill installed here" is a question about this machine. On a CI
    runner with no harness the honest answer is "not applicable", while on a
    laptop that has the harness a missing install is a real failure.
    """
    return unittest.skipUnless(
        shutil.which(binary),
        f"{binary} is not on PATH, so there is no install to check",
    )


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


class StructureChecks:
    """Repo-level checks that hold regardless of which harness runs the skill."""

    def assert_repo_is_a_valid_plugin(self):
        marketplace = REPO_ROOT / ".claude-plugin" / "marketplace.json"
        plugin = REPO_ROOT / ".claude-plugin" / "plugin.json"

        self.assertTrue(marketplace.is_file(), "missing .claude-plugin/marketplace.json")
        self.assertTrue(plugin.is_file(), "missing .claude-plugin/plugin.json")

        m = load_json(marketplace)
        p = load_json(plugin)

        self.assertEqual(m["name"], SKILL_NAME)
        self.assertEqual(p["name"], SKILL_NAME)

        # The local plugin cache is keyed by version. Without this field an
        # install lands in a directory called "unknown" and updates cannot be
        # told apart.
        self.assertIn("version", p, "plugin.json must declare a version")

        sources = [entry["source"] for entry in m["plugins"]]
        self.assertIn("./", sources, "marketplace must point at the repo root")

    def assert_npm_and_plugin_versions_agree(self):
        """The version lives in two manifests and must not drift.

        Claude Code keys its plugin cache off .claude-plugin/plugin.json.
        Pi's catalog and npm updates key off package.json. Nothing keeps them
        in sync automatically.
        """
        pkg = REPO_ROOT / "package.json"
        self.assertTrue(pkg.is_file(), "missing package.json")

        p = load_json(pkg)
        plugin = load_json(REPO_ROOT / ".claude-plugin" / "plugin.json")

        self.assertEqual(p["name"], SKILL_NAME)
        self.assertEqual(
            p["version"],
            plugin["version"],
            "package.json and plugin.json versions have drifted",
        )
        self.assertIn(
            "pi-package",
            p.get("keywords", []),
            "the pi-package keyword is what lists this in the Pi catalog",
        )
        self.assertEqual(p.get("pi", {}).get("skills"), ["./skills"])

        # A dependency here would make `pi install` do real work on every
        # install and update, for a package that is only markdown.
        self.assertNotIn("dependencies", p, "this package must stay dependency-free")

    def assert_skill_files_present(self):
        skill_md = SKILL_DIR / "SKILL.md"
        indicators = SKILL_DIR / "indicators.md"

        self.assertTrue(skill_md.is_file(), f"missing {skill_md}")
        self.assertTrue(indicators.is_file(), f"missing {indicators}")

        text = skill_md.read_text()
        self.assertTrue(text.startswith("---\n"), "SKILL.md needs YAML frontmatter")
        frontmatter = text.split("---", 2)[1]

        # Rules from the Agent Skills specification, as enforced by Pi.
        # https://agentskills.io/specification#frontmatter-required
        name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.M)
        self.assertIsNotNone(name_match, "SKILL.md frontmatter needs a name")
        name = name_match.group(1).strip()
        self.assertEqual(name, SKILL_NAME)
        self.assertLessEqual(len(name), 64, "name may not exceed 64 characters")
        self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$",
                         "name must be lowercase a-z, 0-9 and single hyphens, "
                         "with no leading, trailing or consecutive hyphens")

        # A skill with no description is not loaded at all, so this is the one
        # frontmatter mistake that fails silently rather than warning.
        desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
        self.assertIsNotNone(desc_match, "a skill with no description is never loaded")
        description = desc_match.group(1).strip()
        self.assertLessEqual(len(description), 1024, "description may not exceed 1024 characters")

        catalog = indicators.read_text()
        for group in GROUP_NAMES:
            self.assertIn(f"## {group}", catalog, f"indicators.md missing {group} group")

    def assert_no_cross_skill_references(self):
        """The skill must stand alone. Attribution belongs in the README."""
        for path in (SKILL_DIR / "SKILL.md", SKILL_DIR / "indicators.md"):
            text = path.read_text().lower()
            self.assertNotIn("no-ai-slop", text, f"{path.name} must not reference other skills")

    def assert_fixture_and_answers_are_separate(self):
        """A fixture that ships its own answer key cannot test detection.

        If the expected findings share a context window with the draft, the
        model copies them instead of finding them.
        """
        expected = REPO_ROOT / "examples" / "expected-findings.md"
        self.assertTrue(FIXTURE.is_file())
        self.assertTrue(expected.is_file())

        draft = FIXTURE.read_text()
        for marker in ("Expected", "Machine vocabulary", "Preserve ruling"):
            self.assertNotIn(marker, draft, "answer key leaked into the draft fixture")


class ModeChecks:
    """Behavioural checks driven through a real agent.

    Subclasses provide build_command() and a human-readable harness_name.
    """

    def run_mode(self, mode, workdir):
        """Run one mode, retrying once on a non-zero exit.

        Several agent invocations back to back can fail transiently on rate
        limits or session contention. A single retry separates that from a
        genuine failure without hiding one.
        """
        cmd = self.build_command(PROMPT.format(skill=SKILL_NAME, mode=mode))
        for attempt in (1, 2):
            result = subprocess.run(
                cmd,
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=AGENT_TIMEOUT,
            )
            if result.returncode == 0:
                return result.stdout
            if attempt == 1:
                time.sleep(20)

        self.fail(
            f"{self.harness_name} exited {result.returncode} twice for {mode} mode\n"
            f"{result.stderr[-2000:]}"
        )

    def fresh_workdir(self):
        """A temp directory holding only the draft, so runs cannot see the answers."""
        workdir = Path(tempfile.mkdtemp(prefix="raiwi-"))
        self.addCleanup(shutil.rmtree, workdir, True)
        shutil.copy(FIXTURE, workdir / "slop-draft.md")
        return workdir

    def assert_wrote_nothing(self, workdir, output, banner_word):
        self.assertIn(banner_word, output, f"{banner_word} banner missing from output")
        for group in GROUP_NAMES:
            self.assertIn(group, output, f"output missing {group} findings group")
        files = sorted(p.name for p in workdir.iterdir())
        self.assertEqual(files, ["slop-draft.md"], f"{banner_word} mode must not write files")

    # --- the four modes -------------------------------------------------

    def check_detect(self):
        workdir = self.fresh_workdir()
        before = sha256(workdir / "slop-draft.md")
        output = self.run_mode("detect", workdir)
        self.assert_wrote_nothing(workdir, output, "Detect")
        self.assertEqual(before, sha256(workdir / "slop-draft.md"), "source was modified")

    def check_suggest(self):
        workdir = self.fresh_workdir()
        output = self.run_mode("suggest", workdir)
        self.assert_wrote_nothing(workdir, output, "Suggest")

    def check_edit(self):
        workdir = self.fresh_workdir()
        source = workdir / "slop-draft.md"
        before = sha256(source)

        self.run_mode("edit", workdir)

        produced = workdir / "slop-draft_v2.md"
        self.assertTrue(produced.is_file(), "edit mode did not write slop-draft_v2.md")
        self.assertEqual(before, sha256(source), "edit mode modified the source file")

        # Preserve ruling: the draft is missing an article here and the skill
        # must not fix it. Collapse whitespace first, since the phrase can land
        # across a line break.
        text = produced.read_text()
        flattened = " ".join(text.split())
        self.assertIn(
            "cut attendee list",
            flattened,
            "preserve ruling violated: a missing article was added back",
        )
        self.assertNotIn("—", text, "em dash survived in a draft under 300 words")

    def check_rewrite_increments(self):
        """Rewrite must not clobber an earlier run's output."""
        workdir = self.fresh_workdir()
        taken = workdir / "slop-draft_v2.md"
        taken.write_text("output from an earlier run\n")
        taken_hash = sha256(taken)

        self.run_mode("rewrite", workdir)

        produced = workdir / "slop-draft_v3.md"
        self.assertTrue(
            produced.is_file(),
            "rewrite did not increment past the existing _v2 file",
        )
        self.assertEqual(taken_hash, sha256(taken), "rewrite overwrote the existing _v2 file")
