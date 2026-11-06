# Strategy: should we automate, and how to build automation from scratch

Use for mode B (should we automate / is it worth it) and mode C (building automation on a project). The book's key message: **deciding whether to automate is part of the automator's job.** Agreeing to "automate everything, 80% coverage" without analysis is a common and costly mistake; understanding that not everything should be automated comes with experience.

---

## 1. Should we automate this?

### Signs automation is NOT needed (or not now)
1. **Very short product life:** build in a week, hand over, never change. A good manual check is enough — as long as it's really not the start of a bigger system.
2. **Feature in active development, requirements keep changing:** tests will be rewritten constantly no matter how well designed.
3. **Automating costs far more than checking by hand:** typical for tricky UI (custom scrolling, canvas, odd widgets) where you'd need hacks. Seconds of manual checking vs. days of inventing a bicycle.
4. **Nobody can say what value the tests will bring.** "We need autotests so we have autotests" is not a reason.

### Signs automation IS needed
1. Scenarios must be run **often**, and/or on several environments, browsers, OSes, devices (100 cases × 10 devices × 2 environments × 2 releases a week). Put simply: a full manual run takes too long.
2. The system is **hard or impossible to test by hand:** large generated data sets, many checks, backend without UI, or the manual tester lacks tools for the backend.
3. **Backward compatibility between versions** must be checked (old users' payments still work after a release).
4. **Load testing** — impossible by hand.
5. **Monitoring:** regular quick checks of system health or of scenarios that must always work, including on production.

Real projects are often grey zones: reason from both the principles and the specific project.

### The alternative to autotests: a good checklist
A detailed checklist (test plan) that **any** tester or team member can run: steps, example requests, expected results. It needs almost no maintenance and no coding skills. Writing it well is sometimes as hard as writing autotests. It is a fully legitimate result of the analysis, not a failure.

Questions that expose hidden maintenance cost of autotests: What if the browser version changes? What if the author leaves — who maintains and extends it? What if the framework or the tricky widget changes?

**The book's own story** (useful as an example to tell): an internal monitoring tool showing DB data in web tables, 70% ready, to be handed to another team, will hardly change. The author eagerly built a framework, then spent days fighting a lazy-loading table that standard approaches couldn't read. Then he asked himself why he was doing this — and replaced the autotests with a detailed checklist. Lesson: analyze first, then decide between autotests and a manual test plan.

### Talking to the requester
- Always estimate the cost of writing **and** maintaining before agreeing.
- Don't be afraid to tell the requester that autotests are not worth it here, and explain with numbers.
- Clarify what "coverage" means (code lines? requirements? cases from the manual checklist?) and what risk they want to remove — the real need is often "confidence in quality", not a percentage.

---

## 2. ROI calculation (formula by Roman Savin, author of «Тестирование Dot Com»)

Two characters: a manual tester is useful from day one; an automator is a long-term investment.

Notation:
- Cm / Ca — cost to create a manual / automated test case
- Sm / Sa — cost to support it over its life
- Rm / Ra — cost of one run (manual: tester's time; automated: server/cloud time, small but not zero)
- N — number of runs

Automation pays off when:

```
Cm + Sm + Rm·N  >  Ca + Sa + Ra·N
N  >  (Ca + Sa − Cm − Sm) / (Rm − Ra)
```

Book example: 8 h to create either test; manual tester $1/h, automator $1.2/h → Cm = $8, Ca = $9.6. Manual run 5 min → Rm ≈ $0.083. Support 1 h each → Sm = $1, Sa = $1.2. Automated run 20 s in CI → Ra ≈ $0.01.
→ N > 24.7 runs. At 2 CI runs a day that's about 12 days — looks great.
Now make support realistic: Sa = 4 h → $4.8 → N > ~74 runs. One variable tripled the break-even point.

How to use it:
- Plug in the user's real numbers (salaries or just hours, run time, run frequency, expected life of the product, realistic support time — UI tests cost much more to support than API tests). Show the break-even N and how many days/weeks of runs that is. Show the sensitivity to Sa.
- Say what the formula ignores: + bugs caught right after build are cheaper to fix; + manual testers get time for new features; − failing tests (not always real bugs) can delay releases.
- Conclusion: automation can save money or become an insatiable monster — it depends on what is automated and on which pyramid level.

---

## 3. Building automation from scratch ("Строим дом")

The book compares it to building a house: survey the ground before the foundation (where tests run, which language, where code lives), choose the "utilities contractors" (libraries for DB, HTTP…) so you don't repair the plumbing every week. With experience this preparation takes minutes, but it must happen. The steps, in order:

1. **Do we need autotests at all?** (section 1–2).
2. **Look at what exists:** do developers write unit/integration tests? Were there earlier attempts at API/UI automation? You may have an empty canvas, a half-painted picture of disconnected parts, or something nearly done.
3. **Work on several fronts along the pyramid:**
   - **Unit/integration inside the app.** Mostly persuasion. Arguments: a bug found at method level costs minutes, the same bug found after deploying an environment costs hours; developers get feedback at build time instead of a bug ticket a day later in a branch they've forgotten. Best argument: **break a piece of code and show every stage it passes before the bug is caught.** Lead by example: write a few unit tests and an integration test with mocks yourself — reluctance often comes from not knowing how. For legacy code, require tests only for new classes after date X. Add a coverage report on PRs, and once coverage is decent, block merges that lower it. Promote *testability*: small methods of 2–10 lines instead of one 200-line method.
   - **API/client tests outside the app.** If the inside is well covered, fewer heavy external tests are needed. Prioritize by business importance: ask product owners/managers; think as a user; use production metrics or, if absent, API load per endpoint (and push the team to start collecting metrics — they may reveal that the "million-dollar feature" is barely used). Example: in a banking app, login, account data and money transfer first; changing the avatar can stay manual.
4. **Choose the language for tests** (section 4).
5. **Decide where the test code lives** (section 5).
6. **Shared clients as artifacts** — one client for a shared resource (e.g. the DB used by two services' tests) in its own repo, published as a versioned artifact to an internal repository. Never copy code between projects.
7. **Environments** (section 6).
8. **Automatic runs** — see `processes.md`, section "CI/CD and when to run tests".
9. **Reports** — readable by anyone; see `review-checklist.md` section 6.
10. **Explain, teach, get feedback.** If nobody uses or understands your tests, maybe they aren't needed. Until they're part of the process, explained and used, it's "work for the sake of work". Hold a demo: where the code is, how to run, how to read the report. Write a README / wiki. Ask for feedback and act on it.

Order for future-proofing: need → volume and levels → language → storage and runs → report and its consumers → only then code and frameworks.

---

## 4. Choosing the language for tests

Two camps: the application's language ("developers can fix tests") vs. the language convenient for automators. Research before deciding:
1. Languages and technologies used in each part of the app.
2. Existing tests in the company — compatibility of approaches, how they run and integrate.
3. If none — what your QA colleagues know and like.
4. How tests will run: infrastructure cost of a new language.
5. Which services and storages tests must talk to — are there good libraries?
6. What the test frameworks can do: **parallel runs out of the box**, reports, assertions.

A different language from the app is normal. On "how will developers add and fix your tests?": in practice developers rarely write external tests — better they spend effort on unit tests. They *can* fix your tests if the code is clear and a change touches one place — making that possible is your job.

The book's parable: BestLanguage++ is great for the app, but its test frameworks don't support parallelism, reports are poor → one-hour runs, homemade multiprocess scripts, data leaking between tests. TestLanguage 1.0 with parallelism, a big community and integrations would have avoided all that.

---

## 5. Where test code lives

| Option | Pros | Cons |
|---|---|---|
| **Same repo as the app** | One pull request contains both the feature and its API/UI test changes; reviewed together; tests never lag behind | Mixed languages, heavier repo, risk of accidentally touching app files (low with proper review) |
| **Separate repo** | No monolith; QA's own review/merge rules; running tests doesn't require building the app | A task's changes are split across PRs |

No universal standard: choose what's convenient for you and your colleagues. Don't copy giants — they may do it for historical reasons, by order from above, after a long path, or while knowing it's wrong but too expensive to change. **Your main tool is your own head.**

---

## 6. Environments

Types: developer, test (for QA), production.

| Option | Pros | Cons |
|---|---|---|
| **Environment per test run** (containers/virtualization, created and destroyed with the run) | Full isolation from colleagues' runs and manual checks; destructive tests are safe; no locking schemes | The machine must handle app + tests; complex products need many services |
| **Shared test environment** | Ready to use, good for heavy dependencies and big scheduled releases | Data gets broken by colleagues (Peter's 3-hour setup ruined by Victor), version clashes (someone deploys 1.13 over 1.12 mid-test). Needs written rules of use and several environments |

Advice: make the test environment as light as possible and **startable locally with one command**. A QA engineer who understands deployment builds better checks; the good QA is a tester, a bit of DevOps, developer, analyst and product manager.

---

## 7. Choosing tools and frameworks

1. **By experience:** if you have a proven stack and ready-made code from previous projects, reuse it — fast start, everyone happy.
2. **New technology, no experience:** ask developers (they may have seen tools), former colleagues and the community, read articles. Don't dig in one direction — look at the system **through the user's eyes**. Book example: testing a voice assistant — instead of studying speech processing internals, feed recorded phrases with expected recognized text: "file → expected phrase", then add a million samples.
3. **Two similar frameworks:** GitHub stars are a signal, not a basis. Build small prototypes: how it feels in use, how it integrates with DB/reports, show colleagues, collect evidence for your choice. The time pays off.
4. **Scope and quality of use:** don't pull a heavy library for one helper; count transitive dependencies; don't follow fashion; remember who maintains this in 2–10 years; wrap frameworks in clients so they can be replaced.

## 8. Structure of a test framework (when the user builds their own)

A framework is a set of libraries/tools that speeds up development and shapes code structure — from 50 lines to 1000 classes. It knows nothing about the product. Sometimes not using a framework is the right choice. Classic structure:
1. **External interface** — what users call. Split by functionality (high cohesion), not one 1004-method service. Make it understandable: doc comments, an examples module, and tests of the client (tests are examples of use). Design for a junior with a few months of experience.
2. **Core** — the main logic; knows nothing about interfaces or the product. Several interfaces (code API, CLI) reuse one core.
3. **Domain model** — the entities the framework works with. `FileData getFileText(DataFilters filters)` instead of a growing family of overloads. Expose only your model; never "release the kraken" of the underlying libraries.
4. **Hygiene** — README, examples, doc comments, unit tests, merge rules (review required, coverage must not drop), like open-source projects.
