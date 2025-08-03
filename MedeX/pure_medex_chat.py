#!/usr/bin/env python3
"""
🏥 MedeX - Pure Kimi Medical AI Chat
100% Real Moonshot Kimi Integration - No Fallback Mode

Sistema médico de IA puro basado en Kimi.
Para profesionales médicos y pacientes.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the core module to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from pure_kimi_medex import PureKimiMedeX

class MedeXChatInterface:
    """Pure Kimi MedeX Chat Interface"""
    
    def __init__(self):
        self.api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
        self.medex = None
        self.session_start = datetime.now()
        
    async def start_session(self):
        """Initialize MedeX system"""
        print("🚀 Inicializando MedeX con Kimi Real...")
        
        try:
            self.medex = PureKimiMedeX(self.api_key)
            await self.medex.__aenter__()
            
            # Test connection
            if self.medex.kimi_client:
                connection_ok = await self.medex.kimi_client.test_connection()
                if connection_ok:
                    print("✅ Conexión con Kimi establecida")
                    return True
                else:
                    print("❌ Error: No se pudo conectar con Kimi")
                    return False
            else:
                print("❌ Error: No se pudo inicializar cliente Kimi")
                return False
                
        except Exception as e:
            print(f"❌ Error inicializando MedeX: {e}")
            return False
    
    async def close_session(self):
        """Close MedeX session"""
        if self.medex:
            await self.medex.__aexit__(None, None, None)
    
    def print_header(self):
        """Print MedeX header"""
        print("\n" + "="*80)
        print("🏥 MedeX - SISTEMA MÉDICO DE IA AVANZADA")
        print("🧠 Powered by Moonshot Kimi AI")
        print("⚡ 100% Real AI - Sin modo fallback")
        print("="*80)
        print("🔍 DETECCIÓN AUTOMÁTICA:")
        print("   👤 Paciente: Respuestas claras y comprensibles")
        print("   👨‍⚕️ Profesional: Análisis técnico detallado")
        print("   🚨 Emergencia: Protocolos de urgencia automáticos")
        print("="*80)
        print("💡 COMANDOS ESPECIALES:")
        print("   'test sistema' - Probar funcionalidad")
        print("   'demo paciente' - Ejemplo para pacientes")
        print("   'demo pro' - Ejemplo para profesionales")
        print("   'estado' - Estado del sistema")
        print("   'salir' - Terminar sesión")
        print("="*80)
        print("⚠️  IMPORTANTE: Solo información educativa - No reemplaza consulta médica")
        print("="*80 + "\n")
    
    async def handle_special_commands(self, query: str) -> bool:
        """Handle special commands"""
        query_lower = query.lower().strip()
        
        if query_lower in ['salir', 'exit', 'quit']:
            print("\n👋 Cerrando MedeX. ¡Gracias por usar nuestro sistema!")
            return True
        
        elif query_lower == 'test sistema':
            print("\n🧪 Ejecutando test completo del sistema...")
            results = await self.medex.test_system()
            
            print(f"📡 Conexión Kimi: {'✅' if results['connection'] else '❌'}")
            print(f"👤 Respuesta Paciente: {'✅' if results['patient_response'] else '❌'}")
            print(f"👨‍⚕️ Respuesta Profesional: {'✅' if results['professional_response'] else '❌'}")
            print(f"🚨 Detección Emergencia: {'✅' if results['emergency_response'] else '❌'}")
            
            if results.get('errors'):
                print(f"\n❌ Errores encontrados: {len(results['errors'])}")
                for error in results['errors']:
                    print(f"   • {error}")
            else:
                print("\n✅ Sistema funcionando perfectamente")
            
            return False
        
        elif query_lower == 'demo paciente':
            print("\n👤 DEMO - Consulta de Paciente:")
            demo_query = "Me duele el pecho desde hace 2 horas y me falta el aire"
            print(f"📝 Consulta: {demo_query}")
            print("🤔 Procesando...")
            
            response = await self.medex.generate_medical_response(demo_query)
            print(f"\n🩺 MedeX: {response}")
            return False
        
        elif query_lower == 'demo pro':
            print("\n👨‍⚕️ DEMO - Consulta Profesional:")
            demo_query = "Paciente de 55 años, diabético, con dolor precordial de 2 horas de evolución"
            print(f"📝 Consulta: {demo_query}")
            print("🤔 Procesando...")
            
            response = await self.medex.generate_medical_response(demo_query)
            print(f"\n🩺 MedeX: {response}")
            return False
        
        elif query_lower == 'estado':
            print(f"\n📊 ESTADO DEL SISTEMA:")
            print(f"   🕐 Sesión iniciada: {self.session_start.strftime('%H:%M:%S')}")
            print(f"   🧠 Motor IA: Moonshot Kimi")
            print(f"   🔗 Endpoint: https://api.moonshot.ai/v1")
            print(f"   ⚡ Modo: 100% Real (Sin fallback)")
            print(f"   📡 Estado: {'✅ Conectado' if self.medex else '❌ Desconectado'}")
            return False
        
        return False
    
    async def chat_loop(self):
        """Main chat loop"""
        
        if not await self.start_session():
            print("❌ No se pudo inicializar MedeX. Saliendo...")
            return
        
        self.print_header()
        
        try:
            while True:
                try:
                    # Get user input
                    user_input = input("🩺 Consulta: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle special commands
                    if await self.handle_special_commands(user_input):
                        break
                    
                    # Process medical query
                    print("🤔 Analizando con Kimi...")
                    
                    start_time = datetime.now()
                    response = await self.medex.generate_medical_response(user_input)
                    end_time = datetime.now()
                    
                    processing_time = (end_time - start_time).total_seconds()
                    
                    print(f"\n🩺 MedeX: {response}")
                    print(f"\n⏱️  Tiempo de respuesta: {processing_time:.2f}s")
                    print("-" * 80)
                
                except KeyboardInterrupt:
                    print("\n\n⌨️  Interrupción detectada. Saliendo...")
                    break
                    
                except Exception as e:
                    print(f"\n❌ Error procesando consulta: {e}")
                    print("💡 Intenta reformular tu consulta o usa 'test sistema' para verificar")
                    
        finally:
            await self.close_session()

async def main():
    """Main function"""
    
    print("🏥 MedeX - Iniciando Sistema Médico de IA")
    print("🧠 Basado en Moonshot Kimi AI")
    
    chat = MedeXChatInterface()
    await chat.chat_loop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 MedeX cerrado. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        print("💡 Verifica tu conexión a internet y la validez de la API key")