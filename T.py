from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

# Define the function to handle the message and extract numbers
def extract_numbers(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text  # Get the message text from the user
    
    # Use a regular expression to find all numbers in the string
    numbers = re.findall(r'\d+', user_text)  # Finds all sequences of digits
    
    if numbers:
        # If numbers are found, send them back to the user
        update.message.reply_text(f"Here are the numbers I found: {', '.join(numbers)}")
    else:
        # If no numbers are found, inform the user
        update.message.reply_text("Sorry, I couldn't find any numbers in your message.")

def main():
    # Replace 'YOUR_API_TOKEN' with your actual bot's API token
    api_token = '8078776775:AAEObLeQmcel4R6jaahnS6YWgGX0XAnBRjQ'
    
    # Set up the Updater and Dispatcher
    updater = Updater(api_token)
    dispatcher = updater.dispatcher
    
    # Define a message handler to capture text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, extract_numbers))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
