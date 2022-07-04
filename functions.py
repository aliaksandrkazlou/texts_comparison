import numpy as np
import nltk
from tomark import Tomark
import random

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
    avg_dash = (tokens.count("-") + tokens.count("—")) / float(len(sentences))
    # Dots per sentence
    avg_dots = tokens.count(".") / float(len(sentences))
    # QM per sentence
    avg_qm = tokens.count("?") / float(len(sentences))
    # Exc per sentence
    avg_exc = tokens.count("!") / float(len(sentences))

    return {
        "Mean words per sentence": awps,
        "Sentence length SD": wpssd,
        "Lexical diversity": lex_diversity,
        "Commas per sentence": avg_commas,
        "Semicolons per sentence": avg_semi,
        "Colons per sentence": avg_colons,
        "Dashes per sentence": avg_dash,
        "Dots per sentence": avg_dots,
        "Question marks per sentence": avg_qm,
        "Exclams per sentence": avg_exc,
    }


# TODO: that's def not the correct abstraction, just a placeholder to rewrite later
def bootstrapped_ci(stats, lower=True, n=1000):
    bts = []
    for _ in range(n):
        bts.append([random.choice(stats) for _ in stats])
    if lower:
        pcntl = 0.025
    else:
        pcntl = 0.975
    return {
        "Mean words per sentence": np.percentile(bts["Mean words per sentence"], pcntl),
        "Sentence length SD": np.percentile(bts["Sentence length SD"], pcntl),
        "Lexical diversity": np.percentile(bts["Lexical diversity":], pcntl),
        "Commas per sentence": np.percentile(bts["Commas per sentence"], pcntl),
        "Semicolons per sentence": np.percentile(bts["Semicolons per sentence"], pcntl),
        "Colons per sentence": np.percentile(bts["Colons per sentence"], pcntl),
        "Dashes per sentence": np.percentile(bts["Dashes per sentence"], pcntl),
        "Dots per sentence": np.percentile(bts["Dots per sentence"], pcntl),
        "Question marks per sentence": np.percentile(
            bts["Question marks per sentence"], pcntl
        ),
        "Exclams per sentence": np.percentile(bts["Exclams per sentence"], pcntl),
    }


def get_table(stats1, stats2):
    markdown = Tomark.table([stats1, stats2])
    return markdown
