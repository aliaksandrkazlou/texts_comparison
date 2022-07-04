import nltk
import streamlit as st

import functions

with st.spinner("Loading"):
    nltk.download("popular")

with st.form("text_form"):
    left_column, right_column = st.columns(2)

    with left_column:
        text1 = st.text_area("Enter text 1", placeholder="Text 1")
    with right_column:
        text2 = st.text_area("Enter text 2", placeholder="Text 2")

    submitted = st.form_submit_button("Run")

if submitted:
    if text1 == "" or text2 == "":
        st.write("Please enter both texts")
        st.stop()
    stats1 = functions.get_stats(text1)
    stats2 = functions.get_stats(text2)

    st.write(functions.get_table(stats1, stats2))
