# Not checked: running list for the JS2 sign-off

1. **Gate-1 title calls on the new boards (added 2026-11-10, Prathamesh's decision on FRICTIONAL F6).** The JS1 title rule is unchanged
   (JS1 CONTRACT governs it), and on 2026-11-10 data it makes calls that Claude Code read as questionable. For example, openai "RTL Design Engineer,
   Networking / NoC" → include (network-on-chip, which is chip design); openai "Community Programs Manager, Champion Network" → flag; cloudflare
   "Senior Engineering Manager, Cloudflare Network Interconnect" → include ("Engineering" counts as a role word). No hand labels were made for these boards.
2. **True symlink escape (added 2026-11-10, Prathamesh's decision on FRICTIONAL F8).** The escape test uses a directory junction. A real symlink needs
   admin or Developer Mode on this machine (`mklink /D` was refused on 2026-11-10), so a symlink escape is not tested.
3. **Hard-link escape (added 2026-11-10, Prathamesh's step-7 pick).** `policy.check_write` checks where a path points, not which file it is. A hard link under a writable folder to a
   file outside the project passes the policy. Prathamesh's demo run (`review/07-still-missed.txt`, 09:17:59 EST) showed a plain write (`_write`) changing the outside file, while an atomic
   write (`_write_atomic`) did not. No test covers it, and `policy.py` does not close it. See `review/07-still-missed.md`.
4. **Check-then-write race (added 2026-11-10, Prathamesh's step-7 claim).** A link or junction swapped in between `check_write` and the write is not tested and not prevented.
