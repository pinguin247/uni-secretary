from typing import Final
from telegram import *
from telegram.ext import *
from bottoken import BOT_TOKEN
#Final is just for giving constants a type
TOKEN: Final = BOT_TOKEN
BOT_USERNAME: Final = '@uni_secretary_bot'


#Stored variables
timetables = {} #store timetable images



#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    START_MESSAGE_BUTTONS = [
        #First row, 2 buttons
        [InlineKeyboardButton("Show Timetable", callback_data="Show Timetable"), InlineKeyboardButton("Show Classes", callback_data="ew")],
        #Second rowm 2 buttons
        [InlineKeyboardButton("Show Assignments", callback_data="ew"), InlineKeyboardButton("Send Help", callback_data="ew")]
    ]
    reply_markup = InlineKeyboardMarkup(START_MESSAGE_BUTTONS)
    await update.message.reply_text(
        text="You can use /settimetable to set a new timetable, or replace the existing one "
        , reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help is on the way!")

async def settimetable_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    TIMETABLE_MESSAGE_BUTTONS = [
        #First row, 2 buttons
        [InlineKeyboardButton("Save Timetable Image", callback_data="Image"), InlineKeyboardButton("Parse Timetable", callback_data="ew")],
    ]
    reply_markup = InlineKeyboardMarkup(TIMETABLE_MESSAGE_BUTTONS)
    await update.message.reply_text(
        text="Do you want to save your timetable as an image or parse the timetable to automically update module details?"
        , reply_markup=reply_markup)



# Response Handlers
def handle_response(text: str) -> str: #return a string
    processed: str = text.lower() # make the string less case sensitive

    if 'hello' in processed:
        return 'Hey there!'
    if 'wassup' in processed:
        return 'eh yo wassup'

    return 'nani'

def image_response(photo : PhotoSize, id: int) -> str:
    #If user sends timetable image
    # Check if the message contains an image
    global timetables

    # The message contains an image
    # Get the latest (largest) version of the image

    if photo:
        timetable = photo[-1]

        # Store the photo in the user_images dictionary with the user's ID as the key
        timetables[id] = timetable

        # Respond with a confirmation message
        return "Image stored successfully!"
    else:
        return "No image found in the message."
    

        

#For responding whenever the user calls the bot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type #this will inform us if it is group or private chat
    text: str = update.message.text #incoming message

    #print statement for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: {text}')
    #get user id of sender and the type of chat it is sent in

    if message_type == 'group':
        #If the bot is called in the group chat
        if BOT_USERNAME in text:
            #replace bot username with empty string
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return 
    else: #for all the private chats
        #if user send photo
        if update.message.photo:
            response: str = image_response(update.message.photo, update.message.from_user.id)
        else:
            response: str = handle_response(text)

    #for debugging
    print('Bot', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

#menu handler
async def menu_response(update: Update, context: CallbackContext):
    call_back_data = update.callback_query.data
    chat_id = update.callback_query.message.chat_id  # Get the chat ID

    global timetables

    if call_back_data in ("Show Timetable"):
        # Acknowledge the button click
        await update.callback_query.answer()

        # Check if there are already existing timetables for the user
        user_id = update.callback_query.from_user.id  # Get the user's ID

        if user_id in timetables:
            photo = timetables[user_id]
            await context.bot.send_photo(chat_id=chat_id, photo=photo.file_id)
        else:
            response_message = "You have no timetable saved yet. Please send an image of your timetable."
            await context.bot.send_message(chat_id=chat_id, text=response_message)






if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('settimetable', settimetable_command))

    #Menu 
    app.add_handler(CallbackQueryHandler(menu_response))

    #Messages
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    #Errors
    app.add_error_handler(error)

    #Check constantly for updates
    print('Pollling...')
    app.run_polling(poll_interval=3)