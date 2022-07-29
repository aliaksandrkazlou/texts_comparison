from collections import defaultdict
from numbers import Number
import random

import numpy as np
import nltk
import streamlit as st
from tomark import Tomark

from database import MongoDatabase

word_tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+[-\w*]*")


def load_text(file_path):
    with open(file_path) as f:
        return f.read().replace("\n", " ")


@st.experimental_memo(show_spinner=False)
def get_stats(text):
    tokens = nltk.word_tokenize(text.lower(), language="russian")
    sentences = nltk.sent_tokenize(text, language="russian")
    words_per_sentence = np.array([len(word_tokenizer.tokenize(s)) for s in sentences])

    # average number of words per sentence
    awps = words_per_sentence.mean()
    # sentence length variation
    wpssd = words_per_sentence.std()

    # Commas per sentence
    avg_commas = tokens.count(",") / float(len(sentences))
    # Semicolons per sentence
    avg_semi = tokens.count(";") / float(len(sentences))
    # Colons per sentence
    avg_colons = tokens.count(":") / float(len(sentences))
    # Hyphens per sentence
    hyphen_count = sum([token.count("-") for token in word_tokenizer.tokenize(text)])
    avg_hyphens = hyphen_count / float(len(sentences))
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
        "Commas p/s": avg_commas,
        "Semicolons p/s": avg_semi,
        "Colons p/s": avg_colons,
        "Hyphens p/s": avg_hyphens,
        "Dashes p/s": avg_dash,
        "Dots p/s": avg_dots,
        "Question marks p/s": avg_qm,
        "Exclamation marks p/s": avg_exc,
    }


@st.experimental_memo(show_spinner=False)
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


def get_table(stats1, stats2, round_decimals=3):
    markdown = Tomark.table(
        [
            {
                key: (
                    np.round(stat, round_decimals) if isinstance(stat, Number) else stat
                )
                for key, stat in stats_list.items()
            }
            for stats_list in [stats1, stats2]
        ]
    )
    return markdown


@st.experimental_singleton(show_spinner=False)
def get_db_client():
    db_config = st.secrets["db"]
    db_client = MongoDatabase.from_config(db_config)
    if not db_client.get_status():
        raise ConnectionError("No connection to the database")
    return db_client


@st.experimental_memo(show_spinner=False)
def load_query(query_id):
    db_client = get_db_client()
    document = db_client.get_query(query_id)
    if not document:
        raise KeyError(f"No query found with id {query_id}")
    return document


@st.experimental_memo(show_spinner=False)
def save_query(text1, text2):
    db_client = get_db_client()
    query_document = {"text1": text1, "text2": text2}
    query_id = db_client.save_query(query_document)
    return query_id


def clear_all():
    st.experimental_set_query_params()
    for key in ["text1", "text2"]:
        if key in st.session_state:
            st.session_state[key] = ""
        if f"init_{key}" in st.session_state:
            st.session_state[f"init_{key}"] = ""


def submit():
    st.session_state["submitted"] = True
    if "query_id" in (query_params := st.experimental_get_query_params()):
        for key in ["text1", "text2"]:
            if st.session_state[key] != st.session_state[f"init_{key}"]:
                del query_params["query_id"]
                st.experimental_set_query_params(**query_params)
                return


def save():
    with st.spinner("Saving the query"):
        query_id = save_query(st.session_state["text1"], st.session_state["text2"])
        st.experimental_set_query_params(query_id=query_id)
