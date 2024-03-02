import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from shop.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.\\

def home(request):
    products = Product.objects.filter(trending = 1)
    return render(request,"shop/index.html",{"products" : products})

def login_page(request):
    if request.method == 'POST':
        name =  request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request,username = name,password = pwd) 
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in success ")
            return redirect("/")
        else :
            messages.error(request,"Invaild Username Or Password")
            return redirect("/login")
    # products = Product.objects.filter(trending = 1)
    return render(request,"shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout success")
        return redirect('/login')


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You can Login Now ..!")
            return redirect('/login')

    return render(request,"shop/register.html",{"form" :form})


def collection(request):
    catagory = Catagory.objects.filter(status=0)
    return render(request,"shop/collections.html",{"catagory" :catagory})

def collectionview(request,name):
    if(Catagory.objects.filter(name = name,status=0)):
        products = Product.objects.filter(catagory__name = name)
        return render(request,"shop/product/index.html",{"products" :products,"catagory_name":name})
    else:
        messages.warning(request,'No search catagory')
        return redirect("collections")
 

def product_detail(request,name,pname):
    if(Catagory.objects.filter(name= name ,status =0)):
        if(Product.objects.filter(name = pname ,status = 0)):
            product = Product.objects.filter(name = pname).first()
            return render(request,"shop/product/product_deatils.html",{"products" :product , 'product_name': pname,'catagory_name': name})
        else:
            messages.error(request,'No product Found')
            return redirect('collections') 

    else :
        messages.error(request,'Catagory  not found')  

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            productid = data['pid']
            user_id = request.user.id
            print(productid)
            product_status = Product.objects.get(id = productid)
            if  product_status:
                if Cart.objects.filter(user=user_id,product = productid):
                    return JsonResponse({'status':'Product Already in cart'},status = 200)
                else :
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user = request.user,product_id= productid,product_qty = product_qty)
                        return JsonResponse({'status':'Product Added in cart'},status = 200)
                    else:
                         return JsonResponse({'status':'Product Out of Stock'},status = 200)



            return JsonResponse({'status':'Product aded to the cart'},status = 200)


        else:
            return JsonResponse({'status':'Login to add cart'},status = 200)
        
    else :
        return JsonResponse({'status':"invaild Access "},status = 200)
    


def viewcart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request,"shop/viewcart.html",{"cart":cart})
    else:
        return redirect("/")


def removecart(request,id):
    cartItem = Cart.objects.get(id = id)
    cartItem.delete()
    return redirect("viewcart")




def removefavorite(request,id):
    cartItem = Favorite.objects.get(id = id)
    cartItem.delete()
    return redirect("viewfavorite")


def favorite(request):
     if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            # product_qty = data['product_qty']
            productid = data['pid']
            print("jbbjjjjbjb")
            user_id = request.user.id
            print(productid)
            product_status = Product.objects.get(id = productid)
            if  product_status:
                if Favorite.objects.filter(user=user_id,product = productid):
                    return JsonResponse({'status':'Product Already in favorite'},status = 200)
                else :
                    Favorite.objects.create(user = request.user,product_id= productid)
                    return JsonResponse({'status':'Product Added in favorite'},status = 200)
            else:
                    return JsonResponse({'status':'Product Not Found'},status = 200)



        else:
            return JsonResponse({'status':'Login to add cart'},status = 200)
     else :
        return JsonResponse({'status':"invaild Access "},status = 200)
     



def viewfavorite(request):
    if request.user.is_authenticated:
        fav = Favorite.objects.filter(user=request.user)
        return render(request,"shop/viewfavorite.html",{"fav":fav})
    else:

        return redirect("/")