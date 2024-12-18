import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.axes import Axes
from scipy.stats import randint

from mnoisy.exceptions import NoiseGeneratorLimitError
from mnoisy.noise.base import NoiseGenerator
from mnoisy.noise.factory import GeneratorFactory
from mnoisy.utils import validate_against_schema


class NoiseGridGenerator:
    random_sample_size = 2048

    def __init__(self, image_size_in_pixels: int, noise_generator: NoiseGenerator):
        """Constructor for NoiseGrid class.

        Args:
            image_size_in_pixels (int): Size of the image in pixels.
            m_sequence_constructor (MSequence): MSequence object.
            seed: Seed value for the initial random state.
        """
        if image_size_in_pixels > noise_generator.limit:
            raise NoiseGeneratorLimitError(
                f"Image size must be less than noise generator limit {noise_generator.limit}"
            )
        self.image_size_in_pixels = image_size_in_pixels
        self.noise_generator = noise_generator
        self.grid = np.zeros((image_size_in_pixels, image_size_in_pixels))

    def generate_image(self, seed: int):
        """Generate a new image from noise generator."""
        for i, sd in enumerate(randint(0, 2048).rvs(size=self.image_size_in_pixels, random_state=seed)):
            self.grid[i] = self.noise_generator.generate_noise_1d(sd)[: self.image_size_in_pixels]

        return self.grid, self.build_metadata(seed)

    def build_metadata(self, seed):
        return {
            "timestamp_absolute": datetime.now().isoformat(),
            "random_seed": int(seed),
        }

    @staticmethod
    def plot_single_grid(ax: Axes, frame: np.ndarray):
        im = ax.matshow(frame, cmap="gray", interpolation="none")
        # apply styling to clean up the plot
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.axis("off")
        return ax, im


class NoiseAnimator:
    # global plotting settings
    plt.rcParams["savefig.bbox"] = "tight"
    plt.rcParams["toolbar"] = "None"

    def __init__(
        self,
        image_artist: NoiseGridGenerator,
        display_time_per_frame_in_seconds: float,
        debug: bool = False,
    ):
        """Generates a sequence of NoiseGrid

        Args:
            images (List[NoiseGrid]): List of NoiseGrid objects.
            display_time_per_frame_in_seconds (float): Display time per frame in seconds.
        """
        self.image_artist = image_artist
        self.display_time_per_frame_in_seconds = display_time_per_frame_in_seconds
        self.img_size = image_artist.image_size_in_pixels
        self._debug = debug

    def execute(self, num_frames: int, seed: int, output_filename: str = "noise.gif"):
        """Execute the main logic of the animator.

        Args:
            num_frames (int): Number of frames to generate.
            seed (int): Seed value for the initial random state.
            output_filename (str): Output filename for the animation.
        """
        frames, metadata = self.generate_frames(num_frames, seed, output_filename)
        if self._debug:
            frames.dump("debug-frames.npy")

        self.__write_metadata(metadata)
        self.__animate_frames(frames, metadata.get("animation_fname", output_filename))

    def generate_frames(
        self,
        num_frames: int,
        seed: int,
        output_filename: str = "noise.gif",
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Generate an animation from a list of NoiseGrid objects.

        Args:
            num_frames (int): Number of frames to generate.
            seed (int): Seed value for the initial random state.
            output_filename (str): Output filename for the animation.

        """
        frames = np.zeros((num_frames, self.img_size, self.img_size))
        metadata = self.__get_metadata(output_filename, num_frames, seed)
        for i, sd in enumerate(randint(0, 2048).rvs(size=num_frames, random_state=seed)):
            # generate frame and store its metadata
            frames[i], frame_data = self.image_artist.generate_image(sd)
            frame_data["frame_number"] = i
            frame_data["timestamp_relative"] = str(
                datetime.fromisoformat(frame_data["timestamp_absolute"])
                - datetime.fromisoformat(metadata["created_at"])
            )
            metadata.setdefault("frames", []).append(frame_data)
        return frames, metadata

    def __animate_frames(self, frames: np.ndarray, output_filename: Path):
        """Animate a list of frames."""
        # Set the initial canvas and frame
        fig, ax = plt.subplots(1, 1, figsize=(self.img_size, self.img_size), squeeze=True)
        ax, im = self.image_artist.plot_single_grid(ax, frames[0])

        # define the animation update function
        def updatefig(i):
            im.set_data(frames[i])
            return (im,)

        # interval arg is in ms
        ani = animation.FuncAnimation(
            fig,
            updatefig,
            frames=frames.shape[0],
            interval=self.display_time_per_frame_in_seconds * 1000.0,
            blit=True,
        )
        ani.save(output_filename)
        # this blocks until the animation is manually closed
        plt.show()

    def __get_metadata(self, output_filename: str, num_frames: int, seed: int) -> Dict:
        """Return metadata about the animation."""
        data_fname = Path(output_filename).with_suffix(".json")
        animation_fname = Path(output_filename).with_suffix(".gif")

        return {
            "metadata_fname": str(data_fname),
            "animation_fname": str(animation_fname),
            "created_at": datetime.now().isoformat(),
            "random_seed": seed,
            "num_frames": num_frames,
            "image_size_in_pixels": self.img_size,
            "display_time_per_frame_in_seconds": self.display_time_per_frame_in_seconds,
            "frames": [],
            "noise_generator": self.image_artist.noise_generator.build_metadata(),
        }

    def __write_metadata(self, metadata: Dict):
        """Write metadata to file."""
        validate_against_schema(metadata, Path(__file__).parent.joinpath("schema/animation_data.yml").resolve())
        with open(metadata["metadata_fname"], "w+") as fp:
            json.dump(metadata, fp)

    @classmethod
    def construct_instance_from_metadata(cls, metadata_path: str) -> Tuple["NoiseAnimator", int, int, str]:
        """Parse metadata file.

        Returns:
            Animator instance, number of frames, random seed, output filename
        """
        with open(metadata_path, "r") as fp:
            metadata: Dict[str, Any] = json.load(fp)
        validate_against_schema(metadata, Path(__file__).parent.joinpath("schema/animation_data.yml").resolve())
        generator_metadata = metadata["noise_generator"].copy()
        generator = GeneratorFactory.get_generator(
            generator_type=generator_metadata.pop("generator_type"), **generator_metadata
        )
        return (
            cls(
                NoiseGridGenerator(
                    metadata["image_size_in_pixels"],
                    generator,
                ),
                metadata["display_time_per_frame_in_seconds"],
            ),
            metadata["num_frames"],
            metadata["random_seed"],
            metadata["metadata_fname"],
        )

    def reconstruct_single_frame(self, frame_index: int, master_seed: int, output_slug: str):
        """Reconstruct a single frame from the full sequence."""
        # use the master seed to reproduce the seed for the frame at index frame_index
        seed = randint(0, 2048).rvs(size=frame_index, random_state=master_seed)[-1]
        frame, _ = self.image_artist.generate_image(seed)
        fig, ax = plt.subplots(1, 1, figsize=(self.img_size, self.img_size), squeeze=True)
        ax, im = self.image_artist.plot_single_grid(ax, frame)
        fig.savefig(f"{output_slug}-{frame_index}.png")
        plt.show()
