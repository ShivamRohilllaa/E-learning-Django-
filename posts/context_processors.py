from .models import *


def menu_links(request):
    links = Category.objects.filter(parent=None).order_by('-hit')
    # categoriess = Category.objects.all().filter(top_three_cat=False).filter(parent=None).filter(more=False).order_by('-created_at').order_by('hit')[:15]
    categoriess = Category.objects.all().filter(top_three_cat=False).filter(parent=None).filter(more=False).order_by('-created_at').order_by('hit')[:15]
    footcategories = Category.objects.filter(parent=None)[:2]
    allcat = Category.objects.all()
    catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    catg_parent = Category.objects.all().filter(more=False).exclude(parent=True).order_by('hit')
    latest_catg = Category.objects.order_by("-id")[3:10]
    return dict(links=links, allcat=allcat, categoriess=categoriess, footcategories=footcategories, catg=catg, 
    catg_parent=catg_parent,
     latest_catg=latest_catg)

def cart_total(request):
    if request.user.is_authenticated:
        totalcarts = Cart.objects.filter(user=request.user, purchase=False)
        return dict(totalcarts=totalcarts)
    else:
        totalcarts=[]
        return totalcarts  

def morecat(request):
    more = Category.objects.filter(more=True).order_by('-created_at').order_by('hit')
    return dict(more=more)

def disc(request):
    disc_cat = Category.objects.all().filter(disc=True)
    disc_blog = blog.objects.all().filter(disc=True)
    disc_post = Post.objects.all().filter(disc=True)
    return dict(disc_cat=disc_cat, disc_blog=disc_blog, disc_post=disc_post)

# def get_course_time(request, slug):
#     getpost = get_object_or_404(Post, slug=slug)
#     #for Timing
#     gettime = timing.objects.filter(Post=allpost)
#     return dict(getpost=getpost, gettime=gettime)

def ribbon(request):
    off = offers.objects.filter(active=True)
    return dict(off=off)
