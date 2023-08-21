from django.db import models

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    joined_on = models.DateTimeField(auto_now_add=True)


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
