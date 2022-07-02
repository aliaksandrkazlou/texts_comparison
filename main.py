import functions
import sys
import ssl

if __name__ == "__main__":

    text1 = functions.load_text(sys.argv[1])
    text2 = functions.load_text(sys.argv[2])

    stats1 = functions.get_stats(text1)
    stats2 = functions.get_stats(text2)

    functions.get_table(stats1, stats2)
