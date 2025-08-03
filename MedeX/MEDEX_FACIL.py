#!/usr/bin/env python3
"""
🏥 MEDEX FÁCIL - Con instalación automática de dependencias
"""

import sys
import subprocess
import os

def install_package(package):
    """Instala paquete automáticamente"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
        print(f"✅ {package} instalado correctamente")
        return True
    except:
        print(f"❌ Error instalando {package}")
        return False

def check_and_install_dependencies():
    """Verifica e instala dependencias"""
    required_packages = ["openai"]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} ya está instalado")
        except ImportError:
            print(f"📦 Instalando {package}...")
            if not install_package(package):
                print(f"❌ No se pudo instalar {package}")
                return False
    
    return True

# Verificar e instalar dependencias
print("🔧 Verificando dependencias...")
if not check_and_install_dependencies():
    print("❌ Error en dependencias. Saliendo...")
    sys.exit(1)

# Ahora importar después de instalar
try:
    from openai import OpenAI
    print("✅ OpenAI importado correctamente")
except ImportError:
    print("❌ Error importando OpenAI después de instalación")
    print("💡 Intenta reiniciar el terminal y ejecutar de nuevo")
    sys.exit(1)

import asyncio
import json
import re
from datetime import datetime

class MedeXSimple:
    """Versión simple de MedeX"""
    
    def __init__(self):
        self.api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.moonshot.ai/v1"
        )
        print("✅ MedeX inicializado correctamente")
    
    def detect_user_type(self, query):
        """Detecta tipo de usuario"""
        query_lower = query.lower()
        
        # Patrones profesionales
        professional_patterns = [
            'paciente de', 'caso clinico', 'diagnostico diferencial',
            'protocolo de', 'dosis de', 'mg cada', 'tratamiento con'
        ]
        
        for pattern in professional_patterns:
            if pattern in query_lower:
                return "PROFESIONAL"
        
        # Indicadores de paciente
        patient_indicators = ['me duele', 'tengo', 'siento', 'estoy preocupado']
        for indicator in patient_indicators:
            if indicator in query_lower:
                return "PACIENTE"
        
        return "PACIENTE"
    
    def detect_emergency(self, query):
        """Detecta emergencias"""
        emergency_keywords = [
            'dolor pecho intenso', 'no puedo respirar', 'dolor precordial',
            'convulsiones', 'perdida conciencia', 'hemorragia abundante'
        ]
        
        query_lower = query.lower()
        for keyword in emergency_keywords:
            if keyword in query_lower:
                return True
        return False
    
    def generate_response(self, query):
        """Genera respuesta médica"""
        
        user_type = self.detect_user_type(query)
        is_emergency = self.detect_emergency(query)
        
        print(f"\n🩺 MedeX - Usuario: {user_type} | Emergencia: {'SÍ' if is_emergency else 'NO'}")
        
        # Crear prompt del sistema
        if user_type == "PROFESIONAL":
            system_prompt = """Eres MedeX, sistema médico de IA para profesionales.

PROPORCIONA:
- Análisis clínico detallado
- Diagnósticos diferenciales
- Protocolos de manejo específicos
- Terminología médica apropiada
- Dosis farmacológicas cuando corresponda

Esta información es educativa, no reemplaza consulta médica."""
        else:
            system_prompt = """Eres MedeX, asistente médico para pacientes.

PROPORCIONA:
- Explicaciones claras y comprensibles
- Información educativa sin alarmar
- Cuándo buscar atención médica
- Medidas de autocuidado apropiadas
- Tono empático y tranquilizador

Esta información es educativa, no reemplaza consulta médica.
En emergencias reales, contactar servicios de emergencia."""
        
        if is_emergency:
            system_prompt += "\n\n🚨 EMERGENCIA DETECTADA: Prioriza seguridad del paciente y proporciona instrucciones de acción inmediata."
        
        try:
            print("🤔 Analizando con Kimi K2...")
            
            response = self.client.chat.completions.create(
                model="kimi-k2-0711-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.6,
                max_tokens=1500
            )
            
            result = response.choices[0].message.content
            
            print(f"\n💬 Respuesta MedeX:")
            print("-" * 60)
            print(result)
            print("-" * 60)
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Error: {e}"
            print(error_msg)
            return error_msg

def main():
    """Función principal"""
    
    print("🏥 MedeX FÁCIL - Sistema Médico de IA")
    print("🧠 Powered by Kimi K2-0711-Preview")
    print("="*50)
    
    try:
        medex = MedeXSimple()
        
        print("\n💡 Comandos:")
        print("   'salir' - Terminar")
        print("   O escribe tu consulta médica\n")
        
        while True:
            try:
                user_input = input("🩺 Consulta: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("\n👋 ¡Gracias por usar MedeX!")
                    break
                
                medex.generate_response(user_input)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Saliendo de MedeX...")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("💡 Intenta de nuevo...")
    
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        print("💡 Verifica tu conexión a internet")

if __name__ == "__main__":
    main()