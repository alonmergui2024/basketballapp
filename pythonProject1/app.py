import streamlit as st
from streamlit_extras.switch_page_button import switch_page


def page1():
    st.title("Page 1")
    st.write("Content for Page 1")
    if st.button("Go to Page 2"):
        a = False
        return a


def page2():
    st.title("Page 2")
    st.write("Content for Page 2")
    if st.button("Go to Page 1"):
        a = True
        return a


page = [page1(),page2()]

x = st.slider("x", 0, 10)

if x == 1:
    switch_page("page1")
elif x == 2:
    switch_page("page2")