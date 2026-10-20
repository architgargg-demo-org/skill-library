# Contributing

Skills are proposed through pull requests and reviewed before being added to this library.

## Propose a skill

1. Create a directory at `skills/<skill-name>/`.
2. Add a `SKILL.md` that explains the skill's purpose, when it should be used, and the instructions it provides.
3. Add any necessary supporting files in that directory. Keep the skill focused and self-contained.
4. Open a pull request describing the skill, its intended users, and any relevant limitations or dependencies.

Before submitting, check that the skill is clear, useful, and scoped appropriately. Do not include secrets or sensitive information. Disclose any dependencies, external services, or actions that could affect a user's data or environment.

Use YAML frontmatter with `name` (matching the directory name) and `description`
in every `SKILL.md`, so Copilot can discover and select the skill.

Every merged directory under `skills/` is included in `architgargg-test-plugin`
through the root `plugin.json`; do not duplicate skills in another plugin
directory. When changing shipped skills, bump the plugin version in both
`plugin.json` and its `.github/plugin/marketplace.json` entry. Run
`python3 -m unittest discover -s tests -v` and
`python3 scripts/validate_plugin.py` before submitting.

## Review and approval

Maintainers review proposed skills for usefulness, clarity, scope, and safety. They may ask for changes or decline a proposal. A skill is not approved or part of the library until a maintainer approves and merges its pull request. Contributors should not treat an open or unreviewed pull request as an endorsed skill.
