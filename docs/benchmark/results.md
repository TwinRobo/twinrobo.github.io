# Results

!!! warning "Simulation only: these rank digital twins, not yet the real cameras"
    Every catalog lens is a surrogate (a published design scaled to the camera's focal
    length and f-number; vendors publish no prescriptions), and sensor noise is not
    simulated. Differences between cameras that survive the *framed* and *optics only*
    conditions are mostly within the 95 % intervals. Grounding mostly reflects how the
    model handles each image's size and aspect, not the optics. The VLA column covers six
    cameras, run with two TwinRobo-Core versions (see [Findings](index.md)).

Benchmark commit `8f25621` · TwinRobo-Core `075020f` · copied 2026-10-10.

## Cameras as mounted (each camera's own field of view, from LIBERO's camera pose)

What each camera sees from the same place: field of view, resolution and lens together.

| Camera | Status | Image (px) | HFoV (deg) | Board range (m) | Board found (%) | Pose error (% of dist.) | Corner error (mrad) | Detection mAP50 | Segmentation mIoU | Object depth AbsRel, DA-V2 (%) | Object depth AbsRel, Depth Pro (%) | VLM grounding hit (%) | OpenVLA success (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| *Ideal pinhole (1024x1024, 45 deg)* | ideal | 1024x1024 | 45 | 0.19–1.99 | 66 | 0.03 | 0.068 | 62.7 | 94.7 | 5.3 | 25.0 | 79.0 | 85 (n=100) |
| Intel RealSense D435 / D435i RGB camera | estimated | 1920x1080 | 69 | 0.15–1.99 | 64 | **0.02** | 0.074 | 65.4 | 94.1 | 5.8 | 25.7 | 77.0 | **87 (n=100)** |
| Intel RealSense D455 RGB camera | estimated | 1280x800 | 90 | 0.15–0.91 | 44 | 0.06 | 0.240 | 55.2 | 94.0 | 7.0 | 16.4 | 50.1 | 0 (n=100) |
| Intel RealSense D435 / D435i IR imager (one stereo eye) †* | estimated | 1280x800 | 90 | 0.15–1.01 | 45 | 0.05 | 0.220 | 48.4 | 93.4 | 7.1 | 14.9 | 62.9 | – |
| Intel RealSense D455 IR imager (one stereo eye) †* | estimated | 1280x800 | 90 | 0.15–1.01 | 45 | 0.05 | 0.220 | 48.3 | 93.4 | 7.1 | 14.9 | 63.2 | – |
| Logitech C920 HD Pro Webcam | estimated | 1920x1080 | 70 | 0.15–1.78 | 66 | 0.03 | 0.099 | 63.4 | 94.3 | 5.9 | 25.6 | 74.2 | 84 (n=100) |
| Luxonis OAK-D color camera | estimated | 4056x3040 | 69 | 0.15–1.99 | 70 | 0.02 | **0.046** | 63.3 | 94.3 | **5.5** | 24.3 | 61.0 | – |
| Luxonis OAK-D mono camera (one stereo eye) * | estimated | 1280x800 | 72 | 0.15–1.27 | 56 | 0.02 | 0.086 | 55.1 | 94.0 | 5.7 | 20.7 | 70.0 | 65 (n=100) |
| Raspberry Pi Camera Module 3 | estimated | 4608x2592 | 66 | 0.21–3.12 | **84** | 0.05 | 0.106 | **65.8** | **94.4** | 5.6 | 25.0 | **79.2** | – |
| Raspberry Pi Camera Module 3 Wide | estimated | 4608x2592 | 100 | 0.15–2.49 | 71 | 0.04 | 0.113 | 56.3 | 93.3 | 7.5 | **13.9** | 58.8 | – |
| Stereolabs ZED X / X Mini 2.2 mm eye | estimated | 1920x1200 | 110 | 0.15–1.01 | 48 | 0.04 | 0.218 | 54.9 | 93.6 | 6.6 | 15.2 | 44.9 | 0 (n=100) |
| Stereolabs ZED X 4 mm eye | estimated | 1920x1200 | 74 | 0.15–1.99 | 66 | 0.02 | 0.067 | 62.1 | 94.4 | 5.7 | 23.4 | 59.2 | 46 (n=100) |
| Stereolabs ZED 2i 2.1 mm eye | estimated | 2208x1242 | 95 | 0.15–1.78 | 57 | 0.03 | 0.122 | 59.7 | 94.1 | 6.2 | 22.7 | 63.1 | – |

## Framed like the reference (each camera moved along its axis to see the same workspace)

Placement removed: a wide camera moves closer until the workspace fills its frame as it does the reference's. What is left: resolution, lens, distortion and perspective.

| Camera | Status | Image (px) | HFoV (deg) | Detection mAP50 | Segmentation mIoU | Object depth AbsRel, DA-V2 (%) | Object depth AbsRel, Depth Pro (%) | VLM grounding hit (%) | OpenVLA success (%) |
|---|---|---|---|---|---|---|---|---|---|
| *Ideal pinhole (1024x1024, 45 deg)* | ideal | 1024x1024 | 45 | 62.7 | 94.7 | 5.3 | 25.0 | 79.0 | 85 (n=100) |
| Intel RealSense D435 / D435i RGB camera · framed | estimated | 1920x1080 | 69 | 62.9 | 94.5 | 5.8 | 25.0 | **73.9** | – |
| Intel RealSense D455 RGB camera · framed | estimated | 1280x800 | 90 | 62.8 | 94.1 | 7.4 | 29.9 | 60.0 | – |
| Logitech C920 HD Pro Webcam · framed | estimated | 1920x1080 | 70 | 62.9 | 94.5 | 5.7 | 24.7 | 71.2 | – |
| Luxonis OAK-D color camera · framed | estimated | 4056x3040 | 69 | 63.2 | 94.1 | 6.0 | 26.3 | 67.8 | – |
| Luxonis OAK-D mono camera (one stereo eye) · framed * | estimated | 1280x800 | 72 | 57.2 | 94.1 | 6.1 | **20.3** | 70.1 | – |
| Raspberry Pi Camera Module 3 · framed | estimated | 4608x2592 | 66 | 64.4 | **94.8** | **5.5** | 21.8 | 71.2 | – |
| Raspberry Pi Camera Module 3 Wide · framed | estimated | 4608x2592 | 100 | 64.8 | 94.0 | 8.7 | 28.7 | 69.3 | – |
| Stereolabs ZED X / X Mini 2.2 mm eye · framed | estimated | 1920x1200 | 110 | **66.3** | 94.1 | 9.6 | 40.3 | 60.8 | – |
| Stereolabs ZED X 4 mm eye · framed | estimated | 1920x1200 | 74 | 64.0 | 94.1 | 5.9 | 26.4 | 62.8 | – |
| Stereolabs ZED 2i 2.1 mm eye · framed | estimated | 2208x1242 | 95 | 64.2 | 93.9 | 6.8 | 34.0 | 71.2 | – |

## Optics only (LIBERO's field of view, each camera's sensor resolution and lens blur)

Framing and distortion removed: what each sensor and lens add to an ideal camera of the same view.

| Camera | Status | Image (px) | HFoV (deg) | Detection mAP50 | Segmentation mIoU | Object depth AbsRel, DA-V2 (%) | Object depth AbsRel, Depth Pro (%) | VLM grounding hit (%) | OpenVLA success (%) |
|---|---|---|---|---|---|---|---|---|---|
| *Ideal pinhole (1024x1024, 45 deg)* | ideal | 1024x1024 | 45 | 62.7 | 94.7 | 5.3 | 25.0 | 79.0 | **85 (n=100)** |
| Intel RealSense D435 / D435i RGB camera · optics only | estimated | 1920x1080 | 73 | 64.1 | 94.3 | 5.9 | 25.2 | 69.8 | – |
| Intel RealSense D455 RGB camera · optics only | estimated | 1280x800 | 67 | 63.6 | 94.0 | 5.6 | 27.5 | 63.0 | 83 (n=48) |
| Logitech C920 HD Pro Webcam · optics only | estimated | 1920x1080 | 73 | 63.9 | 94.3 | 5.9 | 25.1 | 71.4 | 82 (n=40) |
| Luxonis OAK-D color camera · optics only | estimated | 4056x3040 | 58 | 64.7 | 94.3 | **5.1** | 24.6 | **74.8** | – |
| Luxonis OAK-D mono camera (one stereo eye) · optics only * | estimated | 1280x800 | 67 | 57.1 | 94.1 | 5.5 | **21.0** | 71.2 | **85 (n=40)** |
| Raspberry Pi Camera Module 3 · optics only | estimated | 4608x2592 | 73 | 64.3 | **94.4** | 5.9 | 23.5 | 71.5 | – |
| Raspberry Pi Camera Module 3 Wide · optics only | estimated | 4608x2592 | 73 | 64.5 | 94.4 | 5.9 | 24.1 | 70.6 | – |
| Stereolabs ZED X / X Mini 2.2 mm eye · optics only | estimated | 1920x1200 | 67 | **65.2** | 94.2 | 5.5 | 26.4 | 66.5 | **85 (n=40)** |
| Stereolabs ZED X 4 mm eye · optics only | estimated | 1920x1200 | 67 | 64.5 | 94.2 | 5.6 | 25.7 | 66.8 | – |
| Stereolabs ZED 2i 2.1 mm eye · optics only | estimated | 2208x1242 | 73 | 64.0 | 94.4 | 5.9 | 24.8 | 70.2 | – |

\* mono sensor (one channel, shown in all three). † a near-infrared imager rendered in
visible light (the simulators render visible light only): its detection, segmentation,
depth and grounding scores are not what it would see in the infrared.

## How to read it

- **Simulation only.** Every catalog lens is a surrogate (status `estimated`): a published
  glass design scaled to the camera's focal length and f-number, because vendors publish
  no prescriptions. Sensor noise, colour filter, exposure and motion are not simulated.
  The table ranks the twins; whether it ranks the real cameras the same way is what the
  real-capture study is for.
- **Three conditions** (tables below): *as mounted* (every camera where LIBERO's agent-view
  camera is: a wide camera sees the same objects smaller), *framed* (moved along its axis so
  the workspace fills the frame as in the reference) and *optics only* (LIBERO's field of
  view with the camera's sensor and lens). The fiducial board is placed relative to each
  camera, so it is reported for the mounted cameras only.
- **Grounding coordinates:** on some image sizes Qwen2.5-VL's boxes are compressed
  horizontally by 2-3 % (seen on the OAK-D colour, ZED X and D455 colour images; not on
  others of the same input size). It lowers those rows' grounding hits; it is the model's,
  not the camera's.
- **Native resolution.** Images are rendered at each sensor's full resolution. The learned
  models resize their input (Grounding DINO ~800 px, SAM 1024 px, Depth Anything 518 px,
  Depth Pro 1536 px, Qwen2.5-VL ~1 MP), so beyond their input size extra pixels do not
  help them; the fiducial task uses every pixel.

## Tasks

| Column | Scenes | Model | Metric |
|---|---|---|---|
| Board range, found, pose and corner error | ChArUco board 21 x 15 cm (7 x 5 squares of 30 mm), a range sweep 0.15-12 m and a grid of 36 poses: 6 distances (0.3-3 m) x 3 field positions (centre, 50 % and 80 % of each camera's half field) x 2 tilts (0, 50 deg) | OpenCV ChArUco detection (markers >= 12 px), solvePnP with the camera's calibration | range: nearest-farthest distance with >= 50 % of corners found (frontal, centred); found: corners found over the grid; pose: mean 3D corner error / distance (median); corner: error of found corners vs. their true projection, in mrad (px / focal length) |
| Detection | 200 LIBERO frames: LIBERO-Spatial demo_0 and demo_1 of all 10 tasks at 0, 1/3 and 2/3 of the episode (60); LIBERO-Object init states 0-3 (40); LIBERO-Goal and LIBERO-10 init states 0-4 (50 each) | Grounding DINO base, prompted with the scene's object phrases | AP at IoU 0.5 per phrase, mean over phrases |
| Segmentation | same frames | SAM ViT-H, prompted with each object's true box | mask IoU with the true visible mask |
| Object depth | same frames | Depth Anything V2 Large (relative: scale and shift fitted in inverse depth over the whole image); Depth Pro (metric, given the camera's calibrated focal length) | AbsRel on the target objects' pixels (whole-image errors are in the cells: they depend on how much floor and wall a camera's view holds) |
| VLM grounding | same frames | Qwen2.5-VL-7B-Instruct, greedy, ~1 MP input: "Locate the {object} ..." | hit: the returned box's centre lies on the object |
| OpenVLA success | LIBERO-Spatial, 10 tasks x 10 initial states | OpenVLA-7B fine-tuned on LIBERO-Spatial (closed loop) | task success; only the cameras run there |

Targets are the objects with at least 16 visible pixels in a camera's image.

## 95 % intervals

Bootstrap over images (fixed seed); OpenVLA: Wilson interval over episodes.

| Camera | Board found (%) | Detection mAP50 | Segmentation mIoU | Object depth AbsRel, DA-V2 (%) | Object depth AbsRel, Depth Pro (%) | VLM grounding hit (%) | OpenVLA success (%) |
|---|---|---|---|---|---|---|---|
| Ideal pinhole (1024x1024, 45 deg) | 52.5–79.6 | 60.1–65.7 | 94.3–95.1 | 5.0–5.6 | 22.3–27.6 | 77.2–80.8 | 76.7–90.7 |
| Intel RealSense D435 / D435i RGB camera | 49.5–77.8 | 63.4–67.9 | 93.7–94.5 | 5.5–6.1 | 23.4–28.0 | 74.6–79.6 | 79.0–92.2 |
| Intel RealSense D455 RGB camera | 28.9–58.5 | 53.5–57.5 | 93.5–94.4 | 6.6–7.4 | 14.9–18.0 | 47.5–52.8 | 0.0–3.7 |
| Intel RealSense D435 / D435i IR imager (one stereo eye) | 30.0–60.1 | 46.4–51.0 | 92.9–93.9 | 6.7–7.5 | 13.2–16.8 | 60.4–65.3 | – |
| Intel RealSense D455 IR imager (one stereo eye) | 30.0–60.1 | 46.4–51.0 | 92.9–93.9 | 6.7–7.5 | 13.2–16.8 | 60.7–65.6 | – |
| Logitech C920 HD Pro Webcam | 51.5–79.3 | 61.5–66.2 | 93.9–94.7 | 5.5–6.2 | 23.2–28.0 | 72.4–76.2 | 75.6–89.9 |
| Luxonis OAK-D color camera | 58.9–81.7 | 61.7–65.9 | 93.9–94.6 | 5.1–5.8 | 21.7–26.8 | 58.3–63.7 | – |
| Luxonis OAK-D mono camera (one stereo eye) | 40.9–70.7 | 53.1–57.4 | 93.6–94.4 | 5.4–6.0 | 18.3–23.1 | 67.7–72.1 | 55.3–73.6 |
| Raspberry Pi Camera Module 3 | 75.3–92.5 | 64.1–68.2 | 94.0–94.9 | 5.3–5.9 | 22.7–27.3 | 77.0–81.3 | – |
| Raspberry Pi Camera Module 3 Wide | 58.0–82.8 | 54.8–58.7 | 92.8–93.8 | 7.0–7.9 | 12.7–15.0 | 55.8–61.6 | – |
| Stereolabs ZED X / X Mini 2.2 mm eye | 33.4–62.4 | 52.9–57.1 | 93.1–94.0 | 6.1–7.0 | 14.1–16.2 | 42.3–47.7 | 0.0–3.7 |
| Stereolabs ZED X 4 mm eye | 52.5–79.2 | 60.2–64.8 | 94.0–94.8 | 5.4–6.1 | 21.0–25.7 | 56.4–61.9 | 36.6–55.7 |
| Stereolabs ZED 2i 2.1 mm eye | 42.5–71.5 | 58.1–61.9 | 93.7–94.5 | 5.8–6.6 | 20.3–25.0 | 60.5–65.7 | – |
| Intel RealSense D435 / D435i RGB camera · framed | – | 61.3–65.3 | 94.1–94.9 | 5.5–6.2 | 22.5–27.3 | 72.0–76.0 | – |
| Intel RealSense D455 RGB camera · framed | – | 61.0–65.5 | 93.7–94.5 | 6.9–7.8 | 26.8–33.1 | 57.0–62.9 | – |
| Logitech C920 HD Pro Webcam · framed | – | 61.0–65.4 | 94.2–94.9 | 5.4–6.1 | 22.2–27.0 | 68.7–73.6 | – |
| Luxonis OAK-D color camera · framed | – | 60.2–66.2 | 93.7–94.6 | 5.6–6.3 | 23.3–29.3 | 65.4–70.4 | – |
| Luxonis OAK-D mono camera (one stereo eye) · framed | – | 55.4–59.3 | 93.6–94.5 | 5.7–6.4 | 18.0–22.6 | 67.8–72.4 | – |
| Raspberry Pi Camera Module 3 · framed | – | 62.7–66.8 | 94.4–95.1 | 5.2–5.8 | 19.5–24.0 | 69.3–73.4 | – |
| Raspberry Pi Camera Module 3 Wide · framed | – | 63.1–67.2 | 93.6–94.4 | 8.2–9.3 | 26.0–31.5 | 66.9–71.8 | – |
| Stereolabs ZED X / X Mini 2.2 mm eye · framed | – | 64.7–69.0 | 93.8–94.6 | 9.0–10.1 | 37.1–43.5 | 58.4–63.4 | – |
| Stereolabs ZED X 4 mm eye · framed | – | 62.1–67.0 | 93.6–94.6 | 5.6–6.3 | 23.7–29.1 | 60.2–65.5 | – |
| Stereolabs ZED 2i 2.1 mm eye · framed | – | 62.5–66.7 | 93.5–94.3 | 6.4–7.3 | 30.6–37.6 | 68.9–73.6 | – |
| Intel RealSense D435 / D435i RGB camera · optics only | – | 62.2–66.5 | 93.9–94.7 | 5.6–6.2 | 22.7–27.7 | 67.3–72.1 | – |
| Intel RealSense D455 RGB camera · optics only | – | 61.5–66.2 | 93.6–94.4 | 5.2–5.9 | 25.0–30.1 | 59.9–65.9 | 70.4–91.3 |
| Logitech C920 HD Pro Webcam · optics only | – | 62.2–66.4 | 93.9–94.7 | 5.6–6.2 | 22.6–27.6 | 69.2–73.5 | 68.0–91.3 |
| Luxonis OAK-D color camera · optics only | – | 62.9–67.3 | 93.8–94.7 | 4.8–5.3 | 22.0–27.1 | 72.7–77.0 | – |
| Luxonis OAK-D mono camera (one stereo eye) · optics only | – | 55.3–59.7 | 93.6–94.5 | 5.2–5.8 | 18.7–23.4 | 68.9–73.3 | 70.9–92.9 |
| Raspberry Pi Camera Module 3 · optics only | – | 62.6–66.5 | 94.1–94.8 | 5.6–6.2 | 21.2–25.7 | 69.3–73.6 | – |
| Raspberry Pi Camera Module 3 Wide · optics only | – | 62.6–66.8 | 94.0–94.8 | 5.6–6.2 | 21.6–26.4 | 68.0–73.0 | – |
| Stereolabs ZED X / X Mini 2.2 mm eye · optics only | – | 63.1–68.0 | 93.7–94.6 | 5.2–5.9 | 23.9–28.9 | 63.7–69.2 | 70.9–92.9 |
| Stereolabs ZED X 4 mm eye · optics only | – | 62.6–67.0 | 93.8–94.7 | 5.2–5.9 | 23.3–28.1 | 64.0–69.6 | – |
| Stereolabs ZED 2i 2.1 mm eye · optics only | – | 62.3–66.4 | 94.0–94.8 | 5.6–6.2 | 22.3–27.2 | 67.6–72.5 | – |

## Provenance

- TwinRobo-Core: 075020f
- da2: `depth-anything/Depth-Anything-V2-Large-hf@7581137eff8d4e94f6e796d3baea0e9fa79b22d2`
- depthpro: `apple/DepthPro-hf@de816c8ce7168afcb231f96d501d72b869d0beda`
- gdino: `IDEA-Research/grounding-dino-base@12bdfa3120f3e7ec7b434d90674b3396eccf88eb`
- policy: `openvla/openvla-7b-finetuned-libero-spatial@962318cec55ac10993ff0f5f43eda9a270b4c873`
- qwen: `Qwen/Qwen2.5-VL-7B-Instruct@cc594898137f460bfe9f0759e9844b3ce807cfb5`
- sam: `facebook/sam-vit-huge@87aecf0df4ce6b30cd7de76e87673c49644bdf67`
- software: deeplens-core (render) 2.5.4, mujoco (render) 3.3.2, numpy (models) 2.5.2, numpy (render) 2.5.3, opencv-python (render) 5.0.0.93, opencv-python-headless (models) 5.0.0.93, torch (models) 2.8.0+cu128, torch (render) 2.10.0, transformers (models) 5.19.0

