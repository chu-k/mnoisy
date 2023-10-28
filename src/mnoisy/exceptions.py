class NoiseGeneratorLimitError(Exception):
    """The NoiseGenerator cannot generate enough signal for the requested image size."""


class NoiseGeneratorNotImplemented(Exception):
    """The requested NoiseGenerator type is not listed in the registry."""
