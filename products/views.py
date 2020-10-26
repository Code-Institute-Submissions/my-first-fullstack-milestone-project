from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Subcategory
from .forms import ProductProfileForm


# Create your views here.
def display_all_products(request):

    products = Product.objects.all()
    search_query = None
    category = None
    subcategory = None
    search_method = "menusearch"
    sortkey = None
    direction = None

    template = 'products/products.html'

    if request.GET:

        # call sorting logic function if we get 'sort' as parameter
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
        else:
            sortkey = 'price'
        if 'direction' in request.GET:
            direction = request.GET['direction']
        else:
            direction = 'asc'

        products = sorting_by(sortkey, direction, products)

        # logic for Search form
        if 'srch_qry' in request.GET:
            search_query = request.GET['srch_qry']
            if not search_query:
                messages.error(request, 'No search results were found')
                return redirect(reverse('products'))

            query_result = Q(name__icontains=search_query) | \
                Q(short_desc__icontains=search_query) | \
                Q(brand__icontains=search_query)

            products = products.filter(query_result)
            search_method = "searchform"

    context = {
        "products": products,
        "search_term": search_query,
        "category": category,
        "subcategory": subcategory,
        "search_method": search_method
    }

    return render(request, template, context)


def products_by_category(request, category_name):

    products = None
    subcategory = None
    category = None
    direction = None
    sortkey = None

    # find the category record first
    category_search = Category.objects.filter(name=category_name)

    #  if found, then find linked products and category
    if category_search:
        cat_products = Product.objects.filter(category__name=category_name)
        products = cat_products
        category = category_search

    # if category not found then, it means the subcategory was passed.
    # so, search subcategory. If found, then get linked products and category
    else:
        subcategory_search = Subcategory.objects.filter(name=category_name)

        """
        queryset codes below learned from:
        https://overiq.com/django-1-11/django-orm-basics-part-2/
        """
        if subcategory_search:
            cat_products = \
                Product.objects.filter(subcategory__name=category_name)

            category_search = \
                Category.objects.filter(subcategory__name=category_name)

            products = cat_products
            subcategory = subcategory_search
            category = category_search

    if request.GET:

        # call sorting logic function if we get 'sort' as parameter
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
        if 'direction' in request.GET:
            direction = request.GET['direction']

        products = sorting_by(sortkey, direction, products)

    template = 'products/products_categories.html'

    search_method = "breadcrumb"

    context = {
        "products": products,
        "category": category,
        "subcategory": subcategory,
        "search_method": search_method
    }

    return render(request, template, context)


def display_product_detail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    template = 'products/product_detail.html'

    context = {
        "product": product,
    }

    return render(request, template, context)


def sorting_by(sortkey, direction, products):

    if sortkey == 'category':
        sortkey = 'category__name'
    if sortkey == 'subcategory':
        sortkey = 'subcategory__name'
    if direction == 'desc':
        sortkey = f'-{sortkey}'  # the - reverses the sorting order

    products_sorted = products.order_by(sortkey)

    return products_sorted


@login_required
def add_product(request):

    # make sure only super users can add products
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry, only store owners are allowed'
                       'to perform this task.')
        return redirect(reverse('home'))

    if request.method == "POST":
        #  instance of the ProductProfileForm based
        #  on the request date from POST
        product_form_data = ProductProfileForm(request.POST, request.FILES)
        if product_form_data.is_valid():
            product = product_form_data.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('display_product_detail',
                            args=[product.id]))
        else:
            messages.error(request,
                           'Failed to add product.'
                           'Please ensure the form is valid.')
    else:
        product_form_data = ProductProfileForm()

    context = {
        'product_form_data': product_form_data,
    }

    template = 'products/addproduct.html'

    return render(request, template, context)


@login_required
def edit_product(request, product_id):

    # make sure only super users can edit products
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry, only store owners are'
                       'allowed to perform this task.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product_form_data = ProductProfileForm(request.POST,
                                               request.FILES, instance=product)
        if product_form_data.is_valid():
            product_form_data.save()
            messages.success(request, 'Product updated successfully')
            return redirect(reverse('display_product_detail',
                            args=[product.id]))
        else:
            messages.error(request,
                           'Update failed. Pleae ensure the form is valid.')
    else:
        # instantiate the product form based on product for display
        product_form_data = ProductProfileForm(instance=product)

    template = 'products/editproduct.html'

    context = {
        'product_form_data': product_form_data,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):

    #  make sure only super users can delete products
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry, only store owners are'
                       'allowed to perform this task.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))

