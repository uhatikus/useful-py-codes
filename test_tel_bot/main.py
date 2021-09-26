from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

HELP_BUTTON_CALLBACK_DATA = 'A unique text for help button callback data'
help_button = InlineKeyboardButton(
    text='Help me', # text that show to user
    callback_data=HELP_BUTTON_CALLBACK_DATA # text that send to bot when user tap button
    )


def command_handler_start(bot, update):
    chat_id = update.message.from_user.id
    bot.send_message(
        chat_id=chat_id,
        text='Hello ...',
        reply_markup=InlineKeyboardMarkup([[help_button]]),
        )


def command_handler_help(bot, update):
    chat_id = update.message.from_user.id
    bot.send_message(
        chat_id=chat_id,
        text='Help text for user ...',
        )

def callback_query_handler(bot, update):
    cqd = update.callback_query.data
    #message_id = update.callback_query.message.message_id
    #update_id = update.update_id
    if cqd == HELP_BUTTON_CALLBACK_DATA:
        command_handler_help(bot, update)
    # elif cqd == ... ### for other buttons


update = Updater('')
bot = update.bot
dp = update.dispatcher
print('Your bot is --->', bot.username)
dp.add_handler(CommandHandler('start', command_handler_start))
dp.add_handler(CommandHandler('help', command_handler_help))
dp.add_handler(CallbackQueryHandler(callback_query_handler))
update.start_polling()

# from telegram.ext import Updater, CallbackQueryHandler
# updater = Updater(token='', use_context=True)

# dispatcher = updater.dispatcher

# import logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                      level=logging.INFO)

# def get_state(message):
#     return USER_STATE[message.chat.id]


# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# from telegram.ext import CommandHandler
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)

# updater.start_polling()

# # def echo(update, context):
# #     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# # from telegram.ext import MessageHandler, Filters
# # echo_handler = MessageHandler(Filters.text, echo)
# # dispatcher.add_handler(echo_handler)

# def caps(update, context):
#     text_caps =  ' '.join(context.args).upper()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


# caps_handler = CommandHandler('caps', caps)
# dispatcher.add_handler(caps_handler)

# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# def ask(update,context):
#   list_of_cities = ['A','B','C', 'D', 'E']
#   button_list = []
#   for each in list_of_cities:
#      button_list.append(InlineKeyboardButton(each, callback_data = each))
#   reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1)) #n_cols = 1 is for single column and mutliple rows
#   context.bot.send_message(chat_id=update.message.chat_id, text='Choose from the following',reply_markup=reply_markup)


# def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
#   menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#   if header_buttons:
#     menu.insert(0, header_buttons)
#   if footer_buttons:
#     menu.append(footer_buttons)
#   return menu

# ask_handler = CommandHandler('ask', ask)
# dispatcher.add_handler(ask_handler)
# bot = updater.bot

# def callback_query_handler(bot, update):
#     cqd = update.callback_query.data
#     context.bot.send_message(chat_id=update.message.chat_id, text=cqd)
# dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))

# def build_menu(buttons,
#                n_cols,
#                header_buttons=None,
#                footer_buttons=None):
#     menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#     if header_buttons:
#         menu.insert(0, [header_buttons])
#     if footer_buttons:
#         menu.append([footer_buttons])
#     return menu

# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# # reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
# # dispatcher.send_message("What?", "A two-column menu", reply_markup=reply_markup)

# def buttons():
#     button_list = [
#         InlineKeyboardButton("col1", callback_data="1"),
#         InlineKeyboardButton("col2", callback_data="2"),
#         InlineKeyboardButton("row 2", callback_data="3")
#     ]
#     keyboard.add(*button_list)
#     return keyboard


# buttons_handler = CommandHandler('buttons', buttons)
# dispatcher.add_handler(buttons_handler)
