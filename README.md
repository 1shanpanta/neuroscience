# neuroscience: a software-only BCI simulator

A rough plan for a brain-computer interface (BCI) built in stages. It starts fully in software with simulated neurons and ends, optionally, with real EEG and a physical device. Each stage works on its own, so the project is useful even if the hardware never happens.

```
spike generator  ->  decoder  ->  cursor / text output
      (sim)          (learned)        (center-out task)
                         ^
        real EEG (OpenBCI) swaps in for the generator later
                         |
                  optional: Arduino / Raspberry Pi device
```

## Status

Planning stage. The folders and stub files exist, and nothing is implemented yet.

## Stage 1: Spike generator (Python)

Simulate a population of motor-cortex-like neurons that fire in response to an intended movement.

- Poisson spike trains whose rate depends on intended movement direction, using cosine tuning: `rate = baseline + gain * cos(theta - preferred_direction)`.
- Each neuron gets a random preferred direction, baseline rate and gain.
- Configurable noise, neuron count, bin size and session length.
- Output is a spike-count matrix of shape `(time_bins, neurons)` plus the true intended velocity, saved to `data/` as `.npz`.
- Stretch: add tuning drift over time and dropped channels, so the decoder has to cope with a messy signal.

Code lives in `bci_sim/spikes/`.

## Stage 2: Decoder and center-out task

Turn spikes into cursor movement and measure how well it works.

- **Task:** a center-out reaching task. The cursor starts at the center, a target appears at one of 8 points on a circle, and the subject (the simulator) has to reach it.
- **Decoders, in order of effort:**
  1. Population vector, a simple baseline.
  2. Linear regression and a Kalman filter on binned spikes.
  3. Optional small neural network (a GRU) for comparison.
- **Closed loop:** the decoded velocity moves the cursor. The simulated user adjusts its intent based on where the cursor is.
- **Metrics:** success rate, time to target, path straightness, and bits per second.
- **Typing variant:** the same decoder picks letters from an on-screen keyboard, with a letter grid or radial menu for target selection.

Code lives in `bci_sim/decoder/` and `bci_sim/tasks/`.

## Stage 3: From simulation to real EEG (OpenBCI)

Spikes come from implanted electrodes, while EEG is much noisier and slower, so the decoder changes shape here.

- **Hardware:** an OpenBCI Cyton board (8 channels) or Ganglion (4 channels), read over BrainFlow, with LSL (Lab Streaming Layer) as an alternative.
- **First step:** a `StreamSource` interface that both the simulator and the OpenBCI board implement, so the decoder never knows which one it is reading.
- **Signal processing:** bandpass 1 to 40 Hz, a 50 or 60 Hz notch filter, artifact rejection for blinks and muscle, and band-power features (mu and beta, 8 to 30 Hz).
- **Realistic first task:** motor imagery (imagined left or right hand movement) or SSVEP, mapped to a coarse cursor command, not smooth continuous control. Smooth control is not realistic with EEG.
- **Validation:** replay public EEG datasets (for example BCI Competition IV 2a) through the same pipeline before touching live hardware.
- **Calibration:** a short training session records labelled trials, and the decoder is then fitted on them.

Code lives in `bci_sim/eeg/`.

## Stage 4 (optional): A physical device

Drive something real from the decoded output.

- A Raspberry Pi or Arduino receives commands such as `LEFT`, `RIGHT`, `FORWARD` and `STOP` over serial or MQTT.
- Candidate targets: a servo or robot arm, a small rover, or an LED and relay board.
- Safety first: a hardware stop button, rate limits, and a dead-man timeout that stops the device if no command arrives.
- The decoder sends a command at a fixed rate. The hardware layer is deliberately dumb and does no decoding.

Code lives in `hardware/`.

## Project structure

```
neuroscience/
  README.md
  pyproject.toml
  bci_sim/
    spikes/        Stage 1: spike generator
    decoder/       Stage 2: decoders
    tasks/         Stage 2: center-out task and typing task
    eeg/           Stage 3: OpenBCI and filtering stubs
  hardware/
    arduino/       Stage 4: firmware sketch stub
    raspberry_pi/  Stage 4: serial / MQTT bridge stub
  notebooks/       exploration
  tests/
  data/            generated data (git-ignored)
```

## Roadmap

- [ ] Spike generator with cosine tuning
- [ ] Population vector decoder
- [ ] Center-out task with a plotted cursor
- [ ] Kalman filter decoder and metrics
- [ ] Typing variant
- [ ] `StreamSource` interface and a replay source for public EEG data
- [ ] Live OpenBCI stream, filtering and calibration
- [ ] Motor-imagery decoder
- [ ] Hardware bridge and a safe stop path

## Setup (planned)

```
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Expected dependencies: numpy, scipy, matplotlib, scikit-learn, brainflow, pyserial.

## Notes

This is a learning project. It is not a medical device and makes no clinical claims.
