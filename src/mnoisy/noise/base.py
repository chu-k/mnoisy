import numpy as np
from typing import Protocol


class NoiseGenerator(Protocol):
    """Generic interface for noise generators, used to construct NoiseGrids."""

    def generate_noise_1d(self, seed: int) -> np.ndarray:
        """Return 1D noise signal."""
        ...

    @property
    def limit(self) -> int:
        """Return the maximum length accesible to the generator."""
        ...
