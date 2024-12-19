from django.shortcuts import render, get_object_or_404, redirect
from .forms import AreasForms, TypesPQRSForms
from django.shortcuts import render, redirect
from .utils import generate_random_password
from django.core.mail import EmailMessage
from account.models import CustumUser
from users.models import PQRS
from .models import Areas, TypesPQRS
from .forms import CreateUserForm, DateForms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .decorators import check_superadmin, check_coordinador
import pandas as pd
from io import BytesIO
from django.http import HttpResponse

@login_required
@check_superadmin()
def areasAll(request):
    areas = Areas.objects.all()
    form = AreasForms()
    if request.method == 'POST':
        form = AreasForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('areas')
    return render(request, 'admin/areas.html', {'areas': areas, 'form': form})

@login_required
@check_superadmin()
def deleteArea(request, id):
    area = get_object_or_404(Areas, id=id)
    area.delete()
    return redirect('areas')

@login_required
@check_superadmin()
def typesPQRSAll(request):
    pqrs = TypesPQRS.objects.all()
    form = TypesPQRSForms()
    if request.method == 'POST':
        form = TypesPQRSForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('typesPQRS')
    return render(request, 'admin/pqrs.html', {'pqrs': pqrs, 'form': form})

@login_required
@check_superadmin()
def deleteTypePQRS(request, id):
    pqrs = get_object_or_404(TypesPQRS, id=id)
    pqrs.delete()
    return redirect('typesPQRS')

@login_required
@check_superadmin()
def updateTypePQRS(request, id):
    pqrs = get_object_or_404(TypesPQRS, id=id)
    if request.method == 'POST':
        form = TypesPQRSForms(request.POST, instance=pqrs)
        if form.is_valid():
            form.save()
            return redirect('typesPQRS')
    else:
        form = TypesPQRSForms(instance=pqrs)
    return render(request, 'admin/update_pqrs.html', {'form': form})

@login_required
@check_superadmin()
def users(request):
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
            
            message = f"""
                Hola {user.username},\n\n
                Tu cuenta ha sido creada con éxito al modulo de PQRS Cootratiempo.\n\n
                Tu nombre de usuario es: {user.username}\n
                Tu correo es {email}\n
                Tu contraseña es: {password}\n\n
                Si deseas cambiar tu contraseña ingresa en olvide contraseña."""
            email_message = EmailMessage(
                subject='Tu cuenta ha sido creada',
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )
            email_message.send()
            return redirect('users')
        else:
            return render(request, 'users/users.html',
                          {'users': usersAll, 'formUser': formUser, 'error': formUser.errors})
    return render(request, 'users/users.html', {'users': usersAll, 'formUser': formUser})

@login_required
@check_superadmin()
def updateUser(request, id):
    user = get_object_or_404(CustumUser, id=id)
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = CreateUserForm(instance=user)
    return render(request, 'users/updateUser.html', {'form': form})

@login_required
@check_superadmin()
def deleteUser(request, id):
    user = get_object_or_404(CustumUser, id=id)
    user.delete()
    return redirect('users')

@login_required
@check_coordinador()
def statistics(request):
    if request.method == 'POST':
        form = DateForms(request.POST)
        if form.is_valid():
            start = form.cleaned_data['dateInit']
            end = form.cleaned_data['dateEnd']
            reports = PQRS.objects.filter(created__range=[start, end])
            data = [{
                'Numero de pqrs': pqrs.num,
                'Tipo de pqrs': pqrs.typePQRS,
                'Nombre': pqrs.name,
                'Cedula': pqrs.asociado,
                'Correo': pqrs.email,
                'Celular': pqrs.phone,
                # 'Fecha de Creacion': pqrs.created,
                'Estado': pqrs.status,
                'Creada por': pqrs.userCreated,
                'Descripcion': pqrs.description
            } for pqrs in reports]
            
            df = pd.DataFrame(data)

            # Crea un buffer en memoria para el archivo Excel
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Reportes")

            # Configura el buffer para lectura
            buffer.seek(0)

            # Configura la respuesta HTTP para descargar el archivo
            response = HttpResponse(
                buffer,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="Reportes_pqrs.xlsx"'

            return response
    else:
        form = DateForms()
            
    usersActives = CustumUser.objects.filter(is_active=True)
    listUsers = [
        {
            "user": user.username,
            "pqrsCreated": PQRS.objects.filter(userCreated=user.username).count(),
            "pqrsOpen": PQRS.objects.filter(status="Open", userCreated=user.username).count(),
            "pqrsWait": PQRS.objects.filter(status="Wait", userCreated=user.username).count(),
            "pqrsClose": PQRS.objects.filter(status="Close", userCreated=user.username).count(),
            "pqrsCloseForUser": PQRS.objects.filter(status="CloseForUser", userCreated=user.username).count(),
            "pqrsExpired": PQRS.objects.filter(status="Expired", userCreated=user.username).count(),
        }
        for user in usersActives]
    return render(request, 'statistics/list.html', {'users': listUsers, 'form': form})