from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView
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
        product_id = self.kwargs['pro_id']

        #get product
        product_obj = Product.objects.get(id = product_id)
        
        #check if cart exists:
        cart_id = self.request.session.get(id = product_id)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id) # Old cart
            this_product_in_cart = cart_obj.cartproducts_set.filter(product = product_obj)

            #item already exists in cart
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id']= cart_obj.id # New Cart
           
        
        #check if product already exists in cart:


class AboutView(TemplateView):
    template_name = "about.html"

class ContactView(TemplateView):
    template_name = "contact.html"
