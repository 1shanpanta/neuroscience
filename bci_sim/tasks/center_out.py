"""Stage 2: center-out reaching task with 8 targets on a circle."""


class CenterOutTask:
    def __init__(self, n_targets=8, radius=1.0):
        raise NotImplementedError

    def run_trial(self, decoder, generator):
        raise NotImplementedError
