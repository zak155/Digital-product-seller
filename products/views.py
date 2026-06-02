import stripe

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect,render


from .models import Product, Price
stripe.api_key = settings.STRIPE_SECRET_KEY

def product_list(request):
    products = Product.objects.all()

    context = {
        "products": products
    }

    return render(request, "products/product_list.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    prices = Price.objects.filter(product=product)

    context = {
        "product": product,
        "prices": prices,
    }

    return render(request, "products/product_detail.html", context)






def create_stripe_checkout_session(request, pk):
    """
    Create a checkout session and redirect the user to Stripe Checkout
    """

    if request.method != "POST":
        return redirect("products:product_list")

    price = get_object_or_404(Price, id=pk)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(price.price * 100),
                    "product_data": {
                        "name": price.product.name,
                        "description": price.product.desc,
                        "images": [
                            f"{settings.BACKEND_DOMAIN}/{price.product.thumbnail}"
                        ],
                    },
                },
                "quantity": price.product.quantity,
            }
        ],
        metadata={
            "product_id": price.product.id,
        },
        mode="payment",
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_CANCEL_URL,
    )

    return redirect(checkout_session.url)
def success_view(request):
    return render(request, "products/success.html")


def cancel_view(request):
    return render(request, "products/cancel.html")