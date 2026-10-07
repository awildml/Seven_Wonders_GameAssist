import streamlit as st 
import pandas as pd
import base64
from pathlib import Path

def webp_to_url(filename):
    path = Path(__file__).parent / "Resources" / filename
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/webp;base64,{encoded}"

players = list(st.session_state.game_info)
cats = st.session_state.cats
category_images = {
    "Wonder Board": webp_to_url("Wonder.webp"),
    "Military Conflict": webp_to_url("Military.webp"),
    "Coins & Debt": webp_to_url("Coins.webp"),
    "Civil Buildings": webp_to_url("Blue.webp"),
    "Commercial": webp_to_url("Yellow.webp"),
    "Scientific": webp_to_url("Green.webp"),
    "Guilds": webp_to_url("Purple.webp"), 
    "Leaders": webp_to_url("Leader.webp"),
    "Naval Conflict": webp_to_url("Naval.webp"),
    "Islands": webp_to_url("Island.webp")
}

image_urls = [
    category_images[category]
    for category in cats
]

if st.button("New game"): 
    st.session_state.wonders = None 
    st.session_state.game_info = {} 
    st.session_state.cats = None 
    st.session_state.pop("score_grid", None)
    st.session_state.grid_version = (
        st.session_state.get("grid_version", 0) + 1
    )
    st.switch_page("game_setup.py")
    
if "grid_version" not in st.session_state:
    st.session_state.grid_version = 0

if "score_grid" not in st.session_state:
    table = pd.DataFrame(0, index=cats, columns=players)
    table.insert(0, "Category", image_urls)

    table.loc["Total", players] = 0
    table.loc["Total", "Category"] = ""

    st.session_state.score_grid = table

edited_scores = st.data_editor(
    st.session_state.score_grid,
    hide_index=True,
    column_config={
        "Category": st.column_config.ImageColumn("Images")
    },
    disabled=["_index", "Category"],
    num_rows="fixed",
    key=f"score_table_{st.session_state.grid_version}"
)

# Detect a change to the numeric cells
if not edited_scores[players].equals(
    st.session_state.score_grid[players]
):
    updated = edited_scores.copy()

    # Sum category rows only, excluding Total
    updated.loc["Total", players] = updated.loc[cats, players].sum(axis=0)

    st.session_state.score_grid = updated
    st.session_state.grid_version += 1
    st.rerun()