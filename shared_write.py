import hashlib
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# إعداد الاتصال بـ Google Sheet
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open("telegram_jobs_data").worksheet("raw_jobs")  # اسم الملف والورقة الجديدة

# كاش لمنع التكرار
HASH_CACHE = set()

# دالة الكتابة
def write_row(row_data):
    try:
        job_text = row_data[2]
        job_hash = hashlib.md5(job_text.encode()).hexdigest()
        if job_hash in HASH_CACHE:
            return
        HASH_CACHE.add(job_hash)
        sheet.append_row(row_data + [job_hash])
    except Exception as e:
        print(f"[ERROR] write_row failed: {e}")
