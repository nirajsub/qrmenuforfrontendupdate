from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, CreateView, FormView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from mymenu.models import *
from .forms import *

class SearchView(TemplateView):
    template_name = "search.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(
            Q(name__icontains=kw) | Q(description__icontains=kw))
        print(results)
        context = {
            "results": results,
        }
        return context

def HomeView(request, pk):
    template_name = "home.html"
    mainuser = Admin.objects.get(uuid=pk)
    category = Category.objects.filter(user=mainuser)
    if request.method == "POST":
        order.delete()
        return redirect("home")
    context = {
        'mainuser':mainuser,
        'category':category,
    }
    return render(request, template_name, context)

# def ExclusiveView(request, pk):
#     template_name = "exclusive.html"
#     mainuser = MainUser.objects.get(uuid=pk)
#     category = Category.objects.filter(user=mainuser)

#     context = {
#         'category':category
#     }
#     return render(request, template_name, context)

# def SpecialView(request, pk):
#     template_name = "special.html"
#     mainuser = MainUser.objects.get(uuid=pk)
#     category = Category.objects.filter(user=mainuser)
#     context = {
#         'category':category
#     }
#     return render(request, template_name, context)

# def updateItem(request):
#     data = json.loads(request.body)
#     productId = data['productId']
#     action = data['action']
#     productprice = (float(data['form']['productprice']))
#     product = Product.objects.get(id=productId)
#     order = Orders.objects.get(confirmed = False)
#     orderItem , created = Items.objects.get_or_create(order=order, product=product, price=productprice)

#     if action =='add':
#         orderItem.quantity = (orderItem.quantity +1)
#     elif action =='remove':
#         orderItem.quantity = (orderItem.quantity -1)
#     elif action =='delete':
#         orderItem.quantity = 0
#     orderItem.save()
#     if orderItem.quantity <= 0:
#         orderItem.delete()
#     print('Action:', action)
#     print('productId:', productId)
#     return JsonResponse('Item is added to the table order', safe=False)



@login_required
def Dashboard(request):
    if request.user.is_staff:
        template_name = "dashboard/dashboard.html"
        mainuser = Admin.objects.get(user=request.user)
        category = Category.objects.filter(user=mainuser)
        # product = Product.objects.filter(category=category)
        context = {
            'mainuser':mainuser,
            # 'product':product,
            'category':category
        }
        return render(request, template_name, context)
    else:
        return redirect('login')

@login_required
def CategoryDetail(request, pk):
    template_name = "dashboard/categorydetail.html"
    category = Category.objects.filter(id=pk)
    context = {
        'category':category
    }
    return render(request, template_name, context)

@login_required
def EditProduct(request, pk):
    template_name = "dashboard/editproduct.html"
    product = Product.objects.get(id=pk)
    form = ProductForm(instance = product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
        return redirect("dashboard")
    context = {
        'product':product,
        'form':form
    }
    return render(request, template_name, context)

class AddProduct(CreateView):
    template_name = "dashboard/addproduct.html"
    form_class = ProductForm
    success_url = reverse_lazy("dashboard")
    
    def form_valid(self, form, **kwargs):
        category = Category.objects.get(id=self.kwargs.get('pk'))
        name = form.cleaned_data.get('name')
        image = form.cleaned_data.get('image')
        price = form.cleaned_data.get('price')
        description = form.cleaned_data.get('description')
        product = Product.objects.create(category=category, name=name, price=price, image=image)
        return redirect("dashboard")

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

def DeleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    
    product.delete()
    context = {
        'product':product
    }
    return redirect('dashboard')
    return render(request, context)

def DeleteCategory(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    context = {
        'category':category
    }
    return redirect('dashboard')
    return render(request, context)

class AddCategory(CreateView):
    template_name = "dashboard/addcategory.html"
    form_class = CategoryForm
    success_url = reverse_lazy("dashboard")
    
    def form_valid(self, form):
        mainuser = Admin.objects.get(user=self.request.user)
        name = form.cleaned_data.get('name')
        image = form.cleaned_data.get('image')
        category = Category.objects.create(user=mainuser, name=name, image=image)
        return super().form_valid(form)
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

@login_required
def EditCategory(request, pk):
    template_name = "dashboard/editcategory.html"
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance = category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
        return redirect("dashboard")
    context = {
        'category':category,
        'form':form
    }
    return render(request, template_name, context)

@login_required
def AllSpecial(request):
    template_name = "dashboard/allspecial.html"
    mainuser = Admin.objects.get(user=request.user)
    category = Category.objects.filter(user=mainuser)
    context = {
        'mainuser':mainuser,
        'category':category,
    }
    return render(request, template_name, context)

@login_required
def AddSpecial(request, pk):
    product = Product.objects.get(id=pk)
    product.todays_special = True
    product.save()
    context = {
        'product':product,
    }
    return redirect('allspecial')
    return render(request, context)

@login_required
def RemoveSpecial(request, pk):
    template_name = "dashboard/removespecial.html"
    product = Product.objects.get(id=pk)
    product.todays_special = False
    product.save()
        
    context = {
        'product':product,
    }
    return redirect('allspecial')
    return render(request, template_name, context)

@login_required
def AllExclusive(request):
    template_name = "dashboard/allexclusive.html"
    mainuser = Admin.objects.get(user=request.user)
    category = Category.objects.filter(user=mainuser)
    context = {
        'mainuser':mainuser,
        'category':category,
    }
    return render(request, template_name, context)

@login_required
def AddExclusive(request, pk):
    template_name = "dashboard/addexclusive.html"
    product = Product.objects.get(id=pk)
    form = ExclusiveForm(instance = product)
    if request.method == 'POST':
        form = ExclusiveForm(request.POST, instance = product)
        if form.is_valid():
            product.exclusive = True
            product.save()
            form.save()
            return redirect('allexclusive')
    else:
        form = ExclusiveForm()
    context = {
        'product':product,
        'form':form
    }
    return render(request, template_name, context)

@login_required
def EditExclusive(request, pk):
    template_name = "dashboard/editexclusive.html"
    exclusive = Product.objects.get(id=pk)
    form = ExclusiveForm(instance = exclusive)
    if request.method == 'POST':
        form = ExclusiveForm(request.POST, instance=exclusive)
        if form.is_valid():
            form.save()
        return redirect("allexclusive")
    context = {
        'exclusive':exclusive,
        'form':form,
    }
    return render(request, template_name, context)

def DeleteExclusive(request, pk):
    exc = Product.objects.get(id=pk)
    exc.exclusive = False
    exc.product_discount = 0
    exc.product_newprice = 0
    exc.save()
    context = {
        'exc':exc
    }
    return redirect('allexclusive')
    return render(request, context)

class RegistrationView(CreateView):
    template_name = "registration/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        email = form.cleaned_data.get("email")
        if User.objects.filter(username=username).exists():
            error = ("Sorry! User with this username already exists.")
            return render(self.request, self.template_name, {'error':error})
        if User.objects.filter(email=email).exists():
            error1= ("Sorry! User with this email already exists. please try new email.")
            return render(self.request, self.template_name, {'error1':error1})
        if password1 == password2:
            user = User.objects.create_user(username, email, password1, is_staff=True)
            form.instance.user = user
        else:
            error2= ("Password didn't match")
            return render(self.request, self.template_name, {'error2':error2})
        return super().form_valid(form)
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url



class LoginView(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("dashboard")
    
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None:
            if usr is not None and Admin.objects.filter(user=usr).exists():
                login(self.request, usr)
            else:
                error_message = ("Invalid Username")
                return render(self.request, self.template_name, {'error_message':error_message})
        else:
            error_message = ("Invalid Username or password")
            return render(self.request, self.template_name, {'error_message':error_message})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
        

