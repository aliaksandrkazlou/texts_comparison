import nltk
import streamlit as st

import utils


st.set_page_config(page_title="Text comparison", page_icon="🧐", layout="wide")

st.title("Text comparison")

with st.spinner("Loading"):
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)

    if "query_id" in (query_params := st.experimental_get_query_params()):
        try:
            query_document = utils.load_query(query_params["query_id"][0])
        except KeyError as e:
            st.error(e)
            st.button(
                label="Start a new query",
                on_click=utils.clear_all,
            )
            st.stop()
        st.session_state.update(query_document)
        st.session_state.update(
            {f"init_{key}": value for key, value in query_document.items()}
        )

if st.session_state.get("saved", False):
    st.success("Query saved! To share it, just copy the link in the address bar")

with st.form("text_form"):
    for i, column in enumerate(st.columns(2), start=1):
        with column:
            st.text_area(
                label=f"Enter text {i}",
                height=600,
                key=f"text{i}",
                placeholder=f"Text {i}",
            )
    st.form_submit_button(label="Run", on_click=utils.submit)

if (
    st.session_state.get("submitted", False)
    or st.session_state.get("saved", False)
    or "query_id" in query_params
):
    text1 = st.session_state["text1"]
    text2 = st.session_state["text2"]
    if text1 == "" or text2 == "":
        st.error("Please enter both texts")
        st.stop()
    with st.spinner("Calculating the metrics"):
        stats1 = utils.get_stats(text1)
        stats2 = utils.get_stats(text2)
    with st.spinner("Calculating the bootstrapped confidence interval for text 1"):
        text1_ci_left = utils.bootstrapped_ci(text1, q=2.5, n=1000)
        text1_ci_right = utils.bootstrapped_ci(text1, q=97.5, n=1000)
    with st.spinner("Calculating the bootstrapped confidence interval for text 2"):
        text2_ci_left = utils.bootstrapped_ci(text2, q=2.5, n=1000)
        text2_ci_right = utils.bootstrapped_ci(text2, q=97.5, n=1000)

    st.write("##### Metrics for text 1 and text 2:")
    st.write(utils.get_table({"": "Text 1", **stats1}, {"": "Text 2", **stats2}))
    st.write("##### Bootstrapped 95% confidence interval for text 1:")
    st.write(
        utils.get_table({"": "Lower", **text1_ci_left}, {"": "Upper", **text1_ci_right})
    )
    st.write("##### Bootstrapped 95% confidence interval for text 2:")
    st.write(
        utils.get_table({"": "Lower", **text2_ci_left}, {"": "Upper", **text2_ci_right})
    )
    st.caption("p/s — per sentence")

    if "query_id" not in query_params:
        st.button("Save query", key="saved", on_click=utils.save)

    st.button(
        label="Start a new query",
        on_click=utils.clear_all,
    )
    st.session_state["submitted"] = False
