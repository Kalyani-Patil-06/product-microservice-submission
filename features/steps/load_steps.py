import requests
from behave import given
from http import HTTPStatus

REST_ENDPOINT = "http://127.0.0.1:5000/products"


@given("the following products")
def step_load_products(context):
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "available": row["available"].lower() in ("true", "1", "yes"),
            "category": row["category"],
        }
        response = requests.post(REST_ENDPOINT, json=payload)
        assert response.status_code in (HTTPStatus.CREATED, HTTPStatus.OK), (
            f"Could not load product {payload['name']}: {response.status_code} {response.text}"
        )
