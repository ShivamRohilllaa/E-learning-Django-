from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as loginUser
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    allposts = Post.objects.all().filter(maincourse=True)
    totalposts = Post.objects.all()
    slider_post = Post.objects.all().filter(slider_post=True)
    top_three_catg = Category.objects.filter(top_three_cat=True)
    main_course = MainCourse.objects.all()
    allcat = Category.objects.all()
    categories = Category.objects.filter(parent=None).order_by('-created_at')[:7]
    footcategories = Category.objects.filter(parent=None)[:2]
    catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    catg_parent = Category.objects.all().exclude(parent=True)
    latest_catg = Category.objects.order_by("-id")[3:10]
    latest_post = Post.objects.order_by('-date')[:4]
    context = {'allposts':allposts, 'main_course':main_course, 'top_three_catg':top_three_catg, 'catg':catg, 'slider_post':slider_post, 'latest_catg':latest_catg, 'latest_post':latest_post, 'totalposts':totalposts, 'catg_parent':catg_parent, 'allcat':allcat, 'categories':categories, 'footcategories':footcategories}
    return render(request, 'core/index.html', context)


def post_by_category(request, slug):
    posts = Post.objects.all()
    cat_post = Post.objects.filter(category__slug=slug)
    allposts = Post.objects.all().filter(maincourse=True)
    slider_post = Post.objects.all().filter(slider_post=True)
    top_three_catg = Category.objects.filter(top_three_cat=True)
    main_course = MainCourse.objects.all()
    allcat = Category.objects.all()
    categories = Category.objects.filter(parent=None).order_by('-created_at')[:7]
    footcategories = Category.objects.filter(parent=None)[:2]
    catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    catg_parent = Category.objects.all().exclude(parent=True)
    latest_catg = Category.objects.order_by("-id")[3:10]
    latest_post = Post.objects.order_by('-date')[:4]
    context = {'posts':posts, 'cat_post':cat_post,'allposts':allposts, 'main_course':main_course, 'top_three_catg':top_three_catg, 'catg':catg, 'slider_post':slider_post, 'latest_catg':latest_catg, 'latest_post':latest_post}
    return render(request, 'core/index.html', context)

  
def post_details(request, category_slug, slug):
    posts = Post.objects.filter(slug=slug).first()
    category = Post.objects.filter(slug=category_slug)
    catg_parent = Category.objects.all().exclude(parent=True)
    allcat = Category.objects.all()
    context = {'posts':posts, 'category':category, 'allcat':allcat, 'catg_parent':catg_parent}
    return render(request, 'core/details.html', context)


# UserSignup Form
def signup(request):
    
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
            return redirect('home')
    context = {'form':form, 'customerForm':customerForm}
    return render(request, 'users/signup.html', context)

# UserSignup Form
def login(request):
    if request.method == 'GET':
        form = Customerloginform() #This comes from forms.py
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
            messages.success(request, "Welcome Sir")    
            return redirect('userdashboard')    
        else:
            context = {'form':form}
            return render(request, 'users/login.html', context)


def logout(request):
    request.session.clear()
    return redirect('home')

def userdashboard(request):
    customer = Customer.objects.all()
    context = {'customer':customer}
    return render(request, 'users/index.html', context)

def userprofile(request):
    customer = Customer.objects.get(user_id=request.user.id)
    context = {'customer':customer}
    return render(request, 'users/profile.html', context)























def webadmin(request):
    postcount = Post.objects.all().count()
    catcount = Category.objects.all().count()
    usercount = User.objects.all().count()
    context = {'postcount':postcount, 'cat':catcount, 'user':usercount}
    return render(request, 'webadmin/index.html', context)  

def add_post(request):
    post= PostForm()
    if request.method=='POST':
        post=PostForm(request.POST, request.FILES)
        if post.is_valid():
            post.save()
        messages.success(request, "post Added Sucessfully !!")    
        return redirect('allposts')
    return render(request, "webadmin/addpost.html", {'post':post})

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

#This is for show all Categories in Custom Admin Panel
def allcat(request):
    cat = Category.objects.all()
    context = {'cat':cat}
    return render(request, 'webadmin/allcat.html', context)

def allcourse(request):
    course = MainCourse.objects.all()
    context = {'course':course}
    return render(request, 'webadmin/allcourse.html', context)

def edit_post(request, id):
    if request.method == 'POST':
        posts = Post.objects.get(id=id)
        editpostForm= EditPostForm(request.POST, instance=posts)
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

def edit_cat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        editcatForm= EditCatForm(request.POST, instance=cat)
        if editcatForm.is_valid():
            editcatForm.save()
        messages.success(request, "Post Update Sucessfully !!")
        return redirect('allcat')
    else:
        cat = Category.objects.get(id=id)
        editcatForm= EditCatForm(instance=cat)

    return render(request, "webadmin/editcat.html", {'editcat':editcatForm})
    
def delete_cat(request, id):
    delete = Category.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Category Deleted Successfully.")
    return redirect('allcat')

def edit_course(request, id):
    if request.method == 'POST':
        course = MainCourse.objects.get(id=id)
        editcourse= EditMaincourse(request.POST, instance=course)
        if editcourse.is_valid():
            editcourse.save()
        messages.success(request, "Course Update Sucessfully !!")
        return redirect('allcat')
    else:
        cat = MainCourse.objects.get(id=id)
        editcourse= EditMaincourse(instance=cat)

    return render(request, "webadmin/editcourse.html", {'editcourse':editcourse})


def delete_course(request, id):
    delete = MainCourse.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "MainCourse Deleted Successfully.")
    return redirect('allcourses')    