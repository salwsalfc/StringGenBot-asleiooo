import traceback

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

from StringGenBot.generate import generate_session, ask_ques, buttons_ques


@Client.on_callback_query(filters.regex(pattern=r"^(generate|pyrogram|pyrogram_bot|telethon_bot|telethon)$"))
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    query = callback_query.matches[0].group(1)
    if query == "generate":
        await callback_query.answer()
        await callback_query.message.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))
    elif query.startswith("بايروجرام ") or query.startswith("telethon"):
        try:
            if query == "بايروجرام":
                await callback_query.answer()
                await generate_session(bot, callback_query.message)
            elif query == "بايروجرام بوت":
                await callback_query.answer("» ᴛʜᴇ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴡɪʟʟ ʙᴇ ᴏғ ᴩʏʀᴏɢʀᴀᴍ ᴠ2.", show_alert=True)
                await generate_session(bot, callback_query.message, is_bot=True)
            elif query == "تليثون بوت ":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, telethon=True, is_bot=True)
            elif query == "تليثون ":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, telethon=True)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            await callback_query.message.reply(ERROR_MESSAGE.format(str(e)))


ERROR_MESSAGE = "أدخل هنا. \n\n𓆘𓆘بوت جلسات المتطور𓆘𓆘 : {} " \
            "\n\n𓆘𓆘@wasit_go𓆘,قناة البوت  " \
  

