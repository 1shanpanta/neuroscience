"""Stage 1: simulated neural population with cosine-tuned Poisson firing."""
import numpy as np


class SpikeGenerator:
    def __init__(self, n_neurons=64, bin_ms=20, seed=0):
        # TODO: sample preferred directions, baselines and gains
        raise NotImplementedError

    def generate(self, velocities):
        """Map intended velocities (T, 2) to spike counts (T, n_neurons)."""
        raise NotImplementedError
