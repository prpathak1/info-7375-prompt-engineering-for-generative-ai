# Local Windows patches to brutalist.art

These patches are applied to `C:\info7375\brutalist.art-latest` (upstream `519fcbb`) and are **not
committed** to the toolkit. They are the same 4 fixes as Week 1, re-applied to the newer code.
The old clone (`C:\info7375\brutalist.art`, `cd4bf20`) was not touched.

| File | Fixes | Applied against |
|---|---|---|
| `01-compile-drawtext-windows-path.diff` | `compile.py`: ffmpeg `drawtext=fontfile=` received a raw `C:\...` path, and the `:` and `\` broke filter parsing | upstream + patch 02 (incremental) |
| `02-compile-timecode-title-safe.diff` | `compile.py`: the review-cut timecode sat outside the 5% title-safe area, so GATE V failed every review cut | upstream |
| `compile-cumulative-01+02.diff` | both compile.py patches as one diff | upstream |
| `03-remotion-scenes-npx-windows.diff` | `remotion_scenes.py`: bare `"npx"` can't be launched by `subprocess` on Windows (it is `npx.cmd`) | upstream |
| `04-setup-elevenlabs-guard-exclude-youtube.diff` | `setup`: the ElevenLabs guard failed on the repo's own `youtube/` example reels (10 hits) | upstream |

Re-apply on a fresh clone (Git Bash, from the toolkit root):

```
git apply <this-folder>/compile-cumulative-01+02.diff
git apply <this-folder>/03-remotion-scenes-npx-windows.diff
git apply <this-folder>/04-setup-elevenlabs-guard-exclude-youtube.diff
```

Revert: `git -C C:\info7375\brutalist.art-latest checkout -- runtime/scripts/compile.py runtime/scripts/remotion_scenes.py setup`
