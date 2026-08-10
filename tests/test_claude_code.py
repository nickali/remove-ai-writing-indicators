"""Install and behaviour checks for Claude Code.

Install first:

    /plugin marketplace add nickali/remove-ai-writing-indicators
    /plugin install remove-ai-writing-indicators@remove-ai-writing-indicators

Then:

    python3 -m unittest tests.test_claude_code                    # structure + install
    SKILL_AGENT_TESTS=1 python3 -m unittest tests.test_claude_code  # plus all four modes
"""

import json
import unittest
from pathlib import Path

from harness import SKILL_NAME, ModeChecks, StructureChecks, agent_tests, needs_harness

CLAUDE_HOME = Path.home() / ".claude"
CLAUDE_SETTINGS = CLAUDE_HOME / "settings.json"
MARKETPLACE_CLONE = CLAUDE_HOME / "plugins" / "marketplaces" / SKILL_NAME
PLUGIN_KEY = f"{SKILL_NAME}@{SKILL_NAME}"


class TestClaudeCode(unittest.TestCase, StructureChecks, ModeChecks):
    harness_name = "claude"

    def build_command(self, prompt):
        # The agent writes files in Edit and Rewrite mode, and the run is
        # non-interactive, so it cannot answer a permission prompt. Every run
        # happens in a throwaway temp directory holding one copy of the draft.
        return ["claude", "-p", "--permission-mode", "bypassPermissions", prompt]

    # --- structure ------------------------------------------------------

    def test_repo_is_a_valid_plugin(self):
        self.assert_repo_is_a_valid_plugin()

    def test_skill_files_present(self):
        self.assert_skill_files_present()

    def test_no_cross_skill_references(self):
        self.assert_no_cross_skill_references()

    def test_fixture_and_answers_are_separate(self):
        self.assert_fixture_and_answers_are_separate()

    def test_surface_phrases_are_in_the_catalogue(self):
        self.assert_surface_phrases_are_in_the_catalogue()

    # --- install --------------------------------------------------------

    @needs_harness("claude")
    def test_plugin_enabled(self):
        self.assertTrue(CLAUDE_SETTINGS.is_file(), f"no settings at {CLAUDE_SETTINGS}")
        enabled = json.loads(CLAUDE_SETTINGS.read_text()).get("enabledPlugins", {})
        self.assertIn(
            PLUGIN_KEY,
            enabled,
            f"{PLUGIN_KEY} is not installed. Run: "
            f"/plugin marketplace add nickali/{SKILL_NAME}",
        )
        self.assertTrue(enabled[PLUGIN_KEY], f"{PLUGIN_KEY} is installed but disabled")

    @needs_harness("claude")
    def test_skill_files_reached_the_marketplace_clone(self):
        skill_md = MARKETPLACE_CLONE / "skills" / SKILL_NAME / "SKILL.md"
        self.assertTrue(
            skill_md.is_file(),
            f"expected the installed skill at {skill_md}. Run: /plugin marketplace update {SKILL_NAME}",
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
    def test_edit_mode_keeps_checklist_members(self):
        self.check_edit_checklist()

    @agent_tests
    def test_rewrite_mode_increments_filename(self):
        self.check_rewrite_increments()


if __name__ == "__main__":
    unittest.main()
