from pyrogram import Client

api_id = 1111  # from config.yaml
api_hash = "1111"  # from config.yaml
username = "name"

with Client("uhatikus", api_id, api_hash) as app:
    app.send_message("me", "Greetings from **Pyrogram**!")
    # message = app.get_messages("Enotikk88", 51113)
    # print(message.message_id, message.from_user.username, message.text)
    for message in app.iter_history(username):
        print(message.message_id, message.from_user.username, message.text)
