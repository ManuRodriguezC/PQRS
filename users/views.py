from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from .models import PQRS, Commets
from django.http import HttpResponseRedirect
from .forms import PQRSCreateForm, CommentForm
from adminUser.models import Areas
from django.db.models import Q

@login_required
def openPQRS(request):
    userType = request.user
    userArea = userType.area
    if userType.is_staff:
        openPQRS = PQRS.objects.filter(status="Open")
    else:    
        openPQRS = PQRS.objects.filter(
            Q(userCreated=userType) | Q(typePQRS__area_redirect=userArea),
            status="Open"
        ).distinct()

    paginator = Paginator(openPQRS, 10)
    page_number = request.GET.get('page', 1)
    try:
        pqrs_open = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseRedirect(f"{request.path}?page=1")
    return render(request, 'open_pqrs.html', {'pqrs': pqrs_open})

@login_required
def closePQRS(request):
    userType = request.user
    if userType.is_staff:
        closePQRS = PQRS.objects.filter(status="Close")
    else:    
        closePQRS = PQRS.objects.filter(userCreated=userType, status="Close")
    paginator = Paginator(closePQRS, 10)
    page_number = request.GET.get('page', 1)
    try:
        pqrs_close = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseRedirect(f"{request.path}?page=1")
    return render(request, 'close_pqrs.html', {'pqrs': pqrs_close})

@login_required
def expiredPQRS(request):
    userType = request.user
    if userType.is_staff:
        expiredPQRS = PQRS.objects.filter(status="Expired")
    else:    
        expiredPQRS = PQRS.objects.filter(userCreated=userType, status="Open")
    paginator = Paginator(expiredPQRS, 10)
    page_number = request.GET.get('page', 1)
    try:
        pqrs_expired = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseRedirect(f"{request.path}?page=1")
    return render(request, 'expired_pqrs.html', {'pqrs': pqrs_expired})

@login_required
def createdPQRS(request):
    form = PQRSCreateForm()
    if request.method == 'POST':
        form = PQRSCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('home')
    return render(request, 'createdpqrs.html', {'form': form})

@login_required
def pqrs(request, id):
    formComment = CommentForm()
    find_pqrs = PQRS.objects.get(id=id)
    comments = Commets.objects.filter(pqrs=find_pqrs)

    if request.method == "POST":
        formComment = CommentForm(request.POST)
        if formComment.is_valid():
            formComment.save(user=request.user, pqrs=find_pqrs)
            return redirect('findpqrs', id=id)

    return render(request, 'pqrs.html', {
        'pqrs': find_pqrs,
        'formComment': formComment,
        'comments': comments
    })