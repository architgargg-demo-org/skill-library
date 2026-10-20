import json
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts.validate_plugin import ROOT, validate


class PluginTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for relative in (
            "plugin.json",
            ".github/plugin/marketplace.json",
            "docs/index.html",
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        shutil.copytree(ROOT / "skills", self.root / "skills")

    def change_json(self, relative, change):
        path = self.root / relative
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def test_repository_is_valid(self):
        self.assertIn("skill-library-smoke-test", validate(self.root))

    def test_new_skills_are_included_without_manifest_edits(self):
        skill = self.root / "skills/another-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: another-skill\ndescription: Another skill.\n---\nInstructions.\n"
        )
        self.assertIn("another-skill", validate(self.root))

    def test_missing_skill_file_is_rejected(self):
        (self.root / "skills/incomplete").mkdir()
        with self.assertRaisesRegex(ValueError, "missing SKILL.md"):
            validate(self.root)

    def test_partial_skill_list_is_rejected(self):
        self.change_json(
            "plugin.json",
            lambda data: data.update(skills=["./skills/skill-library-smoke-test"]),
        )
        with self.assertRaisesRegex(ValueError, "entire canonical skills"):
            validate(self.root)

    def test_mismatched_versions_are_rejected(self):
        self.change_json("plugin.json", lambda data: data.update(version="2.0.0"))
        with self.assertRaisesRegex(ValueError, "versions do not match"):
            validate(self.root)

    def test_wrong_plugin_source_is_rejected(self):
        self.change_json(
            ".github/plugin/marketplace.json",
            lambda data: data["plugins"][0].update(source="./plugins/missing"),
        )
        with self.assertRaisesRegex(ValueError, "repository root"):
            validate(self.root)

    def test_wrong_deep_link_source_is_rejected(self):
        page = self.root / "docs/index.html"
        page.write_text(
            page.read_text().replace(
                "architgargg-test-plugin%40architgargg-skill-library",
                "architgargg-test-plugin%40wrong-marketplace",
            )
        )
        with self.assertRaisesRegex(ValueError, "Incorrect install source"):
            validate(self.root)

    def test_duplicate_query_parameter_is_rejected(self):
        page = self.root / "docs/index.html"
        page.write_text(
            page.read_text().replace(
                "source=architgargg-demo-org%2Fskill-library",
                "source=architgargg-demo-org%2Fskill-library&amp;source=other",
            )
        )
        with self.assertRaisesRegex(ValueError, "Incorrect install source"):
            validate(self.root)


if __name__ == "__main__":
    unittest.main()
