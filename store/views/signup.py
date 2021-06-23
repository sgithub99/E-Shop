from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
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

        error_message = self.validateCustomer(customer)

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

    def validateCustomer(self, customer):
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