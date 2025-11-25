import hashlib
import datetime
from telethon import TelegramClient, events
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# إعدادات Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client_gs = gspread.authorize(creds)
sheet = client_gs.open("telegram_jobs_raw").worksheet("raw_jobs")

# إعدادات Telegram
api_id = 35479481
api_hash = "8f12ca035cdad9e39e471b6ae2e2dd25"
telegram_client = TelegramClient("telegram_jobs_raw_session", api_id, api_hash)

# قنوات التليجرام
CHANNELS = [
    "https://t.me/ewdifh",
    "https://t.me/Engineers_Jobs",
    "https://t.me/grobksa",
]

# كاش الهاشات لمنع التكرار
HASH_CACHE = set()

def write_row(row_data):
    try:
        job_text = row_data[2]
        job_hash = hashlib.md5(job_text.encode()).hexdigest()
        if job_hash in HASH_CACHE:
            return
        HASH_CACHE.add(job_hash)
        sheet.append_row(row_data + [job_hash])
        print(f"[ADDED] {row_data}")
    except Exception as e:
        print(f"[ERROR] write_row failed: {e}")

@telegram_client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    try:
        sender = await event.get_sender()
        username = sender.username if sender else "unknown"
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        job_text = event.message.message
        write_row([username, date_str, job_text])
    except Exception as e:
        print(f"[ERROR] handler failed: {e}")

print("[INFO] Starting Telegram client...")
telegram_client.start()
telegram_client.run_until_disconnected()
