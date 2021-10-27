from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import ConfirmationCode
from .forms import NewUserForm
from .tasks import send_verified_link


def registration(request):
    form = NewUserForm(request.POST or None)
    message = "Fill the blank"
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['email'], is_active=True):
            message = "Check your mail"
            user = User.objects.get(email=request.POST['email'])
            user.set_password(request.POST['password'])
            code = ConfirmationCode.objects.create(user=user)
            send_verified_link.apply_async([request.POST['email'], code.code], )
            return render(request, 'index.html', {'form':form, 'message':message})
        if form.is_valid():
            message = "Check your mail"
            user = form.save()
            user.is_active = False
            user.save()
            message = "OK"
            code = ConfirmationCode.objects.create(user=user)
            send_verified_link.apply_async([request.POST['email'], code.code], )
            return render(request, 'index.html', {'form':form, 'message':message})
        return render(request, 'index.html', {'form':form, 'message':form.errors})
    return render(request, 'index.html', {'form':form,'message':message})
