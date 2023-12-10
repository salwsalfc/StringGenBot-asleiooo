from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "𓆘𓆘𓅄 ذا كنـت تـريد تنـصيـب سـورس مـيوزك
𓅄 فـأسـتـخـࢪج جـلـسـة بـايـروجـرام
𓅄 واذا تـريـد تنـصـيب سـورس تـيلـثون
𓅄 فـأسـتـخـࢪج جـلـسـة تـيـرمـكـس
𓅄 اذا كـان سـورسك مـتحـدث مع اخـر
𓅄 تحديثات البايروجرام فأختار بايروجرام v2
𓅄 يـوجـد اسـتـخـرج جـلسـات ل البـوتات :𓆘𓆘"
buttons_ques = [
    [
        InlineKeyboardButton("بايروجرام", callback_data="بايروجرام"),
        InlineKeyboardButton("تـليثون", callback_data="تليثون "),
    ],
    [
        InlineKeyboardButton("بايروجرام بوت ", callback_data="بايروجرام بوت"),
        InlineKeyboardButton("تـليثون بوت ", callback_data="تليثون بوت "),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="ابدء استخراج جلسة", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if telethon:
        ty = "تليثون "
    else:
        ty = "بايروجرام"
    if is_bot:
        ty += " 𝖡𝖮𝖳"
    await msg.reply(f"𓅄¦ بـدء إنـشـاء جـلسـة تـيلـثـون ...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "𓅄 اࢪسـل الان ايبي ايدي API_ID

𓅄 اضـغـط /skip لـلـتـخـطـي", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/تخطي ":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("𓅄 يجب ان يكون ايبي ايدي عدداً صحيحاً 
𓅄 يࢪجي المحـاولة مـࢪة أخـࢪى...", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "𓅄 اࢪسـل الان ايبي هاش API_HASH", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "𓅄 اࢪسـل الان ࢪقمك مع ࢪمـز دولتك 𓅄 مثـال :+910000000000"
    else:
        t = "𓅄 اࢪسـل الان توكن بوتك BOT_TOKEN
𓅄 مثل : 5432198765:abcdanonymousterabaaplol'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("𓅄 انتظر سوف نرسل كود لحسابك بالتليجرام...")
    else:
        await msg.reply("𓅄 محاولة تسجيل الدخول عبࢪ توكن البوت...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("» ʏᴏᴜʀ 𓆘𓆘ᴀᴩɪ_ɪᴅ𓆘𓆘 ᴀɴᴅ 𓆘𓆘ᴀᴩɪ_ʜᴀsʜ𓆘𓆘 ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ᴅᴏᴇsɴ'ᴛ ᴍᴀᴛᴄʜ ᴡɪᴛʜ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴩᴩs sʏsᴛᴇᴍ. \n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("» ᴛʜᴇ 𓆘𓆘ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ𓆘𓆘 ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ᴅᴏᴇsɴ'ᴛ ʙᴇʟᴏɴɢ ᴛᴏ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ.\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "𓅄 ارسل الان كود التحقق الذي تم ارسالة لك
𓅄 ارسل كود التحقق مثل: 1 2 3 4 5
𓅄 مع فراغ بين الارقام...", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("» ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏғ 10 ᴍɪɴᴜᴛᴇs.\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("» ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs 𓆘𓆘ᴡʀᴏɴɢ.𓆘𓆘\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("» ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs 𓆘𓆘ᴇxᴩɪʀᴇᴅ.𓆘𓆘\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(user_id, "» ᴩʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ 𓆘𓆘ᴛᴡᴏ sᴛᴇᴩ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ𓆘𓆘 ᴩᴀssᴡᴏʀᴅ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("» ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏғ 5 ᴍɪɴᴜᴛᴇs.\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply("» ᴛʜᴇ ᴩᴀssᴡᴏʀᴅ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ᴡʀᴏɴɢ.\n\nᴩʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"𓆘𓆘❲ 𝖳𝖧𝖨𝖲 𝖨𝖲 𝖸𝖮𝖴𝖱 {ty} 𝖲𝖳𝖱𝖨𝖭𝖦 𝖲𝖤𝖲𝖲𝖨𝖮𝖭 ❳𓆘𓆘 \n\n`{string_session}` \n\n𓆘𓆘❲ هذا هو كود التيرمكس الخاص بك لا تعطيه لأي شخص لان معرض للختراق :𓆘𓆘 @wasit_go ❳"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "تم انشاء الجلسة بنجاح ✅ تـيـلـثـون 
يرجى التحقق من رسائلك المحفوظة للحصول عليها !
𓅄 تم بواسطة سورس الفراعنة︙ @wasit_go ❳".format("تليثون " if telethon else "تليثون بوت "))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("𓆘𓆘» ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ᴏɴɢᴏɪɴɢs !𓆘𓆘", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("𓆘𓆘❲ 𝖲𝖴𝖢𝖢𝖤𝖲𝖲𝖥𝖴𝖫𝖫𝖸 𝖱𝖤𝖲𝖳𝖠𝖱𝖤𝖣 𝖳𝖧𝖨𝖲 𝖡𝖮𝖳 𝖥𝖮𝖱 𝖸𝖮𝖴 ❳𓆘𓆘", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/تخطي " in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("𓆘𓆘𓅄 تم إلغاء عملية إنشاء الجلسة !𓆘𓆘", quote=True)
        return True
    else:
        return False
