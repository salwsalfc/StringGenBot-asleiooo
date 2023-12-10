from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""اهلا بك عزيزي 🫶 {msg.from_user.mention},

البوت الاول عل تليجرام  {me2}

𓅄¦ فـي بـوت اسـتـخـراج الـجـلـسـات
𓅄¦ يمكنك استخراج الجلسات الـتالية
𓅄¦ بايروجرام للحسابات & بايروجرام للبوتات
𓅄¦ بـايـروجـرام مـيوزك احـدث إصـدار 
𓅄¦ تيرمـكـس للحسابات & تيرمـكـس للبوتات



مالك البوت  ︙ [🕴آلَمِــــطوُر البوت 𓅄𓆋](tg://user?id={OWNER_ID}) """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="ابدء استخراج جلسة ", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("𓆋 ســـورس آلَفــــرآعـــنه 𓆋", url="https://t.me/wasit_go"),
                    InlineKeyboardButton("🕴آلَمِــــطوُر البوت 𓅄𓆋", user_id=OWNER_ID)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
