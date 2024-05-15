import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product_name):
    """Создание продукта"""
    stripe_product = stripe.Product.create(name=product_name)
    return stripe_product


def create_stripe_price(amount, product):
    """Создание цены"""
    stripe_price = stripe.Price.create(
            currency="rub",
            unit_amount=amount * 100,
            product_data={"name": product.get("id")},
    )
    return stripe_price


def create_stripe_sessions(price):
    """Создание сессии"""
    stripe_sessions = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return stripe_sessions.get('id'), stripe_sessions.get('url')
