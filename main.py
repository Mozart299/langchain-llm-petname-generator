import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
import logging
from typing import Optional, Dict, Union
import json
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PetNameGenerator:
    def __init__(self, temperature: float = 0.7):
        load_dotenv()
        
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.llm = ChatOpenAI(temperature=temperature)
        
        self.prompt_template = ChatPromptTemplate.from_template(
            """I need a creative and fitting name for my {pet_color} {animal_type} who is {gender}.
            Consider these aspects:
            - The animal's color, type, and gender
            - Cultural references that might be fun
            - How the name sounds when called out
            - Any relevant mythology or history
            - Current pop culture references if applicable
            - Names that are appropriate for the specified gender
            
            Please respond with the following format, separated by |:
            1. The name (appropriate for a {gender} pet)
            2. A brief explanation of why you chose it
            3. A fun fact related to the name
            4. A suggested nickname
            
            For example: "Luna | This name reflects both the cat's mysterious nature and silver-gray color | Luna is the Roman goddess of the moon | Suggested nickname: Lunie"""
        )
        
        self.chain = RunnablePassthrough() | self.prompt_template | self.llm

    def generate_name(
        self, 
        animal_type: str, 
        pet_color: str, 
        gender: str,
        retries: int = 3
    ) -> Dict[str, Union[str, Optional[str]]]:
        try:
            # Validate inputs
            if not all(x.strip() for x in [animal_type, pet_color, gender]):
                raise ValueError("Animal type, color, and gender cannot be empty")
            
            # Clean inputs
            animal_type = animal_type.lower().strip()
            pet_color = pet_color.lower().strip()
            gender = gender.lower().strip()
            
            logger.info(f"Generating name for {gender} {pet_color} {animal_type}")
            
            input_data = {
                "pet_color": pet_color,
                "animal_type": animal_type,
                "gender": gender
            }
            
            for attempt in range(retries):
                try:
                    response = self.chain.invoke(input_data)
                    name, explanation, fun_fact, nickname = response.content.strip().split("|")
                    return {
                        "name": name.strip(),
                        "explanation": explanation.strip(),
                        "fun_fact": fun_fact.strip(),
                        "nickname": nickname.strip(),
                        "gender": gender,
                        "error": None
                    }
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == retries - 1:
                        raise
            
        except Exception as e:
            error_msg = f"Failed to generate name: {str(e)}"
            logger.error(error_msg)
            return {
                "name": None,
                "explanation": None,
                "fun_fact": None,
                "nickname": None,
                "gender": None,
                "error": error_msg
            }

def load_favorites():
    try:
        return json.loads(st.session_state.get('favorites', '[]'))
    except:
        return []

def save_favorites(favorites):
    st.session_state['favorites'] = json.dumps(favorites)

def initialize_session_state():
    if 'name_history' not in st.session_state:
        st.session_state.name_history = []
    if 'generation_count' not in st.session_state:
        st.session_state.generation_count = 0
    if 'favorites' not in st.session_state:
        st.session_state.favorites = '[]'

def setup_page_config():
    st.set_page_config(
        page_title="🐾 Perfect Pet Name Generator",
        page_icon="🐾",
        layout="wide"
    )
    
    st.markdown("""
        <style>
        .pet-name {
            font-size: 2.5em;
            font-weight: bold;
            color: #1E88E5;
            text-align: center;
            padding: 20px;
        }
        .highlight {
            background-color: #f0f7ff;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .stButton > button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

def display_name_result(result, pet_color, animal_type, gender):
    st.markdown(f"<div class='pet-name'>{result['name']}</div>", unsafe_allow_html=True)
    
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.markdown("### 💭 Why this name?")
        st.markdown(f"<div class='highlight'>{result['explanation']}</div>", unsafe_allow_html=True)
    
    with info_col2:
        st.markdown("### ⭐ Fun Fact")
        st.markdown(f"<div class='highlight'>{result['fun_fact']}</div>", unsafe_allow_html=True)
    
    with info_col3:
        st.markdown("### 💝 Nickname")
        st.markdown(f"<div class='highlight'>{result['nickname']}</div>", unsafe_allow_html=True)

    if st.button("❤️ Save to Favorites"):
        favorites = load_favorites()
        favorites.append(result)
        save_favorites(favorites)
        st.success("Added to your favorites!")

    st.markdown("---")
    st.markdown("### 📱 Share this name")
    share_text = f"Just found the perfect name for my {gender.lower()} {pet_color.lower()} {animal_type.lower()}: {result['name']}! Generated by the Perfect Pet Name Generator 🐾"
    st.code(share_text, language=None)
    st.button("📋 Copy to Clipboard")

def display_favorites():
    favorites = load_favorites()
    if favorites:
        st.subheader("❤️ Your Favorite Names")
        for fav in favorites:
            with st.expander(f"{fav['name']} - {fav['gender']} {fav['animal_type']}"):
                st.write(f"**Explanation:** {fav['explanation']}")
                st.write(f"**Fun Fact:** {fav['fun_fact']}")
                st.write(f"**Nickname:** {fav['nickname']}")
                if st.button("Remove from Favorites", key=f"remove_{fav['name']}"):
                    favorites.remove(fav)
                    save_favorites(favorites)
                    st.rerun()

def display_name_history():
    if st.session_state.name_history:
        st.subheader("📜 Recently Generated Names")
        for item in reversed(st.session_state.name_history[-5:]):
            with st.expander(f"{item['name']} - {item['timestamp']}"):
                st.write(f"**For:** {item['gender']} {item['pet_color']} {item['animal_type']}")
                st.write(f"**Explanation:** {item['explanation']}")
                st.write(f"**Fun Fact:** {item['fun_fact']}")
                st.write(f"**Nickname:** {item['nickname']}")

def display_tips():
    st.header("🌟 Tips & Tricks for Choosing the Perfect Pet Name")
    
    with st.expander("🎯 What Makes a Great Pet Name"):
        st.markdown("""
        * **Easy to pronounce:** Your pet should recognize their name easily
        * **Distinct sound:** Choose a name that stands out from common commands
        * **Length:** 1-2 syllables are ideal for most pets
        * **Positive associations:** Pick a name you'll be happy to use for years
        * **Gender appropriate:** Consider names that match your pet's gender
        * **Unique but not too complex:** Be creative while keeping it practical
        """)
        
    with st.expander("🚫 Common Naming Mistakes to Avoid"):
        st.markdown("""
        * Choosing names too similar to commands
        * Picking overly long or complicated names
        * Using names that could be embarrassing to call in public
        * Selecting names your pet can't distinguish
        * Picking trendy names that might age poorly
        * Using names that don't match your pet's gender
        """)
        
    with st.expander("💡 Pro Tips for Using the Generator"):
        st.markdown("""
        * Try different creativity levels for varied suggestions
        * Use personality traits to get more tailored names
        * Save your favorites to compare later
        * Generate multiple options before deciding
        * Consider both the main name and nickname
        * Think about how the name suits your pet's gender
        """)

def main():
    setup_page_config()
    initialize_session_state()

    st.title("🐾 Perfect Pet Name Generator")
    st.markdown("*Creating unique and meaningful names for your furry friends!*")

    tab1, tab2, tab3 = st.tabs(["Generate Name", "Name Gallery", "Tips & Tricks"])

    with tab1:
        col1, col2, col3 = st.columns(3)

        pet_types = {
            "Cat": "🐱", "Dog": "🐶", "Bird": "🦜", "Fish": "🐠",
            "Hamster": "🐹", "Rabbit": "🐰", "Snake": "🐍",
            "Lizard": "🦎", "Parrot": "🦜", "Guinea Pig": "🐹",
            "Other": "✨"
        }

        pet_colors = [
            "Black", "White", "Brown", "Golden", "Gray", "Orange",
            "Spotted", "Striped", "Multi-colored", "Other"
        ]

        with col1:
            animal_type = st.selectbox(
                "What kind of pet do you have?",
                options=list(pet_types.keys()),
                format_func=lambda x: f"{pet_types[x]} {x}"
            )
            if animal_type == "Other":
                animal_type = st.text_input("Enter your pet type:")

        with col2:
            pet_color = st.selectbox(
                "What color is your pet?",
                pet_colors
            )
            if pet_color == "Other":
                pet_color = st.text_input("Enter your pet's color:")

        with col3:
            gender = st.selectbox(
                "What's your pet's gender?",
                ["Female", "Male"]
            )

        personality_traits = st.multiselect(
            "Select your pet's personality traits (optional)",
            ["Playful", "Shy", "Energetic", "Calm", "Clever", "Friendly", "Mysterious", "Regal"]
        )

        col4, col5 = st.columns(2)
        with col4:
            temperature = st.slider(
                "Creativity Level",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values will generate more creative and varied names"
            )
        
        with col5:
            name_style = st.selectbox(
                "Name Style Preference",
                ["Any", "Classic", "Modern", "Mythological", "Pop Culture", "Nature-inspired"]
            )

        if st.button("✨ Generate Perfect Name ✨", type="primary"):
            if all([animal_type, pet_color, gender]):
                with st.spinner("Creating the perfect name for your pet..."):
                    try:
                        generator = PetNameGenerator(temperature=temperature)
                        result = generator.generate_name(animal_type, pet_color, gender)

                        if result["name"]:
                            st.session_state.generation_count += 1
                            
                            result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            result["animal_type"] = animal_type
                            result["pet_color"] = pet_color
                            st.session_state.name_history.append(result)

                            display_name_result(result, pet_color, animal_type, gender)

                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please fill in the pet type, color, and gender!")

    with tab2:
        st.header("🖼️ Name Gallery")
        display_favorites()
        display_name_history()

    with tab3:
        display_tips()

    st.markdown("---")
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("Names Generated", st.session_state.generation_count)
    with col_stats2:
        st.metric("Favorites Saved", len(load_favorites()))
    with col_stats3:
        st.metric("Names in History", len(st.session_state.name_history))

if __name__ == "__main__":
    main()