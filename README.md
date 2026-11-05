# neuroscience

A software-only brain-computer interface simulator. It starts with fake neurons and a cursor task, and can grow into real EEG and a physical device.

- **Spike generator:** Python simulation of cosine-tuned, Poisson-firing neurons that encode intended movement.
- **Decoder:** turns spikes into cursor movement or typed text, tested on a center-out reaching task.
- **EEG path:** swap the simulator for real signals from an OpenBCI board through BrainFlow.
- **Hardware (optional):** send decoded commands to an Arduino or Raspberry Pi device.

Status: planning, with stub files only.
