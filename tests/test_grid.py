from unittest import mock

import numpy as np
import pytest

from mnoisy.image import NoiseGeneratorLimitError, NoiseGridGenerator
from mnoisy.noise import MSequence


@pytest.fixture
def noise_grid_generator():
    return NoiseGridGenerator(
        image_size_in_pixels=24,
        noise_generator=mock.Mock(
            spec=MSequence(sequence_length=7),
            limit=7**2 - 1,  # return value for limit property
            generate_noise_1d=mock.Mock(return_value=np.zeros(7**2 - 1)),  # return value for generate_noise_1d method
        ),
    )


def test_invalid_image_size_raises_error():
    with pytest.raises(NoiseGeneratorLimitError):
        NoiseGridGenerator(
            image_size_in_pixels=16,
            noise_generator=mock.Mock(
                spec=MSequence(sequence_length=4),
                limit=4**2 - 1,  # return value for limit property
            ),
        )


def test_constructor(noise_grid_generator):
    assert noise_grid_generator.grid.shape == (24, 24)


def test_metadata(noise_grid_generator):
    assert [key in noise_grid_generator.build_metadata(4242) for key in ["timestamp_absolute", "random_seed"]]


def test_generate_image(noise_grid_generator):
    grid, metadata = noise_grid_generator.generate_image(seed=4242)
    assert grid.shape == (24, 24)


def test_reconstruct_image():
    pass
