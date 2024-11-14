from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from .models import PQRS, Commets
from django.http import HttpResponseRedirect, Http404
from .forms import PQRSCreateForm, CommentForm, SearchForm
from django.db.models import Q

@login_required
def openPQRS(request):
    formSearch = SearchForm()
    userType = request.user
    userArea = userType.area

    if userType.is_staff:
        openPQRS = PQRS.objects.filter(status="Open")
    else:
        openPQRS = PQRS.objects.filter(
            Q(userCreated=userType) | Q(typePQRS__area_redirect=userArea),
            status="Open"
        ).distinct()

    if request.method == "POST":
        formSearch = SearchForm(request.POST)
        if formSearch.is_valid():
            search = formSearch.cleaned_data.get('search')
            if search:
                openPQRS = openPQRS.filter(asociado=search)
                formSearch = SearchForm()

    paginator = Paginator(openPQRS, 10)
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
    if userType.is_staff:
        closePQRS = PQRS.objects.filter(status="Close")
    else:    
        closePQRS = PQRS.objects.filter(
            Q(userCreated=userType) | Q(typePQRS__area_redirect=userType.area), status="Close")
    
    if request.method == 'POST':
        formSearch = SearchForm(request.POST)
        if formSearch.is_valid():
            search = formSearch.cleaned_data.get('search')
            closePQRS = closePQRS.filter(asociado=search)
            formSearch = SearchForm()

    paginator = Paginator(closePQRS, 10)
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
    if userType.is_staff:
        expirePQRS = PQRS.objects.filter(status="Expired")
    else:    
        expirePQRS = PQRS.objects.filter(
            Q(userCreated=userType) | Q(typePQRS__area_redirect=userType.area), status="Open")
        
    if request.method == 'POST':
        formSearch = SearchForm(request.POST)
        if formSearch.is_valid():
            search = formSearch.cleaned_data.get('search')
            expirePQRS = expirePQRS.filter(asociado=search)
            formSearch = SearchForm()
    
    paginator = Paginator(expirePQRS, 10)
    page_number = request.GET.get('page', 1)
    try:
        pqrs_expired = paginator.page(page_number)
    except EmptyPage:
        return HttpResponseRedirect(f"{request.path}?page=1")
    return render(request, 'expired_pqrs.html', {'pqrs': pqrs_expired, 'formSearch': formSearch})

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
    try:
        find_pqrs = get_object_or_404(
            PQRS.objects.filter(
                Q(userCreated=request.user.username) | Q(typePQRS__area_redirect=request.user.area),
                id=id
            )
        )
    except Http404:
        return redirect("home")

    comments = Commets.objects.filter(pqrs=find_pqrs)

    if request.method == "POST":
        formComment = CommentForm(request.POST, request.FILES)
        if formComment.is_valid():
            formComment.save(user=request.user, pqrs=find_pqrs)
            return redirect('findpqrs', id=id)

    return render(request, 'pqrs.html', {
        'pqrs': find_pqrs,
        'formComment': formComment,
        'comments': comments
    })

@login_required
def closedPQRS(request, id):
    pqrs = get_object_or_404(PQRS, id=id)
    try:
        pqrs.closePQRS(request.user.username)
        return redirect('home')
    except Http404:
        return redirect('home')