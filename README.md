# Telegram-bot
A telegram bot that uses spooclar api to fetch the recipe
Here’s an updated description with instructions on how to use the program:

---

This Python script implements a **Telegram bot** that provides food recipes based on random selection or user-provided ingredients. It uses the **python-telegram-bot** library and integrates with the **Spoonacular API** to fetch recipe data.

### Key Features:
1. **Start Command**: When a user sends the `/start` command, the bot fetches a random recipe from the Spoonacular API and displays the recipe name, image, instructions, and source link.
2. **Random Recipe Generator**: The bot provides a random recipe, including an image, title, and instructions.
3. **Recipe by Ingredients**: Users can enter available ingredients, and the bot will suggest recipes that match those ingredients.
4. **Inline Keyboard**: After each recipe, users can interact with buttons to either get a new random recipe or enter their own ingredients.
5. **Ingredient Input**: The bot prompts users to input ingredients, returning a matching recipe with relevant details.
6. **Callback Query Handling**: The bot responds to user button clicks for fetching new recipes or prompting for ingredient input.

### How to Use the Program:

1. **Install Required Libraries**:
   - Ensure the following libraries are installed:
     ```bash
     pip install telegram python-telegram-bot==13.3 telebot pytelegrambotapi
     ```

2. **Set Up**:
   - Get a **Telegram Bot Token** by creating a bot on Telegram via [BotFather](https://core.telegram.org/bots#botfather).
   - Sign up for the **Spoonacular API** and get your API key from [Spoonacular](https://spoonacular.com/food-api).

3. **Configure the Token and API Key**:
   - Replace `TOKEN` and `API_KEY` with your respective Telegram bot token and Spoonacular API key in the script.

4. **Run the Program**:
   - Execute the script:
     ```bash
     python <your_script_name>.py
     ```
   - The bot will start polling for incoming messages.

5. **Using the Bot on Telegram**:
   - Open Telegram and find your bot.
   - Type `/start` to receive a random recipe.
   - Click on the **"Next"** button to get another random recipe.
   - Click on **"Enter Ingredients"** to input ingredients. For example, type `chicken, tomato, cheese` and the bot will return a recipe matching these ingredients.
   
The bot will display the recipe name, image, instructions, and a link to the full recipe source.
