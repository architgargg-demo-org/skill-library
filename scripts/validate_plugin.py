"""Validate the library's plugin packaging and desktop installation links."""

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class InstallLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = {}

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and attributes.get("id") in {
            "add-marketplace",
            "install-plugin",
        }:
            link_id = attributes["id"]
            if link_id in self.links:
                raise ValueError(f"Duplicate install link: {link_id}")
            self.links[link_id] = attributes.get("href", "")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(root=ROOT):
    plugin = json.loads((root / "plugin.json").read_text())
    marketplace = json.loads(
        (root / ".github/plugin/marketplace.json").read_text()
    )
    require(plugin["name"] == "architgargg-test-plugin", "Unexpected plugin name")
    require(
        marketplace["name"] == "architgargg-skill-library",
        "Unexpected marketplace name",
    )
    require(
        plugin.get("skills") == ["./skills/"],
        "The plugin must include the entire canonical skills directory",
    )
    require(len(marketplace["plugins"]) == 1, "Expected one library plugin")
    entry = marketplace["plugins"][0]
    require(entry["name"] == plugin["name"], "Plugin names do not match")
    require(entry["version"] == plugin["version"], "Plugin versions do not match")
    require(entry["source"] == "./", "Plugin source must be the repository root")

    skills_dir = root / "skills"
    skills = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    require(bool(skills), "The plugin must ship at least one skill")
    for skill in skills:
        require(
            (skill / "SKILL.md").is_file(),
            f"Skill directory is missing SKILL.md: {skill.name}",
        )
    require(
        (skills_dir / "skill-library-smoke-test/SKILL.md").is_file(),
        "The documented smoke-test skill is missing",
    )

    page = (root / "docs/index.html").read_text()
    parser = InstallLinks()
    parser.feed(page)
    expected = {
        "add-marketplace": (
            "plugins",
            "/marketplace/add",
            "architgargg-demo-org/skill-library",
        ),
        "install-plugin": (
            "plugins",
            "/install",
            f'{plugin["name"]}@{marketplace["name"]}',
        ),
    }
    for link_id, (host, path, source) in expected.items():
        require(link_id in parser.links, f"Missing install link: {link_id}")
        url = urlsplit(parser.links[link_id])
        require(
            (url.scheme, url.netloc, url.path, url.fragment)
            == ("ghapp", host, path, ""),
            f"Incorrect app route: {link_id}",
        )
        require(
            parse_qs(url.query, keep_blank_values=True) == {"source": [source]},
            f"Incorrect install source: {link_id}",
        )
    for command in (
        "copilot plugin marketplace add architgargg-demo-org/skill-library",
        f'copilot plugin install {plugin["name"]}@{marketplace["name"]}',
    ):
        require(command in page, f"Missing CLI fallback: {command}")
    return [skill.name for skill in skills]


if __name__ == "__main__":
    names = validate()
    print(f"Validated marketplace, plugin, install links, and {len(names)} skill(s):")
    print("\n".join(names))
