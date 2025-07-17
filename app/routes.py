from flask import Blueprint, request, Response
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
