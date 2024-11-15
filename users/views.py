from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from .models import PQRS, Commets
from django.http import HttpResponseRedirect, Http404
from .forms import PQRSCreateForm, CommentForm, SearchForm, FileFormSet
from django.db.models import Q

@login_required
def openPQRS(request):
    formSearch = SearchForm()
    userType = request.user

    if userType.is_staff:
        openPQRS = PQRS.objects.filter(status="Open")
    else:
        openPQRS = PQRS.objects.filter(typePQRS__area_redirect=userType.area, status="Open")

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
        closePQRS = PQRS.objects.filter(typePQRS__area_redirect=userType.area, status="Close")
    
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
        expirePQRS = PQRS.objects.filter(typePQRS__area_redirect=userType.area, status="Expired")
        
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
    if request.method == 'POST':
        pqrs_form = PQRSCreateForm(request.POST)
        file_formset = FileFormSet(request.POST, request.FILES)
        
        if pqrs_form.is_valid() and file_formset.is_valid():
            pqrs_instance = pqrs_form.save(user=request.user)
            for form in file_formset:
                if form.is_valid() and not form.cleaned_data.get('DELETE'):
                    file = form.save(commit=False)
                    file.pqrs = pqrs_instance
                    file.save()
                else:
                    print(f"Form {form.prefix} errors: {form.errors}")
                    
            return redirect('home')
    else:
        pqrs_form = PQRSCreateForm()
        file_formset = FileFormSet()
    return render(request, 'createdpqrs.html', {'pqrs_form': pqrs_form, 'file_formset': file_formset})

@login_required
def pqrs(request, num):
    formComment = CommentForm()
    
    try:
        find_pqrs = get_object_or_404(PQRS.objects.filter(num=num))
    except Http404:
        return redirect("home")
    
    if find_pqrs.typePQRS.area_redirect != request.user.area and not request.user.is_staff:
        return redirect("home")

    comments = Commets.objects.filter(pqrs=find_pqrs)

    if request.method == "POST":
        formComment = CommentForm(request.POST, request.FILES)
        if formComment.is_valid():
            formComment.save(user=request.user, pqrs=find_pqrs)
            return redirect('findpqrs', num=num)

    return render(request, 'pqrs.html', {
        'pqrs': find_pqrs,
        'formComment': formComment,
        'comments': comments
    })

@login_required
def closedPQRS(request, num):
    pqrs = get_object_or_404(PQRS, num=num)
    try:
        pqrs.closePQRS(request.user.username)
        return redirect('home')
    except Http404:
        return redirect('home')
