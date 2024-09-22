# !pip install telegram
# !pip install python-telegram-bot==13.3
# !pip install telebot
# !pip install pytelegrambotapi
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
from telebot import TeleBot
import random
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

# Telegram Bot Token
TOKEN = '6229406413:AAGkHXGCMoXsTRRM-ILNgrZA6jgYmzZelcE'

# Spoonacular API Key
API_KEY = '780d0ac1e9ad48ae8921e4ed80444315'

RANDOM_RECIPE_URL = f'https://api.spoonacular.com/recipes/random?apiKey={API_KEY}'
RECIPE_BY_INGREDIENTS_URL = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}'

def get_random_recipeid():
    response = requests.get(RANDOM_RECIPE_URL)
    if response.status_code == 200:
        data = response.json()
        image_url = data['recipes'][0]['image']
        global random_recipe_id
        random_recipe_id = data['recipes'][0]['id']
        return random_recipe_id
    else:
        return None

def get_food_image(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image_url = data['image']
        return image_url
    else:
        return None

def start(update, context):
    chat_id = update.message.chat_id
    recipe_id = get_random_recipeid()
    context.bot.send_message(chat_id=chat_id, text='Welcome to the Food Recipe Bot!')
    context.bot.send_photo(chat_id=chat_id, photo=get_food_image(recipe_id))
    context.bot.send_message(chat_id=chat_id, text=get_food_name(recipe_id))
    context.bot.send_message(chat_id=chat_id, text=get_recipe(recipe_id))
    context.bot.send_message(chat_id=chat_id, text=get_recipe_source_url(recipe_id), reply_markup=get_inline_keyboard())

def get_recipe_by_ingredients(ingredients):
    ingredients_query = ','.join(ingredients)
    url = f'{RECIPE_BY_INGREDIENTS_URL}&ingredients={ingredients_query}&number=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['id']
    return None

def get_recipe(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        a = data['instructions']
        return a
        #context.bot.send_message(chat_id=chat_id, text=f'Recipe :\n {a}')
    else:
        return None
        #context.bot.send_message(chat_id=chat_id, text='No recipe found for the given ingredients.')

def get_inline_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton('Next', callback_data='next')
        ],
        [
            InlineKeyboardButton('Enter Ingredients', callback_data='ingredients')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard)

def ingredient_input(update, context):
    chat_id = update.message.chat_id
    ingredients = update.message.text.split(',')
    recipe_id = get_recipe_by_ingredients(ingredients)
    if recipe_id:
        context.bot.send_photo(chat_id=chat_id, photo=get_food_image(recipe_id))
        context.bot.send_message(chat_id=chat_id, text=get_food_name(recipe_id))
        context.bot.send_message(chat_id=chat_id, text=f'Recipe ID: {recipe_id}')
        url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            a = data['instructions']
            context.bot.send_message(chat_id=chat_id, text=f'Recipe :\n {a}')
        else:
            return None
        context.bot.send_message(chat_id=chat_id, text=get_recipe_source_url(recipe_id))
        context.bot.send_message(chat_id=chat_id, text='Choose an option:', reply_markup=get_inline_keyboard())
    else:
        context.bot.send_message(chat_id=chat_id, text='No recipe found for the given ingredients.')

def button_callback(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    if query.data == 'recipe':
        recipe_id = query.message.reply_to_message.text.split('\n\n')[1]
        get_recipe_url(recipe_id)
        if recipe_url:
            context.bot.send_message(chat_id=chat_id, text=recipe_url)
        else:
            context.bot.send_message(chat_id=chat_id, text='Sorry, failed to fetch recipe.')
    elif query.data == 'next':
        recipe_id = get_random_recipeid()
        context.bot.send_photo(chat_id=chat_id, photo=get_food_image(recipe_id))
        context.bot.send_message(chat_id=chat_id, text=get_food_name(recipe_id))
        context.bot.send_message(chat_id=chat_id, text=get_recipe(recipe_id))
        context.bot.send_message(chat_id=chat_id, text=get_recipe_source_url(recipe_id), reply_markup=get_inline_keyboard())
    elif query.data == 'ingredients':
        context.bot.send_message(chat_id=chat_id, text='Please enter the available ingredients separated by commas.')

def get_food_name(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        food_name = data['title']
        return food_name
    else:
        return None

def get_recipe_source_url(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        source_url = data['sourceUrl']
        return source_url
    else:
        return None

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers
    start_handler = MessageHandler(Filters.command & Filters.regex('^/start$'), start)
    button_handler = CallbackQueryHandler(button_callback)
    ingredient_handler = MessageHandler(Filters.text & ~Filters.command, ingredient_input)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(button_handler)
    dispatcher.add_handler(ingredient_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()