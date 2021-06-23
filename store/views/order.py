from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Product
from store.models.order import Order


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        order = Order.get_order_by_customer(customer)
        print(order)
        return render(request, 'order.html', {'orders': order})


