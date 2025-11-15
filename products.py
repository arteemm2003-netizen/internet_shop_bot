# products.py - файл с товарами магазин

#список товаров
products = [
    {
        "id": 1,
        "name": "iPhone 13",
        "price": 79990,
        "description": "новый iPhone 13 128GB"
    },
    {
        "id": 2,
        "name": "MacBook Air" ,
        "price": 99990,
        "description": "MacBook Air M1 256GB"
    }
]

# Функция для поиска товара по ID
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return product
    return None