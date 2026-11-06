# Test Automation Coach

A skill for Claude based on the book *Let's automate it!* by Mikhail Sidelnikov. It is useful for automation engineers, developers, manual testers and managers.

## What it does

| Mode | Example request |
|---|---|
| **Explain** | "What is an autotest and the testing pyramid, in plain words?" |
| **Should we automate** | "My manager wants 80% autotest coverage for our internal tool. Is it worth it?" |
| **Strategy and processes** | "I'm the first QA in a 10-person startup. Where do I start?" |
| **Write or review tests** | "Review my API tests" (attach the code) |

You can ask in any language. The skill replies in the language you use.

## What changes with the skill

We gave Claude the same four requests twice, once without the skill and once with it.

| Request | Without the skill | With the skill |
|---|---|---|
| **A manager asks what autotests are** | A good answer, but generic | Everyday analogies from the book. States plainly that an automation engineer is a developer. Shows that a checklist is a valid alternative. Suggests the manager ask how they will see product quality status |
| **"We need autotests with 80% coverage" for a short-lived internal tool** | Doubts the goal, but still picks Playwright and plans a month of work | Decides first whether to automate, and only then chooses tools. Calculates payback: about 154 runs to break even, against about 20 runs before the tool is handed over. Recommends a checklist plus a thin layer of data checks, and gives ready wording for the manager |
| **First QA in a startup** | A strong, modern plan | Keeps the modern practices (Testcontainers, contract tests, Playwright) and adds the processes: task format "Why / What / Definition of Done", showing developers a bug by breaking code live, "tests for new code from date X", bus factor, a status anyone can see, and options with trade-offs |
| **Review of tests full of typical mistakes** | Finds almost everything, but the rewritten code still exposes REST Assured's `ValidatableResponse` to the tests | Catches that too: the API client returns the project's own models. Names over-parameterization explicitly, doesn't add libraries "just in case", and asks for the manual test case IDs so reports can link to them |

The biggest gain is on the question "should we automate at all". On the other three requests the skill keeps good current practice and adds the book's approach on top of it.

## Installation

See the [main README](../../README.md#installation).
