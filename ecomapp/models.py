from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Admin(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile= models.IntegerField(max_length=10)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    joined_on = models.DateTimeField(auto_now_add=True)
    mobile = models.IntegerField(max_length=10,default=9800000000)


    def __str__(self):
        return self.full_name

class Category(models.Model):
    title = models.CharField(max_length=40)
    slug  = models.SlugField(unique = True)

    def __str__(self):
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description =   models.TextField()
    expiry = models.DateField()
    return_policy =models.CharField(max_length=300, null=True,blank = True)
    view_count = models.PositiveIntegerField() 

    def __str__(self):
        return self.title
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)
    
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: "+ str(self.cart.id) + " CartProduct: "+ str(self.id)
    
# You need to define the ORDER_STATUS choices before using them in the model
ORDER_STATUS = (
    ('Order Received', 'Order Received'),
    ('Order Completed', 'Order Completed'),
    ('Order Cancelled', 'Order Cancelled'),
)

METHOD = (
    ("Cash on Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD, default="Cash On Delivery")  # Corrected line
    payment_completed = models.BooleanField(default=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically populate the mobile number from the associated Customer
        if not self.mobile and self.cart.customer:
            self.mobile = self.cart.customer.mobile
        super().save(*args, **kwargs)

    def __str__(self):
        return "Order: " + str(self.id)
