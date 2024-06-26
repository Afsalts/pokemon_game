import streamlit as st
import random

# Define the Pokémon and their moves
pokemons = {
    "Charmander": {
        "level": 5,
        "hp": 39,
        "moves": {"Scratch": 6, "Ember": 10, "Growl": 0, "Smokescreen": 0},
        "attack": 52,
        "defense": 43
    },
    "Squirtle": {
        "level": 5,
        "hp": 44,
        "moves": {"Tackle": 5, "Water Gun": 10, "Tail Whip": 0, "Bubble": 6},
        "attack": 48,
        "defense": 65
    },
    "Bulbasaur": {
        "level": 5,
        "hp": 45,
        "moves": {"Tackle": 5, "Vine Whip": 10, "Growl": 0, "Leech Seed": 0},
        "attack": 49,
        "defense": 49
    }
}

# Game state
if 'battle_log' not in st.session_state:
    st.session_state.battle_log = []
if 'ash_pokemon' not in st.session_state:
    st.session_state.ash_pokemon = None
if 'gary_pokemon' not in st.session_state:
    st.session_state.gary_pokemon = None
if 'ash_hp' not in st.session_state:
    st.session_state.ash_hp = 0
if 'gary_hp' not in st.session_state:
    st.session_state.gary_hp = 0
if 'turn' not in st.session_state:
    st.session_state.turn = 'Ash'
if 'ash_move' not in st.session_state:
    st.session_state.ash_move = None
if 'gary_move' not in st.session_state:
    st.session_state.gary_move = None

# Function to simulate an attack
def attack(attacker, defender, move):
    damage = pokemons[attacker]['moves'][move] + pokemons[attacker]['attack'] - pokemons[defender]['defense']
    damage = max(0, damage)  # Ensure damage is not negative
    return damage

# UI layout
st.title("Pokémon Battle Game")
i=0
if st.session_state.ash_pokemon is None or st.session_state.gary_pokemon is None:
    st.sidebar.header("Choose Your Pokémon")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.subheader("Ash")
        st.session_state.ash_pokemon = st.selectbox("Choose Pokémon for Ash", list(pokemons.keys()), key=f"ash{i}")
        if st.session_state.ash_pokemon:
            st.session_state.ash_hp = pokemons[st.session_state.ash_pokemon]["hp"]
            
    with col2:
        st.subheader("Gary")
        st.session_state.gary_pokemon = st.selectbox("Choose Pokémon for Gary", list(pokemons.keys()), key=f"gary{i}")
        if st.session_state.gary_pokemon:
            st.session_state.gary_hp = pokemons[st.session_state.gary_pokemon]["hp"]
            
    if st.session_state.ash_pokemon and st.session_state.gary_pokemon:
        if st.button("Start Battle"):
    
            st.session_state.battle_log = [f"Battle started: Ash's {st.session_state.ash_pokemon} vs Gary's {st.session_state.gary_pokemon}"]
    i=i+1
else:
    if st.session_state.turn == 'Ash':
        st.subheader(f"Ash's Turn ({st.session_state.ash_pokemon})")
        move = st.radio("Choose a move", list(pokemons[st.session_state.ash_pokemon]['moves'].keys()), key=f"ash_move{i}")
        if st.button("Attack", key="ash_attack"):
            damage = attack(st.session_state.ash_pokemon, st.session_state.gary_pokemon, move)
            st.session_state.gary_hp -= damage
            st.session_state.battle_log.append(f"Ash's {st.session_state.ash_pokemon} used {move}. It dealt {damage} damage.")
            #st.button("Next")
            #if st.button("Next",key="next_turn"):
            st.session_state.turn = 'Gary'
    else:
        st.subheader(f"Gary's Turn ({st.session_state.gary_pokemon})")
        move = st.radio("Choose a move", list(pokemons[st.session_state.gary_pokemon]['moves'].keys()), key=f"gary_move{i}")
        if st.button("Attack", key="gary_attack"):
            damage = attack(st.session_state.gary_pokemon, st.session_state.ash_pokemon, move)
            st.session_state.ash_hp -= damage
            
            st.session_state.battle_log.append(f"Gary's {st.session_state.gary_pokemon} used {move}. It dealt {damage} damage.")
            #if st.button("Next",key="next_turnash"):
            st.session_state.turn = 'Ash'
    i=i+1
    if st.session_state.ash_hp <= 0:
        st.session_state.battle_log.append(f"Ash's {st.session_state.ash_pokemon} has fainted. Gary wins!")
    elif st.session_state.gary_hp <= 0:
        st.session_state.battle_log.append(f"Gary's {st.session_state.gary_pokemon} has fainted. Ash wins!")

    st.write("## Battle Log")
    for log in st.session_state.battle_log:
        st.write(log)
    
    st.write(f"Ash's {st.session_state.ash_pokemon} HP: {max(0, st.session_state.ash_hp)}")
    st.write(f"Gary's {st.session_state.gary_pokemon} HP: {max(0, st.session_state.gary_hp)}")
    
    if st.session_state.ash_hp <= 0 or st.session_state.gary_hp <= 0:
        if st.button("Restart Game"):
            st.session_state.ash_pokemon = None
            st.session_state.gary_pokemon = None
            st.session_state.ash_hp = 0
            st.session_state.gary_hp = 0
            st.session_state.turn = 'Ash'
            st.session_state.battle_log = []

