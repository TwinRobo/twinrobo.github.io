"""Media of the home page (``docs/assets/home/``): the hero video and the compare slider.

    python tools/home_media.py [--runs ~/git/TwinRobo-VLA-benchmark/runs/openvla-libero_spatial/videos]

Two OpenVLA rollouts of the same LIBERO-Spatial task from the same initial state, as the
policy sees them: through the simulator's pinhole (the camera it was trained with; it
succeeds) and through another camera at the same place (it fails). The pinhole side holds
its last frame, marked as a success, until the other ends. Needs ffmpeg.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "docs" / "assets" / "home"
TASK, TRIAL = 3, 0  # "pick up the black bowl on the cookie box and place it on the plate"
LEFT = ("pinhole__pinhole", "Pinhole")
RIGHT = ("camera__intel--realsense-d455--color", "Real camera")  # a real camera, not named on the page
COMPARE = "stereolabs--zed-x--2.2mm"  # the slider's camera (not named on the page)
SIZE = 400  # px per side (the policy's images are 256 x 256)
FPS = 20
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def frames(path: Path) -> int:
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True)  # fmt: skip
    return int(out.stdout.strip())


def text(s: str, y: str, size: int, font: str = FONT, color: str = "white", box: str = "black@0.55",
         enable: str | None = None) -> str:
    t = (f"drawtext=fontfile={font}:text='{s}':x=(w-tw)/2:y={y}:fontsize={size}:fontcolor={color}:"
         f"box=1:boxcolor={box}:boxborderw=10")  # fmt: skip
    return t + (f":enable='{enable}'" if enable else "")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs", type=Path,
                    default=Path.home() / "git/TwinRobo-VLA-benchmark/runs/openvla-libero_spatial/videos")  # fmt: skip
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    left, right = (a.runs / f"{name}__task{TASK}_trial{TRIAL}.mp4" for name, _ in (LEFT, RIGHT))
    nl, nr = frames(left), frames(right)
    tl, tr = nl / FPS, nr / FPS
    hold = max(0.0, tr - tl)
    graph = (
        f"[0:v]scale={SIZE}:{SIZE}:flags=lanczos,tpad=stop_mode=clone:stop_duration={hold:.2f},"
        f"{text(LEFT[1], 'h-th-16', 22)},"
        f"{text('Success', '(h-th)/2', 38, BOLD, 'white', '0x1baf7a@0.9', f'gte(t,{tl:.2f})')}[l];"
        f"[1:v]scale={SIZE}:{SIZE}:flags=lanczos,{text(RIGHT[1], 'h-th-16', 22)},"
        f"{text('Failed', '(h-th)/2', 38, BOLD, 'white', '0xe34948@0.9', f'gte(t,{tr - 1.2:.2f})')},"
        f"tpad=stop_mode=clone:stop_duration=1.5[r];"
        f"[l]tpad=stop_mode=clone:stop_duration=1.5,pad=iw+8:ih:0:0:color=0x16161a[lp];[lp][r]hstack=inputs=2[v]"
    )
    video = OUT / "hero.mp4"
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-i", str(left), "-i", str(right), "-filter_complex", graph,
         "-map", "[v]", "-an", "-r", str(FPS), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24",
         "-preset", "slow", "-movflags", "+faststart", str(video)],
        check=True,
    )  # fmt: skip
    subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-ss", "1.0", "-i", str(video), "-frames:v", "1", "-q:v", "4",
         str(OUT / "hero-poster.jpg")],
        check=True,
    )  # fmt: skip
    (OUT / "hero.json").write_text(json.dumps({"task": TASK, "trial": TRIAL, "left": LEFT[0], "right": RIGHT[0],
                                               "left_s": tl, "right_s": tr}, indent=1))  # fmt: skip
    # the compare slider: a wrist view through the pinhole and a real camera (docs playground)
    pg = SITE / "docs" / "assets" / "playground" / "mujoco-pickplace" / COMPARE
    shutil.copyfile(pg / "pinhole.webp", OUT / "compare-pinhole.webp")
    shutil.copyfile(pg / "raycast.webp", OUT / "compare-camera.webp")
    for f in (video, OUT / "hero-poster.jpg"):
        print(f.relative_to(SITE), f"{f.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
