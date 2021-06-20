from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.category import Category
from .models.customer import Customer


# Create your views here.
def index(request):
    products = None
    categories = Category.get_all_product()
    category_ID = request.GET.get('categori')
    if category_ID:
        products = Product.get_all_product_by_category_id(category_ID)
    else:
        products = Product.get_all_product();
    data = {'products': products, 'categories': categories}
    return render(request, 'index.html', data)


def validateCustomer(customer):
    error_message = None
    if not customer.first_name:
        error_message = "First name is blank"
    elif not customer.last_name:
        error_message = "Last name is blank"
    elif not customer.phone:
        error_message = "Phone is blank"
    elif len(customer.phone) < 10:
        error_message = "Phone number must greater or equal 10 char"
    elif customer.isExist():
        error_message = "Email address already registered"

    return error_message


def registerUser(request):
    postData = request.POST
    first_Name = postData.get('firstName')
    last_Name = postData.get('lastName')
    phone = postData.get('phone')
    email = postData.get('email')
    password = postData.get('password')
    # validation

    value = {
        'first_name': first_Name,
        'last_name': last_Name,
        'phone': phone,
        'email': email
    }
    error_message = None

    customer = Customer(first_name=first_Name, last_name=last_Name, phone=phone, email=email,
                        password=password)

    error_message = validateCustomer(customer)

    if not error_message:
        print(first_Name, last_Name, phone, email, password)
        customer.password = make_password(customer.password)
        customer.register()
        return redirect('homepage')
    else:
        data = {
            'error': error_message,
            'values': value
        }
        return render(request, 'signup.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                return redirect('homepage')
            else:
                error_message = "Password invalid!"
        else:
            error_message = "Email or password invalid !"
        print(customer)
        print(email, password)
        return render(request, 'login.html', {'error': error_message})
