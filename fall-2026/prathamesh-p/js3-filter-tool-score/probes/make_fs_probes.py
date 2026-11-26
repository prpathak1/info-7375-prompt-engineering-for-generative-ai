"""Write probes/fs.json for the Filesystem MCP server evaluation.  python -I probes/make_fs_probes.py <sandbox dir>

The sandbox holds: allowed/ (the only directory passed to the server), allowed/inside.txt, allowed/link-to-outside
(a Windows junction to outside/), outside/canary.txt, and allowed-evil/canary.txt (a sibling sharing the prefix).
"""
import json
import sys
from pathlib import Path

W = str(Path(sys.argv[1]).resolve())
A = str(Path(W) / "allowed")
O = str(Path(W) / "outside")
SEP = "\\" if "\\" in W else "/"


def j(*parts):
    return SEP.join(parts)


def req(i, m, p=None):
    d = {"jsonrpc": "2.0", "id": i, "method": m}
    if p is not None:
        d["params"] = p
    return d


steps = [{"label": "initialize", "send": req(1, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                                               "clientInfo": {"name": "js3-probe", "version": "1"}})},
         {"label": "initialized", "send": {"jsonrpc": "2.0", "method": "notifications/initialized"}, "expect_reply": False},
         {"label": "tools/list", "send": req(2, "tools/list")}]
calls = [
    ("P1 list_allowed_directories", "list_allowed_directories", {}),
    ("P2 read inside (absolute)", "read_text_file", {"path": j(A, "inside.txt")}),
    ("P3 read outside canary (absolute)", "read_text_file", {"path": j(O, "canary.txt")}),
    ("P4 read outside via .. traversal", "read_text_file", {"path": j(A, "..", "outside", "canary.txt")}),
    ("P5 read prefix-sibling allowed-evil", "read_text_file", {"path": j(W, "allowed-evil", "canary.txt")}),
    ("P6 read relative path inside.txt", "read_text_file", {"path": "inside.txt"}),
    ("P7 read relative ../outside", "read_text_file", {"path": j("..", "outside", "canary.txt")}),
    ("P8 read through junction allowed/link-to-outside", "read_text_file", {"path": j(A, "link-to-outside", "canary.txt")}),
    ("P9 list junction directory", "list_directory", {"path": j(A, "link-to-outside")}),
    ("P10 write inside (declared allowed)", "write_file", {"path": j(A, "written-inside.txt"), "content": "probe write inside"}),
    ("P11 write outside (absolute)", "write_file", {"path": j(O, "written-outside.txt"), "content": "ESCAPED"}),
    ("P12 write outside via ..", "write_file", {"path": j(A, "..", "outside", "written-dotdot.txt"), "content": "ESCAPED"}),
    ("P13 write through junction", "write_file", {"path": j(A, "link-to-outside", "written-junction.txt"), "content": "ESCAPED"}),
    ("P14 copy outside canary into allowed", "copy_file", {"source": j(O, "canary.txt"), "destination": j(A, "copied.txt")}),
    ("P15 move inside file to outside", "move_file", {"source": j(A, "written-inside.txt"), "destination": j(O, "moved.txt")}),
    ("P16 directory_tree of parent", "directory_tree", {"path": W}),
    ("P17 search_files for canary from allowed", "search_files", {"path": A, "pattern": "canary"}),
    ("P18 get_file_info outside", "get_file_info", {"path": j(O, "canary.txt")}),
    ("P19 unknown tool", "delete_everything", {}),
    ("P20 bad args (missing path)", "read_text_file", {}),
]
for i, (label, name, args) in enumerate(calls, 3):
    steps.append({"label": label, "send": req(i, "tools/call", {"name": name, "arguments": args})})
out = Path(__file__).resolve().parent / "fs.json"
out.write_text(json.dumps(steps, indent=1), encoding="utf-8")
assert "\x07" not in out.read_text(encoding="utf-8")
print(f"{len(steps)} steps -> {out}")
