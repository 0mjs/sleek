// Leagues: a private GitHub repo where friends share how they're doing (never code or notes).
// Each player owns one file, players/<github-login>.json; the repo's README is a generated leaderboard.
// Sync always resets to the remote and rewrites only your own file, so pushes never conflict.
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { ago, clean, loadAttempts, masteredFolders, passed, type Attempt } from "./attempts";
import { loadConfig, saveConfig, type Config } from "./config";
import { formatDuration } from "./duration";
import { LANGUAGES } from "./languages";
import { CONFIG_DIR, TOOL } from "./paths";
import type { Workspace } from "./workspace";

export const LEAGUE_DIR = join(CONFIG_DIR, "league");
export const LEAGUE_DESCRIPTION = "A SleekCode league 🏆";
const MARKER = ".sleekcode-league.json";

// ---------- gh + git ----------

export const run = (cmd: string[], cwd?: string) => {
  const r = Bun.spawnSync(cmd, { cwd, stdout: "pipe", stderr: "pipe" });
  return { ok: r.exitCode === 0, out: r.stdout.toString().trim(), err: r.stderr.toString().trim() };
};
export const gh = (...args: string[]) => run(["gh", ...args]);
export const hasGh = () => !!Bun.which("gh");
export const ghLoggedIn = () => hasGh() && gh("auth", "status").ok;
/** Your GitHub username (SLEEKCODE_LEAGUE_LOGIN overrides it, for testing) */
export const githubLogin = () => process.env.SLEEKCODE_LEAGUE_LOGIN ?? gh("api", "user", "--jq", ".login").out;

const git = (...args: string[]) => run(["git", ...args], LEAGUE_DIR);
/** A league can also be a local path to a git repo (used for testing without GitHub) */
const isLocal = (repo: string) => repo.startsWith("/");

export function cloneLeague(repo: string): { ok: boolean; err: string } {
  rmSync(LEAGUE_DIR, { recursive: true, force: true });
  mkdirSync(CONFIG_DIR, { recursive: true });
  const r = isLocal(repo) ? run(["git", "clone", "-q", repo, LEAGUE_DIR]) : gh("repo", "clone", repo, LEAGUE_DIR, "--", "-q");
  return { ok: r.ok, err: r.err };
}

const branch = () => git("rev-parse", "--abbrev-ref", "origin/HEAD").out.replace(/^origin\//, "") || "main";

/** Latest from the remote (discards nothing of yours: your file is rebuilt from attempts.json every time) */
export function pullLeague(): boolean {
  if (!existsSync(join(LEAGUE_DIR, ".git"))) return false;
  if (!git("fetch", "-q", "origin").ok) return false;
  return git("reset", "-q", "--hard", `origin/${branch()}`).ok;
}

// ---------- what's shared ----------

/** One attempt, as shared: how you did it, never your code or notes */
type SharedAttempt = Pick<Attempt, "at" | "language" | "pass" | "total" | "seconds" | "help" | "hints" | "complexity" | "aboveTarget" | "feel">;
export type Player = {
  login: string;
  updated: string;
  languages: string[];
  /** Worked out by the player with their own settings, so everyone sees the same numbers */
  mastered?: number;
  problems: Record<string, { id: string; title: string; difficulty: string; pattern: string; blind75: boolean; attempts: SharedAttempt[] }>;
};

export async function playerFile(ws: Workspace, login: string): Promise<Player> {
  const attempts = await loadAttempts(ws);
  const problems: Player["problems"] = {};
  for (const a of attempts) {
    const p = ws.problems.find((x) => x.folder === a.folder);
    problems[a.folder] ??= { id: a.id, title: a.title, difficulty: a.difficulty, pattern: a.pattern, blind75: !!p?.blind75, attempts: [] };
    const { at, language, pass, total, seconds, help, hints, complexity, aboveTarget, feel } = a;
    problems[a.folder]!.attempts.push({ at, language, pass, total, seconds, help, hints, complexity, aboveTarget, feel });
  }
  return { login, updated: new Date().toISOString(), languages: [...new Set(attempts.map((a) => a.language))], mastered: masteredFolders(ws, attempts).size, problems };
}

export function readPlayers(): Player[] {
  const dir = join(LEAGUE_DIR, "players");
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter((f) => f.endsWith(".json")).flatMap((f) => {
    try {
      return [JSON.parse(readFileSync(join(dir, f), "utf8")) as Player];
    } catch {
      return [];
    }
  });
}

// ---------- numbers for the leaderboard ----------

const DAY = 86_400_000;
const allAttempts = (p: Player) => Object.entries(p.problems).flatMap(([folder, x]) => x.attempts.map((a) => ({ ...a, folder, title: x.title, difficulty: x.difficulty as Attempt["difficulty"], id: x.id })));

export function standing(p: Player, graduateAfter: number) {
  const atts = allAttempts(p) as unknown as Attempt[];
  const solved = Object.values(p.problems).filter((x) => x.attempts.some((a) => passed(a as Attempt))).length;
  const latest = Object.values(p.problems).map((x) => x.attempts.at(-1) as Attempt);
  const cleanNow = latest.length ? latest.filter(clean).length / latest.length : 0;
  // mastered: graduateAfter clean solves in a row (time targets aren't shared, so this uses clean only)
  const mastered = p.mastered ?? Object.values(p.problems).filter((x) => {
    let s = 0;
    for (let i = x.attempts.length - 1; i >= 0 && clean(x.attempts[i] as Attempt); i--) s++;
    return s >= graduateAfter;
  }).length;
  const dayStart = (t: number) => { const d = new Date(t); d.setHours(0, 0, 0, 0); return d.getTime(); };
  const days = new Set(atts.map((a) => dayStart(Date.parse(a.at))));
  let streak = 0;
  let cur = dayStart(Date.now());
  if (!days.has(cur)) cur = dayStart(cur - DAY / 2);
  while (days.has(cur)) { streak++; cur = dayStart(cur - DAY / 2); }
  const thisWeek = atts.filter((a) => Date.now() - Date.parse(a.at) < 7 * DAY && passed(a)).length;
  const blind = Object.values(p.problems).filter((x) => x.blind75 && x.attempts.some((a) => passed(a as Attempt))).length;
  return { solved, mastered, cleanNow, streak, thisWeek, blind };
}

/** Everyone's attempts, newest first */
export function activity(players: Player[]) {
  return players.flatMap((p) => allAttempts(p).map((a) => ({ ...a, login: p.login }))).sort((a, b) => b.at.localeCompare(a.at));
}

export const howLabel = (a: SharedAttempt) =>
  a.help === "ai" ? "used AI" : a.help === "lookup" ? "looked it up" : a.help === "person" ? "had help" : a.hints ? `on their own · ${a.hints} hint${a.hints > 1 ? "s" : ""}` : "on their own";

// ---------- the repo's README: a leaderboard you can check on GitHub ----------

function leagueReadme(repo: string, players: Player[], graduateAfter: number): string {
  const rows = players
    .map((p) => ({ p, s: standing(p, graduateAfter) }))
    .sort((a, b) => b.s.solved - a.s.solved || b.s.mastered - a.s.mastered || b.s.cleanNow - a.s.cleanNow);
  const table = rows.map(({ p, s }, i) =>
    `| ${i + 1} | [${p.login}](https://github.com/${p.login}) | ${s.solved} | ${s.mastered} | ${Math.round(s.cleanNow * 100)}% | ${s.streak} | ${s.thisWeek} | ${s.blind}/75 |`);
  const recent = activity(players).slice(0, 15).map((a) =>
    `| ${a.login} | ${a.id}. ${a.title} | ${a.pass === a.total && a.total ? "✅" : "❌"} ${howLabel(a)} | ${a.seconds == null ? "–" : formatDuration(a.seconds)} | ${a.complexity || "–"}${a.aboveTarget ? " ⚠️" : ""} | ${LANGUAGES[a.language as keyof typeof LANGUAGES]?.tag ?? a.language} | ${a.at.slice(0, 10)} |`);
  return `# 🏆 ${repo.split("/").pop()}

A private [SleekCode](https://github.com/0mjs/sleek) league. Updated automatically whenever someone logs a solve with \`sk log\`.

## Leaderboard

| # | Player | Solved | Mastered | Clean now | Streak (days) | This week | Blind 75 |
| - | ------ | ------ | -------- | --------- | ------------- | --------- | -------- |
${table.join("\n")}

## Recent

| Player | Problem | How | Time | Complexity | Lang | Date |
| ------ | ------- | --- | ---- | ---------- | ---- | ---- |
${recent.join("\n")}

---

Shared: problems, how they were solved, complexity, time. Never shared: code or notes.
Join with \`sk league\` once you've been invited.
`;
}

// ---------- publishing ----------

/** Writes your file + the README and pushes. Retries from a fresh copy if someone pushed first. */
export async function publish(ws: Workspace, config: Config): Promise<boolean> {
  const league = config.league;
  if (!league) return false;
  if (!existsSync(join(LEAGUE_DIR, ".git")) && !cloneLeague(league.repo).ok) return false;
  const mine = await playerFile(ws, league.login);
  for (let attempt = 0; attempt < 3; attempt++) {
    if (!pullLeague()) return false;
    mkdirSync(join(LEAGUE_DIR, "players"), { recursive: true });
    await Bun.write(join(LEAGUE_DIR, "players", `${league.login}.json`), JSON.stringify(mine, null, 1) + "\n");
    await Bun.write(join(LEAGUE_DIR, "README.md"), leagueReadme(league.repo, readPlayers(), config.graduateAfter));
    git("add", "-A");
    if (!git("diff", "--cached", "--quiet").ok) git("commit", "-q", "-m", `${league.login}: update`);
    if (git("push", "-q", "origin", `HEAD:${branch()}`).ok) return true;
  }
  return false;
}

/** After sk log / edits: publish without making you wait. Failures are retried on your next sk command. */
export function publishInBackground() {
  Bun.spawn(["bun", join(TOOL, "src", "cli.ts"), "league", "--publish"], { stdio: ["ignore", "ignore", "ignore"], env: process.env }).unref();
}

/** Used by the hidden `sk league --publish`: publish, and remember if it didn't go through */
export async function publishNow(ws: Workspace) {
  const config = await loadConfig();
  if (!config?.league) return;
  const ok = await publish(ws, config);
  if (config.league.pending !== !ok) {
    config.league.pending = !ok;
    await saveConfig(config);
  }
}

// ---------- creating ----------

export async function writeLeagueFiles(repo: string, config: Config) {
  await Bun.write(join(LEAGUE_DIR, MARKER), JSON.stringify({ version: 1, repo, created: new Date().toISOString() }, null, 2) + "\n");
  mkdirSync(join(LEAGUE_DIR, "players"), { recursive: true });
  await Bun.write(join(LEAGUE_DIR, "README.md"), leagueReadme(repo, readPlayers(), config.graduateAfter));
}

export const isLeagueClone = () => existsSync(join(LEAGUE_DIR, MARKER));
export { ago };
