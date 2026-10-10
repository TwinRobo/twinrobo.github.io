# Camera benchmark

**Which camera will my robot see best with?** The TwinRobo benchmark puts each catalog
camera's digital twin on a robot and scores what it sees on perception and robot tasks:
fiducial pose, object detection and segmentation, depth from one image, grounding with a
vision-language model, and a vision-language-action policy's task success.

This is version 0.1, in simulation only. It shows what the twins predict and how the
benchmark works; whether real cameras rank the same way is the next step (see
[What is next](#what-is-next)). The full per-camera numbers are on
[Results](results.md).

## How it works

- **Cameras.** The 12 cameras of the [catalog](../catalog.md) and an ideal pinhole as the
  reference, each in three conditions:
    - **as mounted:** where LIBERO's agent-view camera is, with the camera's own field of
      view, resolution and lens;
    - **framed:** moved along its optical axis until the workspace fills its frame as it
      fills the reference's (a wide camera moves closer), which removes placement;
    - **optics only:** LIBERO's field of view with the camera's sensor resolution and
      lens blur, which removes framing and distortion.
- **Scenes.** 200 fixed LIBERO frames: LIBERO-Spatial demonstrations at three points of
  each episode, and the fixed initial layouts of LIBERO-Object, LIBERO-Goal and LIBERO-10
  (tabletops, a kitchen, a living room). Every image comes with the simulator's depth and
  object labels, warped through the same lens.
- **Tasks.** One model per task, each pinned to an exact release, the same for every
  camera:

| Task | What it measures | Model |
|---|---|---|
| Fiducial | range, corners found and pose error of a 21 x 15 cm ChArUco board | none (OpenCV), with the camera's calibration |
| Detection | mAP at IoU 0.5 of the scene's objects | Grounding DINO |
| Segmentation | mask IoU, given each object's true box | SAM |
| Depth | depth error on the objects, from one image | Depth Anything V2, Depth Pro |
| Grounding | "where is the black bowl?": the answer's box lands on it | Qwen2.5-VL-7B |
| Robot policy | task success, closed loop, 100 episodes | OpenVLA fine-tuned on LIBERO-Spatial |

- **Reproducible.** Seeds, deterministic GPU kernels, greedy decoding and seeded
  confidence intervals: recomputing a result gives the same numbers, bit for bit. Each
  result records the TwinRobo-Core commit and model revisions it was computed with.

## Findings

### Placement decides more than the camera

As mounted, wide cameras find far fewer objects: they see the same scene smaller.
Framed to see the same workspace, every color camera lands within the same few points.

| Detection mAP50 | As mounted | Framed |
|---|---|---|
| Stereolabs ZED X 2.2 mm (110° wide) | 54.9 | 66.3 |
| Intel RealSense D455 RGB (90°) | 55.2 | 62.8 |
| Raspberry Pi Camera Module 3 Wide (100°) | 56.3 | 64.8 |
| Raspberry Pi Camera Module 3 (66°) | 65.8 | 64.4 |
| Intel RealSense D435 RGB (69°) | 65.4 | 62.9 |

The framed values of all nine color cameras span 62.8 to 66.3, and their 95 % intervals
overlap. Before comparing cameras, fix where they will be mounted.

### Lens distortion hurts depth from one image

Monocular depth models assume an undistorted image. Framed, a wide lens fills the image
with the workspace, edges included, where its barrel distortion is strongest, and the
depth error on the objects grows; without the distortion (optics only) it is back with
the others.

| Depth error on objects, Depth Anything V2 | Framed | Optics only |
|---|---|---|
| Stereolabs ZED X 2.2 mm | 9.6 % | 5.5 % |
| Raspberry Pi Camera Module 3 Wide | 8.7 % | 5.9 % |
| Intel RealSense D435 RGB (narrow) | 5.8 % | 5.9 % |

Depth Pro shows the same: 40.3 % framed against 26.4 % optics only for the ZED X 2.2 mm.
Undistorting wide-angle images before a depth model is worth it.

### Color matters for detection

The Luxonis OAK-D's mono camera scores about 7 points below the color cameras in every
condition (55.1 / 57.2 / 57.1 mAP50 as mounted / framed / optics only). This is one
difference between cameras the benchmark measures consistently.

### A VLA policy depends on its training camera's field of view

OpenVLA was fine-tuned on LIBERO's camera (45° vertical). It sees a square center crop,
so the vertical field of view is what changes its input:

| Camera, as mounted | Vertical field of view | OpenVLA success |
|---|---|---|
| Intel RealSense D435 RGB | 42.5° | 87 % |
| Logitech C920 | 43.3° | 84 % |
| LIBERO's own camera (reference) | 45° | 85 % |
| Luxonis OAK-D mono | 48.9° | 65 % |
| Stereolabs ZED X 4 mm | 50.6° | 46 % |
| Intel RealSense D455 RGB | 64.5° | 0 % |
| Stereolabs ZED X 2.2 mm | 80.0° | 0 % |

With LIBERO's field of view and each camera's lens only, the same policy succeeds 82-85 %
of the time (four cameras, 40-48 episodes each): the lens alone does not break it. The
ZED X 4 mm does worse than its field of view alone suggests; why is open. A policy has to
be fine-tuned for, or tested with, the camera it will run with.

### Some models react to the image format, not the camera

- **Grounding** with Qwen2.5-VL varies by up to 12 points between cameras even with the
  same view (optics only), following each image's size and aspect, and on some image
  sizes its boxes come back compressed sideways by 2-3 %. Its results say how this model
  handles an image format more than how good a camera is.
- **Depth Pro** is more accurate for wide cameras as mounted (more context for its
  scale), and less accurate for the same cameras framed.

"Which camera is best" therefore depends on the task and the model: the benchmark reports
each task separately and gives no overall score.

### What the surrogate lenses do not show

With the field of view fixed (optics only), detection spans 63.6 to 65.2 across the
color cameras and segmentation 93.3 to 94.8 overall: within the intervals. The catalog's
lenses are surrogates scaled to each camera's focal length and f-number, so differences
between real lenses are not expected to show yet.

## Limits

- **Simulation only.** Lenses are surrogates; sensor noise, exposure and motion blur are
  not simulated. The results rank digital twins.
- **Infrared eyes in visible light.** The RealSense depth modules' infrared imagers are
  rendered in visible light, so their detection, depth and grounding scores are not what
  they would see.
- **VLA coverage.** Six cameras were run with OpenVLA, most of their episodes with the
  TwinRobo-Core release before its current PSF settings; all other results use
  TwinRobo-Core 075020f.

## What is next

1. **Real captures:** the fiducial test on the bench with the real cameras, compared with
   their twins' ranking.
2. **Measured lenses** for a few cameras (the [calibration tool](../calibration.md)) and
   the sensor noise model, so lens and low-light differences can show.
3. **The robot-policy column** for every camera, framed and optics only.

The benchmark's code will be released with the real-capture study.
