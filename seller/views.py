from django.shortcuts import render
from eKart_admin.models import Category

from seller.models import Product, Seller


# Create your views here.
def seller_home(request):
    return render(request, 'seller/seller_home.html')

def add_product(request):
    category_list = Category.objects.all()
    message = ''

    if request.method == 'POST':
        product_no = request.POST['product_code']
        product_name = request.POST['product_name']
        category = request.POST['category']
        description = request.POST['description']
        stock = request.POST['stock']
        price = request.POST['price']
        image = request.FILES['image']
        seller = request.session['seller']
        

       
             
        product, created = Product.objects.get_or_create(product_no = product_no, seller = seller, defaults = {
            'product_no': product_no, 
            'product_name': product_name.lower(),
            'seller': Seller.objects.get(id = seller),
            'category': Category.objects.get(id = category),
            'description': description.lower(),
            'stock': stock,
            'price': price,
            'image': image,
        })

        if created:
            print('added')
            message = 'Product Added'
        
        else:
            print('else')
            message = 'Product No Already exists'

       

    context = {
        'category': category_list,
        'message': message
    }
    return render(request, 'seller/add_product.html', context)

def add_category(request):
    return render(request, 'seller/add_category.html')

def view_category(request):
    return render(request, 'seller/view_category.html')

def view_products(request):
    products=Product.objects.filter(seller_id=request.session['seller'])
    return render(request, 'seller/view_product.html', {'products':products})

def profile(request):
    return render(request,'seller/profile.html')

def view_orders(request):
    return render(request,'seller/view_orders.html')

def update_stock(request):
    return render(request,'seller/update_stock.html')

def order_history(request):
    return render(request,'seller/order_history.html')