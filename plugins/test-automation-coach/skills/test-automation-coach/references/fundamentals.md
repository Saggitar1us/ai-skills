# Fundamentals: tests, levels, data — with the book's analogies

Use for mode A (explaining) and as background for other modes. When explaining to non-technical people, use these everyday analogies from the book, retold in your own words.

---

## 1. What a test is

**A test is a check that some condition or behavior matches what is required or expected.**
- Test: Mom asks John to go to the shop and **check whether** they have a certain brand of milk. Asking the library whether they have the new book. Reading cough pills' ingredients to see if there's vitamin C.
- Not a test: John buys ice cream. Mary eats porridge. — No check against a condition known in advance.

Almost every test also has a **precondition** — to check the milk you must first get to the shop. Around a test there are **resources** (money), **time** (one of the most important properties) and **experience** gained. Example: two employees sent to Liverpool to check a pie shop — one googled the fastest, cheapest route (train, 8 h, £100), the other rented a car (12 h, £300). Plan the path to the check thoughtfully: "think, then act".

**An automated test** is the same set of actions and checks, executed by software. It can be started by a person or by a computer under some condition: once, every 10 minutes, after each build, "when the coffee machine finishes".

## 2. Rules every test follows

- **Independence:** a test must not depend on another test's result. Peter is sent to the director's office for documents *and then* to the staff room for the grade book; if the documents aren't there, the test stops and nobody learns about the grade book → make two tests.
- **Return the system to its initial state, whatever the result** — Peter comes back to the teacher whether he found the book or not. With truly independent tests you mostly don't need to think about this.
- **One main check;** secondary checks along the way are fine. Several checks in one test are fine when they form one composite check, or when the precondition is very expensive (flying to Washington to check three people in room 301) — but then every check must be executed.
- **Every test has three phases:** prepare data → act → check.

## 3. What "good" means

1. **Optimal** — minimal time to maintain and change.
2. **Convenient** — new tests are quick to write thanks to what already exists.
3. **Understandable** — clear to everyone, even someone without deep knowledge.

Maintenance is usually the longest phase of a test's life. The book's walk-through (John going to the shop for milk and then for cheese): two tests differ in one line → extract "walk to the shop" / "walk home" into methods → move them into before/after hooks that always run → make "check product availability (product)" a parameterized method. If the shop moves, you fix one place; if John starts taking the bus, all tests speed up at once. But in moderation: don't build "universal starships with a thousand parameters".

## 4. Life cycle of an autotest

1. Decide whether this case should be automated at all.
2. Design the architecture (prototypes encouraged — try the design on a tiny example, show it to someone).
3. Write the code.
4. Debug and verify it — everyone makes typos; a red test with a cryptic error undermines colleagues' trust.
5. Describe it (README, comments) and push to the repository — helps future you, colleagues, and automated systems; a laptop forgotten on the bus loses unpushed work.
6. Verify it "in combat" — where it will actually run (missing tools, no access to DB/servers on the CI machine).
7. Maintain it.
8. Delete it when the feature is removed — or disable it with a concrete comment why, if it may become relevant again.

## 5. The testing pyramid

Layers from bottom to top; the area of each layer is how many tests of that kind you want.
- **Unit (bottom, the most):** inside the app code, check single methods; simple, fast, find bugs at the lowest level. Run during the build.
- **Integration / API (middle):** interaction of modules, with a database or other storage (people often forget the DB is part of integration), and the API that clients use.
- **Client / UI and end-to-end (top, the fewest):** what the user sees; heavy, slower, sometimes unstable — but needed, because well-covered code doesn't guarantee the user won't see something terrifying at login.

Real life: often an **inverted** pyramid (mostly UI tests) or a **cylinder** (roughly equal) — the cylinder is "not that bad".

Every level uses the same approaches: three phases, and wrappers/clients over whatever you talk to. "The test type changed — the approach stayed."

## 6. Levels in more detail

### Unit
Test of a minimal piece of code for a given input. Three kinds of methods: returns a result (calculator: 4/2, 9/3, rounding 5/3, n/n, 0/2, division by zero → agreed error); modifies the input object (full name assembled from first/middle/last — the "John null McCain" registration bug when there's no middle name); calls other things and returns nothing (a log line `[SUCCESS]` on which payments to a vendor depend — checked with a mock logging system).
**Stub / mock / spy:** stub — "answer like this, that's all"; mock — "make sure you were called correctly" (expectations, fails otherwise); spy — "watch, don't interfere".
**Parameterized test:** one test, N data sets → N runs. Great when cases differ only in data; beware over-parameterization.
**TDD:** method skeleton → tests (red) → code to make them green → refactor.

### Integration
Modules already exist and are combined; check that they work together, including the DB. Ways to get the value to check: the action returns it; read via the module's own method; read from storage; capture via a mock of the downstream module. Integration tests can live inside the app code or outside, over the network.

### API
API = a description of how one program can interact with another — the "sockets" clients plug into (kettle example: switching on heating from a phone app). Why test it even if developers covered the code: what goes out — format and data — is what thousands of clients depend on. Writing requests straight from tests is quick but expensive later; a **client/wrapper** (the "foreman" between you and the builders) localizes changes. One endpoint — one class; optionally a steps layer.

### Client (UI, web, mobile)
Every browser and device interprets the page in its own way → layouts break → users leave for a competitor (like a shop with expired sausage). Choosing configurations: for a new product, general usage statistics or marketing's target audience; for an existing one, your own analytics metrics (which also show what features are really used).
Elements are found by **locators/selectors** (id is best when available). **Waits:** implicit (global) vs. explicit (wait for a specific element up to N seconds) — explicit is better. Clicks can be done several ways (native click, JS, emulated mouse) — different UIs need different ones.
**Page object:** talk to the page as a whole ("search for this text"), not to its organs; locators live inside; methods that navigate return the next page object. **Element object** for custom widgets, block objects for shared parts like a header. Works the same for mobile ("screen object").
Why few UI tests: hard to write, hard to maintain (locators, UI changes, browser infrastructure), unstable, slow. Mitigate with experience and patterns, explicit waits, cooperation with developers (stable test ids), a browser grid with parallel runs — which requires independent tests. Check logic (e.g. search) at lower levels.

### End-to-end
Full scenarios "from end to end". Example: an advertiser sets up a campaign and pays; someone opens a site, clicks the banner; the statistics must change. Even with good unit, API and UI coverage, infrastructure or out-of-module changes can break the whole chain. E2E tests are expensive (client + API + waiting for data), so keep a **small basic set** that answers "does the product work at all" — including on production after deploy and periodically as monitoring.

## 7. Test data preparation

Each test must be independent; data tied between tests means: both must restore state, no parallel runs, hard failure analysis, one test can destroy others, runners don't guarantee order. Spend the extra seconds on independent data; share expensive data only if no test changes it.

| Approach | Pros | Cons |
|---|---|---|
| **DB snapshot (dump)** — fill, dump, run, restore | Fastest | Lives apart from tests; must be maintained as schema changes; the link "test expects John Smith" breaks when a test changes him (workaround: enough data for every test) |
| **Through the API on the fly** (via a client) | Data and its use side by side; no knowledge of storage structure; reliable | Takes run time; deep dependency chains (organization → team → user) make setup longer than the test — still worth it for independence |
| **Through the storage on the fly** (via a DB client) | Fast, data right in the test | Schema and relations change → constant query maintenance; lots of code for linked entities |
| **Through the UI** | Possible | Slow and fragile — rarely worth it |
| **Split in time** — one process creates data via API, saves ids/JSON to a file; tests read their item by number and create it if missing | Fast tests | Must store and keep the link between the steps |
