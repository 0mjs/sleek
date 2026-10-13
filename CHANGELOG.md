# Changelog

## 1.0.1

- The project's GitHub repo is now github.com/0mjs/sleek. Old links and updates still work.
- Setup now suggests ~/sleek-practice for new workspaces. Existing workspaces aren't affected.

## 1.0.0

SleekCode's first stable release. 🎉

- **New: `sk drill`** — flashcards for the first two minutes of an interview. Read a problem, name the pattern and the target complexity, no coding. It grades you instantly and points out the patterns you keep missing. No AI, no setup.
- Everything from the 0.x series: 150 problems in TypeScript or Python, hidden cases and a speed check, hints, spaced-repetition review, leagues, 15 themes, the sk menu, and updates that install themselves.

## 0.9.0

- **sk on its own opens a menu** of what to do next, based on where you are: start a problem, run the examples or tests, get a hint, log it once the tests pass, resume a paused timer. Each option shows its command, so you learn them as you go.
- "Everything else…" in the menu lists every command, type to search.
- The help page is now sk -h (or sk help). Prefer it when you type sk? sk config -m off.

## 0.8.2

- Updating no longer fails if a release tag was re-made on GitHub ("would clobber existing tag").

## 0.8.1

- Tokyo Night is the default theme: a cool header, and calm green / amber / red in sk stats.
- SleekCode's neon theme is now SynthWave '84, with that theme's real colours (sk config -t synthwave).

## 0.8.0

- **Themes.** sk config -t picks from 15: SleekCode's own (the new default), Tokyo Night, Dracula, One Dark, Monokai, Gruvbox, Nord, Catppuccin Mocha, Solarized Dark, GitHub Dark, Rosé Pine, Kanagawa, Everforest, Night Owl and Ayu Mirage. Everything recolours, header included.
- A new header: neon letters over a horizon grid, in your theme's colours.

## 0.7.1

- Attempt lists (sk attempts, sk submit -a) line up in columns, most telling first: problem, how it felt and the result, how you solved it, complexity, time, language, date. A long row now loses the date, not the emoji.
- "Fine" shows 👍 instead of nothing, and above-target complexity is a short ↑.

## 0.7.0

- **SleekCode updates itself.** Once a day, in the background, so you never wait. You're told what's new (like this) the next time you run sk. Turn it off with sk config -u off.
- **sk intro: a two-minute tour** of what SleekCode is and how to use it, in plain English. Offered at the end of setup, and there any time.
- sk update also refreshes your workspace using the new version's code (before, it used the old one until the next update).

## 0.6.1

- `sk submit -a` always opens the picker. Without a number it lists every attempt you've logged (any problem), not just the current problem's, which often had none.
- `sk submit` only copies code that passes: the current solution is tested first, and a logged attempt must have passed when you logged it.

## 0.6.0

- **Submit any attempt:** `sk submit -a` lets you pick your current solution or any attempt you've logged (newest first), and copies that one for LeetCode. Plain `sk submit` is unchanged.

## 0.5.0

- **Leagues: compete with friends.** `sk league -c` creates a private GitHub repo and invites friends by username; they run `sk league` and accept the invite. Your solves publish automatically after every `sk log`: what you solved, how (on your own, hints, AI…), complexity and time. Never your code or notes.
- `sk league` shows the leaderboard and recent activity; `sk league 15` compares everyone on one problem. The league repo's README is a leaderboard you can check on GitHub.
- A League tab in `sk stats` when you're in one. Leave with `-l`; the creator can delete it with `-d`.

## 0.4.0

- **Pause the timer:** `sk pause` when you step away, `sk start` to resume. Paused time isn't counted.
- **Cancel it:** `sk start -c` throws the timer away; `sk log` asks for the time instead.
- **Forgot to pause?** If the timer says more than 2 hours (or 3× your target for that difficulty), `sk log` asks whether that was really all solving time.
- The running or paused timer shows in `sk` and `sk which`; Zed / VS Code get a "pause timer" task.

## 0.3.0

- **Problems can be mastered.** 4 clean solves in a row (each one on time, on target, no hints or help) and a problem is ✅ mastered: out of the review queue for good. A non-clean redo puts it back. Change the number with `sk config -g`.
- Pattern levels: learning → practising → solid (all solved, 70%+ clean) → mastered (every problem mastered).
- Mastered counts in stats, `sk review`, `sk list` and LIST.md, and `sk log` tells you when it happens.

## 0.2.1

- TypeScript workspaces no longer flag `nums[i]` as "possibly undefined" (`noUncheckedIndexedAccess` is off, like on LeetCode). `strict` stays on. Run `sk update` to apply it to your workspace.

## 0.2.0

- **Not happy with a solution?** `sk log` asks how you feel about it (😬 not happy · 👍 fine · 😎 nailed it). Not happy brings it back for review in 2 days; nailed it waits twice as long.
- **Above the target complexity now counts.** If your time or space is worse than the target, the problem comes back in 3 days and isn't "clean" in stats. Existing attempts are checked too.
- **Stats:** "clean" means how you solved each problem most recently, so a clean redo counts fully.
- **Hidden tests for every problem:** 2,500+ edge and random cases, and speed checks on 75 problems.
- `sk play` runs every example with your logs; `sk submit`; readable lists and trees in your logs.
- `sk config` flags (`-e`, `-r`, `-w`, `-n`, `-d`); remove workspaces safely to the Trash.
- `sk -v` / `sk --version`, and `sk update` shows what changed.

## 0.1.0

- First release: the NeetCode 150 in TypeScript and Python, tests, hints, timer, logging, spaced repetition, stats, Zed / VS Code / Cursor / vim.
