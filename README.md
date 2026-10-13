<div align="center">

<img width="2172" height="724" alt="SleekCode" src="assets/header.png" />

**LeetCode at home, for people who debug with `print`.**

</div>

You could learn to use a debugger. Or you could `console.log` everything until it works.
SleekCode is for the second kind of person.

```
$ sk play
── Example 1 ─────────────────────────────────
head = [1,2,3,4,5]
reversed so far: ListNode(2 → 1)   still to go: ListNode(3 → 4 → 5)
…
✓ [5,4,3,2,1]
```

The NeetCode 150, in TypeScript or Python, with tests, hidden cases, a "too slow" check, hints, and
a log that quietly judges you. macOS only.

## Install

```sh
git clone https://github.com/0mjs/sleek.git ~/sleekcode && bash ~/sleekcode/install.sh
```

It installs what it needs: [Bun](https://bun.sh), and if you pick Python, [uv](https://docs.astral.sh/uv/) and Python too.

Answer three questions (language, editor, folder), take the two-minute tour (`sk intro` any time), then type `sk next`.

## Use

Not sure what to type? `sk` on its own opens a menu of what to do next. `sk -h` lists every command.

```
sk next      next problem
sk start     start the timer (sk pause when you step away)
sk play -w   run the examples and see your logs, on every save
sk test -w   examples + hidden cases + speed check
sk hint      one hint at a time (no shame)
sk log       record how it went (honesty encouraged)
```

## Stats

`sk stats` is a full-screen dashboard in your terminal, because of course it is. Five tabs: your
progress and streaks, every pattern from "not started" to "mastered" (and which to focus on next),
TypeScript vs Python if you do both, how long things take you vs how long they should, and what's due
for review. Everything you log is tracked, so the graphs only lie if you do.

## Compete with friends

```
sk league -c     create a league (a private GitHub repo) and invite friends by GitHub username
sk league        the leaderboard, or accept an invite
sk league 15     everyone's attempts at one problem, head to head
```

Every `sk log` publishes what you solved, how (on your own, hints, AI…), your complexity and your time.
Never your code or notes. Needs the [GitHub CLI](https://cli.github.com) (SleekCode offers to install it).

## Also

`sk drill` (read a problem, name the pattern and target complexity, no coding — interview warm-up), `sk review` (spaced repetition: clean solves come back after 7, 14, 28 days; four in a row and it's ✅ mastered), `sk lang` (switch TypeScript ⇄ Python), `sk submit` (copy it to LeetCode
when you're feeling brave; `-a` to pick an older attempt). `sk` lists the rest.

Can't tell O(n) from O(n log n) yet? [BIG_O_CHEATSHEET.md](BIG_O_CHEATSHEET.md): the finite list of things to know.

15 colour themes (Tokyo Night by default, Dracula, Gruvbox, Catppuccin, SynthWave '84…): `sk config -t`. Works with Zed, VS Code, Cursor or vim. Updates install themselves (once a day, in the background); `sk config -u off` if you'd rather run `sk update` yourself.

## Maybe next

Ideas, not promises ([ROADMAP.md](ROADMAP.md) has the details):

- 🃏 **Pattern drills**: read a problem, name the technique and the complexity, no coding
- 🎤 **Interview habits**: explain your approach out loud, list edge cases before you code
- ⏲️ **Mock interviews**: a random problem, a countdown, no hints (opt-in pressure)
- 🏗️ **System design**: classic prompts, a 45-minute template, rubric checklists and estimation drills
- 🧩 More problem sets (NeetCode 250, Grind 169) and more languages
- 🐍 PyCharm support, for Python

## Fine print

- Your solutions live in your own folder, not in this repo.
- Problem text comes from LeetCode when you set up; it isn't stored here.
- Test answers aren't hand-written: hidden cases are kept only when two independent reference
  solutions agree. Building them yourself: see [build/cases](build/cases/README.md).
- Problem list and hints: [NeetCode](https://neetcode.io) ([MIT](THIRD_PARTY_NOTICES.md)). Problems: [LeetCode](https://leetcode.com).
- SleekCode itself is [MIT](LICENSE): free for anyone to use, change and share.
- Uninstall: `rm -rf ~/sleekcode ~/.config/sleekcode ~/.local/bin/sk ~/.local/bin/sleek`
