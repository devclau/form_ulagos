from django.shortcuts import render, redirect
from django.db import connection, DatabaseError
from django.contrib import messages
from appcontacto.forms  import FormularioLogin, FormularioContacto
from django.conf import settings
import requests
from django.http import HttpResponse
from appcontacto.models import T_UGC_ACTUALIZA_ANTECEDENTES

#import os
#import cx_Oracle
#cx_Oracle.init_oracle_client(lib_dir=r"/opt/oracle/instantclient_21_8")
# Create your views here.

def login_contacto(request):
    if request.method == 'POST':
        form = FormularioLogin(request.POST)
        secret_key = settings.RECAPTCHA_SECRET_KEY

        data = {
            'response': request.POST.get('g-recaptcha-response'),
            'secret': secret_key
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()
      
        if not result_json.get('success'):
            return redirect('/appcontacto/')

        if form.is_valid():
            PERS_COD = form.cleaned_data["RUT"]
            PERS_DV = form.cleaned_data["DV"]
            reg  = regiones()
            region_comuna_destino = region_comuna_seleccionada(PERS_COD)
           
            with connection.cursor() as cursor:
                try:
                    if row_count_select(PERS_COD, PERS_DV) == 0:
                        SQL = f"""SELECT "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."PERS_COD" AS RUT,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."PERS_DV" AS DV,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."NOMBRES" AS NOMBRES,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."APE_PATERNO" AS APE_PATERNO,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."APE_MATERNO" AS APE_MATERNO,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."FECHA_NACIMIENTO" AS FECHA_NACIMIENTO,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."CAMPUS" AS CAMPUS,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."COD_CARRERA" AS COD_CARRERA,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."TELEFONO" AS TELEFONO1,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."TELEFONO2" AS TELEFONO2,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."DIRECCION_PARTICULAR" AS DIRECCION,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."DIRECCION_NUM_PARTICULAR" AS DIRECCION_NUMERO,
                        "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."EMAIL_PERSONAL" AS CORREO_PARTICULAR
                        FROM "DELFOS"."BIE_MATRICULA_ANTECEDENTES"
                        WHERE "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."PERS_COD" = {PERS_COD} AND "DELFOS"."BIE_MATRICULA_ANTECEDENTES"."PERS_DV" = {PERS_DV} """
                        cursor.execute(SQL)#ORIGEN
                    else:
                        cursor.execute(f"""Select * FROM (SELECT * FROM "DELFOS"."T$UGC_ACTUALIZA_ANTECEDENTES" 
                        WHERE "DELFOS"."T$UGC_ACTUALIZA_ANTECEDENTES"."RUT" = {PERS_COD} AND  "DELFOS"."T$UGC_ACTUALIZA_ANTECEDENTES"."DV" = {PERS_DV}
                        ORDER BY "DELFOS"."T$UGC_ACTUALIZA_ANTECEDENTES"."ID" DESC  ) 
                        where rownum = 1""")#DESTINO
                    col_names = [desc[0] for desc in cursor.description]
                    rows = dict(zip(col_names, cursor.fetchone())) 
                    return render(request, 'form_contacto/info_perfil.html',{'data':rows,'regiones': reg, 'region_comuna_destino':region_comuna_destino})
                except:
                    messages.add_message(request, messages.ERROR, 'RUT no encontrado por favor vuelva a ingresar.')
                    messages.add_message(request, messages.WARNING, form.errors)
                    print(f"Error de sql login_contacto")
                    cursor.close()
                    return redirect('/appcontacto/')
                
    else:
        form = FormularioLogin()
        return render(request,'form_contacto/login.html', {'form':form, 'site_key': settings.RECAPTCHA_SITE_KEY})
 

def guardar(request):
    if request.method == 'POST':
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        RUT = request.POST['RUT']
        DV = request.POST['DV']
        form = FormularioContacto(request.POST)
        if form.is_valid():
            
            alumno = T_UGC_ACTUALIZA_ANTECEDENTES(
                RUT  = form.cleaned_data['RUT'],
                DV  = form.cleaned_data['DV'],
                TELEFONO1 = form.cleaned_data['TELEFONO1'],
                TELEFONO2 = form.cleaned_data['TELEFONO2'],
                DIRECCION = form.cleaned_data['DIRECCION'],
                COD_REGION = form.cleaned_data['COD_REGION'],
                COD_COMUNA = form.cleaned_data['COD_COMUNA'],
                DIRECCION_NUMERO = form.cleaned_data['DIRECCION_NUMERO'],
                CORREO_PARTICULAR = form.cleaned_data['CORREO_PARTICULAR'],
                OBSERVACIONES = form.cleaned_data['OBSERVACIONES'],
            )
            alumno.save()
            messages.add_message(request,messages.SUCCESS, f'Datos guardados por:   {nombres} {apellidos} {RUT} - {DV} ')
            return render(request, 'form_contacto/save.html',{})
    else: 
       return HttpResponse('Usuario No autorizado!')


def row_count_select(perscod, dv):
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"select * from DELFOS.T$UGC_ACTUALIZA_ANTECEDENTES WHERE RUT = {perscod} AND DV={dv} ") #TABLA DESTINO
            registros = len(cursor.fetchall())
            return registros   
        except DatabaseError as e:
            print(f"Error de sql:  row_count_select {e} ")
            cursor.close


def regiones():
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"SELECT  * FROM DELFOS.GLO_REGIONES") #TABLA ORIGEN COMUNAS
            regiones = cursor.fetchall()
            return regiones

        except DatabaseError as e:
            print(f"Error de sql:  regiones {e}")
            cursor.close


def comunas(request):
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"SELECT  * FROM DELFOS.GLO_COMUNAS") #TABLA ORIGEN COMUNAS
            col_names = [desc[0] for desc in cursor.description]
            comunas = dict(zip(col_names, cursor.fetchall()))
            return comunas
        except DatabaseError as e:
            print(f"Error de sql:  comunas {e}")
            cursor.close


def regiones_comunas(request):
    reg = request.GET.get('region')
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                f"""SELECT  DELFOS.GLO_COMUNAS.COMU_COD , DELFOS.GLO_COMUNAS.COMU_DES, DELFOS.GLO_COMUNAS.COMU_REGION 
                FROM DELFOS.GLO_COMUNAS 
                INNER JOIN DELFOS.GLO_REGIONES ON DELFOS.GLO_REGIONES.REGI_COD  = DELFOS.GLO_COMUNAS.COMU_REGION 
                WHERE DELFOS.GLO_REGIONES.REGI_COD = {reg}""") #TABLA ORIGEN COMUNAS
           
            comunas = cursor.fetchall()
            
            return render(request, 'form_contacto/combo_comunas.html',{'comunas':comunas})
        except DatabaseError as e:
            print(f"Error de sql:  regiones_comunas {e}")
            cursor.close


def region_comuna_seleccionada(perscod):
    with connection.cursor() as cursor:
        try:
            SQL = f"""SELECT DELFOS.GLO_COMUNAS.COMU_COD , DELFOS.GLO_COMUNAS.COMU_DES, DELFOS.GLO_COMUNAS.COMU_REGION, DELFOS.GLO_REGIONES.REGI_DES
                FROM DELFOS.GLO_COMUNAS
                INNER JOIN DELFOS.GLO_REGIONES  ON DELFOS.GLO_REGIONES.REGI_COD = DELFOS.GLO_COMUNAS.COMU_REGION 
                INNER JOIN DELFOS.T$UGC_ACTUALIZA_ANTECEDENTES ON DELFOS.T$UGC_ACTUALIZA_ANTECEDENTES.COD_COMUNA = DELFOS.GLO_COMUNAS.COMU_COD WHERE DELFOS.T$UGC_ACTUALIZA_ANTECEDENTES.RUT = {perscod} AND  DELFOS.T$UGC_ACTUALIZA_ANTECEDENTES.FECHA_REGISTRO  = (SELECT MAX (DELFOS.T$UGC_ACTUALIZA_ANTECEDENTES.FECHA_REGISTRO) FROM DELFOS.T$UGC_ACTUALIZA_ANTECEDENTES)"""
            
            cursor.execute(SQL)
            comuna_seleccionada = cursor.fetchall()
            
            return comuna_seleccionada

        except DatabaseError as e:
             print(f"Error de sql:  comuna_seleccionada {e}")


def salir(request):
    return redirect('/appcontacto/')

