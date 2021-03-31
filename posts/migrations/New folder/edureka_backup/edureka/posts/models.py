from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='media/profile_pic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    Country = models.CharField(max_length=20,null=False, blank=True)
    Company = models.CharField(max_length=20,null=False, blank=True)
    City =  models.CharField(max_length=20,null=False, blank=True)
    State =  models.CharField(max_length=20,null=False, blank=True)
    Zip_Code =  models.IntegerField(blank=True, default="1")
    Telephone =  models.IntegerField(blank=True, default="1")
    Extension =  models.CharField(max_length=20,null=False, blank=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = True, null=True)
    title = models.CharField(max_length=100) 
    slug = AutoSlugField(populate_from='title', unique=True, null=False)
    top_three_cat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def post_count(self):
        return self.posts.all().count()    

class MainCourse(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, null=False)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=70)
    slug = AutoSlugField(populate_from='title', unique=True, null=False)
    image = models.ImageField(upload_to='media/post')
    logo = models.ImageField(upload_to='media/post') #If user want to add university logo(Slider and Post) 
    desc = RichTextField(blank=True, null=True)
    #for live classes or offline classes
    badge = models.CharField(max_length=70)
    youtube = models.URLField(max_length=500, default='' )
    author = models.CharField(max_length=20, default="admin" )
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="posts")
    hit = models.PositiveIntegerField(default=0) #This field is for popular posts
    button_text = models.CharField(max_length=20, default="Apply Now") #Apply Now and enroll button text
    slider_post = models.BooleanField(default=False)
    maincourse = models.ManyToManyField(MainCourse, blank=True, related_name='posts')
    price = models.IntegerField(default=0)
    old_price = models.IntegerField(default=0)
    discount = models.IntegerField()
    emi_start_price = models.IntegerField()
    why_title = models.CharField(max_length=500, blank=True )
    why1 = RichTextField(blank=True)
    why2 = RichTextField(blank=True)
    why3 = RichTextField(blank=True)

    def __str__(self):
        return self.title    

class Curriculam(models.Model):    
    title = models.CharField(max_length=500)
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='acc_posts')
    content = RichTextField(blank=True, null=True)


class boxes_three(models.Model):
    title = models.CharField(max_length=70)
    slug = AutoSlugField(populate_from='title', unique=True, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)


    def __str__(self):
        return self.title    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)    

    
class Cart(models.Model):
    cart_id = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Post, on_delete=models.CASCADE)
    purchase = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} x {self.item}'

    def get_total(self):
        total = self.item.disc_price * self.quantity
        float_total = format(total, '0.2f')
        return float_total

    

class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total
