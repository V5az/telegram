import hashlib
from telethon import TelegramClient, events
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import asyncio

# ===== إعدادات Telegram =====
api_id = 35479481
api_hash = "8f12ca035cdad9e39e471b6ae2e2dd25"

# اسم الجلسة
client = TelegramClient("telegram_jobs_raw_session", api_id, api_hash)

# القنوات التي سيتم سحب الوظائف منها
CHANNELS = [
    "https://t.me/ewdifh",
    "https://t.me/Engineers_Jobs",
    "https://t.me/grobksa",
]

# ===== إعدادات Google Sheets =====
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("jobautomation-478807-01a5fb3a51f5.json", scope)
client_gs = gspread.authorize(creds)

spreadsheet = client_gs.open("telegram_jobs_raw")
sheet = spreadsheet.worksheet("raw_jobs")

# ====== التجزئة لمنع التكرار ======
def _get_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# ====== الحدث ======
@client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    msg = event.message.message
    msg_hash = _get_hash(msg)

    all_hashes = sheet.col_values(1)
    if msg_hash in all_hashes:
        print("تم تجاهل رسالة مكررة")
        return

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([msg_hash, msg, now])
    print("تمت إضافة وظيفة جديدة")

# ====== التشغيل ======
async def main():
    print("[INFO] Starting Telegram client...")
    await client.start()
    print("[INFO] Telegram client started.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())

