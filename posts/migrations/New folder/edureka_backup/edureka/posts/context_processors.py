from .models import *


def menu_links(request):
    links = Category.objects.filter(parent=None).order_by('-created_at')
    
    categories = Category.objects.filter(parent=None).order_by('-created_at')[:7]
    footcategories = Category.objects.filter(parent=None)[:2]
    allcat = Category.objects.all()
    catg = Category.objects.all().exclude(parent=None).order_by('-created_at')[:7]
    catg_parent = Category.objects.all().exclude(parent=True)
    latest_catg = Category.objects.order_by("-id")[3:10]
    return dict(links=links, allcat=allcat, categories=categories, footcategories=footcategories, catg=catg, catg_parent=catg_parent, latest_catg=latest_catg)
