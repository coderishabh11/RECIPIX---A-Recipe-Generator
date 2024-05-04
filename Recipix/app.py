import requests
import os
import streamlit as st
from Recipe_Generator import generate_recipe_from_ingredients
from ing_list_generator import detect_vegetables
from config import CLASSES, MODEL
import pandas as pd
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML

st.set_page_config(
    page_title='RECIPEPIX',
    page_icon='🍲',
    layout='wide'
)

def option_menu(menu_title, options, orientation):
    if menu_title:
        st.sidebar.title(menu_title)

    if orientation == 'horizontal':
        selected = st.sidebar.radio("Select Option", options)
    elif orientation == 'vertical':
        selected = st.sidebar.selectbox("Select Option", options)
    else:
        raise ValueError("Invalid orientation. Use 'horizontal' or 'vertical'.")

    return selected

def load_image(image_file):
    # Add your image processing logic here
    return image_file

def save_uploaded_file(uploaded_file):
    # Create the "uploads" directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save the uploaded file to the "uploads" directory
    with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return os.path.join("uploads", uploaded_file.name)


def main():
    st.title('RECIPEPIX!!! A RECIPE GENERATOR')

    # Define menu options as a dictionary
    menu_options = {
        'Home': 'home',
        'Recipe from List': 'recipe_from_list',
    }

    # Multiselect widget for the menu
    selected_menu = option_menu(menu_title="Options", options=list(menu_options.keys()), orientation='vertical')

    st.sidebar.markdown("[Rishabh Sagar](https://www.linkedin.com/in/rishabh-sagar-1b0b74229/)", unsafe_allow_html=True)


    # Iterate over selected menu options
    for menu_item in [selected_menu]:
        if menu_options[menu_item] == 'home':
            st.subheader("Home")
            
            # Display a single file uploader for images
            image_files = st.file_uploader("Upload up to 5 images", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)

            # Check if the number of selected images is greater than the specified maximum
            if image_files and len(image_files) > 5:
                st.warning(f"You have selected more images ({len(image_files)}) than specified ({num_images}). Only the first {num_images} images will be processed.")

            # List to store detected ingredients
            all_detected_ingredients = []

            # Iterate over the specified number of images or the number of selected images
            for i in range(len(image_files)):
                image_file = image_files[i]
                img = load_image(image_file)
                st.image(img, caption=f"Image #{i + 1}", width=200)  

                # Save the uploaded image to a temporary file
                temp_file_path = save_uploaded_file(image_file)

                # Detect and classify vegetables for each image
                item_list = detect_vegetables(temp_file_path)

                # Display the generated item list
                st.subheader(f"Detected items in Image #{i + 1}")
                for item in item_list:
                    st.info(item)

                # Add detected ingredients to the list
                all_detected_ingredients.extend(item_list)

            # Get the number of recipes to generate
            num_recipes_to_generate = st.number_input("How many recipes do you want to generate?", min_value=1, value=1)

            # Generate recipe from the combined list of ingredients
            if st.button("Generate Recipes"):
                recipes = generate_recipe_from_ingredients(all_detected_ingredients)[:num_recipes_to_generate]

                # Create a dataframe from the list of recipes
                recipes_df = pd.DataFrame(recipes)

                # Display the generated recipes in a tabular form
                st.subheader("Generated Recipes")

                for i, recipe in enumerate(recipes, 1):
                    st.write(f"Recipe #{i}")
                    st.dataframe(pd.DataFrame({k: [v] for k, v in recipe.items()}).style.set_properties(**{'text-align': 'left'}), height=200)

        elif menu_options[menu_item] == 'recipe_from_list':
            st.subheader('Recipe from List')

            # Create a list of items
            items = CLASSES  # Add more items as needed

            # Display checkboxes for each item
            selected_items = [item for item in items if st.checkbox(item, key=item)]

            # Get the number of recipes to generate
            num_recipes_to_generate = st.number_input("How many recipes do you want to generate?", min_value=1, value=1)

            ## Generate recipe from the combined list of ingredients
            if st.button("Generate Recipes"):
                # Filter out selected items
                selected_ingredients = [item for item in items if item in selected_items]

                # Generate recipes
                recipes = generate_recipe_from_ingredients(selected_ingredients)[:num_recipes_to_generate]

                # Create a dataframe from the list of recipes
                recipes_df = pd.DataFrame(recipes)

                # Display the generated recipes in a tabular form
                st.subheader("Generated Recipes")

                for i, recipe in enumerate(recipes, 1):
                    st.write(f"Recipe #{i}")
                    st.dataframe(pd.DataFrame({k: [v] for k, v in recipe.items()}).style.set_properties(**{'text-align': 'left'}), height=200)



if __name__ == '__main__':
    main()
