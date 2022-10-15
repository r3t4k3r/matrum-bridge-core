from config import *
# import nio


async def download(bot, url_with_mxc):
    server_name, media_id = url_with_mxc.split("mxc://")[1].split('/')
    result = await bot.api.async_client.download(
        server_name=server_name,
        media_id=media_id
    )
    return result.body


async def send_reaction(bot, room_id, event_id, reaction_text):
    content = {
        'm.relates_to': {
            'event_id': event_id,
            'key': reaction_text,
            'rel_type': 'm.annotation'
        }
    }
    await bot.api.async_client.room_send(
        room_id,
        message_type="m.reaction",
        content=content,
        ignore_unverified_devices=True
    )


def get_source(event):
    return event.__dict__['source']


def is_admin(user_id):
    if user_id in ADMINS:
        return True
    return False


def is_me(user_id):
    if user_id == LOGIN:
        return True
    return False


def get_ext(filename):
    splited = filename.split('.')
    if len(splited) > 1:
        return splited[-1]
    return "unknown"
