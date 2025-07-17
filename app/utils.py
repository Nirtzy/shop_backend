import requests
from .models import Product, Category
from . import db
from .logger import logger

API_URLS = [
    "https://bot-igor.ru/api/products?on_main=true",
    "https://bot-igor.ru/api/products?on_main=false"
]

def fetch_all_products():
    products = []
    for url in API_URLS:
        try:
            logger.info(f"Fetching data from {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            # Берём только список продуктов из ключа 'products', если он есть
            if isinstance(data, dict) and "products" in data:
                products.extend(data["products"])
            elif isinstance(data, list):
                products.extend(data)
            else:
                logger.warning(f"Unexpected API response format: {data}")
        except Exception as e:
            logger.error(f"Error fetching from {url}: {e}")
    return products

def update_database(products_data):
    for item in products_data:
        product_id = item.get('Product_ID')
        if not product_id:
            logger.warning(f"Product without Product_ID: {item}")
            continue
        product = Product.query.get(product_id)

        if not product:
            product = Product(id=product_id)
            db.session.add(product)

        product.name = item.get('Product_Name')
        # Цена — первый параметр с price, если есть
        price = None
        for param in item.get('parameters', []):
            if 'price' in param and param['price'] is not None:
                price = param['price']
                break
        product.price = price
        # Картинка — первый image с MainImage=True, иначе просто первая
        image_url = None
        images = item.get('images', [])
        for img in images:
            if img.get('MainImage'):
                image_url = img.get('Image_URL')
                break
        if not image_url and images:
            image_url = images[0].get('Image_URL')
        product.image_url = image_url
        product.on_main = item.get('OnMain', False)

        # Обработка категорий
        product.categories.clear()
        for cat in item.get('categories', []):
            cat_name = cat.get('Category_Name')
            if not cat_name:
                continue
            category = Category.query.filter_by(name=cat_name).first()
            if not category:
                category = Category(name=cat_name)
                db.session.add(category)
            if category not in product.categories:
                product.categories.append(category)

    try:
        db.session.commit()
        logger.info("Database successfully updated with fetched products.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database update failed: {e}")
