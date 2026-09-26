import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession

# --- НАЛАШТУВАННЯ AZGARD SOS + ---
BOT_TOKEN = "8895175280:AAE-V0ka57FNqI5TSAzG6V_PxPJhkDrv8Z8"

# Встав сюди ID, який дізнаєшся за інструкцією нижче:
GROUP_CHAT_ID = -1004461095889  

logging.basicConfig(level=logging.INFO)

session = AiohttpSession(timeout=30)
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

# Кнопка для відправки геолокації
sos_button = KeyboardButton(text="🚨 НАДІСЛАТИ SOS І ЛОКАЦІЮ 🚨", request_location=True)
sos_keyboard = ReplyKeyboardMarkup(
    keyboard=[[sos_button]],
    resize_keyboard=True,
    one_time_keyboard=False
)

# 1. КОМАНДА /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🛡️ Вітаємо в системі AZGARD SOS + !\n\n"
        "Цей бот створено підрозділом Кібербезпеки для захисту бійців та громадян Азгарду."
    )

# 2. КОМАНДА /id (Дізнатися ID чату прямо в Telegram!)
@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    chat_id = message.chat.id
    chat_title = message.chat.title or "Приватний чат"
    text = f"📌 ID цього чату ('{chat_title}'):\n`{chat_id}`"
    await message.answer(text, parse_mode="Markdown")
    print(f"\n[ID ДІЗНАНО] Чат '{chat_title}': {chat_id}\n")

# 3. КОМАНДА /sos
@dp.message(Command("sos"))
async def cmd_sos(message: types.Message):
    await message.answer(
        "🚨 УВАГА! АКТИВОВАНО РЕЖИМ ТРИВОГИ!\n\n"
        "Натисни кнопку нижче, щоб передати свої координати штабу Азгарду!",
        reply_markup=sos_keyboard
    )

# 4. ОБРОБНИК ГЕОЛОКАЦІЇ
@dp.message(F.location)
async def handle_location(message: types.Message):
    user = message.from_user
    username = f"@{user.username}" if user.username else user.full_name
    lat = message.location.latitude
    lon = message.location.longitude

    sos_text = (
        f"🚨 AZGARD SOS + : СИГНАЛ ТРИВОГИ! 🚨\n\n"
        f"👤 Боєць: {username}\n"
        f"📍 Координати: {lat}, {lon}\n"
        f"🗺 Google Maps: https://maps.google.com/?q={lat},{lon}\n\n"
        f"⚔️ Усім бійцям Азгарду: перевірити геопозицію та підготувати підкріплення!"
    )

    try:
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=sos_text)
        await bot.send_location(chat_id=GROUP_CHAT_ID, latitude=lat, longitude=lon)
        await message.answer("✅ Сигнал тривоги та твоя локація успішно передані в штаб!")
        print("✅ УСПІХ: Сигнал SOS доставлено в групу!")
    except Exception as e:
        print(f"❌ ПОМИЛКА ВІДПРАВКИ В ГРУПУ: {e}")
        await message.answer(
            f"❌ Помилка надсилання в штаб: {e}\n\n"
            f"💡 Напиши в групі команду /id, щоб отримати точний ID!"
        )

async def main():
    print("Бот AZGARD SOS + запущений і готовий до чергування...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())