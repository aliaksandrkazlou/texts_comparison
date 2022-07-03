import numpy as np
import nltk
from tomark import Tomark

word_tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")


def load_text(file_path):
    with open(file_path) as f:
        return f.read().replace("\n", " ")


def get_stats(text):

    tokens = nltk.word_tokenize(text.lower())
    words = word_tokenizer.tokenize(text.lower())
    sentences = nltk.sent_tokenize(text, language="russian")
    vocab = set(words)
    words_per_sentence = np.array([len(word_tokenizer.tokenize(s)) for s in sentences])

    # average number of words per sentence
    awps = words_per_sentence.mean()
    # sentence length variation
    wpssd = words_per_sentence.std()
    # Lexical diversity
    lex_diversity = len(vocab) / float(len(words))

    # Commas per sentence
    avg_commas = tokens.count(",") / float(len(sentences))
    # Semicolons per sentence
    avg_semi = tokens.count(";") / float(len(sentences))
    # Colons per sentence
    avg_colons = tokens.count(":") / float(len(sentences))
    # Dashes per sentence
    avg_dash = tokens.count("-") / float(len(sentences))

    return {
        "Mean words per sentence": awps,
        "Sentence length SD": wpssd,
        "Lexical diversity": lex_diversity,
        "Commas per sentence": avg_commas,
        "Semicolons per sentence": avg_semi,
        "Colons per sentence": avg_colons,
        "Dashes per sentence": avg_dash,
    }


def get_table(stats1, stats2):
    markdown = Tomark.table([stats1, stats2])
    print(markdown)
