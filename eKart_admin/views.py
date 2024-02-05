from random import randint
from django.shortcuts import redirect, render
from eKart import settings

from eKart_admin.models import Category, EkartAdmin
from seller.models import Seller
from django.core.mail import send_mail

# Create your views here.
def admin_home(request):
    return render(request,'ekart_admin/admin_home.html')

def view_category(request):
    categories=Category.objects.all()
    return render(request,'ekart_admin/view_category.html', {'categories':categories})

def add_category(request):
    message = ''
    

    if request.method == 'POST':
        category = request.POST['category_name'].lower()
        description = request.POST['description']
        cover_pic = request.FILES['category_image']

        category_exist = Category.objects.filter(category = category).exists()

        if not category_exist:
            category = Category(category = category, description = description, cover_pic = cover_pic)
            category.save()
            message = 'Category Added'
            
        else:
            message = 'Already Added'
    return render(request,'ekart_admin/add_category.html', {'message': message, })

def pending_sellers(request):
    pending_sellers=Seller.objects.filter(status='pending')
    return render(request,'ekart_admin/pending_sellers.html', {'pending_sellers':pending_sellers})

def approved_sellers(request):
    approved_sellers=Seller.objects.filter(status='active')
    print(approved_sellers)
    return render(request,'ekart_admin/approved_sellers.html', {'approved_sellers':approved_sellers})

def customers(request):
    return render(request,'ekart_admin/customers.html')

def admin_login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            admin = EkartAdmin.objects.get(user_name = username, password = password)
            return redirect('ekart_admin:admin_home')
        except Exception as e:
            print(e)
            message = 'Invalid Username Or Password'


    return render(request,'ekart_admin/admin_login.html', {'message': message,})
    
def approve_seller(request,id):

    seller = Seller.objects.get(id = id)
    seller_id = randint(11111, 999999)
    temporary_password = 'sel-' + str(seller_id)  
    subject = 'username and temporary password'
    message = 'Hi! your Ekart account has been approved, your seller id is ' + str(seller_id) + temporary_password + ' and temporary password is ' + str(temporary_password)
    from_email = settings.EMAIL_HOST_USER
    # recipient_list = [seller.email,]
    recipient_list = ['daniyaashah@gmail.com',]

    send_mail(
        subject = subject,
        message = message,
        from_email = from_email,
        recipient_list = recipient_list
    )

    Seller.objects.filter(id = id).update(login_id = seller_id, password = temporary_password, status = 'active')

    return redirect('ekart_admin:pending_sellers')
