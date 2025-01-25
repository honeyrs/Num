from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import re

# Define the function to handle the message and extract numbers
async def extract_numbers(update: Update, context) -> None:
    user_text = update.message.text  # Get the message text from the user
    
    # Use a regular expression to find all numbers in the string
    numbers = re.findall(r'\d+', user_text)  # Finds all sequences of digits
    
    if numbers:
        # If numbers are found, send them back to the user
        await update.message.reply_text(f"Here are the numbers I found: {', '.join(numbers)}")
    else:
        # If no numbers are found, inform the user
        await update.message.reply_text("Sorry, I couldn't find any numbers in your message.")

def main():
    # Replace 'YOUR_API_TOKEN' with your actual bot's API token
    api_token = '8078776775:AAEObLeQmcel4R6jaahnS6YWgGX0XAnBRjQ'
    
    # Create the Application and Dispatcher
    application = Application.builder().token(api_token).build()
    
    # Define a message handler to capture text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, extract_numbers))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
