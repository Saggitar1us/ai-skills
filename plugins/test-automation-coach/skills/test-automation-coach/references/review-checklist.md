# Review checklist for autotests and test frameworks

Use this for mode D (writing or reviewing tests). Each item: what it looks like in code → why it hurts later → what to do instead. The book's core stance: **a test is judged by how cheap it is to maintain and how easy it is to understand, not by how few lines it has.** "Universal" and "you don't have to think about it" are warning signs, not compliments.

Severity hint for findings: **blocker** (test lies, can't run in parallel, or breaks other tests), **important** (maintenance trap that will cost hours later), **minor** (readability).

---

## 1. Test design basics

**1.1 Tests depend on each other** (blocker)
- Looks like: execution order annotations, static fields passing an id from test 1 to test 2, "create" test followed by "get" test that uses its result, tests that only pass when run as a suite.
- Why: can't run in parallel, can't run one test alone, one failure cascades, the root cause is hidden in another test, and most runners don't guarantee order anyway.
- Instead: every test prepares its own data in its own setup phase, even if it costs a few extra seconds. Shared data is acceptable only when preparing it is really expensive (minutes) **and** you can guarantee no test modifies it.

**1.2 Setup and cleanup written inside the test body** (important)
- Looks like: "go to the shop… check milk… go home" all inside one test; cleanup at the end of the test body.
- Why: if the check fails, cleanup never runs and the next tests start from an unknown state.
- Instead: use the framework's before/after hooks, which run regardless of the result. Better still, make tests independent so no cleanup is needed.

**1.3 Several unrelated main checks in one test** (important)
- One main check per test — the reason the test exists. Side checks along the way are fine (after typing into a field, check it's filled). Several checks are fine when they are one composite check (person is present → wearing a dark jacket → no hat) or when the precondition is extremely expensive — but then every check must still run (soft assertions), not stop at the first failure.
- Split when checks are independent of each other: a failure in the first must not hide the result of the second.

**1.4 Three phases are not visible** (minor)
- Every test at every level — unit, integration, API, UI — is *prepare data → act → check*. If a reader can't spot the three phases, restructure.

**1.5 Weak test data** (important)
- One input pair proves nothing (a `divide` that always returns 2 passes the 4/2 test). Cover typical values, boundaries, zero, empty/absent fields (the "John null McCain" bug), errors. When the expected result is unclear, that's a requirements question — ask, don't guess.

**1.6 Disabled tests without a reason** (minor)
- Commented-out or `@Disabled` tests must say why, concretely (whose decision, which ticket). Delete a test only when the feature itself is removed.

---

## 2. The "ПЕРЕ" problems (over-engineering)

The book's name for the family of mistakes where an automator tries to be too clever. Name them in findings — the user (or their team) may know the terms.

**2.1 Перепараметризация тестов — over-parameterized test** (important)
- Looks like: one parameterized test whose parameters include booleans like `checkAge`, `checkInnIfCompanyAndNotInList`, nullable lambdas with "extra checks", rows like `{1, true, "test", true, false, 2}`.
- Why: every change must be checked against all rows; nobody can tell what a row means; the test is really several tests glued together with `if`s.
- Instead: split into separate tests per real scenario (person, company, validation error). Move shared steps and checks into helper methods. If many parameters remain, wrap them in a `TestData` object built with named setters so each row reads `new TestData().setUserType(COMPANY).setName("Acme")`.

**2.2 Переуниверсализация — the universal mechanism** (important)
- Looks like: generic interfaces and "can handle anything" helpers that grow an `if` for each new feature.
- Why: after a few months it's a "bicycle with crutches" nobody else can ride; the next engineer can't change basic tests without breaking it.
- Instead: don't generalize what doesn't need it. Two or three simple methods beat one Swiss-army knife. Inheritance for truly similar entities is fine. Never put "universal" machinery into the business part of tests.

**2.3 Переудобство — "more convenient" via extra libraries** (important)
- Looks like: pulling in a framework to use one or two methods (`verifyStringNotEmpty`, a fluent assertion DSL) for checks the standard assertions already do.
- Why: new dependency, possible conflicts, more for the next person to learn — for syntactic sugar.
- Instead: add a library only when you can name the concrete gain. "I've done this for 5 years, trust me" is not an argument. If you add one, understand how it works inside.

**2.4 Перепараметризация методов — helper methods with growing signatures** (important)
- Looks like: `getUser(name)` → `getUser(name, type)` → `getUser(name, type, flag1, flag2, n)`.
- Instead: separate methods per case, or pass an entity (`User`, a filter object) so new fields don't change the signature for every caller. Cover such shared helpers with their own unit tests.

**2.5 "I know every trick of the framework" — hidden magic** (important)
- Looks like: test data created by custom annotations or framework hooks so the test body "doesn't need to think about it".
- Why: a reader can't see how data is made; a new user type means digging into framework internals.
- Instead: pick the option where it's obvious from the test what happens. Don't start from "how can I use framework X here" — start from the task and compare options.

**2.6 "It's only test code — patterns don't apply"** (important)
- Looks like: page object fields made public and clicked directly from tests, encapsulation ignored, copy-paste "because it's tests".
- Instead: follow the language's normal engineering rules. When the header moves to a side menu, tests that reached into `page.header` all break.

**2.7 Regular expressions in assertions** (important)
- Looks like: `assertThat(body).matches("^\\{\"id\":\\d+,...")`.
- Why: "now you have two problems"; few people can read it; a harmless response change breaks it and the fix risks breaking other tests.
- Instead: parse the response into an object and check fields; check the text as is; check for substrings; build the expected text by concatenation with the known id; cut the string into parts.

**2.8 "We wrote 8 lines instead of 10"** (minor → important)
- Looks like: dropped braces, clever one-liners, code generation or compile-time generators for two small classes.
- Instead: optimize for the reader — someone less experienced, or you in a year. The IDE generates boilerplate in a few clicks.

**2.9 Framework as a black box** (important)
- Looks like: flaky failures only in parallel runs, slowdowns nobody can explain.
- Instead: understand how your framework works — step through it in a debugger at least once; check how it handles parallelism, waits, connections.

**2.10 The universal multi-armed monster** (important)
- A framework chosen because it "does requests AND assertions AND reports" turns out to work only with its own types and resists customization (adding logging).
- Instead: a dedicated tool for each job, joined by your own client layer.

**2.11 Careless dependencies** (important)
- Looks like: an import that works only because some other library brings it in transitively (e.g. an assertion library via a web framework); an "alphabet" of dependencies, some added only to fix build conflicts.
- Why: when the other library drops it or bumps its version, your build breaks or you're stuck on an old version.
- Instead: declare every library you use directly; justify each one.

**2.12 "We can't start a fresh browser for each test"**
- A fresh browser (or app session) per test gives clean state, painless parallelism and independence. If setup is "too complex", talk to developers: a test-only configuration, setting state through API/cookies instead of the UI, a pre-configured browser image.

---

## 3. Architecture of test code

**3.1 Requests/locators straight from the test** (important)
- Looks like: base URL, endpoint paths, raw JSON strings and locators repeated in every test.
- Why: renaming `userId` → `userSystemId` or switching HTTP library means editing hundreds of tests.
- Instead: a **client** (wrapper) layer — the "contractor between you and the builders". Rules from the book:
  - one endpoint = one class, or one class per domain object (users, documents) — never one mega-client for the whole API;
  - an optional **steps** layer on top that combines several requests into a reusable business step ("log in", "top up the balance");
  - UI: page object / screen object (business methods, locators hidden, transitions return the next page object, methods can return `this` for chaining where it helps readability), element objects for custom widgets, block objects for shared parts like a header;
  - the same for databases and third-party libraries: a client over the storage instead of raw SQL in tests.

**3.2 Primitives instead of entities** (important)
- Pass and return your own objects (request/response models, `User`, filters), not loose strings and numbers. New field = add it to the entity; signatures stay the same.

**3.3 Framework types leak into tests** (important)
- Tests should know as little as possible about the HTTP/UI/DB library. Your own domain model at the boundary lets you replace the library later without touching tests. Technology changes more often than you expect.

**3.4 Copy-pasted shared code across projects** (important)
- Shared clients (e.g. a DB client used by several services' tests) live in one repository and are published as a versioned artifact to an internal artifact repository — never copied.

**3.5 Duplication** (minor)
- Code used twice → extract a method. But in moderation: the goal is easy maintenance, not minimal line count.

---

## 4. Levels and mocks

- Check the pyramid: is this check on the cheapest level that can catch the bug? Search-logic variants belong in unit/API tests, not in UI tests. UI tests cover only key user scenarios.
- Mocks/stubs: a **stub** returns canned data and checks nothing; a **mock** has expectations about calls and fails if they're not met; a **spy** watches real calls without changing them. When checking via a mock, first assert the call happened (count), then its content.
- Mocks are powerful but must not replace all real integration: keep some tests against the real component, or its API change will only show after deploy.
- Getting the value to assert in integration tests: returned by the action; read back through the module's own API (then that read method needs its own tests); read from storage (wrap the query in a client); captured by a mock. If no way to read exists, ask developers for a test-only method.

---

## 5. Flaky tests

A test that passes and fails on the same code. "It's just flaky, rerun it" is a red flag — people stop trusting tests and CI becomes a lottery.

Common causes: unstable environment; client renders slower **or faster** than expected; slow external dependencies; async order not guaranteed; random data.

Fixes:
- isolate tests — each prepares its own data and state;
- mock external systems you don't test (weather, currency rates);
- **explicit waits** for a condition or event — never `sleep(5000)`;
- controlled, stable data — less randomness;
- invest in the environment: watch its logs, configure services properly;
- for end-to-end/monitoring checks, run from outside your data center to avoid false results from local network setup.

---

## 6. Reports and readability

- A report must be understandable to someone outside the project. Steps in business language ("created a user", "topped up the balance") with request/response attachments inside each step — not a flat list of HTTP calls.
- If a manual test case exists, the autotest is its twin: same steps, same ID in code and in the report — so you can see what's automated and spot divergence.
- Document the tests: README with how to run, configure and read the report; comments on non-obvious settings.

---

## 7. Future-proofing summary

1. Independent tests.
2. Extract shared code — but don't universalize.
3. Clients and your own model so frameworks can be swapped.
4. Entities, not loose fields.
5. Think of the next person (often less experienced) and of yourself in a year. "They'll figure it out" and "not my problem" are not acceptable.
