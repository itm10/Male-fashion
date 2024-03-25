import datetime
from datetime import timedelta
import json

from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import Product, Images, Shoppingcart, Commment, Order, Category
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse


class HomeView(View):
    template = 'index.html'
    contex = {}

    def get(self, request):
        product_new = Product.objects.filter(
            Q(created_at__gte=datetime.datetime.now() - timedelta(days=3)) &
            Q(created_at__lte=datetime.datetime.now())
        )
        commentss = Commment.objects.all().order_by('-created_at')[:4]
        products_new = []
        for new in product_new:
            img = Images.objects.filter(service=new).first()
            new.image = img
            products_new.append(new)
        self.contex.update({'product_new': products_new})
        self.contex.update({'comments_data': commentss})
        return render(request, self.template, self.contex)


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class Shopview(View):
    template = "shop.html"
    contex = {}

    def get(self, request):
        products_all = Product.objects.all()
        product_brand = set(products_all.values_list('brand', flat=True))
        print(product_brand)
        categories = set(Category.objects.values_list('name', flat=True))
        products_with_images = []
        for product in products_all:
            img = Images.objects.filter(service=product).first()
            if img:
                product.image = img
                products_with_images.append(product)
        context = {
            'products': products_with_images,
            'brand': product_brand,
            'categories': categories,
        }
        return render(request, self.template, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/accounts/login')

        user_id = request.user.id
        product_id = request.POST.get('product_id')
        selected_brands = request.POST.getlist('brand')
        selected_categories = request.POST.getlist('category')

        if product_id:
            if Shoppingcart.objects.filter(user_id=user_id, product_id=product_id).exists():
                messages.error(request, "This product has already been added by you")
            else:
                Shoppingcart.objects.create(product_id=product_id, user_id=user_id)

        selected_products = Product.objects.all()
        if selected_brands:
            selected_products = selected_products.filter(brand__in=selected_brands)
        if selected_categories:
            selected_product_ids = Category.objects.filter(name__in=selected_categories).values_list('product_id',
                                                                                                     flat=True)
            selected_products = selected_products.filter(id__in=selected_product_ids)

        if selected_products.exists():
            products_datas = []
            for product in selected_products:
                img = Images.objects.filter(service=product).first()
                product.image = img
                products_datas.append(product)

            all_brands = set(Product.objects.values_list('brand', flat=True))
            all_categories = set(Category.objects.values_list('name', flat=True))

            context = {
                'selected_products': products_datas,
                'brand': all_brands,
                'categories': all_categories,
            }
            return render(request, self.template, context)


class BlogView(View):
    def get(self, request):
        return render(request, 'blog.html')


class Shop_detailsView(View):
    def get(self, request):
        return render(request, 'shop-details.html')


class ShoppingcartView(View):
    template_name = 'shopping-cart.html'
    context = {}

    def get(self, request):
        if request.user.id is None:
            return redirect('/accounts/login')

        shopping_cart = Shoppingcart.objects.filter(user=request.user)
        data = []

        for index, value in enumerate(shopping_cart):
            product = value.product
            image = Images.objects.filter(service=product).first()
            value.img = image
            value.index = index + 1
            data.append(value)

        self.context.update({'shopping_cart_products': data})
        return render(request, self.template_name, self.context)

    def post(self, request):
        shopping_cart_id = request.POST.get('shopping_cart_id')
        Shoppingcart.objects.get(pk=shopping_cart_id).delete()
        return redirect('/shopping-cart')


class IncrementCountAPIView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            shopping_cart_id = json_data.get('id')
            shopping_cart = Shoppingcart.objects.get(pk=shopping_cart_id)
            shopping_cart.count += 1
            shopping_cart.save()
        except Exception as e:
            return JsonResponse({'success': False, 'error': e})
        return JsonResponse({'success': True})


class DecrementCountAPIView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            shopping_cart_id = json_data.get('id')
            shopping_cart = Shoppingcart.objects.get(pk=shopping_cart_id)
            if shopping_cart.count > 0:
                shopping_cart.count -= 1
                shopping_cart.save()
        except Exception as e:
            return JsonResponse({'success': False, 'error': e})
        return JsonResponse({'success': True})


class ChangeCountAPIView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            shopping_cart_id = json_data.get('id')
            product_count = json_data.get('product_count')

            shopping_cart = Shoppingcart.objects.get(pk=shopping_cart_id)
            if product_count is not None:
                shopping_cart.count = product_count
                shopping_cart.save()
        except Exception as e:
            return JsonResponse({'success': False, 'error': e})
        return JsonResponse({'success': True})


class OrderView(View):
    template_name = 'checkout.html'

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        order_data_with_images = []

        for order in orders:
            img = Images.objects.filter(service=order.service).first()
            if img:
                order.status = order.get_status_display()
                order.service.image = img
                order_data_with_images.append({'order': order, 'image': img})

        context = {'services_data': order_data_with_images}
        return render(request, self.template_name, context)

    def post(self, request):
        shopping_cart_items = Shoppingcart.objects.filter(user=request.user)

        for item in shopping_cart_items:
            order = Order.objects.create(
                user=request.user,
                service=item.product,
                count=item.count,
                status=1
            )
            order.save()

        return redirect(reverse('checkout'))


class Blog_detailsView(View):
    def get(self, request):
        return render(request, 'blog-details.html')


class Add_productView(View):
    template = 'add_product.html'
    contex = {}

    def get(self, request):
        return render(request, self.template, self.contex)

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('desc')
        price = request.POST.get('price')
        images = request.FILES.getlist('images')
        brand = request.POST.get('brand')
        category = request.POST.get('category')

        service = Product.objects.create(
            product_name=title,
            description=description,
            price=price,
            brand=brand
        )
        service.save()
        for img in images:
            image = Images.objects.create(
                image=img,
                service=service
            )
            image.save()
        product_id = service.id
        category_save = Category.objects.create(
            name=category,
            product_id_id=product_id
        )
        category_save.save()
        return redirect('/')


class CommentView(View):
    template = 'comment.html'
    contex = {}

    def get(self, request):
        return render(request, self.template, self.contex)

    def post(self, request):
        message = request.POST.get('message')
        profession = request.POST.get('prof')
        is_anonym = request.POST.get('is_anonymous')

        user = None if is_anonym == 'on' else request.user
        comment = Commment.objects.create(
            message=message,
            user=user,
            profession=profession
        )
        comment.save()
        return redirect('/')
