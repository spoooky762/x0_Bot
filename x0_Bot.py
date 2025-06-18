    # x0_Bot - (v1.0)
import os
import asyncio
import aiohttp
import sys
import random
import time
import requests
import re
import urllib.request
import hashlib
import subprocess
import threading
import io
import telethon
import whois
import traceback
import pytz
from fake_useragent import UserAgent
from getpass import getpass
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import (
    FloodWaitError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
    MessageNotModifiedError
)
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import DocumentAttributeFilename
from telethon.tl.types import DocumentAttributeSticker
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from telethon.tl import types
from threading import Event

                                # ======================
                                # Update system
                                # ======================

GITHUB_RAW_URL = "https://raw.githubusercontent.com/spoooky762/x0_Bot/main/x0_Bot.git"
VERSION_PATTERN = r"# x0_Bot - \((v\d+\.\d+\.\d+)\)"


MESSAGE_CACHE = {}


async def force_update():
             """d updating the script with the installation of dependencies"""
    try:
                       # URL Requirements.txt file in the repository
        REQUIREMENTS_URL = "https://raw.githubusercontent.com/spoooky762/x0_Bot/main/requirements.txt"
        
        print(f"\n{COLORS['header']}Checking dependencies...{COLORS['reset']}")
        
        try:
                      # Download REQUREMENTS.TXT
            response = requests.get(REQUIREMENTS_URL, timeout=10)
            response.raise_for_status()
            
                      # We save to a temporary file
            with open("temp_requirements.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            
                      # Install libraries through PIP
            print(f"{COLORS['info']}Installation/update of libraries...{COLORS['reset']}")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "temp_requirements.txt", "--upgrade"],
                check=True
            )
            print(f"{COLORS['success']}✓ The libraries are successfully updated!{COLORS['reset']}")
            
                     # We delete a temporary file
            os.remove("temp_requirements.txt")
            
        except Exception as e:
            print(f"{COLORS['error']}✖ Library installation error: {str(e)}{COLORS['reset']}")
            traceback.print_exc()

                    # Next is the original script update code ...
           print(f"\n{COLORS['header']}Checking the relevance of files...{COLORS['reset']}")
        
                    # Obtaining a remote version
        with urllib.request.urlopen(GITHUB_RAW_URL) as response:
            remote_content = response.read().decode('utf-8')
            remote_version = re.search(VERSION_PATTERN, remote_content).group(1)
            
                     # Obtaining the current version
        with open(__file__, 'r', encoding='utf-8') as f:
            current_content = f.read()
            current_version = re.search(VERSION_PATTERN, current_content).group(1)
            
                     # Heshei check
        if hashlib.md5(current_content.encode()).hexdigest() == hashlib.md5(remote_content.encode()).hexdigest():
            return False
            
                     # The beginning of the update
        Print (f "\n {colors ['success']} found an update! {colors ['reset']") ")")
        Print (f "{colors ['info']} The current version: {current_version} {colors ['reset']") ")") ")"
        Print (f "{colors ['success"] new version: {Remote_version} {colors [' reset '] ")") ")"
        Print(f"\n{colors['header']} loading the update...{colors['reset']")")

                    # File replacement       
        temp_file = "x0_Bot_temp.py"
        with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(remote_content)    
        os.replace(temp_file, __file__)
        
        #Restart
        print(f"{COLORS['success']}✓The update is successfully loaded!{COLORS['reset']}")
        print(f"{COLORS['info']}Restart the script...{COLORS['reset']}")
        subprocess.Popen([sys.executable, __file__])
        sys.exit(0)
        
    except Exception as e:
        print(f"{COLORS['error']}✖ Error when updating: {str(e)}{COLORS['reset']}")
        traceback.print_exc()
        return False

# Verification versions Telethon

required_version = "1.36.0"
current_version = telethon.__version__
if current_version < required_version:
    print(f"Error: Telethon versions are required {required_version} or higher. The version is installed {current_version}.")
    print("Update Telethon a team: pip install --upgrade telethon")
    sys.exit(1)

                             # Purple palette for console flowers
                             # Red-white palette of flowers for the console
COLORS = {
    'header': '\033[91m', #Bright red
    'input': '\033[97m', # White   
    'success': '\033[92m', # Green
    'error': '\033[91m', # Red
    'info': '\033[37m', # Light-grey
    'prompt': '\033[97m', # White   
    'accent1': '\033[31m', # Darkred
    'accent2': '\033[90m', # DarkGray (For dividers)
    'accent3': '\033[97m', # White   
    'accent4': '\033[38;2;255;69;0m', #PLOWNG-red(RGB)
    'reset': '\033[0m'
}

API_ID = 21551581  
API_HASH = '70d80bdf86811654363e45c01c349e98'  
SESSION_PREFIX = "account_"
TEMP_SESSION = "temp.session"
ACCOUNT_DATA = {}

            # -------------------------------
            # Auxiliary functions
            # -------------------------------

def show_banner():
    """ Displays x0_Bot banner in the console."""
    try:
        with open(__file__, 'r', encoding='utf-8') as f:
            content = f.read()
            version = re.search(VERSION_PATTERN, content).group(1)
    except:
        version = "N/A"
    
    print(rf"""{COLORS['accent1']} __ ___ {COLORS['accent3']}___ ___ _____ {COLORS['reset']}
{COLORS['accent1']}>=>``````>=>```````````````````````````{COLORS['accent3']}```>=>>=>> {COLORS['reset']}
{COLORS['accent1']}`>=>```>=>```````````````````````````````{COLORS['accent3']} >>````>=>`````````````>=> {COLORS['reset']}
{COLORS['accent1']}``>=>`>=>``````>==>````>>`>==>````>=>{COLORS['accent3']}`````>>````>=>````>=>`````>=>>==> {COLORS['reset']}        
{COLORS['accent1']}````>=>``````>>```>=>```>=>`````>=>``>=>{COLORS['accent3']}``>==>>=>````>=>``>=>```>=> {COLORS['reset']}
{COLORS['accent1']}``>=> >=>````>>===>>=>``>=>````>=>````>=>{COLORS['accent3']}`>>````>=>`>=>````>=>``>=> {COLORS['reset']}
{COLORS['accent1']} >=>````>=>``>>`````````>=>`````>=>``>=> {COLORS['accent3']}`>>`````>>``>=>``>=>```>=>​​` {COLORS['reset']}
{COLORS['accent1']}>=>``````>=>``>====>````>==>``````>=> {COLORS['accent3']}````>===>>=>`````>=>```````>=> {COLORS['reset']}
{COLORS['accent1']}`````````````````````{COLORS['accent3']}>>=>>==>>==>>==>>{COLORS['reset']}


{COLORS['header']}Version {version} /{COLORS['accent3']}/ Tg - @o0xCk4sp3r{COLORS['reset']}""")
    print(f"{COLORS['accent2']}-{COLORS['reset']}" * 50)

def clear_screen():
    """Cleans the screen of the console (Windows or Linux)."""
    os.system('cls' if os.name == 'nt' else 'clear')

async def safe_delete(file_path):
    """Safely delays the session file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"{COLORS['error']}Error deleting file: {str(e)}{COLORS['reset']}")
    return False

async def load_valid_accounts():
    """Loads all real accounts from sessions."""
    global ACCOUNT_DATA
    ACCOUNT_DATA = {}
    for session_file in os.listdir('.'):
        if session_file.startswith(SESSION_PREFIX) and session_file.endswith(".session"):
            try:
                async with TelegramClient(session_file, API_ID, API_HASH) as client:
                    if await client.is_user_authorized():
                        me = await client.get_me()
                        account_id = int(session_file.split('_')[1].split('.')[0])
                        ACCOUNT_DATA[account_id] = {
                            'phone': me.phone,
                            'name': me.username or me.first_name or f"Account {account_id}",
                            'session': session_file
                        }
            except Exception as e:
                print(f"{COLORS['error']}The error of loading the session {session_file}: {str(e)}{COLORS['reset']}")
                await safe_delete(session_file)
                continue

async def delete_all_accounts():
    """Removes all accounts and their sessions."""
    deleted = 0
    for account_num in list(ACCOUNT_DATA.keys()):
        session_file = ACCOUNT_DATA[account_num]['session']
        if await safe_delete(session_file):
            del ACCOUNT_DATA[account_num]
            deleted += 1
    print(f"{COLORS['error']}[✓]ㅤ{COLORS['prompt']}Removed accounts: {deleted}{COLORS['reset']}")
    await asyncio.sleep(1)

async def create_account():
    clear_screen()
    show_banner()
    print(f"{COLORS['header']} Adding a new account{COLORS['reset']}")
    print(f"\n")

    client = None
    try:
        await safe_delete(TEMP_SESSION)
        
        while True:
            phone = input(f"{COLORS['error']}[+]ㅤ{COLORS['prompt']}Enter the number [format: +79123456789]: {COLORS['reset']}").strip()
            if re.match(r'^\+\d{8.15}$', phone):
                break
            print(f"{COLORS['error']}[✖]ㅤ{COLORS['prompt']}The wrong format! Example: +79123456789{COLORS['reset']}")

        if any(acc['phone'] == phone for acc in ACCOUNT_DATA.values()):
            print(f"{COLORS['error']}[✖]ㅤ{COLORS['prompt']} This number is already registered!{COLORS['reset']}")
            await asyncio.sleep(1)
            return

        client = TelegramClient(TEMP_SESSION, API_ID, API_HASH)
        await client.connect()

        sent_code = await client.send_code_request(phone)
        print(f"{COLORS['error']}[✓]ㅤ{COLORS['prompt']}The code is sent to {phone}{COLORS['reset']}")

        code = input(f"{COLORS['error']}[-]ㅤ{COLORS['prompt']}Enter the code from Telegram: {COLORS['reset']}").strip().replace(' ', '')

        try:
            await client.sign_in(phone, code=code, phone_code_hash=sent_code.phone_code_hash)
        except SessionPasswordNeededError:
            password = getpass(f"{COLORS['error']}[*]ㅤ{COLORS['prompt']}Enter a 2FA password (Hidden): {COLORS['reset']}")
            await client.sign_in(password=password)

        me = await client.get_me()
        account_id = max(ACCOUNT_DATA.keys(), default=0) + 1
        new_session = f"{SESSION_PREFIX}{account_id}.session"
        
        await client.disconnect()
        await asyncio.sleep(1)

        if os.path.exists(TEMP_SESSION):
            if os.path.exists(new_session):
                os.remove(new_session)
            os.rename(TEMP_SESSION, new_session)

        ACCOUNT_DATA[account_id] = {
            'phone': phone,
            'name': me.first_name or me.username or f"Account {account_id}",
            'session': new_session
        }

        print(f"{COLORS['error']}[✓]ㅤ{COLORS['prompt']}Success! {me.first_name} added{COLORS['reset']}")
        await load_valid_accounts()

    except PhoneNumberInvalidError:
        print(f"{COLORS['error']}[✖]ㅤ{COLORS['prompt']}Invalid phone number!{COLORS['reset']}")
    except PhoneCodeInvalidError:
        print(f"{COLORS['error']}[✖]ㅤ{COLORS['prompt']}Invalid confirmation code!{COLORS['reset']}")
    except Exception as e:
        print(f"{COLORS['error']}[✖]ㅤ{COLORS['prompt']}Critical error: {str(e)}{COLORS['reset']}")

        traceback.print_exc()
    finally:
        if client and client.is_connected():
            await client.disconnect()
        await safe_delete(TEMP_SESSION)
    
    input(f"\n{COLORS['input']}Press Enter to continue...{COLORS['reset']}")

def compress_image(image_bytes):
    """Compresses the image to save space."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img = img.convert('RGB')
        img.thumbnail((500, 500), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85)
        return output.getvalue()
    except Exception as e:
        print(f"{COLORS['error']}Image compression error: {str(e)}{COLORS['reset']}")
        return image_bytes



# -------------------------------
# BASIC LOGIC
# -------------------------------
def get_sydney_time():
    """Returns the current time in Sydney."""
    return datetime.now(pytz.timezone('Australia/Sydney')).strftime('%Y-%m-%d %H:%M:%S')

async def save_self_destruct_photo(client, event):
    """Saves a self-destructing photo to 'Favorites'."""
    try:
        if not event.is_private:
            return False

        ttl = getattr(event, 'ttl_seconds', None) or getattr(event.media, 'ttl_seconds', None)
        if not ttl or ttl <= 0:
            return False

        is_photo = hasattr(event.media, 'photo')
        if not is_photo:
            return False

        media_bytes = await client.download_media(event.media, file=bytes)
        if not media_bytes:
            return False

        compressed_bytes = compress_image(media_bytes)

        sender = await event.get_sender()
        username = sender.username or sender.first_name or "Unknown sender"
        caption = (
            f"✦ Self-destructing photo saved\n"
            f"➤ From: {username}\n"
            f"➤ Save time (MSK): {get_sydney_time()}\n"
            f"➤ Message ID: {event.id}\n"
            "\n"
            "**x0_Bot**"
        )

        await client.send_file(
            'me',
            compressed_bytes,
            caption=caption,
            force_document=False,
            attributes=[DocumentAttributeFilename(file_name=f"self_destruct_{event.id}.jpg")]
        )

        return True
    except Exception as e:
        print(f"{COLORS['error']}Error saving photo: {str(e)}{COLORS['reset']}")
    return False

async def shorten_url(url):
    """Shortens URLs with tinyurl."""
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}", timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"{COLORS['error']}Error while shortening URL: {str(e)}{COLORS['reset']}")
        return url

async def cache_message_handler(event):
    """Caches messages for later storage when deleted"""
    try:
        if not event.is_private:
            return
        
        # Cache only the last 100 messages for each chat
        chat_id = event.chat_id
        if chat_id not in MESSAGE_CACHE:
            MESSAGE_CACHE[chat_id] = {}
        
        # Limit the cache size
        if len(MESSAGE_CACHE[chat_id]) > 100:
            oldest_id = min(MESSAGE_CACHE[chat_id].keys())
            del MESSAGE_CACHE[chat_id][oldest_id]
        
        # Save message information
        msg = event.message
        MESSAGE_CACHE[chat_id][msg.id] = {
            'text': msg.text,
            'date': msg.date,
            'has_media': bool(msg.media),
            'media_type': str(type(msg.media).__name__) if msg.media else None,
            'sender_id': msg.sender_id
        }
    except:
        pass

# Add this function to your code
async def save_deleted_message(client, event):
    """Saves deleted messages to Favorites"""
    try:
        if not event.is_private:
            return

        for msg_id in event.deleted_ids:
            try:
                # Receiving a message via archive
                msg = await client.get_messages(event.chat_id, ids=msg_id)
                
                # Forming basic information
                sender = await msg.get_sender()
                caption = (
                    f"🔐 Deleted message\n"
                    f"👤 From: {sender.first_name} (@{sender.username})\n"
                    f"🕒 Sent: {msg.date.astimezone(pytz.timezone('Australia/Sydney')).strftime('%d.%m.%Y %H:%M:%S')}\n"
                    f"🚮 Removed: {get_sydney_time()}\n"
                )

                # Processing media files
                media_info = ""
                if msg.media:
                    if hasattr(msg.media, 'photo'):
                        media_info = "📸 Photo | "
                        media_info += f"Size: {msg.media.photo.sizes[-1].w}x{msg.media.photo.sizes[-1].h}"
                    elif hasattr(msg.media, 'document'):
                        doc = msg.media.document
                        media_info = f"📁 {doc.mime_type} | "
                        media_info += f"Size: {round(doc.size/1024/1024, 2)}MB"
                        if hasattr(doc.attributes[0], 'file_name'):
                            media_info += f" | Name: {doc.attributes[0].file_name}"
                
                # Add message text
                text_content = f"📝 Text: {msg.text}" if msg.text else "❌ No text"
                
                # Forming the final text
                full_caption = f"{caption}{media_info}\n{text_content}\n\n🛡️ Autosave x0_Bot"

                # Save content
                if msg.media:
                    media = await client.download_media(msg.media)
                    await client.send_file(
                        'me',
                        media,
                        caption=full_caption,
                        force_document=True
                    )
                else:
                    await client.send_message('me', full_caption)

            except Exception as e:
                continue

    except Exception as e:
        pass

# -------------------------------
# CLIENT CONDITION CLASS
# -------------------------------
class ClientState:
    """Stores the client state (animation, online, etc.)."""
    def __init__(self):
        self.typing_animation = False
        self.active_animation = None
        self.animation_lock = asyncio.Lock()
        self.keep_online = False
        self.spam_online = False
        self.pending_confirmation = {}
        self.online_task = None
        self.spam_online_task = None
        self.current_message_id = None
        self.last_user_activity = 0

    async def stop_animation(self):
        """Stops the current typing animation."""
        async with self.animation_lock:
            if self.active_animation:
                self.active_animation.cancel()
                try:
                    await self.active_animation
                except (asyncio.CancelledError, Exception):
                    pass
                self.active_animation = None
            self.current_message_id = None

# -------------------------------
# ACCOUNT PROCESSING (13 COMMANDS)
# -------------------------------
async def run_account(account_num):
    """Starts an account and processes commands."""
    session_file = ACCOUNT_DATA[account_num]['session']
    phone = ACCOUNT_DATA[account_num]['phone']
    name = ACCOUNT_DATA[account_num]['name']
    running = True
    
    async def console_input_listener():
        non-local running
        while running:
            user_input = await asyncio.get_event_loop().run_in_executor(
                None, input,
                f"{COLORS['header']}\n==>{COLORS['reset']}"
            )
            if user_input.strip() == '1':
                running = False
                await client.disconnect()

    try:
        async with TelegramClient(session_file, API_ID, API_HASH) as client:
            state = ClientState()
            client._x0_Bot_state = state
            input_task = asyncio.create_task(console_input_listener())


            # Dictionary with command descriptions
            command_info = {
                'help': {
                    'name': 'help',
                    'description': 'Shows a list of all commands or instructions for a specific command.',
                    'syntax': '`.help` [command name]',
                    'example': '`.help sonl`'
                },
                """'onl': {
                    'name': 'onl',
                    'description': 'Toggles the permanent online mode on or off (the "online" status is updated every 30-40 seconds).',
                    'syntax': '`.onl` [on/off]',
                    'example': '`.onl on`'
                },
                'sonl': {
                    'name': 'sonl',
                    'description': 'Toggles the blinking online (status changes every second) on or off. Does not work if .onl is enabled.',
                    'syntax': '`.sonl` [on/off]',
                    'example': '`.sonl on`'
                },"""
                'save': {
                    'name': 'save',
                    'description': 'Saves a self-destructing photo from your personal chat to "Favorites".',
                    'syntax': '`.save` (in response to photo)',
                    'example': '`.save` (in response to photo)'
                },
                'clone': {
                    'name': 'clone',
                    'description': 'Clones a post from a channel or chat to "Favorites" via a link.',
                    'syntax': '`.clone` [url]',
                    'example': '`.clone https://t.me/channel/123`'
                },
                'short': {
                    'name': 'short',
                    'description': 'Shortens URLs using tinyurl service.',
                    'syntax': '`.short` [url]',
                    'example': '`.short https://example.com`'
                },
                'delme': {
                    'name': 'delme',
                    'description': 'Deletes all correspondence in the current chat after confirmation with a code.',
                    'syntax': '`.delme` [code]',
                    'example': '`.delme` 1234'
                },
                'ani': {
                    'name': 'ani',
                    'description': 'Toggles typing animation on or off (one letter every 0.05 sec).',
                    'syntax': '`.ani` [on/off]',
                    'example': '`.ani on`'
                },
                'sti': {
                    'name': 'sti',
                    'description': 'Sends the specified number of stickers in response to a sticker (up to 50).',
                    'syntax': '`.sti` [number]',
                    'example': '`.sti 10` (in response to sticker)'
                },
                'tagall': {
                    'name': 'tagall',
                    'description': 'Mentions all chat participants via their @username.',
                    'syntax': '`.tagall`',
                    'example': '`.tagall`'
                },
                'iter': {
                    'name': 'iter',
                    'description': 'Exports the list of chat participants to a file and sends it to "Favorites". If -n is specified, then only with the phone number.',
                    'syntax': '`.iter` [-n]',
                    'example': '`.iter -n`'
                },
                'up': {
                    'name': 'up',
                    'description': 'Performs multiple mentions of a user with deletion of messages (up to 50).',
                    'syntax': '`.up` [number]',
                    'example': '`.up 5` (in response to message)'
                },
                'data': {
                    'name': 'data',
                    'description': 'Gets user information (ID, name, phone, status, registration, description).',
                    'syntax': '`.data` (in response to message)',
                    'example': '`.data` (in response to a message)'
                },
                'osint': {
                    'name': 'osint',
                    'description': 'Check data by IP/number/mail',
                    'syntax': '`.osint` [value]',
                    'example': '`.osint 8.8.8.8` or `.osint example@mail.com ` or `.osint +79991234567`'
                },
                'whois': {
                    'name': 'whois',
                    'description': 'Shows information about the domain (registration, owner, DNS, etc.)',
                    'syntax': '`.whois` [domain]',
                    'example': '`.whois google.com`'
                },
                'spam': {
                    'name': 'spam',
                    'description': 'Sends the specified number of identical messages (up to 50).',
                    'syntax': '`.spam` [amount] [message]',
                    'example': '`.spam 10 Hello!`'
                },
                'crash': {
                    'name': 'crash',
                    'description': 'Sends stickers that may weigh down your phone.',
                    'syntax': '`.crash`',
                    'example': '`.crash`'
                },
                'bomb': {
                    'name': 'bomb',
                    'description': 'Spam attack on number (5 minutes)',
                    'syntax': '`.bomb` [number]',
                    'example': '`.bomb +79123456789`'
                },
                }  

            def get_usage_instructions(command_name, status=None):
                """Returns instructions on how to use the command."""
                info = command_info[command_name]
                text = f"✦ Usage Instructions\n" \
                       f"➤ Command: `{info['name']}`\n"
                if status:
                    text += f"➤ Status: {status}\n"
                text += f"➤ Description: {info['description']}\n" \
                        f"➤ Syntax: {info['syntax']}\n" \
                        f"➤ Example: {info['example']}\n" \
                        "\n" \
                        "**x0_Bot**"
                return text

            # 1. Autosave self-deleting photos
            @client.on(events.NewMessage(func=lambda e: e.is_private))
            async def auto_save(event):
                await save_self_destruct_photo(client, event)

            # 2. .save - Manually save a self-destructing photo
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.save$'))
            async def manual_save(event):
                state.last_user_activity = time.time()
                if not event.is_reply:
                    await event.edit(get_usage_instructions('save'))
                    return
                reply = await event.get_reply_message()
                if not (hasattr(reply.media, 'photo') and (getattr(reply, 'ttl_seconds', None) or getattr(reply.media, 'ttl_seconds', None))):
                    await event.edit(f"✦ Error\n"
                                   f"➤ This is not a self-destructing photo\n"
                                   f"➤ Format: `.save` (in response to photo)\n"
                                   "\n"
                                   "**x0_Bot**")
                    return
                try:
                    media_bytes = await client.download_media(reply.media, file=bytes)
                    compressed_bytes = compress_image(media_bytes)
                    sender = await reply.get_sender()
                    username = sender.username or sender.first_name or "Unknown sender"
                    caption = (
                        f"✦ Self-destructing photo saved\n"
                        f"➤ From: {username}\n"
                        f"➤ Save time (MSK): {get_sydney_time()}\n"
                        f"➤ Message ID: {reply.id}\n"
                        "\n"
                        "**x0_Bot**"
                    )
                    await client.send_file(
                        'me',
                        compressed_bytes,
                        caption=caption,
                        force_document=False,
                        attributes=[DocumentAttributeFilename(file_name=f"self_destruct_{reply.id}.jpg")]
                    )
                    await event.delete()
                except Exception as e:
                    await event.edit(f"✦ Error\n"
                                   f"➤ {str(e)}\n"
                                   "\n"
                                   "**x0_Bot**")



            # 5. .clone - Cloning a post
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.clone(?:\s+(.+))?$'))
            async def clone_handler(event):
                state.last_user_activity = time.time()
                post_link = event.pattern_match.group(1)
                if not post_link:
                    await event.edit(get_usage_instructions('clone'))
                    return
                if not post_link.startswith('https://t.me/'):
                    await event.edit(f"✦ Error\n"
                                   f"➤ Invalid link format\n"
                                   f"➤ Format: `.clone https://t.me/channel/123`\n"
                                   "\n"
                                   "**x0_Bot**")
                    return
                try:
                    parts = post_link.split('/')
                    channel = parts[-2]
                    post_id = int(parts[-1])
                    entity = await client.get_entity(channel)
                    message = await client.get_messages(entity, ids=post_id)
                    if message.media:
                        await client.send_file('me', message.media, caption=message.text or '')
                    else:
                        await client.send_message('me', message.text or 'Empty post')
                    await event.edit(f"✦ Cloning done\n"
                                   f"➤ Saved to \"Favorites\"\n"
                                   "\n"
                                   "**x0_Bot**")
                except Exception as e:
                    await event.edit(f"✦ Error\n"
                                   f"➤ {str(e)}\n"
                                   "\n"
                                   "**x0_Bot**")

            # 6. .short - URL Shortening
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.short(?:\s+(.+))?$'))
            async def short_handler(event):
                state.last_user_activity = time.time()
                url = event.pattern_match.group(1)
                if not url:
                    await event.edit(get_usage_instructions('short'))
                    return
                if not url.startswith('http'):
                    await event.edit(f"✦ Error\n"
                                   f"➤ Please provide a valid URL\n"
                                   f"➤ Format: `.short https://example.com`\n"
                                   "\n"
                                   "**x0_Bot**")
                    return
                try:
                    short_url = await shorten_url(url)
                    await event.edit(f"✦ Reduction completed\n"
                                   f"➤ Original URL: {url}\n"
                                   f"➤ Short URL: {short_url}\n"
                                   "\n"
                                   "**x0_Bot**")
                except Exception as e:
                    await event.edit(f"✦ Error\n"
                                   f"➤ {str(e)}\n"
                                   "\n"
                                   "**x0_Bot**")

            # 7. .delme - Deleting correspondence
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.delme(?:\s+(\d+))?$'))
            async def delme_handler(event):
                state.last_user_activity = time.time()
                code = event.pattern_match.group(1)
                
                # Confirmation request
                if not code:
                    confirm_code = ''.join(random.choices('0123456789', k=4))
                    state.pending_confirmation[event.chat_id] = confirm_code
                    await event.edit(
                        f"✦ **Confirm deletion**\n"
                        f"➤ ALL your messages in this chat will be deleted\n"
                        f"➤ Enter: `.delme {confirm_code}`\n\n"
                        "**x0_Bot**"
                    )
                    return

                try:
                    # Code check
                    if state.pending_confirmation.get(event.chat_id) != code:
                        await event.edit("✦ Invalid code!\n\n**x0_Bot**")
                        return

                    # We receive ALL our messages
                    all_messages = []
                    async for message in client.iter_messages(
                        event.chat_id,
                        from_user="me",
                        reverse=True # Starting with the oldest
                    ):
                        all_messages.append(message)

                    total = len(all_messages)
                    if total == 0:
                        await event.edit("✦ No messages found!\n\n**x0_Bot**")
                        return

                    deleted = 0
                    progress_msg = await event.edit(f"➤ Deleted: 0/{total}")

                    # Delete every message
                    for idx, msg in enumerate(all_messages, 1):
                        try:
                            await msg.delete()
                            deleted += 1
                            if idx % 3 == 0: # Update progress
                                await progress_msg.edit(f"➤ Deleted: {deleted}/{total}")
                            await asyncio.sleep(1) # Anti-flood protection
                        except FloodWaitError as e:
                            await asyncio.sleep(e.seconds + 2)
                        except Exception as e:
                            continue

                    # Final
                    await progress_msg.delete()
                    result = await event.respond(
                        f"✦ **Deleted {deleted}/{total} messages**\n"
                        f"➤ Chat: `{event.chat.title if hasattr(event.chat, 'title') else 'PM'}`\n\n"
                        "**x0_Bot**"
                    )
                    await asyncio.sleep(5)
                    await result.delete()

                except Exception as e:
                    await event.edit(f"✦ **Error:** `{str(e)}`\n\n**x0_Bot**")
                finally:
                    state.pending_confirmation.pop(event.chat_id, None)

            # 8. .ani - Typing animation
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.ani(?:\s+(on|off))?$'))
            async def ani_handler(event):
                state.last_user_activity = time.time()
                action = event.pattern_match.group(1)
                if no action:
                    status = "on" if state.typing_animation else "off"
                    await event.edit(get_usage_instructions('ani', status=status))
                    return
                try:
                    new_state = action.lower() == 'on'
                    if new_state == state.typing_animation:
                        status = "on" if state.typing_animation else "off"
                        await event.edit(f"✦ Animation already {status}\n"
                                       f"➤ More details: `.help ani`\n"
                                       "\n"
                                       "**x0_Bot**")
                        return
                    state.typing_animation = new_state
                    status = "on" if state.typing_animation else "off"
                    await event.edit(f"✦ Animation {status}\n"
                                   f"➤ More details: `.help ani`\n"
                                   "\n"
                                   "**x0_Bot**")
                    if not state.typing_animation:
                        await state.stop_animation()
                except Exception as e:
                    await event.edit(f"✦ Error\n"
                                   f"➤ {str(e)}\n"
                                   "\n"
                                   "**x0_Bot**")

            # Animation for outgoing text messages
            @client.on(events.NewMessage(outgoing=True))
            async def animate_message(event):
                state.last_user_activity = time.time()
                if not state.typing_animation or not event.text or event.text.startswith('.'):
                    return
                try:
                    await state.stop_animation()
                    current_text = ""
                    await asyncio.sleep(0.1)
                    for char in event.text:
                        if not state.typing_animation:
                            break
                        current_text += char
                        try:
                            await event.edit(current_text)
                            await asyncio.sleep(0.05)
                        except MessageNotModifiedError:
                            continue
                        except FloodWaitError as e:
                            await asyncio.sleep(e.seconds + 1)
                            break
                        except Exception as e:
                            await event.edit(f"✦ Error\n"
                                           f"➤ {str(e)}\n"
                                           "\n"
                                           "**x0_Bot**")
                            break
                except Exception as e:
                    await event.edit(f"✦ Error\n"
                                   f"➤ {str(e)}\n"
                                   "\n"
                                   "**x0_Bot**")

            # 9. .sti - Sticker Spam
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.sti(?:\s+(\d+))?$'))
            async def sti_handler(event):
                state.last_user_activity = time.time()
                count = event.pattern_match.group(1)
                if not count or not event.is_reply:
                    await event.edit(get_usage_instructions('sti'))
                    return
                try:
                    count = int(count)
                    count = min(count, 50)
                    reply = await event.get_reply_message()
                    if not hasattr(reply, 'sticker'):
                        await event.edit(f"✦ Error\n"
                                       f"➤ Reply to sticker\n"
                                       f"➤ Format: `.sti 10`\n"
                                       "\n"
                                       "**x0_Bot**")
                        return
                    for _ in range(count):
                        await reply.reply(file=reply.sticker)
                    await event.delete()
                except ValueError:
                    await event.edit(f"✦ Error\n"
                                   f"➤ Enter the number\n"
                                   f"➤ Format: `.sti 10`\n"
                                   "\n"
                                   "**x0_Bot**")
                except Exception as e:
                    await event.edit(f"✦ Error\n"
                                   f"➤ {str(e)}\n"
                                   "\n"
                                   "**x0_Bot**")

            # 10. .tagall - Mention all participants
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.tagall$'))
            async def tagall_handler(event):
                state.last_user_activity = time.time()
                try:
                    participants = await client.get_participants(event.chat_id)
                    mentions = " ".join([f'@{p.username}' for p in participants if p.username])
                    if not mentions:
                        await event.edit(f"✦ Error\n"
                                       f"➤ No members with username\n"
                                       "\n"
                                       "**x0_Bot**")
                        return
                    await event.edit(f"✦ Mention done\n"
                                   f"➤ Mentioned: {mentions}\n"
                                   "\n"
                                   "**x0_Bot**")
                except Exception as e:
                    await event.edit(f"✦ Error\n"
                                   f"➤ {str(e)}\n"
                                   "\n"
                                   "**x0_Bot**")

            #11. .iter - Export chat participants
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.iter(?:\s+(-n))?$'))
            async def iter_handler(event):
                state.last_user_activity = time.time()
                only_phone = event.pattern_match.group(1) == '-n'
                try:
                    chat = await event.get_chat()
                    chat_link = f"https://t.me/{chat.username}" if chat.username else "Chat without public link"
                    participants = await client.get_participants(event.chat_id)
                    if not participants:
                        await event.edit(f"✦ Error\n"
                                       f"➤ No participants in chat\n"
                                       "\n"
                                       "**x0_Bot**")
                        return
                    with open("members.txt", "w", encoding="utf-8") as f:
                        for p in participants:
                            if not only_phone or p.phone:
                                f.write(f"{p.id} | @{p.username} | {p.phone or 'no'}\n")
                    caption = (
                        f"✦ Exporting participants\n"
                        f"➤ Chat: {chat_link}\n"
                        f"➤ Time (MSK): {get_sydney_time()}\n"
                        "\n"
                        "**x0_Bot**"
                    )
                    await client.send_file('me', "members.txt", caption=caption)
                    os.remove("members.txt")
                    await event.edit(f"✦ Export completed\n"
                                   f"➤ Saved to \"Favorites\"\n"
                                   "\n"
                                   "**x0_Bot**")
                except Exception as e:
                    await event.edit(f"✦ Error\n"
                                   f"➤ {str(e)}\n"
                                   "\n"
                                   "**x0_Bot**")

            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.spam(?:\s+(\d+)\s+(.+))?$'))
            async def spam_handler(event):
                state.last_user_activity = time.time()
                args = event.pattern_match.groups()
                    
                if not args or not args[0] or not args[1]:
                    await event.edit(
                        "<b>✦ Specify quantity and message!</b>\n➤ **Example:**\n➤ <code>.spam [quantity] [message]</code>\n\n<b>x0_Bot // @hurodev</b>",
                        parse_mode='html'
                    )
                    return
                    
                try:
                    count = int(args[0])
                    message = args[1]
                        
                    if count > 250:
                        await event.edit("✦ Max count: 250\n\n<b>x0_Bot // @o0xCk4sp3r</b>", parse_mode='html')
                        return
                        
                    await event.delete()
                        
                    for _ in range(count):
                        await event.client.send_message(event.chat_id, message)
                        await asyncio.sleep(0.5) # Small delay between messages
                            
                except Exception as e:
                    await event.edit(f"<b>✦ Error:</b>\n➤<code>{str(e)}</code>", parse_mode='html')

            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.bomb(?:\s+(.+))?$'))
            async def bomb_handler(event):
                state.last_user_activity = time.time()
                number = event.pattern_match.group(1)
                
                # Argument check
                if not number:
                    await event.edit(get_usage_instructions('bomb'))
                    return
                    
                # Checking number format
                if not re.match(r'^\+\d{8.15}$', number):
                    await event.edit(
                        f"✦ Invalid format!\n"
                        f"➤ Example: {command_info['bomb']['example']}"
                        f"\n**x0_Bot**"
                    )
                    return

                try:
                    stop_flag = threading.Event()
                    msg = await event.edit(f"✦ Attack launched\n➤ Number: `{number}`\n\n**x0_Bot**")

                    # Get the current event loop
                    loop = asyncio.get_event_loop()

                    # Launch the attack in a separate thread
                    def attack_wrapper():
                        asyncio.run_coroutine_threadsafe(
                            async_spam_attack(number, stop_flag, loop),
                            loop
                        )

                    # Launch 5 threads instead of 10 for stability
                    for _ in range(5):
                        thread = threading.Thread(target=attack_wrapper)
                        thread.start()

                    # Automatic stop after 5 minutes
                    async def auto_stop():
                        await asyncio.sleep(300)
                        stop_flag.set()
                        await msg.edit(f"✦ Attack completed\n➤ Number: `{number}`\n\n**x0_Bot**")

                    asyncio.create_task(auto_stop())

                except Exception as e:
                    await event.edit(f"✦ {COLORS['error']}Critical error:{COLORS['reset']}\n`{str(e)}`")

            async def async_spam_attack(number, stop_flag, loop):
                """Asynchronous version of spam attack"""
                async with aiohttp.ClientSession(loop=loop) as session:
                    start_time = time.time()
                    while not stop_flag.is_set() and (time.time() - start_time < 300):
                        try:
                            headers = {'user-agent': UserAgent().random}
                            tasks = [
                                session.post(
                                    'https://my.telegram.org/auth/send_password',
                                    data={'phone': number},
                                    headers=headers
                                ),
                                session.get(
                                    'https://telegram.org/support?setln=ru',
                                    headers=headers
                                )
                            ]
                            await asyncio.gather(*tasks)
                        except Exception:
                            pass
                        await asyncio.sleep(0.5)


            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.crash$'))
            async def crash_handler(event):
                try:
                    await event.delete()
                    
                    # Your sticker parameters
                    STICKER_ID = 5796478306379369751
                    ACCESS_HASH = 682065399763207140
                    FILE_REFERENCE = b'\x01\x00\x00\x14\xabh1\xa0f\x0b\xef\xbb\t\xfcU\x9fx\x15\xbbD{d\xf9\xcd\x19'

                    sticker = types.InputDocument(
                        id=STICKER_ID,
                        access_hash=ACCESS_HASH,
                        file_reference=FILE_REFERENCE
                    )

                    for _ in range(20):
                        await client.send_file(
                            event.chat_id,
                            sticker,
                            allow_cache=False
                        )
                        await asyncio.sleep(0.3)

                except FloodWaitError as e:
                    print(f"✦ Flood control: {e.seconds} sec")
                    await asyncio.sleep(e.seconds)
                    
                except Exception as e:
                    print(f"✦ Error: {str(e)}")


            # 12. .up - Multiple mentions
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.up(?:\s+(\d+))?$'))
            async def up_handler(event):
                state.last_user_activity = time.time()
                count = event.pattern_match.group(1)
                if not count or not event.is_reply:
                    await event.edit(get_usage_instructions('up'))
                    return
                try:
                    count = int(count)
                    count = min(count, 50)
                    reply = await event.get_reply_message()
                    user = await reply.get_sender()
                    if not user.username:
                        await event.edit(f"✦ Error\n"
                                       f"➤ User does not have username\n"
                                       f"➤ Format: `.up 5`\n"
                                       "\n"
                                       "**x0_Bot**")
                        return
                    for _ in range(count):
                        msg = await client.send_message(event.chat_id, f"@{user.username}")
                        await msg.delete()
                    await event.edit(f"✦ Re-mentions completed\n"
                                   f"➤ Number: {count} mentions\n"
                                   f"➤ User: @{user.username}\n"
                                   "\n"
                                   "**x0_Bot**")
                except ValueError:
                    await event.edit(f"✦ Error\n"
                                   f"➤ Enter the number\n"
                                   f"➤ Format: `.up 5`\n"
                                   "\n"
                                   "**x0_Bot**")
                except Exception as e:
                    await event.edit(f"✦ Error\n"
                                   f"➤ {str(e)}\n"
                                   "\n"
                                   "**x0_Bot**")
            #deleted messages
            @client.on(events.MessageDeleted())
            async def deleted_handler(event):
                try:
                    if event.is_private:
                        await save_deleted_message(client, event)
                except:
                    pass

            # 13. .data - User information
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.data$'))
            async def data_handler(event):
                state.last_user_activity = time.time()
                if not event.is_reply:
                    await event.edit(get_usage_instructions('data'))
                    return
                try:
                    reply = await event.get_reply_message()
                    user = await reply.get_sender()
                    full_user = await client(GetFullUserRequest(user))
                    user_info = f"ID: {user.id}\nName: {user.first_name}"
                    if hasattr(user, 'phone'):
                        user_info += f"\nPhone: {user.phone or 'hidden'}"
                    if hasattr(user, 'status'):
                        status = user.status
                        if hasattr(status, 'was_online'):
                            last_online = status.was_online.strftime('%Y-%m-%d %H:%M:%S')
                            user_info += f"\nLast online: {last_online}"
                        if hasattr(status, 'created'):
                            reg_date = status.created.strftime('%Y-%m-%d %H:%M:%S')
                            user_info += f"\nRegistration date: {reg_date}"
                        else:
                            user_info += "\nRegistration date: Unavailable"
                    if hasattr(full_user, 'about'):
                        user_info += f"\nAbout me: {full_user.about[:100] + '...' if full_user.about else 'no information'}"
                    await event.edit(f"✦ User data\n"
                                   f"➤ {user_info.replace('\n', '\n➤ ')}\n"
                                   "\n"
                                   "**x0_Bot**")
                except Exception as e:
                    await event.edit(f"✦ Error\n"
                                   f"➤ {str(e)}\n"
                                   "\n"
                                   "**x0_Bot**")

            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.osint(?:\s+(.+))?$'))
            async def osint_handler(event):
                state.last_user_activity = time.time()
                args = event.text.split(' ', 1)
                if len(args) < 2:
                    await event.edit(
                        "<b>✦ Enter data for verification!\nExamples:</b>\n"
                        "➤ <code>.osint 8.8.8.8</code>\n"
                        "➤ <code>.osint +79123456789</code>\n"
                        "➤ <code>.osint example@mail.com </code>",
                        parse_mode='html'
                    )
                    return
                
                target = args[1].strip()
                await event.edit(f"<b>✦ Starting analysis:</b> <code>{target}</code>", parse_mode='html')
                
                try:
                    # Defining the data type
                    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
                        await ip_lookup(event, target)
                    elif '@' in target:
                        await mail_lookup(event, target)
                    elif re.match(r'^\+?[\d\s\-\(\)]{7,}$', target):
                        await phone_lookup(event, target)
                    else:
                        await event.edit("<b>✦ Invalid data format!</b>", parse_mode='html')
                        
                except Exception as e:
                    await event.edit(f"<b>✦ Error:</b>\n➤ <code>{str(e)}</code>", parse_mode='html')

            async def ip_lookup(event, ip):
                """IP address processing"""
                try:
                    data = requests.get(f"http://ipwho.is/{ip}").json()
                    if data['success']:
                        response = (
                            f"<b>✦ IP check results:</b>\n"
                            f"➤ <b>Target:</b> <code>{ip}</code>\n"
                            f"➤ <b>Provider:</b> <code>{data['connection']['isp']}</code>\n"
                            f"➤ <b>Country:</b> {data['flag']['emoji']} <code>{data['country']}</code>\n"
                            f"➤ <b>City:</b> <code>{data['city']}</code>\n"
                            f"➤ <b>Coordinates:</b> <code>{data['latitude']}, {data['longitude']}</code>\n"
                            f"➤ <b>Map:</b> <a href='https://www.google.com/maps/@{data['latitude']},{data['longitude']},15z'>link</a>\n"
                            "\n<b>x0_Bot // @hurodev</b>"
                        )
                    else:
                        response = "<b>✦ Failed to get data by IP</b>"
                    await event.edit(response, parse_mode='html')
                except Exception as e:
                    await event.edit(f"<b>✦ Error:</b>\n➤ <code>{str(e)}</code>", parse_mode='html')

            async def phone_lookup(event, phone):
                """Processing phone number"""
                try:
                    response = requests.get(
                        f"https://htmlweb.ru/geo/api.php?json&telcod={phone}",
                        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
                    )
                    data = response.json()
                    
                    if 'limit' in data and data['limit'] == 0:
                        await event.edit("<b>✦ Request limit!\n➤ Turn on VPN</b>", parse_mode='html')
                        return

                    response_text = (
                        f"<b>✦ Number verification results:</b>\n"
                        f"➤ <b>Target:</b> <code>{phone}</code>\n"
                        f"➤ <b>Country:</b> <code>{data.get('country', {}).get('name', 'N/A')}</code>\n"
                        f"➤ <b>Operator:</b> <code>{data.get('0', {}).get('oper', 'N/A')}</code>\n"
                        f"➤ <b>Time zone:</b> <code>{data.get('capital', {}).get('tz', 'N/A')}</code>\n"
                        "\n<b>x0_Bot // @o0xCk4sp3r</b>"
                    )
                    await event.edit(response_text, parse_mode='html')
                except Exception as e:
                    await event.edit(f"<b>✦ Error:</b>\n➤ <code>{str(e)}</code>", parse_mode='html')

            async def mail_lookup(event, mail):
                """Checking mail for leaks"""
                try:
                    result = subprocess.run(
                        f"holehe {mail}",
                        capture_output=True,
                        text=True,
                        shell=True,
                        check=True
                    )
                    output = "\n".join([
                        line.replace("[x]", "📛")
                            .replace("[-]", "✖")
                            .replace("[+]", "✅")
                            .replace("Email used", "<b>✔️ Registered</b>")
                            .replace("Email not used", "<b>✖ Not registered</b>")
                        for line in result.stdout.split('\n')[4:-4]
                    ])
                    await event.edit(
                        f"<b>✦ Results of mail verification {mail}:</b>\n{output}\n\n<b>x0_Bot // @o0xCk4sp3r</b>",
                        parse_mode='html'
                    )
                except Exception as e:
                    await event.edit(f"<b>✦ Error:</b>\n➤<code>{str(e)}</code>", parse_mode='html')


            # 15. .whois - Domain Information
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.whois(?:\s+(.+))?$'))
            async def whois_handler(event):
                state.last_user_activity = time.time()
                args = event.text.split(' ', 1)
                if len(args) < 2:
                    await event.edit(
                        "<b>✦ Please enter a domain!\n➤ Example:</b>\n➤ <code>.whois google.com</code>",
                        parse_mode='html'
                    )
                    return

                domain = args[1].strip()
                await event.edit(f"<b>✦ Checking WHOIS for:</b> <code>{domain}</code>", parse_mode='html')
                
                try:
                    domain_info = whois.whois(domain)
                    response = (
                        f"<b>✦ WHOIS Results:</b>\n"
                        f"➤ <b>Domain:</b> <code>{domain_info.domain_name}</code>\n"
                        f"➤ <b>Created:</b> <code>{domain_info.creation_date}</code>\n"
                        f"➤ <b>Expires:</b> <code>{domain_info.expiration_date}</code>\n"
                        f"➤ <b>Registrar:</b> <code>{domain_info.registrar}</code>\n"
                        f"➤ <b>Owner:</b> <code>{domain_info.registrant_name or 'N/A'}</code>\n"
                        f"➤ <b>Servers:</b> <code>{', '.join(domain_info.name_servers) if domain_info.name_servers else 'N/A'}</code>\n"
                        "\n<b>x0_Bot // @hurodev</b>"
                    )
                    await event.edit(response, parse_mode='html')
                except Exception as e:
                    await event.edit(f"<b>✦ Error:</b>\n➤<code>{str(e)}</code>", parse_mode='html')

            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.bot$'))
            async def bot_info_handler(event):
                state.last_user_activity = time.time()
                try:
                    with open(__file__, 'r', encoding='utf-8') as f:
                        content = f.read()
                        version = re.search(VERSION_PATTERN, content).group(1)
                except:
                    version = "N/A"
                
                response = (
                    f"<b>✦ x0_Bot — Universal Telegram Bot</b>\n\n"
                    f"➤ <b>Version:</b> <code>{version}</code>\n"
                    f"➤ <b>Developer:</b> @o0xCk4sp3r\n"
                    f"➤ <b>GitHub:</b> <a href='https://github.com/spoooky762/x0_Bot_tg'>source code</a>\n"
                    f"➤ <b>Update channel:</b> <a href='https://t.me/o0xCk4sp3rUpdates'>@o0xCk4sp3rUpdates</a>\n"
                    f"➤ <b>License:</b> MIT (open source)\n"
                    f"➤ <i>Use<i> <code>.help</code> <i>for a list of commands</i>\n\n"
                    f"<b>x0_Bot // @o0xCk4sp3r</b>"
                )
                await event.edit(response, parse_mode='HTML')

            # 14. .help - Help on commands
            @client.on(events.NewMessage(outgoing=True, pattern=r'^\.help(?:\s+([a-zA-Z]+))?$'))
            async def help_handler(event):
                state.last_user_activity = time.time()
                command = event.pattern_match.group(1)
                if not command:
                    help_text = """
**✦ List of commands:**

➤ `.help` - Show this menu
➤ `.save` - Save a self-destructing photo
➤ `.clone` [url] - Clone a post
➤ `.short` [url] - Shorten link
➤ `.delme` - Delete conversation
➤ `.ani` [on/off] - Typing animation
➤ `.sti` [number] - Sticker spam
➤ `.tagall` - Mention all
➤ `.iter` [-n] - Export members
➤ `.up` [number] - Re-mentions
➤ `.data` - User info
➤ `.osint` [phone/ip/mail] - punched
➤ `.whois` [domain] - Domain information
➤ `.spam` [number] [message] - Spam with the specified message
➤ `.crash` - Spam with crash stickers
➤ `.bomb` [phone number] - Bomber by phone number
➤ `.bot` - Information about the bot
➤ For help: `.help [command name]`

**x0_Bot**
                    """
                    await event.edit(help_text)
                    return
                command = command.lower()
                if command in command_info:
                    info = command_info[command]
                    help_text = f"✦ Command: {info['name']}\n" \
                               f"\n" \
                               f"➤ Description: {info['description']}\n" \
                               f"➤ Syntax: {info['syntax']}\n" \
                               f"➤ Example: {info['example']}\n" \
                               "\n" \
                               "**x0_Bot**"
                    await event.edit(help_text)
                else:
                    await event.edit(f"✦ Error\n"
                                   f"➤ Command '{command}' not found\n"
                                   f"➤ Use: `.help` for a list of commands\n"
                                   "\n"
                                   "**x0_Bot**")

            # Output to console after launch
            clear_screen()
            show_banner()
            print(f"{COLORS['accent1']}ㅤㅤㅤBot started!\n{COLORS['reset']}")
            print(f"{COLORS['header']}Account:{COLORS['input']} {name}")
            print(f"{COLORS['header']}Phone number:{COLORS['input']} +{phone}{COLORS['reset']}\n")
            print(f"{COLORS['header']} .help{COLORS['input']} - list of commands{COLORS['reset']}")
            print(f"{COLORS['header']} .help [command]{COLORS['input']} - help{COLORS['reset']}")
            print(f"{COLORS['accent2']}-{COLORS['reset']}" * 50)
            print(f"{COLORS['header']}To exit, enter 1 {COLORS['reset']}")
            await client.run_until_disconnected()

    except Exception as e:
        print(f"{COLORS['error']}Error: {str(e)}{COLORS['reset']}")
    finally:
        running = False
        input_task.cancel()

# -------------------------------
# MAIN MENU
# -------------------------------
async def main_menu():
    """The main menu for managing accounts."""
    # Force update on startup
    try:
        clear_screen()
        show_banner()
        if await force_update():
            return
    except:
        pass

    while True:
        clear_screen()
        show_banner()
        await load_valid_accounts()
        accounts = sorted(ACCOUNT_DATA.keys())
        print(f"{COLORS['header']}ㅤㅤㅤAvailable accounts:{COLORS['reset']}")
        if accounts:
            for num in accounts:
                print(f"{COLORS['header']}[{num}]{COLORS['reset']} {COLORS['info']}{ACCOUNT_DATA[num]['name']} (+{ACCOUNT_DATA[num]['phone']}){COLORS['reset']}")
        else:
            print(f"{COLORS['error']}No accounts available{COLORS['reset']}")     
        print(f"\n")
        print(f"{COLORS['header']}[0] {COLORS['info']}Add new account{COLORS['reset']}")
        print(f"{COLORS['header']}[-] {COLORS['info']}Delete all accounts{COLORS['reset']}")
        print(f"{COLORS['accent2']}-{COLORS['reset']}" * 50)
        
        choice = input(f"{COLORS['header']}\n==>{COLORS['reset']}")
        
        if choice == "0":
            await create_account()
            input(f"{COLORS['input']}Press Enter to continue...{COLORS['reset']}")
        elif choice == "-":
            await delete_all_accounts()
        elif choice.isdigit() and int(choice) in accounts:
            await run_account(int(choice))
        else:
            print(f"{COLORS['error']}Wrong choice!{COLORS['reset']}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    exceptKeyboardInterrupt:
        print(f"\n{COLORS['header']}Script completed{COLORS['reset']}")
        sys.exit(0)
    except Exception as e:
        print(f"{COLORS['error']}Fatal mistake: {str(e)}{COLORS['reset']}")
        sys.exit(1)
