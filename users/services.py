import stripe
from config.settings import STRIPE_API_KEY
from forex_python.converter import CurrencyRates

stripe.api_key = STRIPE_API_KEY


def create_product_course(course_title):
    """
    Создает товара курс.
    """
    product = stripe.Product.create(
        name=course_title,
    )
    return product


def create_product_lesson(lesson_title):
    """
    Создает товара урок.
    """
    product = stripe.Product.create(
        name=lesson_title,
    )
    return product


def convert_rub_to_dollars(amount):
    """
    Конвертация рубли в доллары.
    """
    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(amount * rate)


def create_stripe_price(amount):
    """
    Создает цену в страйпе.
    """
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Payments"},
    )


def create_stripe_session(prise):
    """
    Создает сессию на оплвту.
    """
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": prise.get("id"),
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://localhost:8000/",  # Страница при успешной оплате
        cancel_url="http://localhost:8000/",  # Страница при отмене оплаты
    )
    return session.get("id"), session.get("URL")
