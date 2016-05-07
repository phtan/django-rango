import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
    python_cat = add_cat('Python')

    add_page(cat=python_cat,
            title="Official Python tutorial",
            url="http://docs.python.org/2/tutorial/")

    add_page(cat=python_cat,
            title="How to think like a computer scientist",
            url="http://www.greenteapress.com/thinkpython/")

    django_cat = add_cat("Django")

    add_page(cat=django_cat,
            title="Official Django Tutorial",
            url="http://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=django_cat,
            title="Django Rocks",
            url="http://www.djangorocks.com")

    frame_cat = add_cat("Other frameworks")

    add_page(cat=frame_cat,
            title="Bottle",
            url="http://bottlepy.org/docs/dev")

    add_page(cat=frame_cat,
            title="Flask",
            url="http://flask.pocoo.org")

    # Print out what we have added to the user
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views=views
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

# Start execution here
if __name__ == '__main__':
    print "Starting rango population script..."
    populate() 
