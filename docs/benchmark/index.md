# Camera benchmark

!!! warning "Being re-run from the robot's own camera"
    The first results of the TwinRobo camera benchmark were measured with each camera at
    LIBERO's third-person (agent-view) position, not on the robot. That is not where a
    robot's camera sits, so we have withdrawn them. The benchmark is being re-run from the
    robot's wrist camera, and the findings and results will be back here when it is done.

**Which camera will my robot see best with?** The benchmark puts each catalog camera's
digital twin on a robot and scores what it sees: fiducial pose, object detection and
segmentation, depth from one image, grounding with a vision-language model, and a robot
policy's task success. It runs in simulation, with every model pinned to an exact release
and deterministic code, so each result can be recomputed bit for bit.
