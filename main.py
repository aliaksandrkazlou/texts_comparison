import utils
import sys

if __name__ == "__main__":

    text1 = utils.load_text(sys.argv[1])
    text2 = utils.load_text(sys.argv[2])

    stats1 = utils.get_stats(text1)
    stats2 = utils.get_stats(text2)

    print(utils.get_table(stats1, stats2))
