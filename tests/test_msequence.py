import numpy as np
import pytest

from mnoisy.noise.msequence import MSequence


@pytest.fixture
def mseq_instance():
    return MSequence(sequence_length=4)


def test_constructor(mseq_instance):
    assert mseq_instance.repeat_cutoff == 4**2 - 1


def test_invalid_length_raises_error():
    with pytest.raises(NotImplementedError):
        MSequence(sequence_length=13)


@pytest.mark.parametrize(
    "input,expected",
    [
        ([1, 1, 1, 1], [1, 1, 1, 0]),
        ([1, 1, 1, 0], [1, 1, 0, 0]),
        ([1, 1, 0, 0], [1, 0, 0, 0]),
        ([1, 1, 1, 0], [1, 1, 0, 0]),
        ([1, 1, 0, 1], [1, 0, 1, 0]),
        ([1, 0, 1, 1], [0, 1, 1, 1]),
    ],
)
def test_shift_update(mseq_instance, input, expected):
    """Test various length 4 shift register updates."""
    dummy_register = np.array(input)
    assert np.all(mseq_instance.shift_update(dummy_register) == np.array(expected))


def test_generate_noise_1d(mseq_instance):
    """Test that generated noise is the correct length and full sequence is stored."""
    signal = mseq_instance.generate_noise_1d(seed=4242)
    assert signal.shape == (mseq_instance.repeat_cutoff,)
    assert np.all(signal == mseq_instance.grid[:, 0])
