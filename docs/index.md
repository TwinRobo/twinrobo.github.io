---
title: TwinRobo
hide:
  - navigation
  - toc
---

<div class="tr-hero" markdown>

<div class="tr-badges"><span>AGPL-3.0 · commercial</span><span>MuJoCo · Isaac Sim</span></div>

# See through the camera <span class="tr-grad">you will deploy</span>

<p class="tr-lead">Simulators render through a perfect pinhole; robots see through real lenses.
TwinRobo renders simulated scenes through the actual optics of off-the-shelf cameras,
so perception trained in simulation meets the same image on the robot.
<a class="tr-why-link" href="why/">See why TwinRobo?</a></p>

[Try it live](playground.md){ .md-button .md-button--primary }
[Get started](getting-started.md){ .md-button }
[Browse cameras](catalog.md){ .md-button }

<div class="tr-compare tr-compare--hero" style="--pos: 50%">
  <img src="assets/home/compare-camera.webp" width="640" height="400"
       alt="A robot's wrist camera over a bin of groceries, through a real camera's lens (ray-traced)">
  <img class="tr-compare__top" src="assets/home/compare-pinhole.webp"
       width="640" height="400" alt="The same view through the simulator's pinhole">
  <span class="tr-compare__tag tr-compare__tag--left">Pinhole</span>
  <span class="tr-compare__tag tr-compare__tag--right">Real camera</span>
  <input class="tr-compare__range" type="range" min="0" max="100" value="50"
         aria-label="Slide between the pinhole and a real camera">
</div>

<p class="tr-caption">Drag to compare: a robot's wrist camera in MuJoCo, the same frame, pose and field of
view, through the simulator's pinhole and through a real camera's lens.</p>

</div>

<div class="tr-why" markdown>

## Change the camera, and a robot policy drops from <span class="tr-grad">85 % to 0 %</span>

<p class="tr-lead">OpenVLA solves 85 % of its LIBERO tasks through the pinhole camera it was
trained with, and none through a real camera placed where that pinhole was. TwinRobo shows
you that before your robot does. <a class="tr-why-link" href="benchmark/">See the benchmark</a></p>

<figure class="tr-hero-video">
  <video autoplay muted loop playsinline preload="metadata" poster="assets/home/hero-poster.jpg"
         aria-label="The same robot task through a pinhole camera, where the policy succeeds, and through a real camera, where it fails">
    <source src="assets/home/hero.mp4" type="video/mp4">
  </video>
</figure>

<p class="tr-caption">OpenVLA on the same LIBERO task from the same start, seen through its own
(third-person) camera: through the simulator's pinhole it succeeds (left); through a real camera
at the same place it fails (right).</p>

</div>

## One environment, any real camera

<div class="grid cards tr-2col" markdown>

-   :material-camera-iris:{ .lg .middle } __Real lens optics__

    ---

    Lenses traced with DeepLens: depth- and field-dependent blur, the lens' own
    distortion, chromatic aberration and vignetting, from a prescription, not a
    hand-tuned filter.

    [:octicons-arrow-right-24: Optics and rendering](rendering.md)

-   :material-ray-start-arrow:{ .lg .middle } __Two rendering methods__

    ---

    A fast 2.5D PSF renderer, plus a ray caster that traces every pixel's
    rays through the lens into the scene, exact even around defocused
    foreground objects.

    [:octicons-arrow-right-24: Rendering methods](rendering.md#rendering-methods)

-   :material-robot-industrial:{ .lg .middle } __Drop-in for simulators__

    ---

    MuJoCo, LIBERO, RoboCasa and NVIDIA Isaac Sim. Wrap a camera and policies,
    eval scripts and recorded demos run unchanged, now through a real camera.

    [:octicons-arrow-right-24: Simulators](simulators.md)

-   :material-view-grid-plus:{ .lg .middle } __An open camera catalog__

    ---

    RealSense, ZED, OAK-D, a C920 webcam and the Raspberry Pi camera, as single
    cameras or rectified stereo pairs. Every camera works in every simulator and
    method, and a real unit can be [calibrated](calibration.md).

    [:octicons-arrow-right-24: Camera catalog](catalog.md)

</div>

## Support at a glance

| | MuJoCo (incl. LIBERO, RoboCasa) | NVIDIA Isaac Sim 6.x |
|---|---|---|
| Adapter | `MujocoCameraTwin` | `IsaacCameraTwin` |
| `psf`: pinhole + lens blur and distortion | :material-check-bold: | :material-check-bold: |
| `raycast`: lens rays cast into the scene | :material-check-bold: | :material-check-bold: |
| RGB on the GPU, ground-truth depth on request | :material-check-bold: | :material-check-bold: |
| Cameras on robot links, stereo modules | :material-check-bold: | any USD camera prim |
| Setup | `pip install` | Docker recipe included |

## Five lines to a real camera

=== "MuJoCo"

    ```python
    from twinrobo import CameraTwin
    from twinrobo.plugins.mujoco import MujocoCameraTwin, MujocoRenderer

    twin = CameraTwin.from_catalog("stereolabs/zed-x/2.2mm")
    cam = MujocoCameraTwin(twin, MujocoRenderer(model, data), camera="wrist")
    frame = cam.get_frame()          # frame.rgb: the camera's image, on the GPU
    ```

=== "Isaac Sim"

    ```python
    from twinrobo import CameraTwin
    from twinrobo.plugins.isaac import IsaacCameraTwin

    twin = CameraTwin.from_catalog("stereolabs/zed-x/2.2mm", build_psf=False)
    cam = IsaacCameraTwin(twin, "/World/Camera", render="raycast")
    frame = cam.get_frame()          # every pixel ray-traced through the lens
    ```

=== "LIBERO"

    ```python
    from twinrobo import CameraTwin
    from twinrobo.datasets.libero import CameraTwinLiberoEnv, make_env

    env, task, init_states = make_env("libero_spatial", 0, resolution=128)
    env = CameraTwinLiberoEnv(env, {"agentview": CameraTwin.from_catalog("stereolabs/zed-x/4mm")})
    obs = env.reset()                # obs["agentview_image"] now comes from the twin
    ```

=== "Any RGB-D"

    ```python
    from twinrobo import CameraTwin

    twin = CameraTwin.from_catalog("stereolabs/zed-x/2.2mm")
    frame = twin.process(rgb, depth) # in: linear RGB [B,3,H,W], metric depth [B,1,H,W]
    ```

## Validated in both simulators

<div class="grid cards tr-stats" markdown>

-   __46 dB__

    PSF renderer vs DeepLens' reference renderer at 1920×1200.

-   __< 0.1 px__

    Points land where the lens' chief rays point (Isaac Sim).

-   __~0.03 vs ~0.13__

    Error on a defocused foreground edge: ray cast vs pinhole + PSF (Isaac Sim;
    MuJoCo ~0.05).

</div>

<div class="tr-cta" markdown>

### :material-camera-plus: Your camera is missing? Add it

The catalog is the heart of TwinRobo, and it is open. A camera is a
`camera.yaml` and a lens file; once merged it works in every simulator,
rendering method and dataset replay, for everyone.

[How to add a camera](contributing.md#adding-a-camera){ .md-button .md-button--primary }
[Request a camera](https://github.com/TwinRobo/TwinRobo-Core/issues/new?template=new_camera.md){ .md-button }

</div>

<div class="tr-cta" markdown>

### :material-handshake: Camera makers: become a partner

Robot teams now choose and validate cameras in simulation. Ship
`manufacturer_verified` models of your products, get listed as a partner and
showcased, or sponsor the open environment your customers use.

[The partner program](partners.md){ .md-button .md-button--primary }

</div>
