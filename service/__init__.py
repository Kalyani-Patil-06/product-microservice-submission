from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev-only-change-me",
        SQLALCHEMY_DATABASE_URI="sqlite:///products.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)
    db.init_app(app)

    from service.models import Product
    from service.routes import api
    app.register_blueprint(api)

    @app.get("/")
    def home():
        from flask import render_template
        return render_template("index.html")

    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            Product(name="Hat", description="A red fedora", price=59.95, available=True, category="Cloths").create()
            Product(name="Shoes", description="Running shoes", price=89.50, available=False, category="Cloths").create()
            Product(name="Big Mac", description="A classic burger", price=5.99, available=True, category="Food").create()
            Product(name="Sheets", description="Cotton bed sheets", price=29.99, available=True, category="Housewares").create()
    return app
