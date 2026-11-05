"""Stage 3: common interface so the decoder can read simulated or real data."""
from abc import ABC, abstractmethod


class StreamSource(ABC):
    @abstractmethod
    def read(self):
        """Return the next chunk of samples as an array (samples, channels)."""
