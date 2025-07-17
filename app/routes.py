from flask import Blueprint, request, Response, jsonify
from .models import Product, Category
from .schemas import InfoQueryParams
from .logger import logger

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET'])
def root():
    return Response("Welcome to the Shop Backend API!", mimetype="text/plain")

@bp.route('/info', methods=['GET'])
def info():
    try:
        # Получение параметров запроса
        params = InfoQueryParams(
            name=request.args.get("name"),
            category=request.args.get("category")
        )
    except Exception as e:
        logger.warning(f"Invalid query parameters: {e}")
        return Response("Invalid parameters", status=400)

    # Построение запроса к БД
    query = Product.query

    if params.name:
        query = query.filter(Product.name.ilike(f"%{params.name}%"))

    if params.category:
        query = query.join(Product.categories).filter(Category.name.ilike(f"%{params.category}%"))

    products = query.all()

    # Формирование текстового отчета
    total_products = len(products)
    categories_set = set(cat.name for p in products for cat in p.categories)
    images = [p.image_url for p in products if p.image_url]

    summary = f"""
Данные в базе:
- Всего продуктов: {total_products}
- Категорий: {len(categories_set)}
- Категории: {', '.join(categories_set) if categories_set else 'нет'}
- Изображения: {images[0] if images else 'нет'}
"""

    return Response(summary, mimetype="text/plain")

@bp.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return Response("Product not found", status=404)
    # Пример сериализации (можно расширить)
    data = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "image_url": product.image_url,
        "on_main": product.on_main,
        "categories": [c.name for c in product.categories]
    }
    return jsonify(data)
