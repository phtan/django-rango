from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
        context_dict['category_name_slug'] = category.slug

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass # Don't do anything. The template displays the 'No category' message for us.

    return render(request, 'rango/category.html', context_dict)

@login_required
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

@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except CategoryDoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat, 'category_name_slug': category_name_slug}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password) # hashes password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
          'rango/register.html',
          {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):

    login_form = LoginForm()
    status = ''

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Your Rango account is disabled.')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            status = "Invalid login details: {0}, {1}".format(username, password)
            return render(request, 'rango/login.html', {'login_form': login_form, 'status': status})
    else:
        return render(request, 'rango/login.html', {'login_form': login_form, 'status': status})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html' , {'message': "Since you're logged in, you can see this text!"})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
