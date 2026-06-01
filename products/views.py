from django.shortcuts import render, get_object_or_404

from .models import Product, Price


def product_list_view(request):
    products = Product.objects.all()

    context = {
        "products": products
    }

    return render(request, "products/product_list.html", context)


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    prices = Price.objects.filter(product=product)

    context = {
        "product": product,
        "prices": prices,
    }

    return render(request, "products/product_detail.html", context)