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
   and sign in with an account that can read this internal repository.
2. Open the published install page from **Settings > Pages > Visit site** in
   this repository. Publish it using the steps below first.
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

These desktop URI routes were verified against the supplied authenticated
guide and the app's internal URL contract, not a public GitHub Docs promise.
Do not assume that other Copilot clients support them. The public documentation
below covers manifests, marketplaces, CLI commands, and Pages.

### Terminal fallback

```sh
copilot plugin marketplace add architgargg-demo-org/skill-library
copilot plugin install architgargg-test-plugin@architgargg-skill-library
copilot plugin list
copilot skill list
```

You can also use `/skills list` in an interactive CLI session.
Private/internal repository access and any required organization SSO must be
authorized separately from access to the Pages website.

## Publishing the install page

Private GitHub Pages is configured for this repository with GitHub Actions at
<https://turbo-adventure-1gkm9w5.pages.github.io/>. The first deployment still
requires this change to be reviewed and merged; a configured hostname does
not mean the page or default-branch plugin catalog is already published.

1. Review and merge this change into `main`. The install links use the default
   branch, so they cannot find an unmerged catalog on a feature branch.
2. In **Settings > Pages**, set **Build and deployment > Source** to
   **GitHub Actions**. For this internal repository, keep the site **private**
   unless a maintainer explicitly decides to publish it publicly. Pages access
   control for private/internal repositories requires GitHub Enterprise Cloud.
   Do not make the repository public just to enable Pages.
3. Review the `github-pages` environment's deployment branch rules and any
   required approvals; allow deployments from `main`.
4. Run **Actions > Validate plugin and deploy Pages > Run workflow** on `main`
   if the merge's workflow ran before Pages was enabled. Future pushes to
   `main` validate the plugin and deploy automatically.
5. When deployment succeeds, copy **Visit site** from **Settings > Pages** or
   the workflow's deployment URL. Private Pages uses a GitHub-assigned
   `*.pages.github.io` hostname, so do not guess a public `github.io` address.
6. Share that URL with people who can read this repository. The page has the
   app download link, both app buttons, terminal fallbacks, and troubleshooting.

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

Internal-only evidence, available to authorized readers:

- `github/revenue-agent-skills: docs/getting-started.md`, sections 1-2:
  app download and marketplace button, followed by separate plugin installation.
- `github/github-app: src/lib/deeplinks/README.md`, route table:
  `plugin-install` and `plugin-marketplace-add`.
- `github/github-app: src/lib/deeplinks/callbacks/installPlugin.ts` and
  `callbacks/addMarketplace.ts`: trust confirmation and pre-filled forms,
  rather than silent installation.

**Research confidence: Medium — Partially sourced.** Packaging and CLI behavior
are publicly documented; the desktop deep-link contract is internal-only and
can depend on the installed app version.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) for submission and review guidance. Open a pull request to propose a new skill or changes to an existing one. Please wait for review; submitting a pull request does not mean a skill has been approved or adopted.