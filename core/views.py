from django.shortcuts import render
from .forms import ContactForm, ProductModelForm
from django.contrib import messages
from .models import Product
from django.shortcuts import redirect


def index(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'index.html', context)


def contact(request):
    form = ContactForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()

            messages.success(request, 'E-mail enviado com sucesso!')
            form = ContactForm()
        else:
            messages.error(request, 'Erro ao enviar e-mail')
            form = ContactForm()
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


def product(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = ProductModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Produto cadastrado com sucesso.')
                form = ProductModelForm()
            else:
                messages.error(request, 'Erro ao salvar o produto.')
        else:
            form = ProductModelForm()
        context = {
            'form': form
        }
        return render(request, 'product.html', context)
    else:
        return redirect('index')