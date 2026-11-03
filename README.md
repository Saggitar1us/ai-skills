# AI Skills

A collection of skills for Claude. Each skill can be installed separately.

## Skills

<!-- skills:start -->
| Skill | Description | Download |
|---|---|---|
| [harvard-negotiation-coach](plugins/harvard-negotiation-coach/skills/harvard-negotiation-coach/SKILL.md) | Coach for the Harvard negotiation method (Getting to Yes by Fisher, Ury and Patton): dispute analysis, negotiation prep, responses to pressure and dirty tricks, role-play practice. Replies in the user's language. | [zip](dist/harvard-negotiation-coach.zip) |
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

---

Want to add or change a skill? See [CONTRIBUTING.md](CONTRIBUTING.md).
