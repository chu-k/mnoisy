from typing import Protocol

import numpy as np


class NoiseGenerator(Protocol):
    """Generic interface for noise generators, used to construct NoiseGrids."""

    def generate_noise_1d(self, seed: int) -> np.ndarray:
        """Return 1D noise signal."""
        ...

    def build_metadata(self) -> dict:
        """Return metadata about the noise generator."""
        ...

    @property
    def limit(self) -> int:
        """Return the maximum length accesible to the generator."""
        ...
