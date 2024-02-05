from django.shortcuts import redirect, render
from customer.models import Customer
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from seller.models import Product, Seller
# from .models import Customer
# Create your views here.


def customer_home(request):
    products=Product.objects.all()
    context={
        'products':products,

    }
    return render(request, 'customer/customer_home.html', context)


def store(request):
    query = request.GET.get('query', 'all')
    
    if query == 'all':
        products = Product.objects.all()
     
    else:
         
        products = Product.objects.filter(category = query)

    if  'search_text' in request.GET:
        search_text = request.GET.get('search_text')
        products = Product.objects.filter(Q(category__category__icontains = search_text) | Q(product_name__icontains = search_text))
    # Pagination
    paginator = Paginator(products, 1)  # Number of products per page
    page_number = request.GET.get('page')
    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_products = paginator.page(paginator.num_pages)
    context = {
        'products': paginated_products,
        'product_count': paginator.count
    }

    return render(request, 'customer/store.html', context)


def product_detail(request):
    return render(request, 'customer/product_detail.html')


def cart(request):
    return render(request, 'customer/cart.html')


def place_order(request):
    return render(request, 'customer/place_order.html')


def order_complete(request):
    return render(request, 'customer/order_complete.html')


def dashboard(request):
    return render(request, 'customer/dashboard.html')


def seller_register(request):
    message = ''
    if request.method == 'POST':  
        first_name = request.POST['fname'] 
        last_name = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST['gender']
        company_name = request.POST['cmp_name']
        city = request.POST['city']
        country = request.POST['country']
        account_no = request.POST['acc_no']
        bank_name = request.POST['bank_name']
        branch = request.POST['branch']
        ifsc = request.POST['ifsc']
        pic = request.FILES['pic']
       
        seller_exist = Seller.objects.filter(email = email).exists()

        if not seller_exist: 

            seller = Seller(first_name = first_name, last_name = last_name, company_name = company_name,    gender = gender, email = email, 
                            city = city, country = country, account_no = account_no, bank_name = bank_name,
                            branch_name = branch, ifsc = ifsc, pic = pic)
            seller.save()
            message = 'Registration Succesful'
        else:
            message = 'Email Exists'
    return render(request, 'customer/seller_register.html', {'message': message})



def seller_login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST['seller_id']
        password = request.POST['password']

        seller = Seller.objects.filter(login_id = username, password = password)

        if seller.exists():
            request.session['seller'] = seller[0].id
            request.session['seller_name'] = seller[0].first_name + ' ' + seller[0].last_name
            return redirect('Seller:seller_home')

        else:

            message = 'Invalid Username Or Password'
    context={
        'message':message,
    } #dictionary, used if theres a lot
    return render(request, 'customer/seller_login.html', context)


def customer_signup(request):
    message = ''
    status = False
    if request.method == 'POST':  
        first_name = request.POST['fname'] 
        last_name = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST['gender']
        city = request.POST['city']
        country = request.POST['country']
        password = request.POST['password']

        
        
        customer_exist = Customer.objects.filter(email = email).exists()

        if not customer_exist: 

            customer = Customer(first_name = first_name, last_name = last_name, gender = gender, email = email, 
                            city = city, country = country, password = password)
            customer.save()
            message = 'Registration Succesful'
            status = True



    return render(request, 'customer/customer_signup.html', {'message': message, 'status': status})



def customer_login(request):

    message = ''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        
        try:
            customer = Customer.objects.get(email = email, password = password)
            request.session['customer'] = customer.id
            request.session['customer_name'] = customer.first_name + ' ' + customer.last_name
            return redirect('customer:customer_home')

        except:
            message = 'Invalid Username Or Password'

    return render(request, 'customer/customer_login.html', {'message':message})


def forgot_password_customer(request):
    return render(request, 'customer/forgot_password_customer.html')


def forgot_password_seller(request):
    return render(request, 'customer/forgot_password_seller.html')