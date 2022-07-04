from collections import defaultdict
import random

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
    dash_count = tokens.count("-") + tokens.count("–") + tokens.count("—")
    avg_dash = dash_count / float(len(sentences))
    # Dots per sentence
    avg_dots = tokens.count(".") / float(len(sentences))
    # QM per sentence
    avg_qm = tokens.count("?") / float(len(sentences))
    # Exc per sentence
    avg_exc = tokens.count("!") / float(len(sentences))

    return {
        "Words p/s mean": awps,
        "Words p/s SD": wpssd,
        "Lexical diversity": lex_diversity,
        "Commas p/s": avg_commas,
        "Semicolons p/s": avg_semi,
        "Colons p/s": avg_colons,
        "Dashes p/s": avg_dash,
        "Dots p/s": avg_dots,
        "Question marks p/s": avg_qm,
        "Exclamation marks p/s": avg_exc,
    }


def bootstrapped_ci(text, q=0.5, n=1000, k=None):
    random.seed(0)
    sentences = nltk.sent_tokenize(text, language="russian")

    stats = defaultdict(list)
    if k is None:
        k = len(sentences)
    for _ in range(n):
        bootstrapped_text = " ".join(random.choices(sentences, k=k))
        for key, value in get_stats(bootstrapped_text).items():
            stats[key].append(value)
    return {key: np.percentile(stats_list, q) for key, stats_list in stats.items()}


def get_table(stats1, stats2):
    markdown = Tomark.table([stats1, stats2])
    return markdown
