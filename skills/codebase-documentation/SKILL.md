---
name: codebase-documentation
description: Produces seven evidence-backed onboarding documents in docs/codebase/ for an existing repository, covering stack, structure, architecture, conventions, integrations, testing, and concerns.
---

# codebase-documentation

## Purpose

Create a verified knowledge base that helps developers and coding agents work effectively in an existing repository. Produce seven documents in `docs/codebase/`, documenting only facts that can be traced to repository files or command output. Never infer or assume.

## When to use

Use this skill when a user asks to:

- Onboard to an unfamiliar codebase.
- Document a repository's stack, structure, architecture, conventions, integrations, tests, or risks.
- Refresh codebase documentation after significant changes.
- Investigate a focus area, such as "architecture only" or "testing and concerns".

Do not use it to design a new system, invent missing intent, or document generated artifacts.

## Output contract

Before finishing, all of the following must be true:

1. Exactly these files exist in `docs/codebase/`: `STACK.md`, `STRUCTURE.md`, `ARCHITECTURE.md`, `CONVENTIONS.md`, `INTEGRATIONS.md`, `TESTING.md`, and `CONCERNS.md`.
2. Every claim is traceable to source files, configuration, or terminal output.
3. Unknowns are marked `[TODO]`; decisions that depend on team intent are marked `[ASK USER]`.
4. Every document ends with an `Evidence` list containing concrete repository-relative file paths or commands used.
5. The final response includes numbered `[ASK USER]` questions and any intent-versus-reality divergences.

Do not create extra scan or scratch files in `docs/codebase/`. If an existing document would be overwritten, preserve useful verified content and tell the user what changed.

## Workflow

Track this checklist:

```text
- [ ] Phase 1: Inventory the repository and read intent documents
- [ ] Phase 2: Investigate each documentation area
- [ ] Phase 3: Populate all seven docs in docs/codebase/
- [ ] Phase 4: Validate docs, present findings, and list [ASK USER] items
```

### Focus-area mode

If the user supplies a focus area:

1. Complete Phase 1 in full.
2. Fully investigate and complete the focus-area documents first.
3. Keep all required sections in non-focus documents, marking unanalyzed items `[TODO]`.
4. Run Phase 4 validation on all seven documents.

### Phase 1: Inventory and read intent

Work from the target repository root. Use read-only inspection commands and the agent's file search tools. Prefer `git ls-files` when available so ignored and generated files are excluded.

Collect:

- Tracked file list and top-level directory layout.
- File counts by extension and largest source files.
- Package manifests and lockfiles, such as `package.json`, `pyproject.toml`, `requirements*.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`, `Gemfile`, and `composer.json`.
- Runtime and tool versions, such as `.nvmrc`, `.node-version`, `.python-version`, `.tool-versions`, `global.json`, and `rust-toolchain*`.
- CI/CD configuration, such as `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, and `.circleci/`.
- Container and deployment configuration, such as `Dockerfile*`, Compose files, Kubernetes manifests, Helm charts, and Terraform.
- Security and dependency automation, such as `SECURITY.md`, Dependabot, Renovate, CodeQL, Snyk, and SBOM configuration.
- Environment templates, such as `.env.example`, `.env.sample`, and `.env.template`.
- Recent high-churn files from git history, when history is available.

Then find and read intent documents, including `README*`, `PRD*`, `TRD*`, `ROADMAP*`, `SPEC*`, `DESIGN*`, ADRs, and `docs/`. Summarize the stated project intent before reading source code.

Never read or copy secret values. Use environment templates only to identify variable names.

### Phase 2: Investigate

Answer these questions with evidence. If the stack is ambiguous, inspect every manifest and entry point before concluding.

**STACK**

- What languages, runtimes, and versions are used?
- What production frameworks and dependencies are declared?
- What development, build, lint, format, and test tools are declared separately?
- What package managers and lockfiles are used?

**STRUCTURE**

- What are the top-level directories and their responsibilities?
- What are the application, library, CLI, worker, or service entry points?
- Is this a monorepo? If so, what packages or apps exist?
- Which source paths map to aliases, such as TypeScript `paths`?

**ARCHITECTURE**

- What components, layers, or modules are visible in the code?
- How does a typical request, command, job, or event move through the system?
- How is state stored and shared?
- What boundaries or dependency directions are enforced by code or configuration?

**CONVENTIONS**

- What naming, formatting, and import patterns are configured or consistently used in source?
- How are errors, logging, configuration, and validation handled?
- What linting, formatting, commit, or review conventions are configured?

**INTEGRATIONS**

- What external APIs, databases, queues, caches, storage systems, authentication providers, and monitoring tools are used?
- Which environment variable names configure them?
- Where are the integration clients or adapters implemented?

**TESTING**

- What test frameworks and runners are used?
- Where are tests located, and how are they named?
- What commands run unit, integration, end-to-end, or other tests?
- How are fixtures, mocks, test data, and CI test execution handled?

**CONCERNS**

- What production TODOs, FIXMEs, deprecated APIs, or known bugs are present?
- What security, reliability, performance, or maintainability risks are evidenced?
- What tests or coverage gaps are visible?
- Which high-churn or very large files are likely fragile?

### Phase 3: Populate documents

Create or update the documents in this order. Every document must contain the listed required sections plus `Evidence`.

1. `STACK.md`: Summary, Languages and runtimes, Production dependencies, Development tooling, Package management, Evidence.
2. `STRUCTURE.md`: Summary, Directory map, Entry points, Key files, Workspace or package layout, Evidence.
3. `ARCHITECTURE.md`: Summary, Components, Data and control flow, State and persistence, Boundaries and dependencies, Evidence.
4. `CONVENTIONS.md`: Summary, Naming and organization, Formatting and linting, Imports and dependencies, Error handling and logging, Configuration, Evidence.
5. `INTEGRATIONS.md`: Summary, External services, Data stores, Authentication and authorization, Observability, Required configuration, Evidence.
6. `TESTING.md`: Summary, Frameworks and runners, Test organization, Test commands, Fixtures and mocks, CI testing, Evidence.
7. `CONCERNS.md`: Summary, Production technical debt, Security risks, Reliability and performance risks, Test coverage gaps, Fragile areas, Evidence.

Use `[TODO]` for anything that cannot be determined. Use `[ASK USER]` where the correct answer requires team intent. Add optional sections only when repository complexity justifies them.

### Phase 4: Validate, repair, and report

Repeat this loop until all seven documents pass:

1. Confirm all seven files and every required section exist.
2. Check each document against the Phase 2 questions.
3. Confirm every non-trivial claim has evidence.
4. Replace unsupported claims with `[TODO]` or `[ASK USER]`.
5. Fill empty required sections with verified content or an explicit marker.

Validation passes only when there are no unsupported claims, no empty required sections, no assumptions presented as facts, and all team-intent gaps are marked `[ASK USER]`.

Then present:

- A short summary of each document.
- Numbered `[ASK USER]` questions.
- Intent-versus-reality divergences found between intent documents and code.
- Any coverage limitations, such as missing git history or inaccessible files.

## Gotchas

- **Monorepos:** A root manifest may not contain application source. Check workspaces, `packages/`, `apps/`, and nested manifests, and document each package separately.
- **Outdated README files:** README content may describe intended rather than current behavior. Verify it against code and configuration.
- **Path aliases:** Resolve aliases, such as TypeScript `paths`, before describing structure or imports.
- **Generated output:** Do not infer conventions from `dist/`, `build/`, `generated/`, `.next/`, `out/`, `coverage/`, `vendor/`, or `__pycache__/`.
- **Environment configuration:** `.env.example` and similar files reveal required variable names, not values. Never inspect or copy secrets.
- **Production versus development dependencies:** Document linters, formatters, and test frameworks as development tooling unless they are used at runtime.
- **Test TODOs:** TODOs in test directories are coverage gaps, not production technical debt.
- **High-churn files:** Frequently modified files may indicate hidden complexity. Note them in `CONCERNS.md` with git evidence.

## Anti-patterns

| Don't | Do instead |
| --- | --- |
| Claim "Clean Architecture" when no matching code or directories exist. | State only the structure visible in the repository. |
| Call a project Next.js without checking manifests. | Confirm frameworks from dependencies and source usage. |
| Guess a database from a variable name like `dbUrl`. | Confirm drivers, ORMs, schemas, or client code. |
| Document conventions from generated output. | Use source and configuration files only. |
| Replace unknowns with plausible guesses. | Mark them `[TODO]` or `[ASK USER]`. |

## Dependencies and effects

- Requires read access to the target repository and permission to create or update files in `docs/codebase/`.
- Uses common read-only shell and git commands when available. No external services or bundled scripts are required.
- Modifies only the seven documents in `docs/codebase/`. Review generated documentation before committing it.

## Attribution

Adapted from the `acquire-codebase-knowledge` skill in [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/9ce814859eaa473178a1463ee3aa0c54a8860b86/skills/acquire-codebase-knowledge), licensed under the MIT License. See `THIRD_PARTY_NOTICES.md`.
