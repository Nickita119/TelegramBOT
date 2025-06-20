import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Настройка доступа
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Подключение к таблице по названию
sheet = client.open("CRM_Telegram").sheet1

# Добавить данные
sheet.append_row(["1", "Иван", "+79999999999", "Маникюр", "20.06.2025", "новая"])

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

bot = Bot("YOUR_TOKEN")
dp = Dispatcher()

@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    sheet.append_row(["2", "Пётр", "+78888888888", "Стрижка", "20.06.2025", "новая"])
    await message.answer("Клиент добавлен в таблицу!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
