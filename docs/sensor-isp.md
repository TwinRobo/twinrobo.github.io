# Sensor and ISP

A camera's image comes from three stages: the lens, the sensor and the image signal
processor (ISP). TwinRobo lets you change the last two without touching the lens or the scene.
Compare ISPs on one robot task, randomize them during training, or test your own.

```python
from twinrobo import CameraTwin

camera = "raspberrypi/camera-module-3/standard"
twin = CameraTwin.from_catalog(camera, isp=True)
```

## Choose an ISP

| `isp=` | Sensor and ISP |
|---|---|
| `None` (default) | what the camera's spec sets; for every catalog camera today, ideal and none |
| `False` | ideal sensor, no ISP |
| `True` | the camera's own tuning; only cameras with `isp.tuning` have one |
| `"imx477"` | a bundled tuning: `twinrobo.isp.list_tunings()` |
| `"my_tuning.json"` | a Raspberry Pi libcamera tuning file |
| `MyISP()` | your own ISP, with `sensor=` if it needs one |

The bundled tunings are libcamera's, measured by Raspberry Pi: IMX708, IMX708 wide, IMX219,
IMX477, IMX296, OV5647 and IMX500. Each gives auto-exposure, a Bayer mosaic, noise, the ADC,
Bayesian white balance, demosaic, denoise, color matrices, tone curve and sharpening. They
work with both rendering methods, in MuJoCo and in Isaac Sim.

## Switch between frames

```python
import random
from twinrobo.isp import list_tunings

for episode in range(episodes):
    twin.set_isp(random.choice(list_tunings()))
    run_episode(camera_adapter)
```

The switch applies from the next frame, to every adapter of that twin, and starts with no
exposure or other state from earlier frames. A selection that cannot be used leaves the old ISP
in place.
The lens render is kept, so switching does not re-trace rays. To compare ISPs in the same run,
use one twin per ISP, so that each keeps its own sensor and ISP.

## Bring your own ISP

Subclass `ISPModel`. It can be classical or a neural network.

```python
from twinrobo.isp import ISPModel
from twinrobo.isp.color import srgb_to_linear

class Gamma(ISPModel):
    def process(self, raw, metadata=None):
        return srgb_to_linear(raw.clamp(0, 1) ** 0.8)

twin = CameraTwin.from_catalog(camera, isp=Gamma())
```

With no `sensor=`, it receives ideal scene-linear RGB. To work on a Bayer mosaic, declare it
and pass a sensor that gives one:

```python
from twinrobo.isp import load_tuning
from twinrobo.sensor import TunedSensor

class MyDemosaic(ISPModel):
    input_format = "rggb"

    def process(self, raw, metadata=None):
        ...

sensor = TunedSensor(load_tuning("imx708"))
twin = CameraTwin.from_catalog(camera, isp=MyDemosaic(), sensor=sensor)
```

To change the ISP and keep the sensor and its noise, use
`twin.set_isp(MyDemosaic(), sensor=twin.sensor)`.

Your `process` must:

- take the format the sensor gives: `"rgb"` is `[B, 3, H, W]`; `"rggb"` is `[B, 1, H, W]`,
  0 to 1 of full scale above black. A mismatch raises an error that names both;
- leave `raw` unchanged, because it becomes `frame.raw`;
- return float `[B, 3, H, W]` on the same device, with the same size and pixel positions
  (it is converted to the frame's float type).
  Depth and rectification rely on these. Other shapes raise an error, but a shifted image can't
  be detected;
- return linear values, like `frame.rgb`. Decode a display-encoded result with
  `srgb_to_linear`;
- keep anything carried between frames per stream, under `metadata["stream"]`, else
  `metadata["camera"]`, and clear it in `reset`.

`camera_adapter.reset()` starts one camera's frames again when an episode starts, for example
its auto-exposure. Adapters also do this in `attach`.

## Which frame came from which ISP

`frame.metadata["pipeline"]` records it:

```python
{"sensor": "TunedSensor", "isp": "TunedISP", "raw_format": "rggb",
 "sensor_tuning": "imx477", "isp_tuning": "imx477", "matches_spec_tuning": False}
```

`matches_spec_tuning` is `True` for the tuning in the camera's spec, `False` for a different
one, and `None` when there is nothing to compare. `frame.raw` changes shape with the sensor, so
check `raw_format` before storing it.

## Limits

- **These twins have not been compared with a real camera yet.** The strengths, matrices and
  curves are measured. Raspberry Pi's hardware kernels and the sensors' spectral responses are
  not public, so standard methods stand in for them.
- **Another camera's tuning makes a hybrid camera.** `isp="imx477"` on a Pi Camera 3 gives you
  the Pi Camera 3's lens and resolution with the IMX477's noise, exposure and color. It is useful
  for experiments, but it models no real camera. `True` is the camera's own.
- **Simulator images have no absolute light level.** Exposure is not limited by a shutter, and
  gain does not follow the scene. Set `isp.analogue_gain` and `isp.lux` in the spec for the
  light you simulate.
- **Lens shading is not corrected by the ISP.** Render with `shading="corrected"`, the default.
- **Only cameras with public tunings have their own ISP:** the two Pi Camera 3 entries today.
  RealSense, ZED, OAK and Logitech cameras have none, and TwinRobo does not invent one. Your
  own ISP works on any camera, and a bundled tuning on any visible-light color camera.
- **Tuning files must have the structure of the bundled ones.** Mono tunings are not supported.
  A tuning does not hold the sensor's size or bit depth, so set `isp.native_size` and `isp.bits`
  in the spec for a file. Without them it gets 10 bits, and small frames keep full-size noise.
- **One twin has one ISP.** Batches and stereo eyes that share a twin share it. Stereo eyes on
  separate twins are not synchronized, so switch both before the next pair.
