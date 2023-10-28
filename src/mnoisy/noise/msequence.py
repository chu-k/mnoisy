from typing import Callable

import numpy as np
from scipy.stats import randint

from mnoisy.noise.base import NoiseGenerator


class MSequence(NoiseGenerator):
    def __init__(
        self,
        sequence_length: int,
    ) -> None:
        """Constructor for MSequence class.

        Args:
            sequence_length (int): Length of the m-sequence to generate.
        """
        self.sequence_length = sequence_length
        self.update_fn: Callable[[np.ndarray], int] = UpdateFuncRegistry().get(sequence_length)
        self.repeat_cutoff = sequence_length**2 - 1
        self.signal = np.zeros(self.repeat_cutoff)
        self.grid = np.zeros((self.repeat_cutoff, sequence_length))

    @property
    def limit(self) -> int:
        return self.repeat_cutoff

    def generate_noise_1d(self, seed: int) -> np.ndarray:
        """Generate 1D m-sequence noise."""
        register = randint(0, 2).rvs(size=self.sequence_length, random_state=seed)
        for i in range(self.repeat_cutoff):
            self.grid[i] = register
            self.signal[i] = register[0]
            register = self.shift_update(register)
        return self.signal

    def shift_update(self, register: np.ndarray) -> np.ndarray:
        """Shift register and update the last element."""
        shift = np.roll(register, -1)
        shift[-1] = int(self.update_fn(register)) % 2
        return shift

    def build_metadata(self) -> dict:
        return {
            "sequence_length": self.sequence_length,
        }


class UpdateFuncRegistry:
    """Registry for update functions, implemented up to size 12."""

    def __init__(self) -> None:
        self._registry = {}

    def get(self, size: int) -> Callable[[np.ndarray], int]:
        """Return update functions for the final bit in the shift register.
        See http://www.kempacoustics.com/thesis/node83.html
        Can implement for other sizes, see table 7.2 in reference

        NOTE: There may a cleaner way to map size -> update function.
        """
        if size == 1:
            return lambda x: x[0]
        elif size in range(2, 8):
            if size == 5:
                return lambda x: x[0] + x[2]
            return lambda x: np.sum(x[:2])
        elif size == 8:
            return lambda x: x[0] + x[1] + x[5] + x[6]
        elif size == 9:
            return lambda x: x[0] + x[4]
        elif size == 10:
            return lambda x: x[0] + x[3]
        elif size == 11:
            return lambda x: x[0] + x[2]
        elif size == 12:
            return lambda x: x[0] + x[3] + x[4] + x[7]
        else:
            raise NotImplementedError
