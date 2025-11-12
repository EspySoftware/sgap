# 🔓 Vulnerabilidades de Broken Access Control - SGAP

### 1. **Eliminación sin Autorización** (Alta Severidad)
- **Endpoint:** `/eliminar_cita/<id>/`
- **Problema:** No verifica permisos antes de eliminar
- **Exploit:** Cualquier usuario puede eliminar cualquier cita

### 2. **Acceso a Datos de Otros Usuarios** (Alta Severidad)
- **Endpoint:** `/ver_citas_usuario/?user_id=<id>`
- **Problema:** Acepta parámetro user_id sin validación
- **Exploit:** Ver citas de cualquier usuario manipulando el parámetro

### 3. **Elevación de Privilegios** (Severidad Crítica)
- **Endpoint:** `/cambiar_rol/?user_id=<id>&is_staff=true`
- **Problema:** Permite cambiar roles sin autorización
- **Exploit:** Cualquier usuario puede convertirse en administrador

### 4. **Exposición de Información Sensible** (Alta Severidad)
- **Endpoint:** `/listar_usuarios/`
- **Problema:** Devuelve todos los usuarios sin verificar permisos
- **Exploit:** Obtener emails, nombres, roles de todos los usuarios

### 5. **Modificación de Estado sin Permisos** (Media-Alta Severidad)
- **Endpoint:** `/modificar_estado_cita/<id>/`
- **Problema:** No verifica que el usuario sea orientador
- **Exploit:** Auto-aprobar citas pendientes

### 6. **IDOR - Insecure Direct Object Reference** (Alta Severidad)
- **Endpoint:** `/obtener_datos_cita/<id>/`
- **Problema:** No verifica propiedad del recurso
- **Exploit:** Acceder a datos de todas las citas del sistema

---
