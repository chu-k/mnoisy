from typing import Any

from mnoisy.exceptions import NoiseGeneratorNotImplemented
from mnoisy.noise.msequence import MSequence


class GeneratorFactory:
    REGISTRY = {
        "msequence": MSequence,
    }

    @classmethod
    def get_generator(cls, generator_type: str, **kwargs) -> Any:
        """Return a generator instance."""
        try:
            return cls.REGISTRY[generator_type](**kwargs)
        except KeyError:
            raise NoiseGeneratorNotImplemented(f"Generator type {generator_type} is not implemented.")
