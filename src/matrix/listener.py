import nio
from .utils import *
import config

# bot = "botlib.Bot(creds, config)"


async def custom_room_message_hander(room, event):
    event_source = get_source(event)
    message_type = event_source['content']['msgtype']

    if message_type == "m.text":
        await getText(room, nio.RoomMessageText.from_dict(event_source))

    elif message_type == "m.image":
        await getImage(room, nio.RoomMessageImage.from_dict(event_source))

    elif message_type == "m.audio":
        await getAudio(room, nio.RoomMessageAudio.from_dict(event_source))

    elif message_type == "m.video":
        await getVideo(room, nio.RoomMessageVideo.from_dict(event_source))

    elif message_type == "m.file":
        await getFile(room, nio.RoomMessageFile.from_dict(event_source))

    else:
        print("Unknown message event")


async def getText(room, event):
    message = event.source
    sender = message["sender"]

    if is_me(sender):
        return

    if not is_admin(sender):
        return await bot.api.send_text_message(room.room_id, config.NOT_IN_ADMINS_TEXT)

    # if reply or edit
    if "m.relates_to" in message['content'].keys():
        # if reply
        if "m.in_reply_to" in message['content']['m.relates_to']:
            reply_event_id = message['content']['m.relates_to']['m.in_reply_to']['event_id']

            print("reply:", reply_event_id,
                  message['content']['body'].split('\n\n', 1)[1])

        # if edit
        if "rel_type" in message['content']['m.relates_to']:
            if message['content']['m.relates_to']['rel_type'] == "m.replace":
                edit_event_id = message['content']['m.relates_to']['event_id']
                new_message_data = message['content']['m.new_content']['body']

                print("edit:", edit_event_id, new_message_data)
    
    await send_reaction(bot, room.room_id, message['event_id'], 'доставлено')


async def getImage(room, event):
    image = event.source
    sender = image["sender"]

    if is_me(sender):
        return

    if not is_admin(sender):
        return await bot.api.send_text_message(room.room_id, config.NOT_IN_ADMINS_TEXT)

    decrypted_data = nio.crypto.attachments.decrypt_attachment(
        await download(bot, image['content']['file']['url']),
        image["content"]["file"]["key"]["k"],
        image["content"]["file"]["hashes"]["sha256"],
        image["content"]["file"]["iv"],
    )

    with open(f"dec.{get_ext(image['content']['body'])}", "wb") as f:
        f.write(decrypted_data)

    await bot.api.send_text_message(room.room_id, "ok")


async def getAudio(room, event):
    audio = event.source
    sender = audio['sender']

    if is_me(sender):
        return

    if not is_admin(sender):
        return await bot.api.send_text_message(room.room_id, config.NOT_IN_ADMINS_TEXT)

    decrypted_data = nio.crypto.attachments.decrypt_attachment(
        await download(bot, audio['content']['file']['url']),
        audio["content"]["file"]["key"]["k"],
        audio["content"]["file"]["hashes"]["sha256"],
        audio["content"]["file"]["iv"],
    )

    with open(f"dec.{get_ext(audio['content']['body'])}", "wb") as f:
        f.write(decrypted_data)

    await bot.api.send_text_message(room.room_id, "ok")


async def getVideo(room, event):
    video = event.source
    sender = video['sender']

    if is_me(sender):
        return

    if not is_admin(sender):
        return await bot.api.send_text_message(room.room_id, config.NOT_IN_ADMINS_TEXT)

    decrypted_data = nio.crypto.attachments.decrypt_attachment(
        await download(bot, video['content']['file']['url']),
        video["content"]["file"]["key"]["k"],
        video["content"]["file"]["hashes"]["sha256"],
        video["content"]["file"]["iv"],
    )

    with open(f"dec.{get_ext(video['content']['body'])}", "wb") as f:
        f.write(decrypted_data)

    await bot.api.send_text_message(room.room_id, "ok")


async def getFile(room, event):
    myfile = event.source
    sender = myfile['sender']

    print(myfile)

    if is_me(sender):
        return

    if not is_admin(sender):
        return await bot.api.send_text_message(room.room_id, config.NOT_IN_ADMINS_TEXT)

    decrypted_data = nio.crypto.attachments.decrypt_attachment(
        await download(bot, myfile['content']['file']['url']),
        myfile["content"]["file"]["key"]["k"],
        myfile["content"]["file"]["hashes"]["sha256"],
        myfile["content"]["file"]["iv"],
    )

    with open(f"dec.{get_ext(myfile['content']['body'])}", "wb") as f:
        f.write(decrypted_data)

    await bot.api.send_text_message(room.room_id, "ok")


def listener_start(bot_obj):
    global bot

    bot = bot_obj

    bot.listener._registry = [
        [custom_room_message_hander, nio.RoomMessage]
    ]

    bot.run()