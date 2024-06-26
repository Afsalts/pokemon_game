import streamlit as st
import random

# Define Pokémon data with attack types
pokemon_data = {
    "Squirtle": {
        "type": "Water",
        "hp": 100,
        "attacks": {
            "Tackle": {"type": "Normal", "damage": 10},
            "Water Gun": {"type": "Water", "damage": 15},
            "Bite": {"type": "Dark", "damage": 20},
            "Tail Whip": {"type": "Normal", "damage": 5}
        }
    },
    "Charmander": {
        "type": "Fire",
        "hp": 100,
        "attacks": {
            "Scratch": {"type": "Normal", "damage": 10},
            "Ember": {"type": "Fire", "damage": 15},
            "Flamethrower": {"type": "Fire", "damage": 25},
            "Growl": {"type": "Normal", "damage": 5}
        }
    },
    "Bulbasaur": {
        "type": "Grass",
        "hp": 100,
        "attacks": {
            "Tackle": {"type": "Normal", "damage": 10},
            "Vine Whip": {"type": "Grass", "damage": 15},
            "Razor Leaf": {"type": "Grass", "damage": 20},
            "Growl": {"type": "Normal", "damage": 5}
        }
    },
    "Pikachu": {
        "type": "Electric",
        "hp": 100,
        "attacks": {
            "Quick Attack": {"type": "Normal", "damage": 10},
            "Thunder Shock": {"type": "Electric", "damage": 15},
            "Thunderbolt": {"type": "Electric", "damage": 25},
            "Tail Whip": {"type": "Normal", "damage": 5}
        }
    },
    "Jigglypuff": {
        "type": "Fairy",
        "hp": 100,
        "attacks": {
            "Pound": {"type": "Normal", "damage": 10},
            "Disarming Voice": {"type": "Fairy", "damage": 15},
            "Dazzling Gleam": {"type": "Fairy", "damage": 25},
            "Sing": {"type": "Normal", "damage": 5}
        }
    },
    "Meowth": {
        "type": "Normal",
        "hp": 100,
        "attacks": {
            "Scratch": {"type": "Normal", "damage": 10},
            "Bite": {"type": "Dark", "damage": 15},
            "Fury Swipes": {"type": "Normal", "damage": 20},
            "Growl": {"type": "Normal", "damage": 5}
        }
    },
    "Psyduck": {
        "type": "Water",
        "hp": 100,
        "attacks": {
            "Scratch": {"type": "Normal", "damage": 10},
            "Water Gun": {"type": "Water", "damage": 15},
            "Confusion": {"type": "Psychic", "damage": 20},
            "Tail Whip": {"type": "Normal", "damage": 5}
        }
    },
    "Machop": {
        "type": "Fighting",
        "hp": 100,
        "attacks": {
            "Low Kick": {"type": "Fighting", "damage": 10},
            "Karate Chop": {"type": "Fighting", "damage": 15},
            "Seismic Toss": {"type": "Fighting", "damage": 20},
            "Leer": {"type": "Normal", "damage": 5}
        }
    },
    "Geodude": {
        "type": "Rock",
        "hp": 100,
        "attacks": {
            "Tackle": {"type": "Normal", "damage": 10},
            "Rock Throw": {"type": "Rock", "damage": 15},
            "Magnitude": {"type": "Ground", "damage": 20},
            "Defense Curl": {"type": "Normal", "damage": 5}
        }
    },
    "Eevee": {
        "type": "Normal",
        "hp": 100,
        "attacks": {
            "Quick Attack": {"type": "Normal", "damage": 10},
            "Bite": {"type": "Dark", "damage": 15},
            "Swift": {"type": "Normal", "damage": 20},
            "Growl": {"type": "Normal", "damage": 5}
        }
    },
    "Snorlax": {
        "type": "Normal",
        "hp": 100,
        "attacks": {
            "Headbutt": {"type": "Normal", "damage": 15},
            "Body Slam": {"type": "Normal", "damage": 20},
            "Hyper Beam": {"type": "Normal", "damage": 30},
            "Rest": {"type": "Psychic", "damage": 0}
        }
    },
    "Gengar": {
        "type": "Ghost",
        "hp": 100,
        "attacks": {
            "Lick": {"type": "Ghost", "damage": 10},
            "Shadow Ball": {"type": "Ghost", "damage": 25},
            "Dream Eater": {"type": "Psychic", "damage": 30},
            "Confuse Ray": {"type": "Ghost", "damage": 5}
        }
    },
    "Lapras": {
        "type": "Water",
        "hp": 100,
        "attacks": {
            "Water Gun": {"type": "Water", "damage": 10},
            "Ice Beam": {"type": "Ice", "damage": 20},
            "Body Slam": {"type": "Normal", "damage": 25},
            "Sing": {"type": "Normal", "damage": 5}
        }
    }
}


type_effectiveness = {
    ("Water", "Fire"): 2,
    ("Fire", "Grass"): 2,
    ("Grass", "Water"): 2,
    ("Fire", "Water"): 0.5,
    ("Grass", "Fire"): 0.5,
    ("Water", "Grass"): 0.5,
    ("Normal", "Rock"): 0.5,
    ("Normal", "Ghost"): 0,
    ("Dark", "Ghost"): 2,
}

# Initialize game state
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        "player1": {"name": "Ash", "pokemon": None, "hp": 0, "attacks": {}},
        "player2": {"name": "Gary", "pokemon": None, "hp": 0, "attacks": {}},
        "current_turn": "player1",
        "battle_log": [],
        "winner": None,
    }

def select_pokemon(player_key):
    player = st.session_state.game_state[player_key]
    st.subheader(f"{player['name']}, select your Pokémon")
    selected_pokemon = st.selectbox(f"Choose a Pokémon for {player['name']}", ["Squirtle", "Charmander", "Bulbasaur"], key=f"{player_key}_selectbox")
    if selected_pokemon and st.button(f"Confirm {player['name']}'s Pokémon selection", key=f"{player_key}_button"):
        player['pokemon'] = selected_pokemon
        player['hp'] = pokemon_data[selected_pokemon]['hp']
        player['attacks'] = pokemon_data[selected_pokemon]['attacks']
        st.session_state[f"{player_key}_selected"] = True
        st.experimental_rerun()

def calculate_damage(attacker, defender, attack):
    attack_info = attacker['attacks'][attack]
    base_damage = attack_info['damage']
    attack_type = attack_info['type']
    attacker_type = pokemon_data[attacker['pokemon']]['type']
    defender_type = pokemon_data[defender['pokemon']]['type']
    effectiveness = type_effectiveness.get((attack_type, defender_type), 1)
    damage = base_damage * effectiveness
    return damage, effectiveness

def battle_turn():
    current_player = st.session_state.game_state[st.session_state.game_state['current_turn']]
    opponent_player = st.session_state.game_state['player1'] if st.session_state.game_state['current_turn'] == 'player2' else st.session_state.game_state['player2']
    
    st.subheader(f"{current_player['name']}'s turn")
    attack = st.selectbox("Choose an attack", list(current_player['attacks'].keys()), key=f"{st.session_state.game_state['current_turn']}_attack")
    
    if st.button("Attack"):
        damage, effectiveness = calculate_damage(current_player, opponent_player, attack)
        opponent_player['hp'] -= damage
        
        effectiveness_message = ""
        if effectiveness > 1:
            effectiveness_message = "It's super effective!"
        elif effectiveness < 1:
            effectiveness_message = "It's not very effective..."
        else:
            effectiveness_message = "It's effective."

        st.session_state.game_state['battle_log'].append(
            f"{current_player['name']}'s {current_player['pokemon']} used {attack}! {effectiveness_message} It dealt {damage:.2f} damage."
        )
        
        if opponent_player['hp'] <= 0:
            st.session_state.game_state['winner'] = current_player['name']
        else:
            st.session_state.game_state['current_turn'] = 'player1' if st.session_state.game_state['current_turn'] == 'player2' else 'player2'
            st.experimental_rerun()

def display_battle_log():
    for log in st.session_state.game_state['battle_log']:
        st.write(log)

def display_hp():
    player1 = st.session_state.game_state['player1']
    player2 = st.session_state.game_state['player2']
    st.write(f"Ash's {player1['pokemon']} HP: {player1['hp']}")
    st.write(f"Gary's {player2['pokemon']} HP: {player2['hp']}")

st.title("Pokémon Battle Game")

if not st.session_state.game_state['player1']['pokemon']:
    select_pokemon('player1')
elif not st.session_state.game_state['player2']['pokemon']:
    select_pokemon('player2')
else:
    if st.session_state.game_state['winner']:
        st.header(f"{st.session_state.game_state['winner']} wins!")
    else:
        display_hp()
        battle_turn()
    display_battle_log()
