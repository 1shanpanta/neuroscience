"""Stage 2: baseline decoder. Sum of preferred directions weighted by firing rate."""


class PopulationVectorDecoder:
    def fit(self, spikes, velocities):
        raise NotImplementedError

    def predict(self, spikes):
        raise NotImplementedError
