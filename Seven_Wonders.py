import streamlit as st 

page = st.navigation([
    st.Page("game_setup.py", title="Game Setup"),
    st.Page("scores.py",      title="scores")
])

page.run()