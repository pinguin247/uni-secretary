from typing import Final
from telegram import *
from telegram.ext import *
from bottoken import BOT_TOKEN
#Final is just for giving constants a type
TOKEN: Final = BOT_TOKEN
BOT_USERNAME: Final = '@uni_secretary_bot'


#Stored variables
timetables = {} #store timetable images
courses = {}


#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    START_MESSAGE_BUTTONS = [
        #First row, 2 buttons
        [InlineKeyboardButton("Show Timetable", callback_data="Show Timetable"), InlineKeyboardButton("Show Course Details", callback_data="Courses")],
        #Second rowm 2 buttons
        [InlineKeyboardButton("Show Assignments", callback_data="Assignments"), InlineKeyboardButton("Send Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(START_MESSAGE_BUTTONS)
    await update.message.reply_text(
        text="You can use /settimetable to set a new timetable, or replace the existing one."
        , reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help is on the way!")


async def settimetable_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    TIMETABLE_MESSAGE_BUTTONS = [
        #First row, 2 buttons
        [InlineKeyboardButton("Save Image", callback_data="Save Image"), InlineKeyboardButton("Parse Timetable", callback_data="Parse")],
    ]
    reply_markup = InlineKeyboardMarkup(TIMETABLE_MESSAGE_BUTTONS)
    await update.message.reply_text(
        text="Do you want to save your timetable as an image or parse the timetable to automically update course details?"
        , reply_markup=reply_markup)


async def setcourses_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You do not have any courses saved! Please use /setcoursedetails to set course details first.")



async def setassignments_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global courses
    if len(courses) == 0:
        await update.message.reply_text("You do not have any courses saved! Please use /setcoursedetails to set course details first.")
    else:
        await update.message.reply_text("I can't help you now sorry :(")



# Response Handlers
def handle_response(text: str) -> str: #return a string
    processed: str = text.lower() # make the string less case sensitive

    if 'hello' in processed:
        return 'Hey there!'
    if 'wassup' in processed:
        return 'eh yo wassup'

    return 'Sorry I do not understand, please press /start to see list of commands'


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
        return "Image stored successfully! You can now access it by selecting 'Show Timetable' on the main menu."
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
    user_id = update.callback_query.from_user.id 
    global timetables

    if call_back_data in ("Show Timetable"):
        # Acknowledge the button click
        await update.callback_query.answer()

        # Check if there are already existing timetables for the user
        if user_id in timetables:
            photo = timetables[user_id]
            await context.bot.send_photo(chat_id=chat_id, photo=photo.file_id)
        else:
            response_message = "You have no timetable saved yet. Please send an image of your timetable."
            await context.bot.send_message(chat_id=chat_id, text=response_message)


    if call_back_data in ("Save Image"):
        # Acknowledge the button click
        await update.callback_query.answer()

        #Check if there is already a timetable saved
        if user_id in timetables:
            SAVE_TIMETABLE_MESSAGE_BUTTONS = [
                [InlineKeyboardButton("Yes", callback_data="Delete Timetable"), InlineKeyboardButton("No", callback_data="Return")],
            ]
            reply_markup = InlineKeyboardMarkup(SAVE_TIMETABLE_MESSAGE_BUTTONS)
            await context.bot.send_message(chat_id=chat_id, text="You already have an existing timetable. Would you like to replace it with a new timetable?", reply_markup=reply_markup)

        else:
            response_message = "Please send an image of your timetable in png or jpeg format."
            await context.bot.send_message(chat_id=chat_id, text=response_message)

    if call_back_data in ("Delete Timetable"):
        # Acknowledge the button click
        await update.callback_query.answer()
        response_message = "Please send an image of your timetable in png or jpeg format."
        await context.bot.send_message(chat_id=chat_id, text=response_message)

    if call_back_data in ("Return"):
        # Acknowledge the button click
        await update.callback_query.answer()
        response_message = "Understood. Please use the /start command to return to main menu."
        await context.bot.send_message(chat_id=chat_id, text=response_message)

    if call_back_data in ("Parse"):
        await context.bot.send_message(chat_id=chat_id, text="Sorry this feature is not implemeted yet!")

    if call_back_data in ("Show Assignments"):
        await context.bot.send_message(chat_id=chat_id, text="Assignments? What assignments lolol")

    if call_back_data in ("Show Courses"):
        await context.bot.send_message(chat_id=chat_id, text="If you must cross a coarse, cross cow across a crowded cow crossing, cross the cross, coarse cow across the crowded cow crossing carefully.")

    if call_back_data in ("help"):
        await context.bot.send_message(chat_id=chat_id, text="Sorry cant..")




if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('settimetable', settimetable_command))
    app.add_handler(CommandHandler('setcourses', setcourses_command))
    app.add_handler(CommandHandler('setassignments', setassignments_command))

    #Menu 
    app.add_handler(CallbackQueryHandler(menu_response))

    #Messages
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    #Errors
    app.add_error_handler(error)

    #Check constantly for updates
    print('Pollling...')
    app.run_polling(poll_interval=3)