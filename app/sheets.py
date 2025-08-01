import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API uchun scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Kalit fayl orqali ulanish (asosiy papkada turgan fayl)
credentials = ServiceAccountCredentials.from_json_keyfile_name("innovatebot-credentials.json", scope)

# Avtorizatsiya va sheetga ulanish
client = gspread.authorize(credentials)

# Siz bergan Google Sheet ID
SPREADSHEET_ID = "1i8rF4cqOkS0K3mDzhledJjcqybwgTeu4yvhP2VXjh-Q"

# 1-sheet (gid=0) bilan ishlaymiz
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

def add_user_data(data: dict):
    """Foydalanuvchi ma'lumotlarini sheetga yozish"""
    sheet.append_row([
        data.get("name", ""),
        data.get("school", ""),
        data.get("grade", ""),
        data.get("address", ""),
        data.get("phone", ""),
        str(data.get("telegram_id", ""))
    ])
