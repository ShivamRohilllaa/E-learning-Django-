from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser, update_session_auth_hash
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.urls import reverse
import json
from time import time
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from edureka.settings import *
import razorpay
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
# Create your views here.

def home(request):
    allposts = Post.objects.all().filter(maincourse=True)
    totalposts = Post.objects.all().order_by('-date')[:8]
    slider_post = Post.objects.all().filter(slider_post=True)
    top_three_catg = Category.objects.filter(top_three_cat=True)[:3]
    main_course = MainCourse.objects.all()
    allcat = Category.objects.all()
    categories = Category.objects.all().filter(top_three_cat=False).filter(more=False).order_by('-created_at')[:7]
    footcategories = Category.objects.filter(parent=None)[:2]
    catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    # catg_parent = Category.objects.all().exclude(parent=True).order_by('-hit')
    latest_catg = Category.objects.filter(parent=None)[:5]
    latest_catg_all = Category.objects.filter(parent=None)[5:]
    latest_post = Post.objects.order_by('-date')[:4]
    rev = Reviews.objects.all().order_by('-created')[:6]
    context = {'allposts':allposts, 'main_course':main_course, 'top_three_catg':top_three_catg, 'catg':catg, 'slider_post':slider_post, 'latest_catg':latest_catg, 'latest_post':latest_post, 'totalposts':totalposts, 
    
    # 'catg_parent':catg_parent,
     'allcat':allcat, 'categories':categories, 'footcategories':footcategories, 'rev':rev, 'latest_catg_all':latest_catg_all}
    return render(request, 'core/index.html', context)

def totalposts(request):
    total = Post.objects.all()
    context = {'total':total}
    return render(request, 'core/total.html', context)

def post_by_category(request, catslug):
    posts = Post.objects.all()
    cat_post = Post.objects.filter(category__slug=catslug)
    allposts = Post.objects.all().filter(maincourse=True)
    slider_post = Post.objects.all().filter(slider_post=True)
    top_three_catg = Category.objects.filter(top_three_cat=True)[:3]
    main_course = MainCourse.objects.all()
    allcat = Category.objects.all()
    categories = Category.objects.filter(parent=None).order_by('-created_at')[:7]
    footcategories = Category.objects.filter(parent=None)[:2]
    catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    catg_parent = Category.objects.all().exclude(parent=True)
    latest_catg = Category.objects.filter(parent=None)[:5]
    latest_post = Post.objects.order_by('-date')[:4]
    latest_catg_all = Category.objects.filter(parent=None)[5:]
    rev = Reviews.objects.all().order_by('-created')[:6]
    context = {'latest_catg_all':latest_catg_all, 'rev':rev, 'posts':posts, 'cat_post':cat_post,'allposts':allposts, 'main_course':main_course, 'top_three_catg':top_three_catg, 'catg':catg, 'slider_post':slider_post, 'latest_catg':latest_catg, 'latest_post':latest_post}
    return render(request, 'core/index.html', context)

def allpost_by_category(request, postslug):
    posts = Post.objects.all()
    cat_post = Post.objects.filter(category__slug=postslug)
    subcat_post = Post.objects.filter(subcategory__slug=postslug)
    allposts = Post.objects.all().filter(maincourse=True)
    allcat = Category.objects.all()
    context = {'posts':posts,'subcat_post':subcat_post, 'cat_post':cat_post,'allposts':allposts,'allcat':allcat,}
    return render(request, 'core/allposts.html', context)

def subcat_by_category(request, subcatslug):
    allcats = get_object_or_404(Category, slug=subcatslug)
    category = subcat.objects.filter(slug=subcatslug)
    # allsubcatg = allcats.subcat.filter(parent__slug=slug)
    cat_subcat = subcat.objects.filter(parent__slug=subcatslug)
    context = {'cat_subcat':cat_subcat, 'category':category, 'allcats':allcats}
    return render(request, 'core/catg_subcat.html', context)
  
def post_details(request, category_slug, slug):
    posts = Post.objects.filter(slug=slug).first()
    category = Post.objects.filter(slug=category_slug)
    catg_parent = Category.objects.all().exclude(parent=True)    
    allcat = Category.objects.all()
    allpost = get_object_or_404(Post, slug=slug)
    #for add curriculam 
    curriculam = Curriculam.objects.filter(Post=allpost)
    #for class features
    feature = features.objects.filter(Post=allpost)
    #for frequently asked questions
    faqs = faq.objects.filter(Post=allpost)
    #for Timing
    time = timing.objects.filter(Post=allpost)    
    #for Videos
    vid = video.objects.filter(post=allpost)    
    #for Reviews
    if request.method == 'POST' and request.user.is_authenticated:
        allstars = request.POST.get('stars', 3)
        allcontent = request.POST.get('content', '')
        review = Reviews.objects.create(post=allpost, user=request.user, stars=allstars, content=allcontent)
        return redirect('home')        
    reviews = Reviews.objects.filter(post=allpost)    

    context = {'posts':posts, 'category':category, 'allcat':allcat, 'catg_parent':catg_parent, 'curriculam':curriculam, 'allpost':allpost, 'reviews':reviews, 'features':feature, 'faqs':faqs, 'time':time, 'videos':vid}
    return render(request, 'core/details.html', context)

def search(request):
    search = request.GET['search']
    totalposts = Post.objects.filter(title__icontains=search)
    # allpostcontent = Post.objects.filter(desc__icontains=search)
    context = {'totalposts':totalposts, 'search':search}
    return render(request, 'core/search.html', context)

def videos(request):
    return render(request, 'core/videos.html')

def blogs(request):
    categories = Category.objects.all().filter(top_three_cat=False).filter(more=False).order_by('-created_at')
    recent_blogs = blog.objects.all().order_by('-date')
    context = {'categories':categories, 'recent_blogs':recent_blogs}
    return render(request, 'core/blog.html', context) 

def blog_catposts(request, blogcatslug):
    blogpost = blog.objects.filter(category__slug=blogcatslug)
    context = {'blogpost':blogpost}
    return render(request, 'core/blogcatpost.html', context)

def blogdetails(request, detslug):
    blogs = blog.objects.filter(slug=detslug).first()
    context = {'blogs':blogs}
    return render(request, 'core/blogdetails.html', context)  

def courses(request):
    main_course = MainCourse.objects.all()
    context = {'main_course':main_course}
    return render(request, 'core/courses.html', context)

def blank_page(request, slug):
    blank = blankpage.objects.filter(slug=slug).first()
    allblank = get_object_or_404(blankpage, slug=slug)
    #for add t&c 
    tc = tcforblog.objects.filter(blank_page=allblank)
    context = {'blank':blank, 'tc':tc}
    return render(request, 'core/blankdetails.html', context)

def getpromo(request, code):
    try:
        promo = promocode.objects.get(code=code)
        return promo
    except ObjectDoesNotExist:
        messages.info(request, 'This coupon is not available')
        return redirect('home')

def add_promo(request, code):
    if request.method == "POST":
        form = promoform(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order= Order.objects.get(user=request.user, ordered=False)        
                order.coupon = getpromo(request, code)
                order.save()
                messages.success(request, 'Coupon is added !!')
                return redirect('home')

            except ObjectDoesNotExist:
                messages.info(request, 'This coupon is not available')
                return redirect('home')

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = request.POST
        context = {}
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            order = Order.objects.get(order_id = razorpay_order_id)
            order.payment_id = razorpay_payment_id
            order.ordered = True
            order.save()
            cart_items = Cart.objects.filter(user=request.user, purchase=False)
            for item in cart_items:
                item.purchase = True
                item.save()
            return redirect('userhome')
        except:
            return HttpResponse("Invalid Payment Details")    

# UserSignup Form
def signup(request):
    next_page = request.GET.get('next')
    form=CustomerCreationForm()
    customerForm=CustomerForm()
    mydict={'form':form,'customerForm':customerForm}
    if request.method=='POST':
        form = CustomerCreationForm(request.POST)
        customerForm=CustomerForm(request.POST,request.FILES)
        if form.is_valid() and customerForm.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('userlogin')
    context = {'form':form, 'customerForm':customerForm}
    return render(request, 'users/signup.html', context)

# UserSignup Form
def login(request):
    if request.method == 'GET':
        form = Customerloginform() #This comes from forms.py
        next_page = request.GET.get('next') #If url has next value so this function will redirect the user on next page url                
        context = {'form':form}
        return render(request, 'users/login.html', context)
    else:
        form = Customerloginform(data=request.POST) #This comes from forms.py
        if form.is_valid():
            username = form.cleaned_data.get('username')    
            password = form.cleaned_data.get('password')    
            user = authenticate(username=username, password=password)
            if user:
                loginUser(request, user) #We use loginUser here because yaha 2 login ho gye hai to alag se import kiya hai isko humne
            # messages.success(request, "Welcome Sir")
            #If url has next value so this function will redirect the user on next page url
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:        
                return redirect('userhome')  
        else:
            context = {'form':form}
            return render(request, 'users/login.html', context)


def logout(request):
    request.session.clear()
    return redirect('home')

def userdashboard(request):
    customer = Customer.objects.all()
    carts = Cart.objects.filter(user=request.user, purchase=True)
    orders = Order.objects.filter(user=request.user, ordered=True)
    # if orders.exists() and carts.exists():
    #     order = orders[0]
    #     return render(request, 'users/index.html', context={'carts':carts,'orders':orders})
    context = {'carts':carts,'customer':customer, 'orders':orders}
    return render(request, 'users/index.html', context)

def userprofile(request):
    customer = Customer.objects.get(user_id=request.user.id)
    context = {'customer':customer}
    return render(request, 'users/profile.html', context)

def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomerCreationEditForm(request.POST or None, request.FILES or None, instance=request.user)
        profile_form = CustomerEditForm(request.POST or None, request.FILES or None, instance=request.user.customer)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            # print(user_form)
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = CustomerCreationEditForm(instance=request.user)
        profile_form = CustomerEditForm(instance=request.user.customer)
    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# def edit_profile(request):
#     user=User.objects.get(id=request.user.id)
#     userForm=CustomerCreationEditForm(instance=request.user)
#     mydict={'userForm':userForm}
#     if request.method=='POST':
#         userForm=CustomerCreationEditForm(request.POST,instance=request.user)
#         if userForm.is_valid():
#             user=userForm.save()
#             # user.set_password(user.password)
#             user.save()
#             return redirect('profile')
#     return render(request,'users/edit_profile.html',context=mydict)


# def edit_user_data(request, id):
#     if request.method == 'POST':
#         customer = Customer.objects.get(id=id)
#         editcustomerform= CustomerEditForm(request.POST, instance=customer)
#         if editcustomerform.is_valid():
#             editcustomerform.save()
#         messages.success(request, "Data Update Sucessfully !!")
#         return redirect('userhome')
#     else:
#         customer = Customer.objects.get(id=id)
#         editcustomerform= CustomerEditForm(instance=customer)

#     return render(request, "users/edit_data.html", {'edit':editcustomerform})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userhome')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/edit_password.html', {
        'form': form
    })


@login_required(login_url='/userlogin/')
def add_to_cart(request, slug):
    course = get_object_or_404(Post, slug=slug)
    order_item = Cart.objects.get_or_create(item=course, user=request.user, purchase=False)
    order_object = Order.objects.filter(user=request.user, ordered=False)
    if order_object.exists():
        order = order_object[0]
        if order.orderitems.filter(item=course).exists():
            messages.success(request, "This Product is already added in your cart.")
            return redirect('cart')
        else:
            order.orderitems.add(order_item[0])
            messages.success(request, "Product is added in your cart.")
            return redirect('cart')
    else:
        order = Order(user= request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.success(request, "Product is added in your cart.")
        return redirect('cart')

def checkout(request):
    user = None
    coupon = promocode.objects.all()
    if request.method == 'get':
        try:
            orders = Order.objects.get(user=request.user, ordered=False)
            context = {'orders':orders}
            return render(request, 'core/checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(request, 'You do not have an active order')
            return redirect('checkout')
    
    orders = Order.objects.filter(user=request.user, ordered=False)           
    user = request.user        
    if orders.exists():
        order = orders[0]   
    orderss = None    
    order_payment = None
    action = request.GET.get('action')    
    if action == 'create_payment':
        amount = int(order.get_totals() * 100)
        currency = "INR"
        receipt = f"inetsoftware.org-{int(time())}"
        notes = {
                "email": user.email,
                "name": f'{user.first_name} {user.last_name}'
        }
        orderss = client.order.create({
        'amount':amount,
        'currency':currency,
        'receipt':receipt,
        'notes':notes
        })

        orders = Order.objects.filter(user=request.user, ordered=False)    
        order_payment = orders[0]
        order_payment.user = user
        order_payment.emailAddress = user.email
        order_payment.coupon = order.coupon
        order_payment.order_id = orderss.get('id')
        order_payment.total = orderss.get('amount')
        order_payment.save()
    context = {'orderss':orderss, 'order_payment':order_payment, 'orders':orders, 'order':order, 'couponform':CouponForm()}
    return render(request, 'core/checkout.html', context)


def get_coupon(request, code):
    try:
        promo = promocode.objects.get(code=code)
        return promo
    except ObjectDoesNotExist:
        messages.info(request, 'This promocode does not exist')
        return redirect('checkout')

def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST or None)
        if form.is_valid():    
            try:
                code = form.cleaned_data.get('code')
                orders = Order.objects.get(user=request.user, ordered=False)
                orders.coupon = get_coupon(request, code)
                orders.save()
                messages.success(request, "Successfully Promocode is Added !!")
                return redirect('checkout')
            except ObjectDoesNotExist:
                messages.info(request, 'You do not have an active order')
                return redirect('checkout')
    return None

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchase=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'core/cart.html', context={'carts':carts,'order':order,'orders':orders})
    else:
        messages.warning(request, "You don't have any item in your cart")
        return redirect('home')

# @login_required
# def order_view(request):
#     orders = Order.objects.filter(user=request.user, ordered=True)
#     context = {'orders':orders}
#     return render(request, "users/index.html", context)


def remove_from_cart(request, id):
    item = get_object_or_404(Post, id=id)
    order_obj = Order.objects.filter(user=request.user, ordered=False)
    if order_obj.exists():
        order = order_obj[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchase=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This product is removed form your cart")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart")
    else:
        messages.info(request,"You don't have an active order")
        return redirect("home")



def webadmin(request):
    postcount = Post.objects.all().count()
    catcount = Category.objects.all().count()
    usercount = User.objects.all().count()
    orders = Order.objects.all()
    context = {'postcount':postcount, 'cat':catcount, 'user':usercount,"orders":orders}
    return render(request, 'webadmin/index.html', context)  


# def add_post(request):
#     post= PostForm()
#     faq = faqform()
#     curriculam = Curriculamform()
#     features = featuresform()
#     if request.method=='POST':
#         post = PostForm(request.POST, request.FILES)
#         faq = [faqform(prefix=str(
#                 x), instance=Post()) for x in range(7)]
#         curriculam = Curriculamform(request.POST, request.FILES)
#         features=featuresform(request.POST, request.FILES)
#         if post.is_valid() and faq.is_valid() and curriculam.is_valid() and features.is_valid():
#             post.save()
#             faq.save()
#             curriculam.save()
#             features.save()
#         messages.success(request, "post Added Sucessfully !!")    
#         return redirect('allposts')
#     return render(request, "webadmin/addpost.html", {'post':post, 'faq':faq, 'features':features, 'curriculam':curriculam})

# def add_post(request):
#     if request.method == 'POST':
#         postform = PostForm(data=request.POST)
#         faq_form = faqform(data=request.POST)
#         curriculums_form = Curriculamform(data=request.POST)
#         features_form = featuresform(data=request.POST)
#         timing_form = timingform(data=request.POST)
#         if faq_form.is_valid and curriculums_form.is_valid and features_form.is_valid and timing_form.is_valid:
#             postform.save()
#             faq_form.save()
#             curriculums_form.save()
#             features_form.save()
#             timing_form.save()
#             return HttpResponseRedirect(reverse('allposts'))
#     else:
#         postform = PostForm()
#         faq_form = faqform()
#         curriculums_form = Curriculamform()
#         features_form = featuresform()
#         timing_form = timingform()
#     context = {"post":postform,"faq_form":faq_form, "curriculums_form": curriculums_form, "features_form":features_form,"timing_form" : timing_form}
#     return render(request, 'webadmin/addpost.html', context)  

def add_post(request):
    posts= PostForm()
    if request.method=='POST':
        posts=PostForm(request.POST, request.FILES)
        if posts.is_valid():
            posts.save()
        messages.success(request, "Posts Added Sucessfully !!")    
        return redirect('allposts')
    return render(request, "webadmin/addpost.html", {'post':posts})


def add_course(request):
    course= Maincourse()
    if request.method=='POST':
        course=Maincourse(request.POST, request.FILES)
        if course.is_valid():
            course.save()
        messages.success(request, "Course Added Sucessfully !!")    
        return redirect('allcourses')
    return render(request, "webadmin/addcourse.html", {'course':course})


def add_cat(request):
    category= CatForm()
    if request.method=='POST':
        category=CatForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addcat.html", {'category':category})

def add_curriculam(request):
    category= CatForm()
    if request.method=='POST':
        category=CatForm(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('webadmin')
    return render(request, "webadmin/addcat.html", {'category':category})

#This is for show all Posts in Custom Admin Panel
def allposts(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'webadmin/allposts.html', context)

#This is for show all Users in Custom Admin Panel
def allusers(request):
    # users = User.objects.all()
    customer = Customer.objects.all()
    context = {
        # 'users':users
    'customer':customer
    }
    return render(request, 'webadmin/allusers.html', context)

def userdetails(request, id):
    customer = Customer.objects.filter(id=id).first()
    context = {'customer':customer}
    return render(request, 'webadmin/user_detail.html', context)

def allorders(request):
    orders = Order.objects.filter(ordered=True)
    carts = Cart.objects.all()
    context = {
    'orders':orders, 'carts':carts,
    }
    return render(request, 'webadmin/allorders.html', context)

def approve_certificates(request, id):
    if request.method == 'POST':
        carts = Cart.objects.get(id=id)
        approve_cert= approve_certForm(request.POST or None, request.FILES or None, instance=carts)
        if approve_cert.is_valid():
            approve_cert.save()
        messages.success(request, "Certificate Is Enable !!")
        return redirect('allorders')
    else:
        carts = Cart.objects.get(id=id)
        approve_cert= approve_certForm(instance=carts)

    return render(request, "webadmin/editcarts.html", {'editcarts':approve_cert})
    
#This is for show all Categories in Custom Admin Panel
def allcat(request):
    cat = Category.objects.filter(parent=None).order_by('hit')
    context = {'cat':cat}
    return render(request, 'webadmin/allcat.html', context)

def allcourse(request):
    course = MainCourse.objects.all()
    context = {'course':course}
    return render(request, 'webadmin/allcourse.html', context)

def edit_post(request, id):
    if request.method == 'POST':
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(request.POST or None, request.FILES or None, instance=posts)
        if editpostForm.is_valid():
            editpostForm.save()
        messages.success(request, "Post Update Sucessfully !!")
        return redirect('allposts')
    else:
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(instance=posts)

    return render(request, "webadmin/editposts.html", {'editpost':editpostForm})
    
def delete_post(request, id):
    delete = Post.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Post Deleted Successfully.")
    return redirect('allposts')


#For edit the categories
def edit_cat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= CatForm(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= CatForm(instance=cat)

    return render(request, "webadmin/editcat.html", {'editcat':editcatForm})

#For delete the categories    
def delete_cat(request, id):
    delete = Category.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Category Deleted Successfully.")
    return redirect('allcat')


#For edit the course
def edit_course(request, id):
    if request.method == 'POST':
        course = MainCourse.objects.get(id=id)
        editcourse= EditMaincourse(request.POST or None, request.FILES or None, instance=course)
        if editcourse.is_valid():
            editcourse.save()
        messages.success(request, "Course Update Sucessfully !!")
        return redirect('allcat')
    else:
        cat = MainCourse.objects.get(id=id)
        editcourse= EditMaincourse(instance=cat)

    return render(request, "webadmin/editcourse.html", {'editcourse':editcourse})

#For delete the course
def delete_course(request, id):
    delete = MainCourse.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "MainCourse Deleted Successfully.")
    return redirect('allcourses')    

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

    
def usercertificate(request, category_slug, slug):
    posts = Post.objects.filter(slug=slug).first()
    category = Post.objects.filter(slug=category_slug)
    carts = Cart.objects.filter(user=request.user, purchase=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render_to_pdf('users/certificate.html',{'customerName':request.user.first_name,'customerNamelast':request.user.last_name,
        'customerEmail':request.user.email,'carts':carts,'order':order,'posts':posts})

    return render_to_pdf('users/certificate.html', {'posts':posts})

def add_videos(request):
    video= videoform()
    if request.method=='POST':
        video=videoform(request.POST, request.FILES)
        if video.is_valid():
            video.save()
        messages.success(request, "video Added Sucessfully !!")    
        return redirect('home')
    return render(request, "webadmin/addvideo.html", {'video':video})

def edit_videos(request, id):
    if request.method == 'POST':
        vid = video.objects.get(id=id)
        editvideoForm= videoform(request.POST or None, request.FILES or None, instance=vid)
        if editvideoForm.is_valid():
            editvideoForm.save()
        messages.success(request, "Video Update Sucessfully !!")
        return redirect('allcat')
    else:
        vid = video.objects.get(id=id)
        editvideoForm= videoform(instance=vid)

    return render(request, "webadmin/editvideo.html", {'editvideo':editvideoForm})

def delete_video(request, id):
    delete = video.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "video Deleted Successfully.")
    return redirect('allcourses')   

def allvideos(request):
    vid = video.objects.all()
    context = {'video':vid}
    return render(request, 'webadmin/allvideo.html', context)

def paid_video(request, slug):
    allpost = get_object_or_404(Post, slug=slug)
    vid = video.objects.filter(post=allpost)
    context = {'allpost':allpost, 'vid':vid}
    return render(request, 'users/video.html', context)

def allfaq(request):
    f = faq.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allfaq.html', context)

def add_faq(request):
    faq= faqForm()
    if request.method=='POST':
        faq= faqForm(request.POST, request.FILES)
        if faq.is_valid():
            faq.save()
        messages.success(request, "faq Added Sucessfully !!")    
        return redirect('allfaq')
    return render(request, "webadmin/add_faq.html", {'faq':faq})

def edit_faq(request, id):
    if request.method == 'POST':
        faqs = faq.objects.get(id=id)
        EditfaqForm= faqForm(request.POST, instance=faqs)
        if EditfaqForm.is_valid():
            EditfaqForm.save()
        messages.success(request, "FAQ Update Sucessfully !!")
        return redirect('allfaq')
    else:
        faqs = faq.objects.get(id=id)
        EditfaqForm= faqForm(instance=faqs)   

    return render(request, "webadmin/editfaq.html", {'faqForm':EditfaqForm})

def delete_faq(request, id):
    delete = faq.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "faq Deleted Successfully.")
    return redirect('allfaq') 

def alltime(request):
    f = timing.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/alltime.html', context)

def add_time(request):
    time= timingform()
    if request.method=='POST':
        time= timingform(request.POST, request.FILES)
        if time.is_valid():
            time.save()
        messages.success(request, "Timings Added Sucessfully !!")    
        return redirect('alltime')
    return render(request, "webadmin/add_time.html", {'time':time})

def edit_time(request, id):
    if request.method == 'POST':
        time = timing.objects.get(id=id)
        Edittimingform= timingform(request.POST, instance=time)
        if Edittimingform.is_valid():
            Edittimingform.save()
        messages.success(request, "Timings Update Sucessfully !!")
        return redirect('alltime')
    else:
        time = timing.objects.get(id=id)
        Edittimingform= timingform(instance=time)   

    return render(request, "webadmin/edit_time.html", {'time':Edittimingform})

def delete_time(request, id):
    delete = timing.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Timing Deleted Successfully.")
    return redirect('alltime') 

def allfeatures(request):
    f = features.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allfeatures.html', context)

def add_features(request):
    features= featuresform()
    if request.method=='POST':
        features= featuresform(request.POST, request.FILES)
        if features.is_valid():
            features.save()
        messages.success(request, "Timings Added Sucessfully !!")    
        return redirect('allfeatures')
    return render(request, "webadmin/add_features.html", {'features':features})

def edit_features(request, id):
    if request.method == 'POST':
        feat = features.objects.get(id=id)
        editfeatures = featuresform(request.POST, instance=feat)
        if editfeatures .is_valid():
            editfeatures .save()
        messages.success(request, "featuress Update Sucessfully !!")
        return redirect('allfeatures')
    else:
        feat = features.objects.get(id=id)
        editfeatures = featuresform(instance=feat)   

    return render(request, "webadmin/edit_features.html", {'features':editfeatures })

def delete_features(request, id):
    delete = features.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Features Deleted Successfully.")
    return redirect('allfeatures') 

def allcurriculam(request):
    f = Curriculam.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allcurriculam.html', context)

def add_curriculam(request):
    curr= Curriculamform()
    if request.method=='POST':
        curr= Curriculamform(request.POST, request.FILES)
        if curr.is_valid():
            curr.save()
        messages.success(request, "Curriculam Added Sucessfully !!")    
        return redirect('allcurriculam')
    return render(request, "webadmin/add_curr.html", {'curr':curr})

def edit_curriculam(request, id):
    if request.method == 'POST':
        curr = Curriculam.objects.get(id=id)
        editcurr = Curriculamform(request.POST, instance=curr)
        if editcurr.is_valid():
            editcurr.save()
        messages.success(request, "Curriculam Update Sucessfully !!")
        return redirect('allcurriculam')
    else:
        curr = Curriculam.objects.get(id=id)
        editcurr = Curriculamform(instance=curr)   

    return render(request, "webadmin/edit_curriculam.html", {'editcurr':editcurr })

def delete_curriculam(request, id):
    delete = Curriculam.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Curriculam Deleted Successfully.")
    return redirect('allcurriculam') 

def allsubcatg(request):
    f = subcat.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allsubcat.html', context)

def add_subcatg(request):
    sub= subcatg()
    if request.method=='POST':
        sub= subcatg(request.POST, request.FILES)
        if sub.is_valid():
            sub.save()
        messages.success(request, "Subcat Added Sucessfully !!")    
        return redirect('allsubcatg')
    return render(request, "webadmin/add_subcat.html", {'sub':sub})

def edit_subcatg(request, id):
    if request.method == 'POST':
        sub = subcat.objects.get(id=id)
        editsub = subcatg(request.POST, instance=sub)
        if editsub.is_valid():
            editsub.save()
        messages.success(request, "Subcat Update Sucessfully !!")
        return redirect('allsubcatg')
    else:
        sub = subcat.objects.get(id=id)
        editsub = subcatg(instance=sub)   

    return render(request, "webadmin/edit_subcat.html", {'subcat':editsub })

def delete_subcatg(request, id):
    delete = subcat.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Subcat Deleted Successfully.")
    return redirect('allsubcatg') 

def allblogs(request):
    f = blog.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allblogs.html', context)

def add_blogs(request):
    blog= blogform()
    if request.method=='POST':
        blog= blogform(request.POST, request.FILES)
        if blog.is_valid():
            blog.save()
        messages.success(request, "blog Added Sucessfully !!")    
        return redirect('allblog')
    return render(request, "webadmin/add_blog.html", {'blog':blog})

def edit_blogs(request, id):
    if request.method == 'POST':
        blogs = blog.objects.get(id=id)
        editblog = blogform(request.POST or None, request.FILES or None, instance=blogs)
        if editblog.is_valid():
            editblog.save()
        messages.success(request, "Blog Update Sucessfully !!")
        return redirect('allblog')
    else:
        blogs = blog.objects.get(id=id)
        editblog = blogform(instance=blogs)   

    return render(request, "webadmin/edit_blog.html", {'editblog':editblog })  

def delete_blogs(request, id):
    delete = blog.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Blog Deleted Successfully.")
    return redirect('allblog') 

def allblank(request):
    f = blankpage.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/allblank.html', context)

def add_blank(request):
    blank= blankform()
    if request.method=='POST':
        blank= blankform(request.POST, request.FILES)
        if blank.is_valid():
            blank.save()
        messages.success(request, "blank Added Sucessfully !!")    
        return redirect('allblank')
    return render(request, "webadmin/add_blank.html", {'blank':blank})

def edit_blank(request, id):
    if request.method == 'POST':
        blank = blankpage.objects.get(id=id)
        editblank = blankform(request.POST or None, request.FILES or None, instance=blank)
        if editblank.is_valid():
            editblank.save()
        messages.success(request, "Blank Page Update Sucessfully !!")
        return redirect('allblank')
    else:
        blank = blankpage.objects.get(id=id)
        editblank = blankform(instance=blank)   

    return render(request, "webadmin/edit_blank.html", {'editblank':editblank })  

def delete_blank(request, id):
    delete = blankpage.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Blank Deleted Successfully.")
    return redirect('allblank') 

def alltc(request):
    f = tcforblog.objects.all()
    context = {'f':f}
    return render(request, 'webadmin/alltc.html', context)

def add_tc(request):
    tc= tcblog()
    if request.method=='POST':
        tc= tcblog(request.POST, request.FILES)
        if tc.is_valid():
            tc.save()
        messages.success(request, "tc Added Sucessfully !!")    
        return redirect('alltc')
    return render(request, "webadmin/add_tc.html", {'tc':tc})

def edit_tc(request, id):
    if request.method == 'POST':
        tcs = tcforblog.objects.get(id=id)
        Edittcblog= tcblog(request.POST, instance=tcs)
        if Edittcblog.is_valid():
            Edittcblog.save()
        messages.success(request, "tc Update Sucessfully !!")
        return redirect('alltc')
    else:
        tcs = tcforblog.objects.get(id=id)
        Edittcblog= tcblog(instance=tcs)   

    return render(request, "webadmin/edittc.html", {'tcblog':Edittcblog})

def delete_tc(request, id):
    delete = tcforblog.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "tc Deleted Successfully.")
    return redirect('alltc')     

def add_leftcat(request):
    category= leftmenu()
    if request.method=='POST':
        category=leftmenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addleftcat.html", {'category':category})

#For edit the categories
def edit_leftcat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= leftmenu(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= leftmenu(instance=cat)

    return render(request, "webadmin/editleftcat.html", {'editcat':editcatForm})

def add_middlecat(request):
    category= middlemenu()
    if request.method=='POST':
        category=middlemenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addmiddlecat.html", {'category':category})

#For edit the categories
def edit_middlecat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= middlemenu(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= middlemenu(instance=cat)

    return render(request, "webadmin/editmiddlecat.html", {'editcat':editcatForm})

def add_rightcat(request):
    category= rightmenu()
    if request.method=='POST':
        category=rightmenu(request.POST, request.FILES)
        if category.is_valid():
            category.save()
        messages.success(request, "category Added Sucessfully !!")    
        return redirect('allcat')
    return render(request, "webadmin/addrightcat.html", {'category':category})

#For edit the categories
def edit_rightcat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= rightmenu(request.POST or None, request.FILES or None, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
            messages.success(request, "Category Update Sucessfully !!")
            return redirect('allcat')
        else:
            messages.warning(request, "Category is not Updated !!")
            return redirect('allcat')    
    else:
        cat = Category.objects.get(id=id)
        editcatForm= rightmenu(instance=cat)

    return render(request, "webadmin/editrightcat.html", {'editcat':editcatForm})

def admin_reviews(request):
    review= admin_reviewsform()
    if request.method=='POST':
        review = admin_reviewsform(request.POST, request.FILES)
        if review.is_valid():
            review.save()
        messages.success(request, "Review Added Sucessfully !!")    
        return redirect('alladmin_review')
    return render(request, "webadmin/add_reviews.html", {'review':review})

def delete_admin_review(request, id):
    delete = Reviews.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Admin Review Deleted Successfully.")
    return redirect('alladmin_review')   

def edit_admin_review(request, id):
    if request.method == 'POST':
        review = Reviews.objects.get(id=id)
        edit_admin_reviews = admin_reviewsform(request.POST, instance=review)
        if edit_admin_reviews .is_valid():
            edit_admin_reviews .save()
        messages.success(request, "Reviews Update Sucessfully !!")
        return redirect('alladmin_review')
    else:
        faqs = Reviews.objects.get(id=id)
        edit_admin_reviews = admin_reviewsform(instance=faqs)

    return render(request, "webadmin/edit_admin_reviews.html", {'edit':edit_admin_reviews })    

def alladmin_review(request):
    review = Reviews.objects.all()
    context = {'review':review}
    return render(request, 'webadmin/all_reviews.html', context)    

def allribbon(request):
    ribbon = offers.objects.all()
    context = {'ribbon':ribbon}
    return render(request, 'webadmin/allribbon.html', context)

def add_ribbon(request):
    ribbon= ribbonform()
    if request.method=='POST':
        ribbon = ribbonform(request.POST, request.FILES)
        if ribbon.is_valid():
            ribbon.save()
        messages.success(request, "Offers Added Sucessfully !!")    
        return redirect('allribbon')
    return render(request, "webadmin/add_ribbon.html", {'add':ribbon})

def delete_ribbon(request, id):
    delete = offers.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Offer Deleted Successfully.")
    return redirect('allribbon')   

def edit_ribbon(request, id):
    if request.method == 'POST':
        ribbon = offers.objects.get(id=id)
        ribbon = ribbonform(request.POST, instance=ribbon)
        if ribbon.is_valid():
            ribbon.save()
        messages.success(request, "Offer Update Sucessfully !!")
        return redirect('allribbon')
    else:
        ribbon = offers.objects.get(id=id)
        ribbon = ribbonform(instance=ribbon)

    return render(request, "webadmin/edit_ribbon.html", {'edit':ribbon })    
    