import os
from pyrogram import Client, filters
import string_extract, hashtags_extract, domain_extract


Bot = Client(
    "String-Extract-Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

types = [
    "lines",
    "spaces",
    "words",
    "hashtags",
    "total_hashtags",
    "links",
    "urls",
    "domains"
]


@Bot.on_message(filters.command("start"))
async def start(bot, update):
    
    text = f"Hi {update.from_user.mention}," + "\n" + "I am a simple string extract bot." + "\n\n" + "Send /extract {type} as reply a message for extracting" + "\n\n" + "**Types:**" + ", ".join(types) + "\n\n" + "Made by @FayasNoushad"
    
    await update.reply_text(
        text=text,
        quote=True
    )


@Bot.on_message(filters.command("extract"))
async def extract(bot, update):
    
    if " " not in update.text or not update.reply_to_message.text or not update.reply_to_message.caption:
        await update.reply_text("Please send command with type as reply to a string")
    
    else:
        type = update.text.split()[1]
        string = update.reply_to_message.text if update.reply_to_message.text else update.reply_to_message.caption
        
        if type not in types:
            await update.reply_text("`Invalid type!`")
        
        else:
            if type == "lines":
                text = string_extract.lines(string)
            elif type == "spaces":
                text = string_extract.spaces(string)
            elif type == "words":
                text = string_extract.words(string)
            elif type == "hashtags":
                text = "\n".join(hashtags_extract.hashtags(string, hash=True))
            elif type == "total_hashtags":
                text = len(hashtags_extract.hashtags(string))
            elif type == "links":
                text = string_extract.links(string)
            elif type == "urls":
                text = "\n".join(string_extract.urls(string))
            elif type == "domains":
                text = "\n".join(domain_extract.string_domains(string))
            
            await update.reply_text(
                text=str(text),
                quote=True,
                disable_web_page_preview=True
            )


Bot.run()
