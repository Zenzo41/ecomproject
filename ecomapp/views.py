from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView
from .models import *

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all().order_by("-id")
        return context

class AllProductsView(TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context

class ProductDetailView(TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context
    
class AddToCartView(TemplateView):
    template_name="addtocart.html"

    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        
        #get product id from requested url:
        product_id = self.kwargs['pro_id'] #fetching the id from the url

        #get product
        product_obj = Product.objects.get(id = product_id) # getting the object based on the id
        
        #check if cart exists:
        cart_id = self.request.session.get("cart_id",None)  
        if cart_id:  #fetch the cart
            cart_obj = Cart.objects.get(id=cart_id) # Old cart
            this_product_in_cart = cart_obj.cartproduct_set.filter(product = product_obj) #check if the item we want is already in cart

            # cartproduct_set means all cart products in Cart 

            #if item already exists in cart we need to increase
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

            #new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart = cart_obj,product = product_obj , rate = product_obj.selling_price,quantity = 1, subtotal = product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

        else: #create a new cart
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id']= cart_obj.id # New Cart in same session
            cartproduct = CartProduct.objects.create( # new cartproduct
                    cart = cart_obj,product = product_obj , rate = product_obj.selling_price,quantity = 1, subtotal = product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context

class MyCartView(TemplateView):
    template_name="mycart.html"  # had forgot to put this which caused major issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart = Cart.objects.get(id = cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context
    
class ManageCartView(View):

    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity +=1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()

        elif action == "dec":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()

            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()

        else:
            pass

        return redirect("ecomapp:mycart")

class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contact.html"




