import argparse

from mnoisy.sequence import MSequence
from mnoisy.visualize import ImageGenerator, GIFGenerator


def main():
    parser = argparse.ArgumentParser(description="Generate a sequence of pseudorandom noisy images using m-sequences.")
    parser.add_argument("-l", "--sequence_length", type=int, help="Length of the m-sequence to generate")
    parser.add_argument("-s", "--initial_seed", type=int, help="Seed value for the initial register")
    parser.add_argument("-i", "--image_size", type=int, help="Square image size in pixels")
    parser.add_argument("seed", type=int, help="Seed value for the initial register")
    args = parser.parse_args()

    # Use the input arguments to generate the m-sequence and visualize it
    mseq = MSequence(args.sequence_length, args.initial_seed)
    img_gen = ImageGenerator(args.image_size, mseq)
    img_gen.generate_image()
    gif_gen = GIFGenerator(mseq)
    gif_gen.generate_gif()


if __name__ == "__main__":
    main()
