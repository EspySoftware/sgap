from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import FormularioCita
from .models import Cita

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html',
                              {'form': UserCreationForm,
                               'error': 'El usuario ya existe en la base de datos'},
                              )
        return render(request, 'signup.html',
                      {'form': UserCreationForm,
                       'error': 'Las contraseñas no coinciden'},
                      )


def citas(request):
    if request.user.username == 'espy':
        citas = Cita.objects.all()  # VISTA DEL ORIENTADOR
    else:
        citas = Cita.objects.filter(user=request.user)  # VISTA DEL USUARIO
    return render(request, 'citas.html', {
        'citas': citas
    })


def detalle_cita(request, id_cita):
    if request.user.username == 'espy':
        if request.method == "GET":
            cita = get_object_or_404(Cita, pk=id_cita)
            form = FormularioCita(instance=cita)
            return render(request, 'detalle_cita.html', {'cita': cita, 'form': form})
        else:
            try:
                cita = get_object_or_404(Cita, pk=id_cita)
                form = FormularioCita(request.POST, instance=cita)
                form.save()
                return redirect('citas')
            except ValueError:
                return render(request, 'detalle_cita.html', {
                    'cita': cita,
                    'form': form,
                    'error': 'Por favor, verifica los datos ingresados'
                })
    else:
        if request.method == "GET":
            cita = get_object_or_404(Cita, pk=id_cita, user=request.user)
            form = FormularioCita(instance=cita)
            return render(request, 'detalle_cita.html', {'cita': cita, 'form': form})
        else:
            try:
                cita = get_object_or_404(Cita, pk=id_cita, user=request.user)
                form = FormularioCita(request.POST, instance=cita)
                form.save()
                return redirect('citas')
            except ValueError:
                return render(request, 'detalle_cita.html', {
                    'cita': cita,
                    'form': form,
                    'error': 'Por favor, verifica los datos ingresados'
                })


def citas_confirmadas(request):
    if request.user.username == 'espy':
        citas = Cita.objects.filter(estado='C').order_by('fecha')
    else:
        citas = Cita.objects.filter(
            estado='C', user=request.user).order_by('fecha')
    return render(request, 'citas.html', {
        'citas': citas})


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El usuario y/o contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('citas')


def crear_cita(request):
    if request.method == "GET":
        return render(request, 'crear_cita.html', {
            'form': FormularioCita
        })
    else:
        try:
            form = FormularioCita(request.POST)
            nueva_cita = form.save(commit=False)
            nueva_cita.user = request.user
            nueva_cita.save()
            return redirect('citas')
        except ValueError:
            return render(request, 'crear_cita.html', {
                'form': FormularioCita,
                'error': 'Por favor, verifica los datos ingresados'
            })
