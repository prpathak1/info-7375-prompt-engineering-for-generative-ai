# Not checked: running list for the JS2 sign-off

1. **Gate-1 title calls on the new boards (added 2026-11-10, Prathamesh's decision on FRICTIONAL F6).** The JS1 title rule is unchanged
   (JS1 CONTRACT governs it), and on 2026-11-10 data it makes calls that Claude Code read as questionable. For example, openai "RTL Design Engineer,
   Networking / NoC" → include (network-on-chip, which is chip design); openai "Community Programs Manager, Champion Network" → flag; cloudflare
   "Senior Engineering Manager, Cloudflare Network Interconnect" → include ("Engineering" counts as a role word). No hand labels were made for these boards.
2. **True symlink escape (added 2026-11-10, Prathamesh's decision on FRICTIONAL F8).** The escape test uses a directory junction. A real symlink needs
   admin or Developer Mode on this machine (`mklink /D` was refused on 2026-11-10), so a symlink escape is not tested.
