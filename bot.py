import logging
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChannelPrivate
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

gif = [
    'https://te.legra.ph/file/a1b3d4a7b5fce249902f7.mp4',
    'https://te.legra.ph/file/0c855143a4039108df602.mp4',
    'https://te.legra.ph/file/d7f3f18a92e6f7add8fcd.mp4',
    'https://te.legra.ph/file/9e334112ee3a4000c4164.mp4',
    'https://te.legra.ph/file/652fc39ae6295272699c6.mp4',
    'https://te.legra.ph/file/702ca8761c3fd9c1b91e8.mp4',
    'https://te.legra.ph/file/a1b3d4a7b5fce249902f7.mp4',
    'https://te.legra.ph/file/d7f3f18a92e6f7add8fcd.mp4',
    'https://te.legra.ph/file/0c855143a4039108df602.mp4',
    'https://te.legra.ph/file/9e334112ee3a4000c4164.mp4',
    'https://te.legra.ph/file/702ca8761c3fd9c1b91e8.mp4'
]

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    required_channels = cfg.REQUIRED_CHANNELS
    missing_channels = []

    try:
        for channel in required_channels:
            try:
                await app.get_chat_member(channel, kk.id)
            except UserNotParticipant:
                missing_channels.append(channel)
            except (ChatAdminRequired, ChannelPrivate):
                logger.error(f"Bot is not admin or channel {channel} is private")
                continue

        if missing_channels:
            channels_list = "\n".join([f"@{channel}" for channel in missing_channels])
            await app.send_message(kk.id, f"**To access this group, please join the following channels:**\n{channels_list}")
        else:
            add_group(m.chat.id)
            await app.approve_chat_join_request(op.id, kk.id)
            img = random.choice(gif)
            await app.send_video(kk.id, img, f"**Hello {kk.mention}!\nWelcome To {m.chat.title}\n\n__Powered By : @TandavBots __**")
            add_user(kk.id)

        # Check if user left any required channel after joining
        asyncio.create_task(check_user_in_channel(kk.id, op.id, required_channels))

    except Exception as err:
        logger.error(f"Error in approve function: {err}")

async def check_user_in_channel(user_id, chat_id, required_channels):
    await asyncio.sleep(300)  # Wait for 5 minutes
    for channel in required_channels:
        try:
            await app.get_chat_member(channel, user_id)
        except UserNotParticipant:
            try:
                await app.ban_chat_member(chat_id, user_id)
                await app.unban_chat_member(chat_id, user_id)
                await app.send_message(user_id, f"You have been removed from the group because you left the required channel {channel}")
            except Exception as e:
                logger.error(f"Error removing user {user_id} from chat {chat_id}: {e}")
            return

@app.on_message(filters.command("start"))
async def start(_, m: Message):
    try:
        logger.info(f"User {m.from_user.id} is starting the bot.")
        logger.info(f"Trying to access chat with ID {cfg.CHID}")

        chat_member = await app.get_chat_member(cfg.CHID, m.from_user.id)
        logger.info(f"Chat member fetched successfully: {chat_member}")

        if m.chat.type == enums.ChatType.PRIVATE:
            # Normal processing logic
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🗯 Channel", url="https://t.me/TandavBots"),
                 InlineKeyboardButton("💬 Support", url="https://t.me/TandavBots_Support")]
            ])
            add_user(m.from_user.id)
            await m.reply_photo("https://graph.org/file/d57d6f83abb6b8d0efb02.jpg", 
                                caption=f"**🦊 Hello {m.from_user.mention}!\nI'm an auto-approve [Admin Join Requests]({m.chat.title}) Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.\n\n__Powered By : @TandavBots __**", 
                                reply_markup=keyboard)

        elif m.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            # Handle group start command
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/autoaccept_requesttb_bot")
            ]])
            add_group(m.chat.id)
            await m.reply_text(f"**🦊 Hello {m.from_user.first_name}!\nWrite me private for more details**", reply_markup=keyboard)

        logger.info(f"{m.from_user.first_name} has successfully started your bot!")

    except UserNotParticipant:
        key = InlineKeyboardMarkup([[InlineKeyboardButton("🍀 Check Again 🍀", "chk")]])
        await m.reply_text(f"**⚠️ Access Denied! ⚠️\n\nPlease join @{cfg.FSUB} to use me. If you joined, click the check again button to confirm.**", reply_markup=key)
    except Exception as err:
        logger.error(f"Error in start function: {err}")

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🗯 Channel", url="https://t.me/TandavBots"),
                 InlineKeyboardButton("💬 Support", url="https://t.me/TandavBots_Support")]
            ])
            add_user(cb.from_user.id)
            await cb.message.edit(f"**🦊 Hello {cb.from_user.mention}!\nI'm an auto-approve [Admin Join Requests]({cb.message.chat.title}) Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.\n\n__Powered By : @TandavBots __**", reply_markup=keyboard, disable_web_page_preview=True)
        logger.info(f"{cb.from_user.first_name} has started your bot!")
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You are not joined to the channel. Join and try again. 🙅‍♂️", show_alert=True)
    except Exception as err:
        logger.error(f"Error in chk function: {err}")

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(f"✅ Successfully sent to `{success}` users.\n❌ Failed for `{failed}` users.\n👾 Found `{blocked}` blocked users.\n👻 Found `{deactivated}` deactivated users.")

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.forward(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(f"✅ Successfully forwarded to `{success}` users.\n❌ Failed for `{failed}` users.\n👾 Found `{blocked}` blocked users.\n👻 Found `{deactivated}` deactivated users.")

@app.on_message(filters.command(["ban", "unban"]) & filters.user(cfg.SUDO))
async def ban_unban(_, m: Message):
    if len(m.command) != 2:
        await m.reply_text("Usage: /ban or /unban <user_id>")
        return

    user_id = int(m.command[1])
    chat_id = m.chat.id
    try:
        if m.command[0].lower() == "ban":
            await app.ban_chat_member(chat_id, user_id)
            await m.reply_text(f"User {user_id} has been banned.")
        else:
            await app.unban_chat_member(chat_id, user_id)
            await m.reply_text(f"User {user_id} has been unbanned.")
    except Exception as e:
        await m.reply_text(f"An error occurred: {str(e)}")

print("I'm Alive Now!")
app.run()
