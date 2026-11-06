# AI Skills

A collection of skills for Claude. Each skill can be installed separately.

## Skills

<!-- skills:start -->
| Skill | Description | Download |
|---|---|---|
| [harvard-negotiation-coach](plugins/harvard-negotiation-coach/skills/harvard-negotiation-coach/SKILL.md) | Helps you get through a tough conversation: asking for a raise, agreeing on a price or contract, a disagreement with a colleague, a family dispute. Analyzes the situation, helps you prepare, suggests what to say when you're under pressure, and lets you rehearse. Based on the book Getting to Yes. | [zip](https://github.com/sidelnikovmike/ai-skills/raw/main/dist/harvard-negotiation-coach.zip) |
| [test-automation-coach](plugins/test-automation-coach/skills/test-automation-coach/SKILL.md) | Explains test automation in plain words, helps decide whether automating is worth it, plans automation and QA processes from scratch, and reviews or writes autotests without over-engineering. Based on the book Let's automate it! | [zip](https://github.com/sidelnikovmike/ai-skills/raw/main/dist/test-automation-coach.zip) |
<!-- skills:end -->

## Installation

### Claude (web, desktop, mobile)

1. Download the skill's zip from the table above.
2. Open **Settings → Capabilities → Skills**.
3. Click **Upload skill** and select the zip file.

### Claude Code: via the plugin marketplace

Add the collection (once):

```
/plugin marketplace add sidelnikovmike/ai-skills
```

Install a skill, for example:

```
/plugin install harvard-negotiation-coach@ai-skills
```

To get newly added skills and updates: `/plugin marketplace update ai-skills`.

### Claude Code: manually

Unzip the skill's archive into `~/.claude/skills/`.

## Sources

Skills based on books contain an original summary of the ideas, not the text of the book. The books themselves are not included in this repository.

- **harvard-negotiation-coach**: Roger Fisher, William Ury, Bruce Patton. *Getting to Yes: Negotiating Agreement Without Giving In*. Russian edition: «Гарвардский метод переговоров» (Mann, Ivanov & Ferber).
- **test-automation-coach**: Mikhail Sidelnikov. *Let's automate it!* (in Russian).

---

Want to add or change a skill? See [CONTRIBUTING.md](CONTRIBUTING.md).
