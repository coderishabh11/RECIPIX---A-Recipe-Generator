# RECIPIX---A-Recipe-Generator

This project builds a recipe generator web app using Streamlit. It leverages computer vision to detect vegetables from user-uploaded images and then retrieves recipes from the Spoonacular API based on the detected ingredients.

![Screenshot 2024-05-04 121244](https://github.com/coderishabh11/RECIPIX---A-Recipe-Generator/assets/128208221/2fbbc480-80aa-4afd-85f3-db65a3134939)

![Screenshot 2024-05-04 120928](https://github.com/coderishabh11/RECIPIX---A-Recipe-Generator/assets/128208221/7d756a82-4fdc-4851-86c7-fc6456fe8a52)

![Screenshot 2024-05-04 121009](https://github.com/coderishabh11/RECIPIX---A-Recipe-Generator/assets/128208221/4171b385-56ea-4c4f-bbe2-2677e173cc03)

**Recipix** is a user-friendly recipe generator powered by computer vision and the Spoonacular API. It helps you discover delicious meals based on the vegetables you have on hand.

## Key Features:

**Vegetable Detection:** Recipix leverages computer vision to accurately identify multiple vegetables in a single image or multiple images.

**Recipe Generation:** Seamlessly integrates with the Spoonacular API to generate a variety of recipes tailored to the detected vegetables.

**User-Friendly Interface:** Built with Streamlit, Recipix provides a simple and intuitive web app experience.

## How it Works:

1. **Upload Image(s):** Select one or more images containing the vegetables you want to use.
2. **Vegetable Detection:** Recipix employs a computer vision model to identify the vegetables in your images.
3. **Recipe Generation:** The detected vegetables are sent to the Spoonacular API, which returns a list of delicious recipe options.
4. **Enjoy Cooking!** Explore the generated recipes and choose the one that inspires you.

## Getting Started:

**Prerequisites:** Ensure you have Python (version X.X or later) and the required libraries installed (mention specific libraries like OpenCV, Streamlit, etc.).

**Clone the Repository:** Use Git to clone this repository (provide the Git clone command).

**Run the App:** Navigate to the project directory and execute the command `streamlit run app.py` (replace app.py with your actual script name). This will launch the Recipix web app in your browser.

## Additional Notes:

- Feel free to customize the project to fit your needs, such as adding support for dietary restrictions or user ratings.
- Consider including a section on how to contribute to the project (if applicable).
