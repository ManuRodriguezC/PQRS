from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from .models import PQRS, Commets, Files
from adminUser.models import TypesPQRS
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *

@login_required
def openPQRS(request):
    formSearch = SearchForm()
    userType = request.user

    if userType.permissions == "superadmin" or userType.permissions == "coordinador":
        openPQRS = PQRS.objects.filter(status="Open")
    else:
        openPQRS = PQRS.objects.filter(areas__icontains=userType.area, status="Open")

    if request.method == "POST":
        formSearch = SearchForm(request.POST)
        if formSearch.is_valid():
            search = formSearch.cleaned_data.get('search')
            if search:
                try:
                    search_int = int(search)
                    openPQRS = openPQRS.filter(asociado=search_int)
                except ValueError:
                    openPQRS = openPQRS.filter(num=search)
                formSearch = SearchForm()

    paginator = Paginator(openPQRS, 5)
    page_number = request.GET.get('page', 1)
    try:
        pqrs_open = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseRedirect(f"{request.path}?page=1")

    return render(request, 'open_pqrs.html', {'pqrs': pqrs_open, 'formSearch': formSearch})

@login_required
def closePQRS(request):
    formSearch = SearchForm()
    userType = request.user
    if userType.permissions == "superadmin" or userType.permissions == "coordinador":        
        closePQRS = PQRS.objects.filter(status="Close")
    else:
        closePQRS = PQRS.objects.filter(areas__icontains=userType.area, status="Close")
    
    if request.method == 'POST':
        formSearch = SearchForm(request.POST)
        if formSearch.is_valid():
            search = formSearch.cleaned_data.get('search')
            if search:
                try:
                    search_int = int(search)
                    closePQRS = closePQRS.filter(asociado=search_int)
                except ValueError:
                    closePQRS = closePQRS.filter(num=search)
                formSearch = SearchForm()
                
    paginator = Paginator(closePQRS, 5)
    page_number = request.GET.get('page', 1)
    try:
        pqrs_close = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseRedirect(f"{request.path}?page=1")
    return render(request, 'close_pqrs.html', {'pqrs': pqrs_close, 'formSearch': formSearch})

@login_required
def expiredPQRS(request):
    formSearch = SearchForm()
    userType = request.user
    if userType.permissions == "superadmin" or userType.permissions == "coordinador":        
        expirePQRS = PQRS.objects.filter(status="Expired")
    else:
        expirePQRS = PQRS.objects.filter(areas__icontains=userType.area, status="Expired")
        
    if request.method == 'POST':
        formSearch = SearchForm(request.POST)
        if formSearch.is_valid():
            search = formSearch.cleaned_data.get('search')
            if search:
                try:
                    search_int = int(search)
                    expirePQRS = openPQRS.filter(asociado=search_int)
                except ValueError:
                    expirePQRS = openPQRS.filter(num=search)
                formSearch = SearchForm()
    
    paginator = Paginator(expirePQRS, 5)
    page_number = request.GET.get('page', 1)
    try:
        pqrs_expired = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseRedirect(f"{request.path}?page=1")
    return render(request, 'expired_pqrs.html', {'pqrs': pqrs_expired, 'formSearch': formSearch})

@login_required
def waitResponsePQRS(request):
    formSearch = SearchForm()
    userType = request.user
    if userType.permissions == "superadmin" or userType.permissions == "coordinador":        
        waitPQRS = PQRS.objects.filter(status="Wait")
    else:
        waitPQRS = PQRS.objects.filter(areas__icontains=userType.area, status="Wait")
        
    if request.method == 'POST':
        formSearch = SearchForm(request.POST)
        if formSearch.is_valid():
            search = formSearch.cleaned_data.get('search')
            if search:
                try:
                    search_int = int(search)
                    waitPQRS = waitPQRS.filter(asociado=search_int)
                except ValueError:
                    waitPQRS = waitPQRS.filter(num=search)
                formSearch = SearchForm()
    
    paginator = Paginator(waitPQRS, 5)
    page_number = request.GET.get('page', 1)
    try:
        pqrs_wait = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseRedirect(f"{request.path}?page=1")
    return render(request, 'wait_pqrs.html', {'pqrs': pqrs_wait, 'formSearch': formSearch})

@login_required
def closeForUserPQRS(request):
    formSearch = SearchForm()
    userType = request.user
    if userType.permissions == "superadmin" or userType.permissions == "coordinador":
        closedForUser = PQRS.objects.filter(status="CloseForUser")
    else:
        closedForUser = PQRS.objects.filter(areas__icontains=userType.area, status="CloseForUser")
        
    if request.method == 'POST':
        formSearch = SearchForm(request.POST)
        if formSearch.is_valid():
            search = formSearch.cleaned_data.get('search')
            if search:
                try:
                    search_int = int(search)
                    closedForUser = closedForUser.filter(asociado=search_int)
                except ValueError:
                    closedForUser = closedForUser.filter(num=search)
                formSearch = SearchForm()
    
    paginator = Paginator(closedForUser, 5)
    page_number = request.GET.get('page', 1)
    try:
        pqrs_closed_for_user = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseRedirect(f"{request.path}?page=1")
    return render(request, 'closeUser_pqrs.html', {'pqrs': pqrs_closed_for_user, 'formSearch': formSearch})


@login_required
def createdPQRS(request):
    if request.method == 'POST':
        pqrs_form = PQRSCreateForm(request.POST)
        file_formset = FileFormSet(request.POST, request.FILES)
        
        if pqrs_form.is_valid() and file_formset.is_valid():
            try:
                # Guardar la instancia principal PQRS
                pqrs_instance = pqrs_form.save(user=request.user, path=request.path)

                # Guardar los archivos asociados
                for form in file_formset:
                    if form.is_valid() and not form.cleaned_data.get('DELETE'):
                        file = form.save(commit=False)
                        file.pqrs = pqrs_instance
                        file.save()
                    else:
                        print(f"Form {form.prefix} errors: {form.errors}")
                
                # Agregar un mensaje de éxito
                messages.success(request, "PQRS creada exitosamente.")

            except Exception as e:
                # Registrar y manejar errores
                print(f"Error al procesar la solicitud: {e}")
                messages.error(request, "Hubo un problema al enviar la notificacion.")

            # Redirigir al usuario a una página de confirmación o inicio
            return redirect('home')
    else:
        pqrs_form = PQRSCreateForm()
        file_formset = FileFormSet()

    return render(request, 'createdpqrs.html', {'pqrs_form': pqrs_form, 'file_formset': file_formset})


@login_required
def pqrs(request, num):
    formComment = CommentForm()
    formResponse = ResponsePQRSForm()
    
    try:
        find_pqrs = get_object_or_404(PQRS.objects.filter(num=num))
    except Http404:
        return redirect("home")
    
    listAreas = find_pqrs.areas.split(",")
    if str(request.user.area) not in listAreas and not (request.user.permissions == "superadmin" or request.user.permissions == "coordinador"):
        return redirect("home")

    formShare = ShareForm(areas=find_pqrs.areas)

    comments = Commets.objects.filter(pqrs=find_pqrs)
    files = Files.objects.filter(pqrs=find_pqrs)

    if request.method == "POST":
        if 'submit_comment' in request.POST:    
            formComment = CommentForm(request.POST, request.FILES)
            if formComment.is_valid():
                formComment.save(user=request.user, pqrs=find_pqrs)
                messages.success(request, "Se ha agregado el comentario exitosamente!")
                return redirect('findpqrs', num=num)

        if 'submit_response' in request.POST:    
            formResponse = ResponsePQRSForm(request.POST, request.FILES)
            if formResponse.is_valid():
                formResponse.save(user=request.user, pqrs=find_pqrs)
                messages.success(request, "Se ha enviado la respuesta de forma exitosa!")
                return redirect('home')

        if 'submit_share' in request.POST:
            formShare = ShareForm(data=request.POST, areas=find_pqrs.areas)
            if formShare.is_valid():
                formShare.process(find_pqrs)
                find_pqrs.save()
                messages.success(request, "Se ha compartido la pqrs con el area de forma exitosa!")
                return redirect('findpqrs', num=num)
                

    return render(request, 'pqrs.html', {
        'pqrs': find_pqrs,
        'formComment': formComment,
        'formResponse': formResponse,
        'formShare': formShare,
        'comments': comments,
        'files': files
    })

@login_required
def updatePqrs(request, num):
    pqrs = get_object_or_404(PQRS, num=num)
    if pqrs.status != "Open":
        return redirect('findpqrs', num=pqrs.num)

    if request.method == 'POST':
        form = PQRSUpdateForm(request.POST, instance=pqrs)
        if form.is_valid():
            form.save()
            return redirect('findpqrs', num=pqrs.num)
    else:
        form = PQRSUpdateForm(instance=pqrs)
    return render(request, 'update_pqrs.html', {'form': form})

@login_required
def closedPQRS(request, num):
    pqrs = get_object_or_404(PQRS, num=num)
    try:
        pqrs.closePQRS(request.user.username)
        return redirect('home')
    except Http404:
        return redirect('home')

def checkSuccessfull(request, num, token):
    try:
        pqrs = get_object_or_404(PQRS, num=num, tokenControl=token)
        if pqrs.status != "Wait":
            print("Ya se cerro el caso")
            return redirect('success')
        pqrs.closedForUser()
        pqrs.save()
        
        return redirect('success')
    except Http404:
        return render(request, '404.html', status=404)

def checkBad(request, num, token):
    try:
        pqrs = get_object_or_404(PQRS, num=num, tokenControl=token)
        if pqrs != "Wait":
            return redirect('success')
        pqrs.status = 'Open'
        pqrs.tokenControl = ""
        pqrs.save()
        return redirect('failed')
    except Http404:
        return render(request, '404.html', status=404)

def success(request):
    return render(request, 'successfull.html')

def failed(request):
    return render(request, 'failed.html')
