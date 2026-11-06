# Processes: QA and automation inside the company

Use for mode C. The book's stance: **test automation is not only code — most of it is process.** Without being part of the process, tests are "letters and digits that bring no value". The automator's duties include building processes, not just writing tests.

---

## 1. The goal of testing

Not just "check the product works" or "cover everything with cases". A key goal is a **transparent status of the product at any moment**: the QA engineer is responsible for quality, must know the current state of the product or feature and be ready to show it any time.

## 2. Introducing QA into a company — the steps

1. **Map functional areas:** features, microservices, how they interact — boxes, circles and arrows. Split the system into parts that can be checked separately in depth.
2. **Build the team:** manual and automation people who can both design test cases and build automation that brings real value.
3. **Embed QA in every stage, not only "testing":**
   - planning — what will we need to check;
   - writing tasks — why the task exists and its quality criteria;
   - development — unit tests / TDD, checks on dev environments;
   - testing — checks, bugs, ping-pong with developers;
   - deploy and post-deploy — checks on production, monitoring, acceptance tests, talking to managers.
4. **Effective CI/CD** — move away from multi-week releases: small task → quick check → deploy → verify.
5. **Effective tooling:** test frameworks, bug tracker, test management system, links between code storage and build systems — all serve transparency.

### The hardest part: changing habits
In a company where developers tested their own code and shipped to production, hiring a tester does not fix things by itself. **Start with how tasks are planned.** A well-formed development task contains:
- **Why?** — why we are doing this at all, in detail;
- **What to do?** — the list of changes: DB changes, migrations, API, etc.;
- **Definition of Done** — the actions that confirm the feature works;
- **Acceptance criteria / acceptance tests** (optional, can be merged with DoD) — tests showing the functionality works as intended.

All of this is settled at planning, before development. QA owns keeping this practice and writing the DoD and acceptance tests.

## 3. CI/CD and when to run tests

When tests, app code and production are separate, fast quality releases are impossible; joined together they become a "sports car". The CI/CD set:
- code builds fast and deploys to a test environment;
- a fast, effective test suite runs on every change (think of the pyramid);
- reports are clear and arrive where they're needed;
- deploy is fast and painless;
- monitoring is set up on production.

### When to run
- **On a schedule (nightly):** common for long suites, but fragile — a broken commit or an environment being updated silently ruins the run, and everyone must know "every night at 2:00 we run branch A on environment B". Ask a counter-question: **why does the suite take 3–4 hours?** Maybe it's time to optimize and revisit the pyramid. Admitting you went too far and rolling back is strength, not weakness.
- **On an event (best):** developer opens a PR/MR → tests run automatically → the passed/failed result **comes back into the PR** → repository rules block merge on failure. Delivering the result back to where it started is essential; otherwise anyone can press merge. Ways to build it: the VCS's built-in CI config file, webhooks to any system, or a big build system.

### How to run — the reference pipeline
1. Change → PR.
2. Automatically bring up the needed environment.
3. Run the autotests on it.
4. Collect results and upload them where they're needed.
5. Destroy the environment.

Requires fast, independent tests. Variations (shared environment, existing CI/CD) are fine — the point is to know the building blocks.

### Where in the pipeline each level runs
- **Unit:** during the build; a failing unit test fails the build. No excuses like "it fails sometimes, non-critical". Unit tests are the foundation.
- **Integration:** after the build, with modules deployed and wired (or mocked).
- **API:** with a fully running environment — servers up, databases configured; after unit and integration.
- **Client (UI):** additionally needs browser/device infrastructure (usually a hub that balances many browsers); after API tests say the server is fine.
- **End-to-end:** a small basic set on a fully ready system, including **production** — right after deploy as a quick health answer, and periodically as monitoring (power cut in the data center, network blip). Run them from outside your data center to avoid false results caused by your own network.

## 4. Delivering the report to the end user

Remember **bus factor**: how many people must leave before the project stalls. If the status lives only in your head, it's low.

Typical pain: the manager wants a quality status every 3 days, and each time you collect links to test reports, tasks, commits by hand. **Think ahead:** what information is needed for the status? Collect it automatically into one place so anyone at any moment can see what changed, which tests ran, and a clear report of the run.

## 5. Teaching and feedback

- If tests aren't used or understood, they may not be needed. Until tests are embedded, explained and used, it's "work for the sake of work".
- Run a session for colleagues: where the code is, how to run, how to configure, how to read the report.
- Don't explain it to every newcomer personally — write it down: README in the code (better than a wiki far away).
- Collect feedback: is it convenient, fast enough, is the report clear? Colleagues often give the seed of the next improvement.

## 6. Persuading developers to write tests

See `strategy.md`, section 3 ("Unit/integration inside the app"): show the cost of late detection by breaking code live, lead by example, require tests only for new code after date X, coverage report on PRs and then a "coverage must not drop" merge rule, promote testability. Expect objections like "why do we need testers then?" — the point is not duplicating work but putting each check where it's cheapest.

## 7. Who the automator is (for role and hiring questions)

Duties: writing autotests; maintaining them (often the hardest phase — good design makes it cheap, bad design turns it into a hungry monster); designing test architecture; building tools and libraries (report systems, code generators, patching open-source libs); introducing processes (CI integration, checks on unmerged code, explaining to the team why autotests matter); choosing tools.

The automator is a developer, doing the same work as other developers — often harder and more interesting.

Growth ladder (technical skills and responsibility):
1. **Junior** — writes tests by analogy, supports existing ones, follows an established process under close mentoring; "builds muscle" by writing lots of tests.
2. **Middle** — writes complex tests independently, builds helper libraries, integrates with VCS and CI, can carry a project; helps juniors.
3. **Senior** — chooses directions and approaches, builds complex tools, fixes third-party libraries, reads product code, can write unit tests in it, leads a small group of juniors/middles, keeps several projects in mind.
4. **Lead** — automation strategy for a whole direction or company, processes from scratch, language and tool choices for many people, defends the vision to management and to teams that never thought about automation; mostly teaching and leading.
5. **"Guru"** — rarely a separate position; builds solutions used across companies, teaches and consults, improves the field as a whole.

It's hard to grade yourself — ask more experienced colleagues where you stand and what's missing.

Advice for people entering the field: learn testing itself first (types, approaches, terms), then learn to code; understand what you use; try different companies early to see different processes and tools; decide clearly whether you want automation or industrial development — they are often confused; plan where you want to be in 5 years. The work includes much beyond code: building processes, proving the value of autotests, introducing tools.
