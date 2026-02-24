from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator

from products.models import Product
from products.utils import q_search


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)

    query = request.GET.get('q', None)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)

    if category_slug == "all":
        products = Product.objects.all()
    elif query:
        products = q_search(query)
    else:
        products = get_list_or_404(Product.objects.filter(
            category__slug=category_slug))

    if on_sale:
        products = products.filter(discount__gt=0)

    if order_by and order_by != "default":
        products = products.order_by(order_by)

    paginator = Paginator(products, 3)
    current_page = paginator.page(page)

    context = {
        "products": current_page,
        "category_slug": category_slug,
        }

    return render(request, "products/catalog.html", context)


def product(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    context = {
        "product": product,
    }
    return render(request, "products/product.html", context)
