from datetime import datetime

from flask import Flask, jsonify, request, abort
from sqlalchemy import func

from app import app
from app.models import *
from utils.cache_utils import cached
from config import CACHE_TIMEOUT
from time import time




@app.route('/api/products', methods=["GET"])
@cached(timeout=CACHE_TIMEOUT)
def get_products():
    t_start = time()
    if request.method == "GET":
        products = Product.query.all()
        t_finish = time()
        return jsonify({"result": [{"id": product.id, "name": product.name} for product in products]})

@app.route('/api/products', methods=["POST"])
def add_product():
    data = request.json
    if not data:
        return jsonify({"result": {"error": "No parameters are specified"}})
    print(data)
    try:
        id_category = data['category_id']
        print(id_category)
        product_name = data['product_name']
        print(product_name)
    except KeyError:
        return jsonify({"result": {"error": "Parameter error"}})

    cat = Category.query.get(id_category)
    if not cat:
        return jsonify({"result": {"error": "There is no category with this id"}})

    prod = Product.query.filter_by(name=product_name).first()
    if prod:
        return jsonify({"result": {"error": "Such a product already exists"}})
    else:
        new_product = Product(name=product_name, category=cat)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"result": {"success": "product added"}})

@app.route('/api/products/<int:id>', methods=["PUT"])
def change(id):
    print(id)
    product = Product.query.get(id)
    if not product:
        return jsonify({"result": {"error": "There is no product with this id"}})
    if not request.json:
        return jsonify({"result": {"error": "No parameters are specified"}})

    product_name = request.json.get('product_name')
    category_id = request.json.get('category_id')
    if product_name:
        check_prod = Product.query.filter_by(name=product_name).first()
        if check_prod:
            return jsonify({"result": {"error": "Such a name already exists"}})
        product.name = product_name
    if category_id:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"result": {"error": "There is no category with this id"}})
        product.category_id = category_id

    try:
        db.session.commit()
        return jsonify({"result": {"success": "The product has been updated"}})
    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({"result": {"error": "The name may be repeated or the data type is incorrect."}})

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"result": {"error": "There is no product with this id"}})

    db.session.delete(product)
    db.session.commit()
    return jsonify({"result": {"success": "The product was successfully deleted"}})

@app.route('/api/sales/total', methods=['GET'])
def get_total_sales():
    print(request.args)
    start_date_str = request.args.get('date_from')
    end_date_str = request.args.get('date_to')
    print(start_date_str)

    if not start_date_str or not end_date_str:
        return jsonify({"result": {"error": "date_from and date_to are required"}})

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"result": {"error": "Invalid date format. Use YYYY-MM-DD"}})

    total_sales = db.session.query(func.sum(Sale.quantity)).filter(Sale.date >= start_date, Sale.date <= end_date).scalar()

    if total_sales is None:
        total_sales = 0

    return jsonify({'total_sales': total_sales})

@app.route('/api/sales/top-products', methods=['GET'], endpoint='get_top_products')
@cached(timeout=CACHE_TIMEOUT)
def get_top_products():
    t_start = time()
    start_date_str = request.args.get('date_from')
    end_date_str = request.args.get('date_to')
    limit_str = request.args.get('limit', '10')  # Значение по умолчанию - 10

    if not start_date_str or not end_date_str:
        return jsonify({"result": {"error": "date_from and date_to are required"}})

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        limit = int(limit_str)
    except ValueError:
        return jsonify({"result": {"error": "Invalid date format. Use YYYY-MM-DD"}})

    top_products = (
        db.session.query(Product.name, func.sum(Sale.quantity).label('total_quantity'))
        .join(Sale, Product.id == Sale.product_id)
        .filter(Sale.date >= start_date, Sale.date <= end_date)
        .group_by(Product.name)
        .order_by(func.sum(Sale.quantity).desc())
        .limit(limit)
        .all()
    )
    t_finish = time()
    lead_time = t_finish - t_start

    result = [{'product_name': name, 'total_quantity': quantity} for name, quantity in top_products]

    return jsonify({"lead_time": lead_time,'top_products': result})
