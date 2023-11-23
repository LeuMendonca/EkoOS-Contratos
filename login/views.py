from django.shortcuts import render,redirect
from .forms import FormLogin
from django.http import HttpResponse
from .models import Login,Empresa,EkUsuarioEmpresa
import psycopg2
from django.db import connection

# Create your views here.

def login(request):
    model_empresa = Empresa.objects.all()
    formulario = FormLogin(request.POST)
    formulario = FormLogin()
    status = request.GET.get('status')
    print(status)
    
    return render(request,'login/login.html',{'formulario':formulario,'empresas':model_empresa,'status':status})


def autenticar_login(request):
    model = Login
    
    usuario = request.POST.get('login')
    senha = request.POST.get('password')
    empresa = request.POST.get('empresa')
    
    if model.objects.filter(login=usuario,password=senha).exists():
        cod_usuario = Login.objects.get(login=usuario,password=senha).id_usuario

        cursor = connection.cursor()
        cursor.execute(f'''
                       select * from ek_usuario_empresa where cod_usuario in 
                                    (select cod_usuario from ek_usuario where nome_usuario = '{usuario}' and senha = '{senha}')
                                                and cod_empresa = {empresa}
                       ''')
        valida_empresa = cursor.fetchall()
        
        if (valida_empresa):

            cursor.execute(f'select nome_empresa from ek_Empresa where num_empresa = {empresa}')
            nome_empresa = cursor.fetchall()[0][0]
            
            request.session['num_empresa'] = empresa
            request.session["nome_empresa"] = nome_empresa
            request.session['cod_usuario'] = cod_usuario
            request.session['nome_usuario'] = usuario
            return redirect('index')
    else:
        return redirect(f'/login/?status=1')

def sair(request):
    request.session.flush()
    return redirect('login')
