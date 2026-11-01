# Get started

## Install

TwinRobo needs **Python 3.12** (inherited from DeepLens) and a CUDA GPU for
practical speeds.

=== "From a checkout"

    For development, and for the LIBERO support:

    ```bash
    git clone https://github.com/TwinRobo/TwinRobo-Core.git && cd TwinRobo-Core
    conda create -n twinrobo python=3.12 -y && conda activate twinrobo
    pip install -e ".[dev]"          # core + DeepLens
    pip install -e ".[libero]"       # + MuJoCo, NVIDIA Warp and LIBERO support
    ```

=== "Release (v0.1.0)"

    ```bash
    conda create -n twinrobo python=3.12 -y && conda activate twinrobo
    pip install "twinrobo-core[mujoco]"   # TwinRobo, DeepLens, MuJoCo and NVIDIA Warp
    ```

    With Isaac Sim 6.1 instead (Ubuntu 22.04 or later; in an environment of its own, since
    Isaac Sim brings its own MuJoCo):

    ```bash
    pip install "twinrobo-core[isaac]" --extra-index-url https://pypi.nvidia.com
    ```

    From [PyPI](https://pypi.org/project/twinrobo-core/);
    [release notes](https://github.com/TwinRobo/TwinRobo-Core/releases/tag/v0.1.0).

!!! note "Other simulators"
    LIBERO itself is used from a checkout (`LIBERO_ROOT`). RoboCasa needs
    robosuite 1.5 and gets its own environment ([details](simulators.md#robocasa)).
    Isaac Sim installs from PyPI (above) or runs in NVIDIA's container, with TwinRobo on
    Isaac's own Python and torch ([details](simulators.md#installing-isaac-sim)):

    ```bash
    docker pull nvcr.io/nvidia/isaac-sim:6.1.0        # needs the NVIDIA Container Toolkit
    docker/isaac/run.sh examples/01_isaac_camera.py   # builds the image on first use
    ```

## Mount a real camera on a robot

Pick a camera from the catalog, mount it on a robot link, and render what it
would record, here in robosuite's PickPlace scene (`pip install -e ".[libero]"`
brings robosuite; no LIBERO checkout needed):

```python
import robosuite

from twinrobo import CameraSpec, CameraTwin, CatalogRegistry
from twinrobo.plugins.mujoco import MujocoCameraTwin, RobosuiteRenderer, to_uint8
from twinrobo.plugins.mujoco.mounts import CameraMount, mounted

env = robosuite.make(
    "PickPlace",
    robots="Panda",
    has_renderer=False,
    has_offscreen_renderer=True,
    use_camera_obs=False,
)
env.reset()

# 1. Pick a real camera from the catalog (here read out at 960x600).
path = CatalogRegistry().resolve("stereolabs/zed-x/2.2mm")
twin = CameraTwin.from_spec(CameraSpec.from_yaml(path, width=960, height=600))

# 2. Mount it on a robot link: position (m) and yaw/pitch/roll (deg) in the link's frame.
wrist = CameraMount("wrist", body="robot0_right_hand", pos=(0.08, 0, 0), rpy_deg=(67, -48, 173))

# 3. Render what that camera would record.
with mounted(env.sim.model._model, env.sim.data._data, wrist) as host:
    frame = MujocoCameraTwin(twin, RobosuiteRenderer(env), camera=host).get_frame(force_depth=True)

image = to_uint8(frame.rgb)          # the real camera's image, uint8 [H, W, 3]
pinhole = to_uint8(frame.rgb_ideal)  # the simulator's ideal pinhole, same camera
depth = frame.depth[0, 0]            # ground-truth z-depth (m): a label, the ZED X outputs none
```

The first call builds the lens's PSF bank with DeepLens (about 20 s on a GPU)
and caches it; after that a frame takes a fraction of a second. The mount moves
with the link, so it follows the robot as it acts or replays a demo.

`examples/05_mount_camera_on_robot.py` does this for two catalog cameras on
the same wrist mount:

```bash
MUJOCO_GL=egl python examples/05_mount_camera_on_robot.py   # writes outputs/05_mount_camera.jpg
```

![Two catalog cameras on the same wrist mount: pinhole vs TwinRobo image, close-up, difference and depth](images/quickstart_cameras.jpg)

- **Simulator pinhole / TwinRobo camera:** each lens's own field of view. The
  ZED X 2.2 mm's wide lens shows its barrel distortion, which a pinhole cannot.
- **Close-up:** the same patch at native resolution; the traced lens softens the
  lettering, as the camera would.
- **Difference ×4:** where the optics change the image.
- **Ground-truth depth:** the simulator's metric z-depth, aligned pixel for pixel with the
  camera's image; a label for training, not an output of the camera (`force_depth=True`).

## Switch the sensor and ISP

The image above comes from the lens alone. Add a camera's sensor and ISP, and you also get its
auto-exposure, noise, white balance and color. Here the Raspberry Pi Camera 3 uses its own
tuning, then another sensor's, then an ISP of your own:

```python
from twinrobo.isp import ISPModel, list_tunings
from twinrobo.isp.color import srgb_to_linear

path = CatalogRegistry().resolve("raspberrypi/camera-module-3/standard")
twin = CameraTwin.from_spec(CameraSpec.from_yaml(path, width=960, height=540), isp=True)
print(list_tunings())                # the sensors you can switch to

class Gamma(ISPModel):               # your own ISP
    def process(self, raw, metadata=None):
        return srgb_to_linear(raw.clamp(0, 1) ** 0.8)

twin.set_isp("imx477")               # from the next frame; the lens render is kept
twin.set_isp(Gamma())
twin.set_isp(True)                   # back to the camera's own
```

Render with `MujocoCameraTwin(twin, ...)` as above. `frame.metadata["pipeline"]` records which
sensor and ISP made each frame. Another sensor's tuning on this lens is a hybrid that models no
real camera, and these ISPs have not been compared with a real camera yet.
[Sensor and ISP](sensor-isp.md) has the details and limits.

<a id="next-steps"></a>

## Try next

<div class="grid cards" markdown>

-   :material-ray-start-arrow: __Trace lens rays__

    Pass `render="raycast"` to `MujocoCameraTwin`.
    [Rendering methods](rendering.md#rendering-methods)

-   :material-cube-outline: __Isaac Sim__

    The same twin on any USD camera prim, with both methods.
    [Isaac Sim](simulators.md#isaac-sim)

-   :material-robot: __A LIBERO policy's camera__

    `CameraTwinLiberoEnv` swaps observations in place; eval scripts run
    unchanged. [LIBERO](simulators.md#libero)

-   :material-tune: __Your own ISP__

    Switch tunings between frames, or plug in your own ISP.
    [Sensor and ISP](sensor-isp.md)

-   :material-camera-plus: __Your own camera__

    Copy a catalog spec, or add one for everyone.
    [Cameras](cameras.md) · [Contributing](contributing.md#adding-a-camera)

</div>
