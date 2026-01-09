import traceback
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InputMediaPhoto
)

from Flexyy.generate import generate_session, ask_ques, buttons_ques


ERROR_MESSAGE = """ɪғ ʏᴏᴜ ᴀʀᴇ ɢᴇᴛᴛɪɴɢ ᴇʀʀᴏʀ!
ʏᴏᴜ ʜᴀᴠᴇ ᴅᴏɴᴇ sᴏᴍᴇ ᴍɪsᴛᴀᴋᴇ ᴡʜɪʟᴇ ɢᴇɴᴇʀᴀᴛɪɴɢ.
ᴛʀʏ ᴀɢᴀɪɴ.
ᴏʀ ғᴏʀᴡᴀʀᴅ ᴇʀʀᴏʀ ᴛᴏ ᴏᴡɴᴇʀ."""


@Client.on_callback_query(
    filters.regex(r"^(generate|pyrogram|pyrogram_bot|telethon_bot|telethon)$")
)
async def _callbacks(bot: Client, cq: CallbackQuery):
    query = cq.data

    try:
        if query == "generate":
            await cq.answer()

            # 🔥 FIX: SAME MESSAGE EDIT + PHOTO CHANGE
            await cq.message.edit_media(
                media=InputMediaPhoto(
                    media="https://files.catbox.moe/rjteel.jpg",
                    caption=ask_ques
                ),
                reply_markup=InlineKeyboardMarkup(buttons_ques)
            )

        elif query == "pyrogram":
            await cq.answer()
            await generate_session(bot, cq.message)

        elif query == "pyrogram_bot":
            await cq.answer("ᴘʏʀᴏɢʀᴀᴍ ᴠ2 ʙᴏᴛ", show_alert=True)
            await generate_session(bot, cq.message, is_bot=True)

        elif query == "telethon":
            await cq.answer()
            await generate_session(bot, cq.message, telethon=True)

        elif query == "telethon_bot":
            await cq.answer()
            await generate_session(bot, cq.message, telethon=True, is_bot=True)

    except Exception as e:
        print(traceback.format_exc())
        await cq.message.reply(ERROR_MESSAGE)