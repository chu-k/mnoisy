# Summary
This package implements a CLI script for generating pseudorandom noise from M-sequences.


# Installation
```
pip install .

# Optionally, to run tests below
pip install .[test]
```

# Usage
```
usage: mnoisy-gen [-h] -i IMAGE_SIZE -n NUM_FRAMES [-t FRAME_TIME_SEC] [-l SEQUENCE_LENGTH] [-s INITIAL_SEED] [-o OUTPUT_FILE]

$ mnoisy-gen -i 24 -n 3
OR
$ python -m mnoisy -i 15 -n 30 -l 10 -s 1234
```

# Limitations and Assumptions
Currently, the update function up to M-sequences of length 12 are implemented. That means image sizes are limited to 143x143 px.

Based on my understanding, an M-Sequence generates N = m*2-1 signal bits. To create an NxN image, multiple (N) sequences must be generated with different seeds then stacked to form the image.

# Tests
```
pip install .[test]
python -m pytest --cov=src/ tests/
```

# References
[1] https://en.wikipedia.org/wiki/Maximum_length_sequence
[2] http://www.kempacoustics.com/thesis/node83.html
