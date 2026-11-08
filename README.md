# AI Skills

A collection of skills for Claude and Codex. Each skill can be installed separately.

## Skills

<!-- skills:start -->
| Skill | Description | Download |
|---|---|---|
| [harvard-negotiation-coach](plugins/harvard-negotiation-coach/skills/harvard-negotiation-coach/SKILL.md) | Helps you get through a tough conversation: asking for a raise, agreeing on a price or contract, a disagreement with a colleague, a family dispute. Analyzes the situation, helps you prepare, suggests what to say when you're under pressure, and lets you rehearse. Based on the book Getting to Yes. | [zip](https://github.com/sidelnikovmike/ai-skills/raw/main/dist/harvard-negotiation-coach.zip) |
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

### Codex in the ChatGPT desktop app

Open this repository as a Codex project. From the repository root, run the following
commands on macOS or Linux if the skill link does not already exist:

```sh
mkdir -p .agents/skills
ln -s ../../plugins/harvard-negotiation-coach/skills/harvard-negotiation-coach \
  .agents/skills/harvard-negotiation-coach
```

Codex scans `.agents/skills/` for project skills. The link points to the entire
skill folder, so Codex can read both `SKILL.md` and the files in `references/`.
In the project's Codex chat, type `$` and select `harvard-negotiation-coach`.
If the skill does not appear, restart the app and reopen the project.

Example prompt:

> $harvard-negotiation-coach Help me prepare for a conversation with my manager about a raise. Then let's rehearse it.

See [Build skills](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
for details on project skill discovery.

### ChatGPT on the web and mobile

To use the skill in ChatGPT on the web or mobile, package the skill folder
as an OpenAI plugin and make it available in your ChatGPT workspace.
The ZIP in the table above is the Claude distribution. See
[Package your plugin](https://developers.openai.com/plugins/build/plugins)
for the required manifest and folder layout.

## Sources

Skills based on books contain an original summary of the ideas, not the text of the book. The books themselves are not included in this repository.

- **harvard-negotiation-coach**: Roger Fisher, William Ury, Bruce Patton. *Getting to Yes: Negotiating Agreement Without Giving In*. Russian edition: «Гарвардский метод переговоров» (Mann, Ivanov & Ferber).

---

Want to add or change a skill? See [CONTRIBUTING.md](CONTRIBUTING.md).
