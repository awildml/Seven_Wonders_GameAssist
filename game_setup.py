import streamlit as st 
import random 



# ----- Wonder Choice -----# 

# Add expansions as preferenced 
def choose_expansions(cities, leaders, armada, edifice): 
    wonders = basegame.copy()
    cats = cat_basegame.copy() 
    if cities:
        wonders.extend(["Byzantium", "Petra"])
        cats.extend(["Black Cards"])
    if leaders: 
        wonders.extend(["Roma", "Abu Simbel"])
        cats.extend(["Leaders"])
    if armada:
        wonders.extend(["Siracusa"])
        cats.extend(["Naval Conflict", "Islands"])
    if edifice:
        wonders.extend(["Ur", "Carthage"])
    return wonders, cats

def choose_wonder(wonders): 

    wonder_idx = random.randint(0, len(wonders)-1)
    side_idx   = random.randint(0, 1) 
    wonder     = wonders.pop(wonder_idx)
    side       = sides[side_idx]
    return wonder, side 

basegame = ["Alexandria", "Babylon", "Éphesos", "Gizah", "Halikarnassos", "Olympia", "Rhódos"]
sides    = ["(A)", "(B)"]
cat_basegame = ["Wonder Board", "Military Conflict", "Coins & Debt", "Civil Buildings", "Commercial", "Scientific", "Guilds"]

# Initialise once per session 
if "wonders" not in st.session_state: 
    st.session_state.wonders = None 

if "game_info" not in st.session_state: 
    st.session_state.game_info = {} 

if "cats" not in st.session_state: 
    st.session_state.cats = None 

# Reset button 
if st.button("New game"): 
    st.session_state.wonders = None 
    st.session_state.game_info = {} 
    st.session_state.cats = None 
    st.session_state.pop("score_grid", None)
    st.session_state.grid_version = (
        st.session_state.get("grid_version", 0) + 1
    )
    st.switch_page("game_setup.py")

# Select Expansions
if st.session_state.wonders is None: 
    with st.form("Expansions"): 
        st.write("Expansions")
        cb_cities  = st.checkbox("Cities") 
        cb_leaders = st.checkbox("Leaders") 
        cb_armada  = st.checkbox("Armada") 
        cb_edifice = st.checkbox("Edifice")

        started = st.form_submit_button("Continue") 
        if started: 
            st.session_state.wonders, st.session_state.cats = choose_expansions(
                cb_cities, cb_leaders, cb_armada, cb_edifice) 
            st.rerun() # Will not show after rerun due to if statement 

# Wonder allocation 
else: 
    with st.form("Wonders", clear_on_submit=True): 
        player = st.text_input("Player name:")
        submitted = st.form_submit_button("Confirm")
        
        if submitted: 
            player = player.strip() 
            if not player: 
                st.error("Enter player name") 
            elif player in st.session_state.game_info: 
                st.error("Player already registered") 
            elif not st.session_state.wonders: 
                st.error("No wonders remain") 
            else: 
                wonder, side = choose_wonder(st.session_state.wonders) 
                st.session_state.game_info[player] = {
                    "Wonder": wonder,
                    "Side": side 
                }
                st.success(f"{player}: {wonder} {side}")

    if st.button("Scores Calculator"): 
        st.switch_page("scores.py")