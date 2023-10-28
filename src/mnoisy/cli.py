import argparse
import sys
from datetime import datetime
from pathlib import Path

from mnoisy.image import NoiseAnimator, NoiseGridGenerator
from mnoisy.noise.msequence import MSequence


def parse_args_main(args_list: list):
    parser = argparse.ArgumentParser(description="Generate a sequence of pseudorandom noisy images using m-sequences.")
    parser.add_argument("-i", "--image_size", type=int, help="Square image size in pixels", required=True)
    parser.add_argument("-n", "--num_frames", type=int, help="Number of frames in the animation", required=True)
    parser.add_argument("-t", "--frame_time_sec", type=float, help="Display time per frame in seconds", default=0.2)
    parser.add_argument("-l", "--sequence_length", type=int, help="Length of the m-sequence to generate", default=7)
    parser.add_argument("-s", "--initial_seed", type=int, help="Global seed value", default=4242)
    parser.add_argument("-d", "--debug", action="store_true", default=False)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    parser.add_argument("-o", "--output_file", type=str, help="Output file name", default=f"noise-{timestamp}.gif")

    return parser.parse_args(args_list)


def main():
    args = parse_args_main(sys.argv[1:])
    animator = NoiseAnimator(
        NoiseGridGenerator(
            args.image_size,
            MSequence(args.sequence_length),  # currently only support m-sequence, but can be replace with factory
        ),
        args.frame_time_sec,
        args.debug,
    )
    animator.execute(args.num_frames, args.initial_seed, args.output_file)


def parse_args_rebuild(args_list: list):
    parser = argparse.ArgumentParser(description="Reconstruct a sequence pseudorandom noisy images from metadata")
    parser.add_argument("-f", "--filename", type=str, help="Metadata filename", required=True)
    parser.add_argument("-i", "--index_of_frame", type=int, help="frame_index")
    return parser.parse_args(args_list)


def rebuild():
    args = parse_args_rebuild(sys.argv[1:])
    animator, num_frames, seed, output_filename = NoiseAnimator.construct_instance_from_metadata(args.filename)
    rebuild_slug = f"rebuild-{Path(output_filename).with_suffix('')}"
    if not args.index_of_frame:
        animator.execute(num_frames, seed, rebuild_slug)
        return

    animator.reconstruct_single_frame(args.index_of_frame, seed, rebuild_slug)


if __name__ == "__main__":
    main()
