import nltk
import streamlit as st

import functions

st.set_page_config(page_title="Text comparison", page_icon="🧐", layout="wide")

with st.spinner("Loading"):
    nltk.download("popular")

with st.form("text_form"):
    left_column, right_column = st.columns(2)

    with left_column:
        text1 = st.text_area("Enter text 1", placeholder="Text 1", height=600)
    with right_column:
        text2 = st.text_area("Enter text 2", placeholder="Text 2", height=600)

    submitted = st.form_submit_button("Run")

if submitted:
    if text1 == "" or text2 == "":
        st.write("Please enter both texts")
        st.stop()
    with st.spinner("Calculating the metrics"):
        stats1 = functions.get_stats(text1)
        stats2 = functions.get_stats(text2)
        text1_ci_left = functions.bootstrapped_ci(text1, q=0.025, n=1000)
        text1_ci_right = functions.bootstrapped_ci(text1, q=0.975, n=1000)
        text2_ci_left = functions.bootstrapped_ci(text2, q=0.025, n=1000)
        text2_ci_right = functions.bootstrapped_ci(text2, q=0.975, n=1000)

    st.write(functions.get_table(stats1, stats2))
    st.write(functions.get_table(text1_ci_left, text1_ci_right))
    st.write(functions.get_table(text2_ci_left, text2_ci_right))
    st.caption("p/s — per sentence")
