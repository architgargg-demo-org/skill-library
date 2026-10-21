# Skill Library

This repository is a collection of skills proposed by the community and reviewed before they are added to the library. Skills are submitted as pull requests; a skill becomes part of the library only after maintainer approval and merge.

## Repository layout

Each skill belongs in its own directory under `skills/`:

```text
skills/
  skill-name/
    SKILL.md
    ...optional supporting files
```

`SKILL.md` should describe the skill's purpose and explain how and when to use it. Include supporting files only when the skill needs them.

## Install the library as a plugin

The plugin is named **architgargg-test-plugin**. Its root `plugin.json` includes
the entire `skills/` directory, so every library skill ships together, without
copying files into a second plugin directory. The marketplace is named
**architgargg-skill-library** and its catalog lives in
`.github/plugin/marketplace.json`.

There were no merged skills in this repository when the plugin was added.
`skill-library-smoke-test` is the initial sample. Skills in open proposals are
not included until their pull requests are reviewed and merged.

### Desktop app

1. [Download the GitHub Copilot app](https://gh.io/app), install or update it,
   and sign in.
2. Open the install page at
   <https://architgargg-demo-org.github.io/skill-library/>.
3. Click **Add marketplace in Copilot**, allow the browser to open the app,
   review the app's confirmation, and submit the pre-filled add form.
4. Return to the page and click **Install plugin in Copilot**. Review the
   confirmation and submit **Install**. Alternatively, find the plugin in the
   app's plugin-management screen (Settings > Plugins or Customize, depending
   on the app version).
5. Start a new session, check that `skill-library-smoke-test` is listed among
   the available skills, and ask: `Run the skill library smoke test.`
   The expected response is
   `Skill Library smoke test passed: architgargg-test-plugin loaded this skill.`
   Check the skill listing as well; matching text alone does not prove loading.

### What the "one-click install" actually does

The getting-started guide's button **adds a marketplace**, not the desktop app
or all its plugins. A marketplace is a catalog; plugin installation is a
separate operation.

The install page uses two ordinary HTML anchors, with URL-encoded `source`
query parameters:

```text
ghapp://plugins/marketplace/add?source=architgargg-demo-org%2Fskill-library
ghapp://plugins/install?source=architgargg-test-plugin%40architgargg-skill-library
```

The browser hands the `ghapp://` URL to the desktop app registered for that
scheme. A compatible app shows a trust confirmation, then opens its
plugin-management surface with the appropriate form pre-filled. You still
submit **Add** or **Install**. The install route requires `plugin@marketplace`,
and that marketplace must already be registered. A web page cannot bypass
those trust steps or install the desktop app itself.

The app/CLI reads `.github/plugin/marketplace.json` from the source repository.
The catalog's `source: "./"` selects the repository root as the plugin
directory; `plugin.json` uses the supported legacy Copilot manifest format
and points to `./skills/`. This keeps compatibility with the supplied app
guide's plugin layout without requiring the newer Agent Plugins schema.
No MCP servers, hooks, or external-service authentication are added by this
sample plugin.

Both routes are documented in
[Using deep links to open the GitHub Copilot app](https://docs.github.com/en/copilot/how-tos/github-copilot-app/open-with-deep-links#plugin-parameters),
which states that they do not install a plugin or add a marketplace until the
user confirms in the app. The same page documents an HTTPS launcher,
`https://github.com/copilot/app/launch?open=<encoded ghapp:// link>`, which
shows a fallback page when the browser cannot hand off to the app. These routes
are for the desktop app; other Copilot clients use the CLI commands below.

### Terminal fallback

```sh
copilot plugin marketplace add architgargg-demo-org/skill-library
copilot plugin install architgargg-test-plugin@architgargg-skill-library
copilot plugin list
copilot skill list
```

You can also use `/skills list` in an interactive CLI session.

## Publishing the install page

The install page is published with GitHub Actions at
<https://architgargg-demo-org.github.io/skill-library/>.

1. In **Settings > Pages**, keep **Build and deployment > Source** set to
   **GitHub Actions**.
2. The `github-pages` environment allows deployments from `main` only. Every
   push to `main` validates the plugin and redeploys the page; you can also
   run **Actions > Validate plugin and deploy Pages > Run workflow** on `main`.
3. The install links read the marketplace catalog from the default branch,
   so plugin changes take effect only after they are merged into `main`.
4. If the repository's visibility changes, the Pages URL changes too: public
   repositories use `https://<owner>.github.io/<repo>/`, while private Pages
   sites use a GitHub-assigned `*.pages.github.io` hostname. Copy the current
   URL from **Settings > Pages > Visit site** rather than reusing an old link.

The workflow publishes **only `docs/`**, not the skills or the whole repository.
Pull requests run validation without deploying. The page is static HTML: no
build dependencies, JavaScript, automatic redirects, or secrets are needed.
If Pages is unavailable under organization policy, the CLI commands still
work after merge.

## Developing and updating the plugin

Run the dependency-free checks:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_plugin.py
```

To try the checkout without installing it persistently, use
`copilot --plugin-dir .` and then `/skills list`. To test the installation
flow locally, use `copilot plugin marketplace add .` followed by
`copilot plugin install architgargg-test-plugin@architgargg-skill-library`.
Local test registration uses the same marketplace name as the published
source; do not replace a registration you already use. Use an isolated
`COPILOT_HOME` and `COPILOT_CACHE_HOME` for disposable CLI testing.

After reviewed skills are added under `skills/<skill-name>/SKILL.md`, bump the
plugin version in both `plugin.json` and the marketplace's plugin entry.
Refresh the marketplace and update the plugin in the app, or run:

```sh
copilot plugin marketplace update architgargg-skill-library
copilot plugin update architgargg-test-plugin@architgargg-skill-library
```

Start a new session to load the updated skills. New skills may require tools
or services; document their dependencies instead of assuming the plugin adds
them.

## Sources

Public documentation (retrieved October 20, 2026):

- [Using deep links to open the GitHub Copilot app](https://docs.github.com/en/copilot/how-tos/github-copilot-app/open-with-deep-links#plugin-parameters):
  `ghapp://plugins/marketplace/add` and `ghapp://plugins/install`, the
  confirmation requirement, and the HTTPS launcher.
- [Customizing the app: adding plugins](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app#adding-plugins).
- [Creating a Copilot plugin](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating):
  manifest formats, skills, local testing, and cached installs.
- [Creating a plugin marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace):
  `.github/plugin/marketplace.json` and repository-relative plugin sources.
- [CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference):
  manifest fields, installation, registration, listing, and updates.
- [Configuring a Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site):
  GitHub Actions publishing.
- [Pages access control](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site):
  private sites, read-access requirements, and assigned private hostnames.

Supporting internal evidence, available to authorized readers:

- `github/revenue-agent-skills: docs/getting-started.md`, sections 1-2:
  app download and marketplace button, followed by separate plugin installation.
- `github/github-app: src/lib/deeplinks/README.md`, route table:
  `plugin-install` and `plugin-marketplace-add`.
- `github/github-app: src/lib/deeplinks/callbacks/installPlugin.ts` and
  `callbacks/addMarketplace.ts`: trust confirmation and pre-filled forms,
  rather than silent installation.

**Research confidence: High — Fully sourced.** Packaging, CLI behavior, and
the desktop deep-link routes are publicly documented. Exact dialog wording can
vary with the installed app version.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) for submission and review guidance. Open a pull request to propose a new skill or changes to an existing one. Please wait for review; submitting a pull request does not mean a skill has been approved or adopted.