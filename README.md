# Sistema de Gestión para Atención Psicopedagógica

Este proyecto es una aplicación web para la gestión de citas entre estudiantes y orientadores. Permite a los usuarios registrarse, iniciar sesión, crear citas, ver citas pendientes y confirmadas, y gestionar horarios disponibles para las citas.

## Características

- **Registro de usuarios:** Los usuarios pueden registrarse y crear una cuenta.
- **Inicio de sesión:** Los usuarios pueden iniciar sesión en sus cuentas.
- **Gestión de citas:** Los usuarios pueden crear, ver y cancelar citas.
- **Gestión de horarios:** Los administradores pueden definir y gestionar los horarios disponibles para las citas.
- **Roles de usuario:** Diferentes vistas y permisos para usuarios regulares y personal administrativo.

## Tecnologías Utilizadas

- Django
- HTML
- CSS
- JavaScript
- jQuery
- Bootstrap

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/tu_proyecto.git
   cd tu_proyecto
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows usa `env\Scripts\activate`
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realizar migraciones de la base de datos:**
   ```bash
   python manage.py migrate
   ```

5. **Crear un superusuario para el acceso administrativo:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

7. **Acceder a la aplicación en el navegador:**
   ```
   http://127.0.0.1:8000
   ```

## Uso

### Registro de Usuario

Los usuarios pueden registrarse en la página de registro proporcionando un nombre de usuario y una contraseña.

### Inicio de Sesión

Los usuarios pueden iniciar sesión en la página de inicio de sesión proporcionando su nombre de usuario y contraseña.

### Crear Cita

Los usuarios pueden crear una cita llenando el formulario de creación de citas. Si el usuario no es personal administrativo, ciertos campos serán predeterminados y ocultos.

### Ver Citas

Los usuarios pueden ver sus citas en la página de citas. El personal administrativo puede ver todas las citas.

### Detalle de Cita

Los usuarios pueden ver los detalles de una cita específica. El personal administrativo puede editar la fecha y otros detalles de la cita.

### Gestión de Horarios

El personal administrativo puede definir y gestionar los horarios disponibles para las citas.
