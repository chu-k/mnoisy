from typing import List, Optional

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import randint

from mnoisy.noise import NoiseGenerator


class NoiseGrid:
    random_sample_size = 2048

    def __init__(self, image_size_in_pixels: int, noise_generator: NoiseGenerator):
        """Constructor for NoiseGrid class.

        Args:
            image_size_in_pixels (int): Size of the image in pixels.
            m_sequence_constructor (MSequence): MSequence object.
            seed: Seed value for the initial random state.
        """
        if image_size_in_pixels > noise_generator.limit:
            raise ValueError(f"Image size must be less than noise generator limit {noise_generator.limit}")
        self.image_size_in_pixels = image_size_in_pixels
        self.noise_generator = noise_generator
        self.grid = np.zeros((image_size_in_pixels, image_size_in_pixels))

    def update_image_metadata(self):
        """Write frame data to file."""
        pass

    def generate_image(self, seed: int):
        """Generate a new image from noise generator."""
        for i, sd in enumerate(randint(0, 2048).rvs(size=self.image_size_in_pixels, random_state=seed)):
            self.grid[i] = self.noise_generator.generate_noise_1d(sd)[: self.image_size_in_pixels]

        return self.grid

    def reconstruct_image(self):
        """Reconstruct image from metadata."""
        pass


class NoiseAnimator:
    def __init__(self, image_artist: NoiseGrid, display_time_per_frame_in_seconds: float, seed: Optional[int] = None):
        """Generates a sequence of NoiseGrid

        Args:
            images (List[NoiseGrid]): List of NoiseGrid objects.
            display_time_per_frame_in_seconds (float): Display time per frame in seconds.
        """
        self.image_artist = image_artist
        self.display_time_per_frame_in_seconds = display_time_per_frame_in_seconds

    def generate_animation(self, seed: int):
        """Generate an animation from a list of NoiseGrid objects."""
        for i in range(self.image_artist.noise_generator.limit):
            image.generate_image(seed + i)
            image.update_image_metadata()
        return
