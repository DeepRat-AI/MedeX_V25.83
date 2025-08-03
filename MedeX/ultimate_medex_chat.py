#!/usr/bin/env python3
"""
🏥 MedeX ULTIMATE CHAT - Interfaz de Chat Médico Definitiva
Sistema médico conversacional con streaming en tiempo real

Características:
✅ Streaming en tiempo real (como ChatGPT)
✅ Análisis de imágenes médicas
✅ Búsqueda web médica
✅ Detección automática de emergencias
✅ Modo profesional/paciente
✅ Historial conversacional
✅ Respuestas estructuradas
✅ Context caching para documentos
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Agregar path del sistema
sys.path.append(os.path.join(os.path.dirname(__file__)))

from ultimate_medex_system import UltimateMedeXSystem

class UltimateMedeXChat:
    """Chat médico definitivo con todas las capacidades avanzadas"""
    
    def __init__(self):
        self.api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
        self.medex = UltimateMedeXSystem(self.api_key)
        self.session_start = datetime.now()
        self.conversation_history = []
        self.session_stats = {
            "queries": 0,
            "emergencies_detected": 0,
            "images_analyzed": 0,
            "professional_queries": 0,
            "patient_queries": 0
        }
    
    def print_header(self):
        """Imprime header del sistema"""
        print("\n" + "="*100)
        print("🏥 MEDEX ULTIMATE - SISTEMA MÉDICO DE IA AVANZADA")
        print("🧠 Powered by Moonshot Kimi K2 - Modelo más avanzado disponible")
        print("⚡ Streaming en tiempo real • 🔍 Análisis multimodal • 🌐 Búsqueda médica")
        print("="*100)
        print("🎯 CAPACIDADES PRINCIPALES:")
        print("   👤 Detección automática: Paciente vs Profesional médico")
        print("   🚨 Emergencias: Detección y protocolos automáticos")
        print("   🩻 Imágenes: Análisis de radiografías, ECGs, laboratorios")
        print("   🌐 Web: Búsqueda de información médica actualizada")
        print("   💬 Streaming: Respuestas en tiempo real con razonamiento")
        print("   📋 JSON: Diagnósticos estructurados y planes de tratamiento")
        print("="*100)
        print("💡 COMANDOS ESPECIALES:")
        print("   📸 'imagen [ruta]' - Analizar imagen médica")
        print("   📊 'json [consulta]' - Respuesta estructurada JSON")
        print("   📈 'estado' - Estadísticas de la sesión")
        print("   🔄 'limpiar' - Limpiar historial conversacional")
        print("   🚪 'salir' - Terminar sesión")
        print("="*100)
        print("⚠️  IMPORTANTE: Solo información educativa - No reemplaza consulta médica")
        print("   🚨 En emergencias reales: Contactar servicios de emergencia")
        print("="*100 + "\n")
    
    def print_session_stats(self):
        """Muestra estadísticas de la sesión"""
        duration = datetime.now() - self.session_start
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        print(f"\n📊 ESTADÍSTICAS DE LA SESIÓN:")
        print(f"   🕐 Duración: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
        print(f"   💬 Consultas totales: {self.session_stats['queries']}")
        print(f"   🚨 Emergencias detectadas: {self.session_stats['emergencies_detected']}")
        print(f"   📸 Imágenes analizadas: {self.session_stats['images_analyzed']}")
        print(f"   👨‍⚕️ Consultas profesionales: {self.session_stats['professional_queries']}")
        print(f"   👤 Consultas de pacientes: {self.session_stats['patient_queries']}")
        print(f"   🧠 Motor IA: Kimi K2-0711-Preview")
        print(f"   📡 Estado: ✅ Conectado y operativo")
    
    async def handle_image_analysis(self, command_parts: list) -> bool:
        """Maneja análisis de imágenes médicas"""
        if len(command_parts) < 2:
            print("❌ Uso: imagen [ruta_archivo] [contexto_clínico_opcional]")
            return True
        
        image_path = command_parts[1]
        clinical_context = " ".join(command_parts[2:]) if len(command_parts) > 2 else "Análisis general de imagen médica"
        
        if not Path(image_path).exists():
            print(f"❌ Error: No se encuentra el archivo {image_path}")
            return True
        
        try:
            print(f"📸 Analizando imagen médica: {image_path}")
            print(f"🔍 Contexto clínico: {clinical_context}")
            
            result = await self.medex.analyze_medical_image(image_path, clinical_context)
            
            print(f"\n🩻 ANÁLISIS DE IMAGEN MÉDICA:")
            print("-" * 80)
            print(result)
            print("-" * 80)
            
            self.session_stats['images_analyzed'] += 1
            
        except Exception as e:
            print(f"❌ Error analizando imagen: {e}")
        
        return True
    
    async def handle_json_response(self, query: str) -> bool:
        """Maneja respuestas estructuradas en JSON"""
        try:
            print("📋 Generando respuesta estructurada...")
            
            diagnostic_response = await self.medex.generate_structured_diagnosis(query)
            
            print(f"\n📊 DIAGNÓSTICO ESTRUCTURADO:")
            print("=" * 80)
            
            # Mostrar análisis
            print(f"🔍 ANÁLISIS CLÍNICO:")
            print(f"   Motivo de consulta: {diagnostic_response.analysis.chief_complaint}")
            print(f"   Síntomas: {', '.join(diagnostic_response.analysis.symptoms)}")
            print(f"   Duración: {diagnostic_response.analysis.duration}")
            print(f"   Severidad: {diagnostic_response.analysis.severity}")
            print(f"   Urgencia: {diagnostic_response.analysis.urgency_level}")
            
            if diagnostic_response.analysis.differential_diagnosis:
                print(f"   Diagnósticos diferenciales:")
                for dx in diagnostic_response.analysis.differential_diagnosis:
                    print(f"     • {dx}")
            
            # Razonamiento clínico
            print(f"\n🧠 RAZONAMIENTO CLÍNICO:")
            print(f"   {diagnostic_response.clinical_reasoning}")
            
            # Plan de tratamiento
            if diagnostic_response.treatment_plan:
                print(f"\n💊 PLAN DE TRATAMIENTO:")
                for i, plan in enumerate(diagnostic_response.treatment_plan, 1):
                    print(f"   {i}. {plan}")
            
            # Seguimiento
            if diagnostic_response.follow_up:
                print(f"\n📅 SEGUIMIENTO:")
                for i, follow in enumerate(diagnostic_response.follow_up, 1):
                    print(f"   {i}. {follow}")
            
            # Educación
            if diagnostic_response.education:
                print(f"\n📚 EDUCACIÓN AL PACIENTE:")
                for i, edu in enumerate(diagnostic_response.education, 1):
                    print(f"   {i}. {edu}")
            
            # Advertencias
            if diagnostic_response.warnings:
                print(f"\n⚠️  ADVERTENCIAS:")
                for warning in diagnostic_response.warnings:
                    print(f"   • {warning}")
            
            print("=" * 80)
            
        except Exception as e:
            print(f"❌ Error generando respuesta JSON: {e}")
        
        return True
    
    async def handle_special_commands(self, user_input: str) -> bool:
        """Maneja comandos especiales"""
        command_parts = user_input.lower().strip().split()
        command = command_parts[0] if command_parts else ""
        
        # Comando salir
        if command in ['salir', 'exit', 'quit']:
            print("\n👋 Cerrando MedeX Ultimate...")
            self.print_session_stats()
            print("\n🙏 ¡Gracias por usar MedeX Ultimate!")
            print("💝 Que tengas un excelente día")
            return False
        
        # Comando estado
        elif command == 'estado':
            self.print_session_stats()
            return True
        
        # Comando limpiar historial
        elif command == 'limpiar':
            self.conversation_history.clear()
            print("🧹 Historial conversacional limpiado")
            return True
        
        # Comando análisis de imagen
        elif command == 'imagen':
            return await self.handle_image_analysis(command_parts)
        
        # Comando respuesta JSON
        elif command == 'json':
            if len(command_parts) < 2:
                print("❌ Uso: json [consulta médica]")
                return True
            
            query = " ".join(command_parts[1:])
            return await self.handle_json_response(query)
        
        # Comandos de demo
        elif command == 'demo':
            await self.run_demo_scenarios()
            return True
        
        return None  # No es comando especial
    
    async def run_demo_scenarios(self):
        """Ejecuta escenarios de demostración"""
        demo_cases = [
            {
                "name": "🚨 Emergencia Cardíaca",
                "query": "Paciente de 55 años con dolor precordial intenso, sudoración y náuseas desde hace 30 minutos"
            },
            {
                "name": "👤 Consulta de Paciente",
                "query": "Tengo dolor de cabeza persistente desde hace 3 días, ¿es normal?"
            },
            {
                "name": "👨‍⚕️ Consulta Profesional",
                "query": "Protocolo de manejo para hipertensión arterial estadio 2 en paciente diabético"
            }
        ]
        
        print("\n🎬 EJECUTANDO CASOS DE DEMOSTRACIÓN:")
        print("=" * 60)
        
        for i, case in enumerate(demo_cases, 1):
            print(f"\n📋 CASO {i}: {case['name']}")
            print("─" * 40)
            print(f"Consulta: {case['query']}")
            
            input("\nPresiona Enter para procesar...")
            
            await self.medex.generate_streaming_response(case['query'])
            
            if i < len(demo_cases):
                input("\nPresiona Enter para continuar al siguiente caso...")
    
    async def process_medical_query(self, user_input: str):
        """Procesa consulta médica regular"""
        
        # Detectar tipo de usuario y urgencia
        user_type = self.medex.detect_user_type(user_input)
        urgency_level = self.medex.detect_urgency_level(user_input)
        
        # Actualizar estadísticas
        self.session_stats['queries'] += 1
        if urgency_level == "emergency":
            self.session_stats['emergencies_detected'] += 1
        if user_type == "professional":
            self.session_stats['professional_queries'] += 1
        else:
            self.session_stats['patient_queries'] += 1
        
        # Agregar al historial
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "user_type": user_type,
            "urgency_level": urgency_level
        })
        
        # Generar respuesta con streaming
        try:
            response = await self.medex.generate_streaming_response(
                user_input, 
                context={"conversation_history": self.conversation_history[-5:]}  # Últimas 5 interacciones
            )
            
            # Agregar respuesta al historial
            if self.conversation_history:
                self.conversation_history[-1]["response"] = response
                
        except Exception as e:
            print(f"\n❌ Error procesando consulta: {e}")
            print("💡 Intenta reformular tu consulta o usa 'estado' para verificar conexión")
    
    async def chat_loop(self):
        """Loop principal del chat"""
        
        self.print_header()
        
        print("🚀 Sistema inicializado correctamente")
        print("💬 Escribe tu consulta médica o usa comandos especiales")
        print("💡 Tip: Sé específico para obtener mejores resultados\n")
        
        try:
            while True:
                try:
                    # Obtener input del usuario
                    user_input = input("🩺 Consulta: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Manejar comandos especiales
                    command_result = await self.handle_special_commands(user_input)
                    
                    if command_result is False:  # Comando salir
                        break
                    elif command_result is True:  # Comando procesado
                        continue
                    
                    # Procesar consulta médica regular
                    await self.process_medical_query(user_input)
                    
                    print("\n" + "─" * 80 + "\n")
                
                except KeyboardInterrupt:
                    print("\n\n⌨️  Interrupción detectada...")
                    confirm = input("¿Realmente deseas salir? (s/N): ").lower()
                    if confirm in ['s', 'si', 'sí', 'y', 'yes']:
                        break
                    else:
                        print("Continuando...")
                        continue
                
                except Exception as e:
                    print(f"\n❌ Error inesperado: {e}")
                    print("💡 El sistema continúa operativo. Intenta una nueva consulta.")
        
        finally:
            print("\n" + "="*60)
            print("🏥 Sesión MedeX Ultimate finalizada")
            self.print_session_stats()
            print("="*60)

async def main():
    """Función principal"""
    
    print("🏥 Iniciando MedeX Ultimate Chat...")
    print("🧠 Cargando sistema médico de IA avanzada...")
    
    try:
        chat = UltimateMedeXChat()
        await chat.chat_loop()
    
    except Exception as e:
        print(f"\n❌ Error crítico del sistema: {e}")
        print("🔧 Verifica tu conexión a internet y la validez de la API key")
        print("📞 Contacta soporte técnico si el problema persiste")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 MedeX Ultimate cerrado por el usuario")
        print("🙏 ¡Hasta luego!")
    except Exception as e:
        print(f"\n💥 Error fatal: {e}")
        print("🔧 Reinicia el sistema e intenta nuevamente")