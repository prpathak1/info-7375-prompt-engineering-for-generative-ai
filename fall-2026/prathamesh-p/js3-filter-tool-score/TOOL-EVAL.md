# Agent as a tool: my server and one third-party server, evaluated the same way

- **Drafted by:** Claude Code (Opus 5.5), 2026-11-25 about 19:20 EST.
- **Every "actual" line below is from a transcript in `transcripts/`.**
- **Trust decisions** are Prathamesh's, inserted verbatim on 2026-11-25. They were drafted by Claude (claude.ai chat) at his request, and he reviewed and edited them where he disagreed.
- **The transcripts were redacted after capture** (2026-11-25 19:30 EST, `python -I redact_paths.py --apply`). Every occurrence of the Windows user folder (long name and 8.3 short name, in every escaped form) was replaced with `<USER_HOME>`, and nothing else changed (the JSONL still parses). So where this document says a message "echoes the full absolute path", the stored transcript now shows `<USER_HOME>` in its place.

## A. `js3-score-posting` (mine, `mcp_server.py`, written from scratch)

**Shape:**
- newline-delimited JSON-RPC 2.0 over stdio;
- `initialize`, `notifications/initialized`, `ping`, `tools/list`, `tools/call`;
- one tool, `score_posting(board, posting_id)`;
- Python standard library only.

### Transcripts

| File | What it is |
|---|---|
| `transcripts/probe-own.jsonl` | Scripted client `mcp_probe.py`, 18 steps, 2026-11-25 19:14 EST: every message sent and received, plus server stderr |
| `transcripts/server-20261125T191434-2620.jsonl` | The server's own wire log for that session |
| `transcripts/claude-client-20261125T191455.jsonl` | **Real client: Claude Code 2.1.332** (`claude -p ... --mcp-config probes/claude-mcp-config.json --strict-mcp-config --allowedTools mcp__js3__score_posting --output-format stream-json --verbose`), 19:14:55–19:15:13 EST, exit 0 |
| `transcripts/server-20261125T191459-33532.jsonl` | The server's wire log for the Claude Code session (complete: discover, initialize, tools/list, tools/call, EOF) |
| `transcripts/probe-own-v0.3-smoke.jsonl`, `server-20261125T192830-15960.jsonl` | 4-step smoke test after the server moved to 0.3.0 / FILTER v0.3 (2026-11-25 19:28 EST): initialize, tools/list and one call returned `filter_version: v0.3` |

All rows above except the smoke test were captured with the server at **0.2.0 (FILTER v0.2)**. The server now runs FILTER v0.3. The probes of its declared behavior were not re-run in full at 0.3.0; only the smoke test was.

### Declared vs. actual

| Declared | Actual (evidence) |
|---|---|
| One tool, `score_posting`; capabilities `tools` only | `tools/list` returned exactly 1 tool. `resources/list` → -32601 (probe 12). Claude Code's start-up listed only `mcp__js3__score_posting` for js3. |
| Read-only (`readOnlyHint: true`), no network | No network code in `mcp_server.py`, `filter.py` or `postings.py` (they read `raw/` only). **Not proven at runtime:** no network monitor was run. |
| **First version of the description said "no writes, no side effects"** | **False:** the server writes its own transcript log (`transcripts/server-*.jsonl`) on every message. Found while writing this evaluation, after the scripted probe. **The description was corrected at about 19:14:40 EST, before the Claude Code session.** The probe transcript still shows the old wording. |
| Arguments: exactly `{board, posting_id}`, patterned strings | Extra arg (6), missing arg (7), `../../../GATE.md` (8), `..\..\fixtures` (9) and a number (10) were all refused with -32602 before any file access. Unknown tools `delete_posting` (5) and `write_file` (13) → -32602. |
| Unknown posting → tool error | `does-not-exist` → `isError: true` (11) |
| Robust framing | Malformed JSON → -32700 (14). Batch → -32600 (15). 100 KB line → -32600, and the next `ping` was still answered (16, 17). |
| Protocol versions: answers the client's version if it is known | The scripted client asked for 2025-06-18 and got 2025-06-18. **Claude Code first sent `server/discover` (protocol `2026-07-28`)**, which this server doesn't implement: it got -32601. Claude Code then fell back to `initialize` with `2025-11-25`, which was accepted. |
| The output is evidence, not advice | Every result carries `"note": "Evidence only..."`. Claude Code repeated the note in its answer. |

### What a compatible client is NOT entitled to

- any write, network request, login, application or message (none is offered);
- the persona's resume (it is read internally, never returned);
- any posting not already in `raw/`, or any file by path;
- a listing of all postings (there is no list tool);
- correctness of the decision (FILTER v0.2 has known limits: GROUNDING.md, the audit);
- a promise that its calls are private: **every call is logged** in `transcripts/`;
- treating `readOnlyHint` as a guarantee: it is my claim, checked only by the probes above.

### Client behavior seen

- The prompt said "Do not use any other tool". Claude Code still called its built-in `ToolSearch` once, to load the MCP tool's definition, and said so in its answer.
- `--allowedTools` limits which tools are *approved*, not the harness's own tool loading.

**Trust decision (Prathamesh's; drafted by Claude in claude.ai chat at his request, reviewed and edited by him, see SOURCES.md):**

> TRUST DECISION, my server (js3-score-posting): I trust it for one use: letting a client score postings already saved on disk. The transcripts show one tool with strict arguments that refuses traversal, unknown tools and oversized input. I don't trust its output as advice: it passes employer-written posting text to the client, which must treat it as data, not instructions. Its own description was wrong once (it said "no writes" while logging every call), which is why I check transcripts, not descriptions.

## B. Third party: Filesystem MCP server `@modelcontextprotocol/server-filesystem@2.2.0`

- **Version:** pinned 2.2.0, published 2026-11-04 per `npm view ... time`; the latest at evaluation time was 2.4.0. It reports itself as `serverInfo: secure-filesystem-server 2.2.0`.
- **How it was run:** `npx -y @modelcontextprotocol/server-filesystem@2.2.0 <sandbox>\allowed`, through the same `mcp_probe.py`.
- **The sandbox** is in Claude's scratchpad, outside the repo:
  - `allowed/` (the only directory given to the server), holding `inside.txt` and `link-to-outside`, a **Windows directory junction to `outside/`**;
  - `outside/canary.txt`;
  - `allowed-evil/canary.txt`, a sibling sharing the name prefix.

### Transcripts

- `transcripts/probe-fs-discover.jsonl` (initialize + tools/list)
- `transcripts/probe-fs.jsonl` (23 steps, 2026-11-25 19:17 EST)
- `transcripts/probe-fs.INVALID-mangled-paths-191625.jsonl`: the first attempt. **Invalid:** a shell heredoc turned `\a` in `\allowed` into a bell character, so its paths were wrong. It is kept only as a record and is not evidence about the server.

### Declared vs. actual

| Declared | Actual (evidence) |
|---|---|
| Capabilities `tools` (listChanged) and `resources` (listChanged) | 16 tools listed (10 `readOnlyHint: true`; 6 not: write_file, append_file, edit_file, create_directory, move_file, copy_file). Resources were not probed. |
| 16 tools with annotations: 10 `readOnlyHint: true`; `write_file`, `edit_file` and `move_file` are `destructiveHint: true` | Annotations are self-reported. `write_file` inside `allowed/` succeeded (P10) **with no confirmation step**: any connected client can create, overwrite or move files inside the allowed directory. |
| Access limited to the allowed directories (`list_allowed_directories`, P1) | **Held in every probe:** absolute outside (P3), `..` traversal (P4, P12), prefix-sibling `allowed-evil` (P5), relative `..\outside` (P7), **read, list and write through the junction** (P8, P9, P13: "symlink target outside allowed directories"), copy outside → inside (P14), move inside → outside (P15), the parent's tree (P16), outside `get_file_info` (P18). `search_files` didn't follow the junction (P17: no matches). |
| — | **Disk state after the run:** the only new file is `allowed/written-inside.txt`. `outside/` holds only `canary.txt`. Nothing escaped. |
| Relative paths | `inside.txt` (P6) resolved inside `allowed/` and was read. |
| Errors | Unknown tool → -32602 (P19). A missing argument → `isError` with a validation message (P20). **Every refusal message echoes the full absolute path**, including the Windows user folder: information disclosure to the client. |
| Allowed directories fixed by the command line | stderr: "Client does not support MCP Roots, using allowed directories set from server args". With a **Roots-capable client, the client can change the allowed directories**, so the boundary is then whatever the client says. **Not probed.** |

### What a compatible client is NOT entitled to

- reads or writes outside the allowed directories (enforced in these probes);
- following links out of them (enforced for a junction);
- assuming `readOnlyHint` or `destructiveHint` are enforced by anyone (they are hints);
- a confirmation step before a destructive call (the server has none; that is the client's job).

### Not checked (genuine gaps)

- symlink or junction **swap races** (time-of-check vs time-of-use);
- 8.3 short names as an escape (stderr shows it normalizes both `PRATHA~1` and the long form for the allowed directory; outside short names were not tried);
- UNC paths and alternate data streams;
- case variation;
- huge files;
- `edit_file` and `append_file` behavior;
- the resources API;
- the Roots-driven directory change;
- the package's source code and npm integrity (beyond what npx does itself).

**Trust decision (Prathamesh's; drafted by Claude in claude.ai chat at his request, reviewed and edited by him, see SOURCES.md):**

> TRUST DECISION, Filesystem MCP server 2.2.0: I trust it only in a narrow setup: pinned to 2.2.0, given one throwaway folder holding nothing I care about, and used with a client that asks me before every write. Its boundary held in every probe I ran, including through a junction, but it writes with no confirmation and its error messages expose my full paths. I would not point it at my home folder or my repo, and I didn't test the MCP Roots path, so I wouldn't use a client that changes its allowed folders.
