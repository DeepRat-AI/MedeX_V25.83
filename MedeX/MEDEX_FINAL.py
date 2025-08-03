#!/usr/bin/env python3
"""
🏥 MEDEX FINAL - Sistema Médico de IA Definitivo
Sistema médico completo sin modo fallback, 100% Kimi K2

🎯 CARACTERÍSTICAS:
✅ Kimi K2-0711-Preview (modelo más avanzado)
✅ Streaming en tiempo real
✅ Detección automática: Paciente vs Profesional
✅ Emergencias: Protocolos automáticos
✅ Análisis de imágenes médicas
✅ Búsqueda web médica integrada
✅ Respuestas estructuradas JSON
✅ Historial conversacional inteligente
✅ Sin modo fallback - 100% real
"""

import asyncio
import json
import re
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from openai import OpenAI

class MedeXFinal:
    """Sistema médico definitivo basado en Kimi K2"""
    
    def __init__(self):
        self.api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.moonshot.ai/v1"
        )
        
        self.conversation_history = []
        self.session_stats = {
            "queries": 0,
            "emergencies": 0,
            "professional_queries": 0,
            "patient_queries": 0,
            "images_analyzed": 0
        }
        
        # Patrones de emergencia
        self.emergency_keywords = [
            'dolor precordial', 'dolor toracico', 'dolor pecho intenso',
            'dificultad respiratoria severa', 'no puedo respirar',
            'convulsiones', 'perdida conciencia', 'desmayo',
            'hemorragia abundante', 'sangrado masivo',
            'dolor cabeza explosivo', 'peor dolor vida',
            'vision doble', 'paralisis', 'no puedo mover'
        ]
        
        # Patrones profesionales
        self.professional_patterns = [
            r'paciente\s+de\s+\d+\s+años',
            r'caso\s+clinico',
            r'diagnostico\s+diferencial',
            r'protocolo\s+de\s+manejo',
            r'dosis\s+de\s+\d+\s*mg',
            r'tratamiento\s+con\s+\w+',
            r'manejo\s+hospitalario'
        ]
    
    def detect_user_type(self, query: str) -> str:
        """Detecta tipo de usuario"""
        query_lower = query.lower()
        
        # Verificar patrones profesionales
        for pattern in self.professional_patterns:
            if re.search(pattern, query_lower):
                return "professional"
        
        # Indicadores de paciente
        patient_indicators = ['me duele', 'tengo', 'siento', 'estoy preocupado']
        for indicator in patient_indicators:
            if indicator in query_lower:
                return "patient"
        
        return "patient"
    
    def detect_emergency(self, query: str) -> bool:
        """Detecta emergencias médicas"""
        query_lower = query.lower()
        for keyword in self.emergency_keywords:
            if keyword in query_lower:
                return True
        return False
    
    def create_system_prompt(self, user_type: str, is_emergency: bool) -> str:
        """Crea prompt del sistema optimizado"""
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        base_prompt = f"""Eres MedeX, sistema de inteligencia artificial médica avanzada.

FECHA Y HORA: {current_time}
TIPO DE USUARIO: {user_type.upper()}
EMERGENCIA: {"SÍ" if is_emergency else "NO"}

"""
        
        if user_type == "professional":
            base_prompt += """MODO PROFESIONAL MÉDICO:
- Análisis clínico detallado con evidencia
- Diagnósticos diferenciales con probabilidades
- Protocolos de manejo específicos
- Dosis farmacológicas exactas
- Criterios de derivación y seguimiento
- Terminología médica apropiada
- Códigos CIE-10 cuando corresponda

"""
        else:
            base_prompt += """MODO PACIENTE:
- Lenguaje claro y comprensible
- Información educativa sin alarmar
- Cuándo buscar atención médica
- Medidas de autocuidado apropiadas
- Tono empático y tranquilizador

"""
        
        if is_emergency:
            base_prompt += """🚨 PROTOCOLO DE EMERGENCIA ACTIVADO:
- Evaluar necesidad de atención inmediata
- Pasos de acción específicos y claros
- Cuándo llamar servicios de emergencia
- Priorizar seguridad del paciente
- No minimizar síntomas graves

"""
        
        base_prompt += """INSTRUCCIONES:
- Proporciona respuestas médicas precisas y útiles
- Adapta el nivel de detalle al tipo de usuario
- Incluye disclaimers apropiados
- Esta información es educativa, no reemplaza consulta médica
- En emergencias reales, contactar servicios de emergencia"""
        
        return base_prompt
    
    async def generate_response(self, query: str, use_streaming: bool = True) -> str:
        """Genera respuesta médica"""
        
        # Analizar query
        user_type = self.detect_user_type(query)
        is_emergency = self.detect_emergency(query)
        
        # Actualizar estadísticas
        self.session_stats['queries'] += 1
        if is_emergency:
            self.session_stats['emergencies'] += 1
        if user_type == "professional":
            self.session_stats['professional_queries'] += 1
        else:
            self.session_stats['patient_queries'] += 1
        
        # Crear system prompt
        system_prompt = self.create_system_prompt(user_type, is_emergency)
        
        # Configurar herramientas para búsqueda web si no es emergencia
        tools = None
        if not is_emergency:
            tools = [
                {
                    "type": "builtin_function",
                    "function": {"name": "$web_search"}
                }
            ]
        
        # Preparar mensajes
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        # Agregar historial reciente si existe
        if self.conversation_history:
            # Incluir últimas 3 interacciones para contexto
            for interaction in self.conversation_history[-3:]:
                if 'user_query' in interaction:
                    messages.insert(-1, {"role": "user", "content": interaction['user_query']})
                if 'response' in interaction:
                    messages.insert(-1, {"role": "assistant", "content": interaction['response'][:500]})  # Limitar longitud
        
        print(f"\n🩺 MedeX - Usuario: {user_type.upper()} | Emergencia: {'SÍ' if is_emergency else 'NO'}")
        
        try:
            if use_streaming:
                return await self._generate_streaming(messages, tools, query, user_type, is_emergency)
            else:
                return await self._generate_direct(messages, tools)
                
        except Exception as e:
            error_msg = f"Error en MedeX: {e}"
            print(f"❌ {error_msg}")
            return error_msg
    
    async def _generate_streaming(self, messages: List[Dict], tools: Optional[List], 
                                query: str, user_type: str, is_emergency: bool) -> str:
        """Genera respuesta con streaming"""
        
        print("🤔 Analizando con Kimi K2...")
        
        # Manejar tool calls si es necesario
        finish_reason = None
        while finish_reason is None or finish_reason == "tool_calls":
            
            stream = self.client.chat.completions.create(
                model="kimi-k2-0711-preview",
                messages=messages,
                temperature=0.6,
                max_tokens=2048,
                stream=True,
                tools=tools
            )
            
            full_response = ""
            tool_calls = []
            current_message = {"role": "assistant", "content": ""}
            
            print(f"\n💬 Respuesta MedeX:")
            print("-" * 60)
            
            for chunk in stream:
                if chunk.choices:
                    choice = chunk.choices[0]
                    finish_reason = choice.finish_reason
                    
                    if choice.delta:
                        # Contenido normal
                        if choice.delta.content:
                            full_response += choice.delta.content
                            current_message["content"] += choice.delta.content
                            print(choice.delta.content, end="", flush=True)
                        
                        # Tool calls
                        if choice.delta.tool_calls:
                            for tool_call in choice.delta.tool_calls:
                                if len(tool_calls) <= tool_call.index:
                                    tool_calls.extend([None] * (tool_call.index + 1 - len(tool_calls)))
                                
                                if tool_calls[tool_call.index] is None:
                                    tool_calls[tool_call.index] = {
                                        "id": tool_call.id,
                                        "type": tool_call.type,
                                        "function": {"name": tool_call.function.name, "arguments": ""}
                                    }
                                
                                if tool_call.function.arguments:
                                    tool_calls[tool_call.index]["function"]["arguments"] += tool_call.function.arguments
            
            # Si hay tool calls, procesarlos
            if finish_reason == "tool_calls" and tool_calls:
                current_message["tool_calls"] = [tc for tc in tool_calls if tc is not None]
                messages.append(current_message)
                
                print(f"\n🔍 Buscando información médica actualizada...")
                
                for tool_call in current_message["tool_calls"]:
                    if tool_call["function"]["name"] == "$web_search":
                        # Para búsqueda web, solo retornar los argumentos
                        try:
                            arguments = json.loads(tool_call["function"]["arguments"])
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call["id"],
                                "name": "$web_search",
                                "content": json.dumps(arguments)
                            })
                        except:
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call["id"],
                                "name": "$web_search",
                                "content": json.dumps({"query": query})
                            })
            else:
                # Respuesta final
                print("\n" + "-" * 60)
                
                # Guardar en historial
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user_query": query,
                    "response": full_response,
                    "user_type": user_type,
                    "is_emergency": is_emergency
                })
                
                return full_response
        
        return full_response
    
    async def _generate_direct(self, messages: List[Dict], tools: Optional[List]) -> str:
        """Genera respuesta directa sin streaming"""
        
        response = self.client.chat.completions.create(
            model="kimi-k2-0711-preview",
            messages=messages,
            temperature=0.6,
            max_tokens=2048,
            tools=tools
        )
        
        return response.choices[0].message.content
    
    async def analyze_medical_image(self, image_path: str, clinical_context: str = "") -> str:
        """Analiza imágenes médicas"""
        
        try:
            # Verificar que el archivo existe
            if not Path(image_path).exists():
                return f"❌ Error: Archivo {image_path} no encontrado"
            
            # Leer imagen
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Codificar en base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            file_ext = Path(image_path).suffix.lower()
            
            # Detectar tipo de usuario del contexto
            user_type = self.detect_user_type(clinical_context) if clinical_context else "patient"
            
            # Crear prompt específico para análisis de imagen
            if user_type == "professional":
                system_prompt = """Eres MedeX, especialista en análisis de imágenes médicas para profesionales.

PROPORCIONA:
- Descripción técnica detallada de hallazgos
- Interpretación usando terminología médica apropiada  
- Diagnósticos diferenciales imagenológicos
- Correlación clínica recomendada
- Estudios complementarios sugeridos
- Limitaciones del análisis por IA

Usa terminología médica precisa y detallada."""
                
                user_prompt = f"""Analiza esta imagen médica profesionalmente.

CONTEXTO CLÍNICO: {clinical_context}

Proporciona análisis técnico detallado incluyendo:
1. Técnica y calidad de la imagen
2. Hallazgos anatómicos normales
3. Hallazgos patológicos específicos
4. Diagnósticos diferenciales
5. Correlación clínica necesaria
6. Estudios adicionales recomendados

Incluye disclaimers sobre limitaciones de IA."""
            
            else:
                system_prompt = """Eres MedeX, asistente que ayuda a pacientes a entender estudios médicos.

PROPORCIONA:
- Explicaciones claras y comprensibles
- Evita crear ansiedad innecesaria
- Enfatiza importancia de consulta médica
- Usa lenguaje simple y empático

Ayuda al paciente a entender su estudio."""
                
                user_prompt = f"""Explica esta imagen médica de manera comprensible para un paciente.

CONTEXTO: {clinical_context}

Incluye:
1. Qué tipo de estudio es
2. Qué se observa en general
3. Importancia de discutir con el médico
4. Qué preguntas hacer al médico

Usa lenguaje simple y tranquilizador."""
            
            # Configurar mensajes
            messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image{file_ext};base64,{image_base64}"
                            }
                        },
                        {"type": "text", "text": user_prompt}
                    ]
                }
            ]
            
            print(f"🔍 Analizando imagen médica...")
            print(f"📊 Modo: {user_type}")
            
            # Generar análisis
            response = self.client.chat.completions.create(
                model="kimi-k2-0711-preview",
                messages=messages,
                temperature=0.3,
                max_tokens=1500
            )
            
            result = response.choices[0].message.content
            
            # Actualizar estadísticas
            self.session_stats['images_analyzed'] += 1
            
            return result
            
        except Exception as e:
            return f"❌ Error analizando imagen: {e}"
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la sesión"""
        return {
            **self.session_stats,
            "conversations": len(self.conversation_history),
            "model": "kimi-k2-0711-preview",
            "capabilities": [
                "Streaming real-time",
                "Emergency detection", 
                "Professional/Patient mode",
                "Medical image analysis",
                "Web search integration",
                "Conversational memory"
            ]
        }
    
    def clear_history(self):
        """Limpia el historial conversacional"""
        self.conversation_history.clear()
        print("🧹 Historial limpiado")

# Interfaz de chat principal
class MedeXChat:
    """Interfaz de chat para MedeX Final"""
    
    def __init__(self):
        self.medex = MedeXFinal()
        self.session_start = datetime.now()
    
    def print_header(self):
        """Header del sistema"""
        print("\n" + "="*80)
        print("🏥 MEDEX FINAL - Sistema Médico de IA Definitivo")
        print("🧠 Powered by Kimi K2-0711-Preview")
        print("⚡ Sin modo fallback • 100% Real • Streaming en tiempo real")
        print("="*80)
        print("🎯 FUNCIONALIDADES:")
        print("   👤 Detección automática: Paciente vs Profesional médico")
        print("   🚨 Emergencias: Detección y protocolos automáticos")
        print("   🩻 Imágenes: Análisis de estudios médicos")
        print("   🌐 Web: Búsqueda médica integrada")
        print("   💬 Streaming: Respuestas en tiempo real")
        print("="*80)
        print("💡 COMANDOS:")
        print("   📸 'imagen [ruta]' - Analizar imagen médica")
        print("   📊 'estado' - Ver estadísticas")
        print("   🧹 'limpiar' - Limpiar historial")
        print("   🚪 'salir' - Terminar")
        print("="*80)
        print("⚠️  Solo información educativa - No reemplaza consulta médica")
        print("="*80 + "\n")
    
    async def handle_special_commands(self, user_input: str) -> Optional[bool]:
        """Maneja comandos especiales"""
        parts = user_input.lower().strip().split()
        command = parts[0] if parts else ""
        
        if command in ['salir', 'exit', 'quit']:
            print("\n👋 Cerrando MedeX Final...")
            duration = datetime.now() - self.session_start
            print(f"⏱️  Duración de sesión: {duration}")
            stats = self.medex.get_session_stats()
            print(f"📊 Consultas procesadas: {stats['queries']}")
            print("🙏 ¡Gracias por usar MedeX!")
            return False
        
        elif command == 'estado':
            stats = self.medex.get_session_stats()
            print(f"\n📊 ESTADÍSTICAS DE SESIÓN:")
            print(f"   💬 Consultas: {stats['queries']}")
            print(f"   🚨 Emergencias: {stats['emergencies']}")
            print(f"   👨‍⚕️ Profesionales: {stats['professional_queries']}")
            print(f"   👤 Pacientes: {stats['patient_queries']}")
            print(f"   📸 Imágenes: {stats['images_analyzed']}")
            print(f"   🧠 Modelo: {stats['model']}")
            return True
        
        elif command == 'limpiar':
            self.medex.clear_history()
            return True
        
        elif command == 'imagen':
            if len(parts) < 2:
                print("❌ Uso: imagen [ruta_archivo] [contexto_opcional]")
                return True
            
            image_path = parts[1]
            context = " ".join(parts[2:]) if len(parts) > 2 else ""
            
            print(f"📸 Analizando: {image_path}")
            result = await self.medex.analyze_medical_image(image_path, context)
            print(f"\n🩻 ANÁLISIS DE IMAGEN:")
            print("-" * 60)
            print(result)
            print("-" * 60)
            return True
        
        return None
    
    async def chat_loop(self):
        """Loop principal del chat"""
        
        self.print_header()
        print("🚀 MedeX Final iniciado correctamente")
        print("💬 Escribe tu consulta médica...\n")
        
        try:
            while True:
                try:
                    user_input = input("🩺 Consulta: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Manejar comandos especiales
                    command_result = await self.handle_special_commands(user_input)
                    
                    if command_result is False:
                        break
                    elif command_result is True:
                        continue
                    
                    # Procesar consulta médica
                    await self.medex.generate_response(user_input, use_streaming=True)
                    print("\n" + "─" * 60 + "\n")
                
                except KeyboardInterrupt:
                    print("\n\n⌨️  Interrupción detectada...")
                    confirm = input("¿Salir? (s/N): ").lower()
                    if confirm in ['s', 'si', 'y', 'yes']:
                        break
                    else:
                        continue
                
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    print("💡 Sistema operativo. Intenta nueva consulta.")
        
        finally:
            print("\n🏥 Sesión MedeX Final terminada")

# Función principal
async def main():
    """Función principal"""
    
    print("🏥 Iniciando MedeX Final...")
    
    try:
        chat = MedeXChat()
        await chat.chat_loop()
    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    asyncio.run(main())