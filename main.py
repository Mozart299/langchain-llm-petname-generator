import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
import logging
from typing import Optional, Dict, Union

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PetNameGenerator:
    def __init__(self, temperature: float = 0.7):
        # Load environment variables
        load_dotenv()
        
        # Verify API key exists
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.llm = ChatOpenAI(temperature=temperature)
        
        self.prompt_template = ChatPromptTemplate.from_template(
            """I need a creative and fitting name for my {pet_color} {animal_type}.
            The name should be easy to call out and appropriate for the animal's appearance.
            Consider the following aspects:
            - The animal's color and type
            - Cultural references that might be fun
            - How the name sounds when called out
            Please respond with just the name, followed by a brief explanation of why you chose it, separated by a |. 
            For example: "Shadow | This name reflects both the cat's dark color and mysterious nature"."""
        )
        
        self.chain = (
            RunnablePassthrough()
            | self.prompt_template
            | self.llm
        )

    def generate_name(
        self, 
        animal_type: str, 
        pet_color: str,
        retries: int = 3
    ) -> Dict[str, Union[str, Optional[str]]]:
        try:
            if not animal_type.strip() or not pet_color.strip():
                raise ValueError("Animal type and color cannot be empty")
            
            animal_type = animal_type.lower().strip()
            pet_color = pet_color.lower().strip()
            
            logger.info(f"Generating name for {pet_color} {animal_type}")
            
            input_data = {
                "pet_color": pet_color,
                "animal_type": animal_type
            }
            
            for attempt in range(retries):
                try:
                    response = self.chain.invoke(input_data)
                    name, explanation = response.content.strip().split("|")
                    return {
                        "name": name.strip(),
                        "explanation": explanation.strip(),
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
                "error": error_msg
            }

def main():
    st.set_page_config(
        page_title="Pet Name Generator",
        page_icon="🐾",
        layout="wide"
    )

    st.title("🐾 Pet Name Generator")
    st.write("Generate the perfect name for your furry (or scaly!) friend")

    # Create two columns for inputs
    col1, col2 = st.columns(2)

    # Predefined lists of common pet types and colors
    pet_types = [
        "Cat", "Dog", "Bird", "Fish", "Hamster", "Rabbit", 
        "Snake", "Lizard", "Parrot", "Guinea Pig", "Other"
    ]
    pet_colors = [
        "Black", "White", "Brown", "Golden", "Gray", "Orange",
        "Spotted", "Striped", "Multi-colored", "Other"
    ]

    with col1:
        # Animal type selection with "Other" option
        animal_type = st.selectbox(
            "What type of pet do you have?",
            pet_types
        )
        if animal_type == "Other":
            animal_type = st.text_input("Enter your pet type:")

    with col2:
        # Color selection with "Other" option
        pet_color = st.selectbox(
            "What color is your pet?",
            pet_colors
        )
        if pet_color == "Other":
            pet_color = st.text_input("Enter your pet's color:")

    # Temperature slider for name generation randomness
    temperature = st.slider(
        "Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values will generate more creative and varied names"
    )

    # Generate button
    if st.button("Generate Name 🎲", type="primary"):
        if animal_type and pet_color:
            with st.spinner("Generating the perfect name..."):
                try:
                    generator = PetNameGenerator(temperature=temperature)
                    result = generator.generate_name(animal_type, pet_color)

                    if result["name"]:
                        # Display results in a nice format
                        st.success("Here's your suggested pet name:")
                        
                        # Create columns for name and explanation
                        name_col, explain_col = st.columns([1, 2])
                        
                        with name_col:
                            st.markdown(f"### {result['name']}")
                        
                        with explain_col:
                            st.info(result["explanation"])
                            
                        # Add a fun note
                        st.markdown("---")
                        st.markdown("*💡 Don't like this name? Adjust the creativity level and try again!*")
                    else:
                        st.error(f"Error: {result['error']}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please fill in both the pet type and color!")

    # Add helpful tips
    with st.expander("Tips for choosing a pet name"):
        st.markdown("""
        * Choose a name that's easy to pronounce and remember
        * Consider a name that matches your pet's personality
        * Test calling the name out loud a few times
        * Avoid names that could be confused with commands
        * Make sure all family members like the name
        """)

if __name__ == "__main__":
    main()