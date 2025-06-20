from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

BOT_TOKEN = '8165959081:AAGV4GKMBh0aaZ1uUeXsZ42t7hAUZpYYUSA'

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Простые состояния для формы
class UserForm(StatesGroup):
    waiting_name = State()
    waiting_age = State()

# Простая инлайн клавиатура
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Заполнить форму", callback_data="form")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ])
    return keyboard

# Команда /start - ВАЖНО: специфичные хэндлеры должны быть ВЫШЕ общих!
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я бот Флави! 👋\n\n"
        "Выбери что хочешь сделать:",
        reply_markup=get_main_keyboard()
    )

# Команда /help
@dp.message(Command("help"))
async def help_handler(message: Message):
    help_text = """
🔧 Мои команды:
/start - Запустить бота
/help - Показать помощь
/about - Обо мне

📝 Я умею:
• Отвечать на сообщения
• Реагировать на стикеры и фото
• Заполнять простую форму
    """
    await message.answer(help_text)

# Команда /about
@dp.message(Command("about"))
async def about_handler(message: Message):
    await message.answer("Я простой бот Флави! 🤖\nСоздан для изучения aiogram.")

# Обработка кнопки "Помощь"
@dp.callback_query(F.data == "help")
async def help_callback(callback):
    await callback.message.answer(
        "🔧 Мои команды:\n"
        "/start - Запустить бота\n"
        "/help - Показать помощь\n"
        "/about - Обо мне"
    )
    await callback.answer()

# Начало формы
@dp.callback_query(F.data == "form")
async def start_form(callback, state: FSMContext):
    await state.set_state(UserForm.waiting_name)
    await callback.message.answer("Как тебя зовут? 😊")
    await callback.answer()

# Получение имени
@dp.message(UserForm.waiting_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserForm.waiting_age)
    await message.answer(f"Приятно познакомиться, {message.text}! 👋\nСколько тебе лет?")

# Получение возраста и завершение формы
@dp.message(UserForm.waiting_age)
async def get_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        data = await state.get_data()
        await state.clear()
        
        await message.answer(
            f"Отлично! 🎉\n\n"
            f"Твои данные:\n"
            f"Имя: {data['name']}\n"
            f"Возраст: {age} лет\n\n"
            f"Форма заполнена!",
            reply_markup=get_main_keyboard()
        )
    except:
        await message.answer("Пожалуйста, введи возраст цифрами 😅")

# Стикеры - ВАЖНО: специфичные фильтры ВЫШЕ общих
@dp.message(F.sticker)
async def sticker_handler(message: Message):
    await message.answer("Ого! Это стикер! КЛАСС! 😍")

# Фото
@dp.message(F.photo)
async def photo_handler(message: Message):
    await message.answer("Какое красивое фото! 📸✨")

# Общий обработчик - ВАЖНО: должен быть ПОСЛЕДНИМ!
@dp.message()
async def echo_handler(message: Message):
    print(f"Получено сообщение: {message.text}")
    await message.reply(f"Ты написал: {message.text}")

# Корутина
async def main():
    print("Бот запущен, ожидаем апдейты...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())