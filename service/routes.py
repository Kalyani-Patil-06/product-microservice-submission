from flask import Blueprint, abort, jsonify, request
from http import HTTPStatus
from service.models import Product

api = Blueprint("products_api", __name__)


@api.route("/products", methods=["GET"])
def list_products():
    query = Product.query
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")
    if name:
        query = query.filter(Product.name.ilike(name))
    if category:
        query = query.filter_by(category=category)
    if available is not None and available != "":
        query = query.filter_by(available=available.lower() in ("true", "1", "yes", "on"))
    return jsonify([p.serialize() for p in query.order_by(Product.id).all()]), HTTPStatus.OK


@api.route("/products/<int:product_id>", methods=["GET"])
def read_product(product_id):
    product = Product.find(product_id)
    if product is None:
        abort(HTTPStatus.NOT_FOUND, description=f"Product with id '{product_id}' was not found.")
    return jsonify(product.serialize()), HTTPStatus.OK


@api.route("/products", methods=["POST"])
def create_product():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), HTTPStatus.BAD_REQUEST
    data = request.get_json(silent=True) or {}
    if not data.get("name"):
        return jsonify({"error": "Product name is required"}), HTTPStatus.BAD_REQUEST
    product = Product(name=data["name"], description=data.get("description", ""),
                      price=data.get("price", 0), available=data.get("available", True),
                      category=data.get("category", "Unknown"))
    product.create()
    return jsonify(product.serialize()), HTTPStatus.CREATED


@api.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), HTTPStatus.BAD_REQUEST
    product = Product.find(product_id)
    if product is None:
        abort(HTTPStatus.NOT_FOUND, description=f"Product with id '{product_id}' was not found.")
    product.deserialize(request.get_json(silent=True) or {})
    product.update()
    return jsonify(product.serialize()), HTTPStatus.OK


@api.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.find(product_id)
    if product is None:
        abort(HTTPStatus.NOT_FOUND, description=f"Product with id '{product_id}' was not found.")
    product.delete()
    return "", HTTPStatus.NO_CONTENT
