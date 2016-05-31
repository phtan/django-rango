from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    top_5_views_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': "I am bold font from the context", 'categories': category_list, 'topViews': top_5_views_list}


    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass # Don't do anything. The template displays the 'No category' message for us.

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form  = CategoryForm(request.POST)

        if form.is_valid():
            cat = form.save(commit=True)
            print cat, cat.slug

            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})
