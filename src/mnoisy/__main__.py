import argparse
from datetime import datetime

from mnoisy.image import NoiseAnimator, NoiseGridGenerator
from mnoisy.noise import MSequence


def main():
    parser = argparse.ArgumentParser(description="Generate a sequence of pseudorandom noisy images using m-sequences.")
    parser.add_argument("-i", "--image_size", type=int, help="Square image size in pixels", required=True)
    parser.add_argument("-n", "--num_frames", type=int, help="Number of frames in the animation", required=True)
    parser.add_argument("-t", "--frame_time_sec", type=int, help="Display time per frame in seconds", default=0.2)
    parser.add_argument("-l", "--sequence_length", type=int, help="Length of the m-sequence to generate", default=7)
    parser.add_argument("-s", "--initial_seed", type=int, help="Global seed value", default=4242)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    parser.add_argument("-o", "--output_file", type=str, help="Output file name", default=f"noise-{timestamp}.gif")
    args = parser.parse_args()

    animator = NoiseAnimator(
        NoiseGridGenerator(
            args.image_size,
            MSequence(args.sequence_length),
        ),
        args.frame_time_sec,
    )
    animator.execute(args.num_frames, args.initial_seed, args.output_file)


if __name__ == "__main__":
    main()
