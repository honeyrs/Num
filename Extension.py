from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# User data storage for file name, file type selection, and accumulated text
user_data = {}

# Default file types
FILE_TYPES = ['.txt', '.py', '.md']

# Start command to greet user and prompt them to select a file type
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    # Initialize user data if not already done
    if user_id not in user_data:
        user_data[user_id] = {'file_type': '.txt', 'file_name': f'user_{user_id}', 'text': []}

    # Define a keyboard for file type selection
    keyboard = [
        [KeyboardButton(f"Set File Type: {file_type}") for file_type in FILE_TYPES],
        [KeyboardButton("Change File Name")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    # Welcome message with file type selection prompt
    await update.message.reply_text(
        "Welcome to the File Converter Bot!\n\nPlease select the file type or customize your file.",
        reply_markup=reply_markup
    )

# Command to change file name
async def change_file_name(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    await update.message.reply_text(
        "Please send me the custom file name (without extension).",
        reply_markup=ReplyKeyboardRemove()
    )

# Command to change file type
async def set_file_type(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    selected_file_type = update.message.text.strip()

    # Check if the selected file type is valid
    if selected_file_type in FILE_TYPES:
        user_data[user_id]['file_type'] = selected_file_type
        await update.message.reply_text(f"File type set to {selected_file_type}. You can now send your text.")
    else:
        await update.message.reply_text("Invalid file type! Please choose from the available options.")

# Handle text messages and accumulate them
async def handle_text(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_text = update.message.text

    # Get the user's selected file type and custom file name
    file_type = user_data[user_id].get('file_type', '.txt')
    file_name = user_data[user_id].get('file_name', f'user_{user_id}')

    # Add the user text to the accumulated text list
    user_data[user_id]['text'].append(user_text)

    # Notify user that their text has been added
    await update.message.reply_text(f"Text added! You can continue typing or send /done when you're finished.")

# Handle the custom file name from the user
async def handle_custom_file_name(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    custom_name = update.message.text.strip()

    if custom_name:
        user_data[user_id]['file_name'] = custom_name
        await update.message.reply_text(f"File name set to {custom_name}. You can now send your text.", reply_markup=ReplyKeyboardMarkup(
            [['Set File Type'], ['Change File Name']], resize_keyboard=True))
    else:
        await update.message.reply_text("Please provide a valid name for the file.")

# /done command to merge all accumulated text into a single file and send it
async def done(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id not in user_data or not user_data[user_id]['text']:
        await update.message.reply_text("You haven't sent any text yet! Please send some text first.")
        return

    # Get the user's selected file type and custom file name
    file_type = user_data[user_id].get('file_type', '.txt')
    file_name = user_data[user_id].get('file_name', f'user_{user_id}')

    # Merge all the accumulated text
    merged_text = "\n\n".join(user_data[user_id]['text'])

    # Create the final file
    file_name_with_extension = f"{file_name}{file_type}"

    try:
        # Create the file and save the merged text in it
        with open(file_name_with_extension, 'w') as file:
            file.write(merged_text)

        # Send the file back to the user
        await update.message.reply_document(document=open(file_name_with_extension, 'rb'))

        # Optionally delete the file after sending it to clean up
        os.remove(file_name_with_extension)

        # Clear the accumulated text for the user after sending the file
        user_data[user_id]['text'] = []
    except Exception as e:
        await update.message.reply_text(f"An error occurred while saving the file: {str(e)}")

# Command to show available file types again
async def change_file_type(update: Update, context: CallbackContext) -> None:
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
    api_token = '8077701911:AAFxhvmzRy4Q2vbDWiQO9aUK2Ho6V2mDJEU'

    # Create the Application
    application = Application.builder().token(api_token).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("done", done))  # /done command to merge and send the file
    application.add_handler(CommandHandler("change_file_type", change_file_type))  # Command to change file type
    application.add_handler(CommandHandler("change_file_name", change_file_name))  # Command to change file name
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))  # Handle text input
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^(Set File Type: .*)$"), set_file_type))  # Handle file type selection
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_file_name))  # Handle custom file name input

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
