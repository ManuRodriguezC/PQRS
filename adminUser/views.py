from django.shortcuts import render, get_object_or_404, redirect
from .forms import AreasForms, TypesPQRSForms
from django.shortcuts import render, redirect
from .utils import generate_random_password
from django.core.mail import EmailMessage
from account.models import CustumUser
from users.models import PQRS
from .models import Areas, TypesPQRS
from .forms import CreateUserForm
from django.conf import settings

def areasAll(request):
    if not request.user.is_staff:
        return redirect('home')

    areas = Areas.objects.all()
    form = AreasForms()
    if request.method == 'POST':
        form = AreasForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('areas')
    return render(request, 'admin/areas.html', {'areas': areas, 'form': form})

def deleteArea(request, id):
    if not request.user.is_staff:
        return redirect('home')
    area = get_object_or_404(Areas, id=id)
    area.delete()
    return redirect('areas')

def typesPQRSAll(request):
    if not request.user.is_staff:
        return redirect('home')
    pqrs = TypesPQRS.objects.all()
    form = TypesPQRSForms()
    if request.method == 'POST':
        form = TypesPQRSForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('typesPQRS')
    return render(request, 'admin/pqrs.html', {'pqrs': pqrs, 'form': form})

def deleteTypePQRS(request, id):
    if not request.user.is_staff:
        return redirect('home')
    pqrs = get_object_or_404(TypesPQRS, id=id)
    pqrs.delete()
    return redirect('typesPQRS')

def updateTypePQRS(request, id):
    if not request.user.is_staff:
        return redirect('home')
    pqrs = get_object_or_404(TypesPQRS, id=id)
    if request.method == 'POST':
        form = TypesPQRSForms(request.POST, instance=pqrs)
        if form.is_valid():
            form.save()
            return redirect('typesPQRS')
    else:
        form = TypesPQRSForms(instance=pqrs)
    return render(request, 'admin/update_pqrs.html', {'form': form})

def users(request):
    if not request.user.is_staff:
        return redirect('home')
    usersAll = CustumUser.objects.all()
    formUser = CreateUserForm()
    if request.method == "POST":
        formUser = CreateUserForm(request.POST)
        if formUser.is_valid():
            user = formUser.save(commit=False)
            password = generate_random_password()
            user.set_password(password)
            user.save()
            email = formUser.cleaned_data.get('email')
            message = f"Hola {user.username},\n\nTu cuenta ha sido creada con éxito al modulo de PQRS Cootratiempo.\n\nTu correo es {email}\nTu contraseña es: {password}\n\nSi deseas cambiar tu contraseña ingresa en olvide contraseña."
            email_message = EmailMessage(
                subject='Tu cuenta ha sido creada',
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )
            email_message.send()
            return redirect('users')
        else:
            print(formUser.errors)
            return render(request, 'users/users.html',
                          {'users': usersAll, 'formUser': formUser, 'error': formUser.errors})
    return render(request, 'users/users.html', {'users': usersAll, 'formUser': formUser})

def updateUser(request, id):
    if not request.user.is_staff:
        return redirect('home')
    user = get_object_or_404(CustumUser, id=id)
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = CreateUserForm(instance=user)
    return render(request, 'users/updateUser.html', {'form': form})

def statistics(request):
    if not request.user.is_staff:
        return redirect('home')
    
    usersActives = CustumUser.objects.filter(is_active=True)
    listUsers = [
        {
            "user": user.username,
            "pqrsCreated": PQRS.objects.filter(userCreated=user.username).count(),
            "pqrsOpen": PQRS.objects.filter(status="Open", userCreated=user.username).count(),
            "pqrsClose": PQRS.objects.filter(status="Close", userCreated=user.username).count(),
            "pqrsExpired": PQRS.objects.filter(status="Expired", userCreated=user.username).count(),
        }
        for user in usersActives]
    return render(request, 'statistics/list.html', {'users': listUsers})