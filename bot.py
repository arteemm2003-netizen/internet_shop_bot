# bot.py - интернет магазин с админ панелью
import time  # ДОБАВЬ ЭТУ СТРОКУ В НАЧАЛО ФАЙЛА
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "8006690371:AAEF_2Xr1SqrtI5Q0TGFgtzC8GK3UJikHYk"  # ЗАМЕНИ НА СВОЙ ТОКЕН
ADMIN_ID = 8320186175 # ЗАМЕНИ НА СВОЙ ID

# ================== ТОВАРЫ ==================
products = [
    {
        "id": 1,
        "name": "📱 iPhone 13",
        "price": 79990,
        "description": "Новый iPhone 13 128GB"
    },
    {
        "id": 2, 
        "name": "💻 MacBook Air",
        "price": 99990,
        "description": "MacBook Air M1 256GB"
    },
    {
        "id": 3,
        "name": "🎧 AirPods",
        "price": 15990, 
        "description": "AirPods 3 поколение"
    },
    {
    "id": 4,
    "name": "⌚ Apple Watch",
    "price": 29990,
    "description": "Apple Watch Series 8"
}

]

# ================== КОРЗИНА ==================
user_carts = {}

# ================== СОЗДАЕМ БОТА ==================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ================== КОМАНДА /start ==================
@dp.message(Command("start"))
async def start_command(message: types.Message):
    # Отправляем приветствие
    await message.answer(
        "🛍️ Добро пожаловать в магазин!\n\n"
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/products - посмотреть товары\n" 
        "/cart - корзина\n"
        "/admin - админ панель\n"
        "/myid - узнать свой ID"
    )

# ================== КОМАНДА /products ==================
@dp.message(Command("products"))
async def show_products(message: types.Message):
    # Создаем текст с товарами
    products_text = "🛍️ НАШИ ТОВАРЫ:\n\n"
    
    # Перебираем все товары
    for product in products:
        products_text += f"{product['name']}\n"
        products_text += f"Цена: {product['price']} руб.\n"
        products_text += f"{product['description']}\n"
        products_text += f"Добавить: /add_{product['id']}\n\n"
    
    # Отправляем сообщение
    await message.answer(products_text)

# ================== ДОБАВЛЕНИЕ В КОРЗИНУ ==================
@dp.message(lambda message: message.text and message.text.startswith('/add_'))
async def add_to_cart(message: types.Message):
    # Получаем ID товара из команды /add_1, /add_2 и т.д.
    try:
        product_id = int(message.text.split('_')[1])
    except:
        await message.answer("❌ Ошибка добавления товара!")
        return
    
    # Ищем товар по ID
    product = None
    for p in products:
        if p["id"] == product_id:
            product = p
            break
    
    # Если товар не найден
    if not product:
        await message.answer("❌ Товар не найден!")
        return
    
    # Получаем ID пользователя
    user_id = message.from_user.id
    
    # Создаем корзину если ее нет
    if user_id not in user_carts:
        user_carts[user_id] = {}
    
    # Добавляем товар в корзину
    if product_id in user_carts[user_id]:
        user_carts[user_id][product_id] += 1
    else:
        user_carts[user_id][product_id] = 1
    
    # Сообщаем об успехе
    await message.answer(f"✅ {product['name']} добавлен в корзину!")

# ================== КОМАНДА /cart ==================
@dp.message(Command("cart"))
async def show_cart(message: types.Message):
    user_id = message.from_user.id
    
    # Проверяем есть ли корзина
    if user_id not in user_carts or not user_carts[user_id]:
        await message.answer("🛒 Ваша корзина пуста!")
        return
    
    # Создаем текст корзины
    cart_text = "🛒 ВАША КОРЗИНА:\n\n"
    total_price = 0
    
    # Перебираем товары в корзине
    for product_id, quantity in user_carts[user_id].items():
        # Находим товар
        product = None
        for p in products:
            if p["id"] == product_id:
                product = p
                break
        
        if product:
            item_total = product["price"] * quantity
            total_price += item_total
            cart_text += f"{product['name']}\n"
            cart_text += f"Количество: {quantity} шт.\n"
            cart_text += f"Сумма: {item_total} руб.\n\n"
    
    cart_text += f"💵 ОБЩАЯ СУММА: {total_price} руб."
    
    await message.answer(cart_text)

# ================== АДМИН ПАНЕЛЬ ==================
# ================== КОМАНДА /admin ==================
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    # Проверяем является ли пользователь админом
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У вас нет доступа к админ панели!")
        return
    
    # Показываем админ меню
    admin_text = "👑 АДМИН ПАНЕЛЬ\n\n"
    admin_text += "/admin_products - список товаров\n"
    admin_text += "/admin_stats - статистика магазина\n"
    admin_text += "/admin_users - пользователи с корзинами\n"
    admin_text += "/myid - узнать свой ID"
    
    await message.answer(admin_text)

# ================== АДМИН: СПИСОК ТОВАРОВ ==================
@dp.message(Command("admin_products"))
async def admin_products(message: types.Message):
    # Проверяем админа
    if message.from_user.id != ADMIN_ID:
        return
    
    # Создаем текст со всеми товарами
    products_text = "👑 ВСЕ ТОВАРЫ:\n\n"
    
    for product in products:
        products_text += f"🆔 ID: {product['id']}\n"
        products_text += f"📦 Название: {product['name']}\n"
        products_text += f"💰 Цена: {product['price']} руб.\n"
        products_text += f"📝 Описание: {product['description']}\n"
        products_text += "─" * 20 + "\n"
    
    await message.answer(products_text)

# ================== АДМИН: СТАТИСТИКА ==================
@dp.message(Command("admin_stats"))
async def admin_stats(message: types.Message):
    # Проверяем админа
    if message.from_user.id != ADMIN_ID:
        return
    
    # Считаем статистику
    total_products = len(products)
    total_value = sum(product["price"] for product in products)
    total_users = len(user_carts)
    
    # Создаем текст статистики
    stats_text = "📊 СТАТИСТИКА МАГАЗИНА:\n\n"
    stats_text += f"📈 Всего товаров: {total_products}\n"
    stats_text += f"💰 Общая стоимость: {total_value} руб.\n"
    stats_text += f"👥 Пользователей с корзинами: {total_users}\n"
    stats_text += f"👑 Админ ID: {ADMIN_ID}"
    
    await message.answer(stats_text)

# ================== АДМИН: ПОЛЬЗОВАТЕЛИ ==================
@dp.message(Command("admin_users"))
async def admin_users(message: types.Message):
    # Проверяем админа
    if message.from_user.id != ADMIN_ID:
        return
    
    # Создаем текст с пользователями
    if not user_carts:
        await message.answer("📊 Нет пользователей с корзинами!")
        return
    
    users_text = "👥 ПОЛЬЗОВАТЕЛИ С КОРЗИНАМИ:\n\n"
    
    for user_id, cart in user_carts.items():
        users_text += f"👤 ID: {user_id}\n"
        users_text += f"🛒 Товаров в корзине: {len(cart)}\n"
        
        # Считаем общую сумму корзины
        user_total = 0
        for product_id, quantity in cart.items():
            for product in products:
                if product["id"] == product_id:
                    user_total += product["price"] * quantity
                    break
        
        users_text += f"💰 Сумма корзины: {user_total} руб.\n"
        users_text += "─" * 15 + "\n"
    
    await message.answer(users_text)

# ================== КОМАНДА /myid ==================
@dp.message(Command("myid"))
async def show_my_id(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f"🆔 Ваш ID: {user_id}")


# ================== ЗАПУСК БОТА ==================
async def main():
    print("🟢 Бот запущен!")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    # Бесконечный цикл для автоматического перезапуска
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("🛑 Бот остановлен!")
            break
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            print("♻️ Перезапуск через 10 секунд...")
            time.sleep(10)