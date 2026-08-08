"""Install and behaviour checks for the Pi coding agent.

Install globally first:

    pi install git:github.com/nickali/remove-ai-writing-indicators

Then:

    python3 -m unittest tests.test_pi                    # structure + install
    SKILL_AGENT_TESTS=1 python3 -m unittest tests.test_pi  # plus all four modes
"""

import json
import shutil
import unittest
from pathlib import Path

from harness import SKILL_NAME, ModeChecks, StructureChecks, agent_tests

PI_HOME = Path.home() / ".pi" / "agent"
PI_SETTINGS = PI_HOME / "settings.json"
PI_CLONE = PI_HOME / "git" / "github.com" / "nickali" / SKILL_NAME


class TestPi(unittest.TestCase, StructureChecks, ModeChecks):
    harness_name = "pi"

    def build_command(self, prompt):
        return ["pi", "-p", "--no-session", prompt]

    # --- structure ------------------------------------------------------

    def test_repo_is_a_valid_plugin(self):
        self.assert_repo_is_a_valid_plugin()

    def test_npm_and_plugin_versions_agree(self):
        self.assert_npm_and_plugin_versions_agree()

    def test_skill_files_present(self):
        self.assert_skill_files_present()

    def test_no_cross_skill_references(self):
        self.assert_no_cross_skill_references()

    def test_fixture_and_answers_are_separate(self):
        self.assert_fixture_and_answers_are_separate()

    # --- install --------------------------------------------------------

    def test_pi_is_installed(self):
        self.assertIsNotNone(shutil.which("pi"), "pi is not on PATH")

    def test_skill_registered_globally(self):
        self.assertTrue(PI_SETTINGS.is_file(), f"no Pi settings at {PI_SETTINGS}")
        packages = json.loads(PI_SETTINGS.read_text()).get("packages", [])
        matching = [p for p in packages if SKILL_NAME in p]
        self.assertTrue(
            matching,
            f"{SKILL_NAME} not in Pi's global packages. "
            f"Run: pi install git:github.com/nickali/{SKILL_NAME}",
        )

    def test_skill_files_reached_the_clone(self):
        skill_md = PI_CLONE / "skills" / SKILL_NAME / "SKILL.md"
        self.assertTrue(
            skill_md.is_file(),
            f"expected the installed skill at {skill_md}. Run: pi update git:github.com/nickali/{SKILL_NAME}",
        )

    # --- behaviour ------------------------------------------------------

    @agent_tests
    def test_detect_mode(self):
        self.check_detect()

    @agent_tests
    def test_suggest_mode(self):
        self.check_suggest()

    @agent_tests
    def test_edit_mode(self):
        self.check_edit()

    @agent_tests
    def test_rewrite_mode_increments_filename(self):
        self.check_rewrite_increments()


if __name__ == "__main__":
    unittest.main()
