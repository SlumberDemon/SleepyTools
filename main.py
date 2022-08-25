import requests
import validators
import streamlit as st

st.markdown(f"# SleepyTools")

with st.sidebar:
    tool = st.selectbox("Select tool", ["Link Shortener", "Embed Creator"])

st.markdown(f"###### {tool}")

if tool == "Link Shortener":
    url = st.text_input("Url")
    if url:
        if validators.url(url) is True:
            submit = st.button("Shorten")
            if submit:
                r = requests.post(f"https://sleepy.deta.dev/shorten?url={url}")
                st.success(f"Link shortened: {r.json()['url']}")
        else:
            st.warning("Make sure the input is a valid url")
        
elif tool == "Embed Creator":
    c1, c2 = st.columns(2)
    b1, b2 = st.columns(2)
    with c1:
        title = st.text_input("Title")
    with c2:
        description = st.text_input("Description")
    with b1:
        image = st.text_input("Image url")
        size = st.selectbox("Image size", [None, "small", "large"])
    with b2:
        url = st.text_input("Website url")
        colour = st.color_picker("Colour")
        c = colour.replace("#", "")

    submit = st.button("Generate embed")

    if submit:
        r = requests.post(
            f"https://sleepy.deta.dev/embed?title={title}&description={description}&image={image}&colour={c}&size={size}&url={url}"
        )
        st.success(f"Embed created: {r.json()['url']}")

st.caption("[Source](https://github.com/SlumberDemon/SleepyTools)")
