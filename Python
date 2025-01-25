from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# User data storage for file type selection
user_file_type = {}

# Default file types
FILE_TYPES = ['.txt', '.py', '.md']

# Start command to greet user and prompt them to select a file type
async def start(update: Update, context: CallbackContext) -> None:
    # Define a keyboard for file type selection
    keyboard = [
        [KeyboardButton(f"Set File Type: {file_type}") for file_type in FILE_TYPES]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    # Welcome message with file type selection prompt
    await update.message.reply_text(
        "Welcome to the File Converter Bot!\n\nPlease select the file type you want to use for your text:",
        reply_markup=reply_markup
    )

# Command to change file type
async def set_file_type(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    selected_file_type = update.message.text.strip()

    # Check if the selected file type is valid
    if selected_file_type in FILE_TYPES:
        user_file_type[user_id] = selected_file_type
        await update.message.reply_text(f"File type set to {selected_file_type}. You can now send your text.")
    else:
        await update.message.reply_text("Invalid file type! Please choose from the available options.")

# Handle text messages and convert to the selected file type
async def handle_text(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_text = update.message.text

    # Get the user's selected file type, or default to '.txt'
    file_type = user_file_type.get(user_id, '.txt')

    # Create the file based on the selected file type
    file_name = f"user_{user_id}{file_type}"

    try:
        # Create the file and save the user text in it
        with open(file_name, 'w') as file:
            file.write(user_text)

        # Send the file back to the user
        await update.message.reply_document(document=open(file_name, 'rb'))

        # Optionally delete the file after sending it to clean up
        os.remove(file_name)
    except Exception as e:
        await update.message.reply_text(f"An error occurred while saving the file: {str(e)}")

# Command to show available file types again
async def change_file_type(update: Update, context: CallbackContext) -> None:
    # Show the available file types again so the user can change it
    keyboard = [
        [KeyboardButton(f"Set File Type: {file_type}") for file_type in FILE_TYPES]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "You can change the file type again. Please choose a new file type.",
        reply_markup=reply_markup
    )

def main():
    # Replace 'YOUR_API_TOKEN' with your bot's API token
    api_token = '8078776775:AAFKg2wwC7ZCb5oqIPJ1mcvNTz-lC_MnuQs'

    # Create the Application
    application = Application.builder().token(api_token).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("change_file_type", change_file_type))  # Command to change file type
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))  # Handle text input
    application.add_handler(MessageHandler(filters.TEXT, set_file_type))  # Handle file type selection

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
