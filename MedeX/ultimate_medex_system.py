#!/usr/bin/env python3
"""
🏥 MedeX ULTIMATE - Sistema Médico de IA Definitivo
Basado en Kimi K2 con capacidades completas de razonamiento médico

Características:
- Streaming en tiempo real
- Análisis multimodal (imágenes médicas)
- Búsqueda web médica integrada
- Detección inteligente de emergencias
- Respuestas estructuradas JSON
- Context caching para documentos médicos
"""

import asyncio
import json
import re
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

import aiohttp
from openai import OpenAI

@dataclass
class MedicalAnalysis:
    """Análisis médico estructurado"""
    chief_complaint: str
    symptoms: List[str]
    duration: str
    severity: str
    patient_type: str  # "patient" or "professional"
    urgency_level: str  # "routine", "urgent", "emergency"
    differential_diagnosis: List[str]
    recommended_actions: List[str]
    red_flags: List[str]
    
@dataclass
class DiagnosticResponse:
    """Respuesta diagnóstica estructurada"""
    analysis: MedicalAnalysis
    clinical_reasoning: str
    treatment_plan: List[str]
    follow_up: List[str]
    education: List[str]
    warnings: List[str]

class UltimateMedeXSystem:
    """Sistema MedeX Definitivo con Kimi K2"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.ai/v1"
        )
        
        # Patrones de emergencia médica
        self.emergency_patterns = {
            'cardiac': [
                'dolor precordial', 'dolor toracico', 'dolor pecho', 'chest pain',
                'infarto', 'sindrome coronario', 'angina', 'palpitaciones severas'
            ],
            'respiratory': [
                'dificultad respiratoria severa', 'disnea severa', 'cianosis',
                'edema pulmonar', 'neumotorax', 'embolia pulmonar'
            ],
            'neurological': [
                'accidente cerebrovascular', 'ictus', 'avc', 'convulsiones',
                'perdida conciencia', 'deficit neurologico agudo'
            ],
            'trauma': [
                'traumatismo craneal', 'hemorragia masiva', 'shock',
                'fractura abierta', 'lesion medular'
            ]
        }
        
        # Patrones para detectar profesionales médicos
        self.professional_patterns = [
            r'paciente\s+de\s+\d+\s+años',
            r'caso\s+clinico',
            r'diagnostico\s+diferencial',
            r'protocolo\s+de\s+manejo',
            r'tratamiento\s+con\s+\w+\s+mg',
            r'dosis\s+de\s+\d+\s*mg',
            r'codigo\s+cie',
            r'manejo\s+hospitalario',
            r'seguimiento\s+ambulatorio'
        ]
    
    def detect_user_type(self, query: str) -> str:
        """Detecta si es paciente o profesional médico"""
        query_lower = query.lower()
        
        # Verificar patrones profesionales
        for pattern in self.professional_patterns:
            if re.search(pattern, query_lower):
                return "professional"
        
        # Indicadores de paciente
        patient_indicators = [
            'me duele', 'tengo', 'siento', 'me pasa', 'estoy preocupado',
            'que sera', 'es normal', 'debo preocuparme'
        ]
        
        for indicator in patient_indicators:
            if indicator in query_lower:
                return "patient"
        
        return "patient"  # Por defecto, asumir paciente por seguridad
    
    def detect_urgency_level(self, query: str) -> str:
        """Detecta nivel de urgencia médica"""
        query_lower = query.lower()
        
        # Verificar emergencias por categoría
        for category, keywords in self.emergency_patterns.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return "emergency"
        
        # Indicadores de urgencia
        urgent_indicators = [
            'urgente', 'inmediato', 'rapido', 'ahora',
            'empeorando', 'severo', 'intenso'
        ]
        
        for indicator in urgent_indicators:
            if indicator in query_lower:
                return "urgent"
        
        return "routine"
    
    def extract_medical_context(self, query: str) -> Dict[str, Any]:
        """Extrae contexto médico de la consulta"""
        context = {}
        query_lower = query.lower()
        
        # Extraer edad
        age_match = re.search(r'(\d{1,3})\s*años?', query_lower)
        if age_match:
            context['age'] = int(age_match.group(1))
        
        # Extraer género
        if any(word in query_lower for word in ['hombre', 'masculino', 'varón']):
            context['gender'] = "masculino"
        elif any(word in query_lower for word in ['mujer', 'femenino', 'femenina']):
            context['gender'] = "femenino"
        
        # Extraer duración
        duration_patterns = [
            r'(\d+)\s*horas?',
            r'(\d+)\s*dias?',
            r'(\d+)\s*semanas?',
            r'(\d+)\s*meses?'
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, query_lower)
            if match:
                context['duration'] = match.group(0)
                break
        
        # Extraer antecedentes médicos
        medical_history = []
        if 'diabetic' in query_lower or 'diabetes' in query_lower:
            medical_history.append('Diabetes Mellitus')
        if 'hipertenso' in query_lower or 'hipertension' in query_lower:
            medical_history.append('Hipertensión Arterial')
        if 'cardiaco' in query_lower or 'corazon' in query_lower:
            medical_history.append('Cardiopatía')
        
        if medical_history:
            context['medical_history'] = medical_history
        
        return context
    
    def create_medical_system_prompt(self, user_type: str, urgency_level: str, context: Dict[str, Any]) -> str:
        """Crea prompt del sistema adaptado al tipo de usuario y urgencia"""
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        base_prompt = f"""Eres MedeX, un sistema de inteligencia artificial médica avanzada desarrollado con tecnología Kimi K2.

FECHA Y HORA ACTUAL: {current_time}

INFORMACIÓN DEL CONTEXTO:
- Tipo de usuario: {user_type}
- Nivel de urgencia: {urgency_level.upper()}
- Contexto médico: {json.dumps(context, ensure_ascii=False)}

"""
        
        if user_type == "professional":
            base_prompt += """MODO PROFESIONAL MÉDICO ACTIVADO:

PROTOCOLOS DE RESPUESTA:
- Proporciona análisis clínico detallado con evidencia científica
- Incluye diagnósticos diferenciales con probabilidades estimadas
- Especifica protocolos de manejo y dosis farmacológicas exactas
- Cita guías clínicas actuales cuando sea relevante
- Indica criterios de derivación y seguimiento
- Usa terminología médica apropiada
- Incluye códigos CIE-10 cuando corresponda

"""
        else:
            base_prompt += """MODO PACIENTE ACTIVADO:

PROTOCOLOS DE RESPUESTA:
- Usa lenguaje claro y comprensible
- Proporciona información educativa sin alarmar innecesariamente
- Enfatiza cuándo es importante buscar atención médica
- Incluye medidas de autocuidado apropiadas
- Mantén un tono empático y tranquilizador
- Evita diagnósticos específicos

"""
        
        if urgency_level == "emergency":
            base_prompt += """🚨 PROTOCOLO DE EMERGENCIA ACTIVADO 🚨

INSTRUCCIONES CRÍTICAS:
- Evalúa si se requiere atención médica inmediata
- Proporciona pasos de acción específicos y claros
- Incluye cuándo llamar al servicio de emergencias
- No minimices síntomas potencialmente graves
- Prioriza la seguridad del paciente

"""
        
        base_prompt += """CAPACIDADES ESPECIALES:
- Análisis de imágenes médicas (radiografías, ECGs, laboratorios)
- Búsqueda de información médica actualizada
- Respuestas estructuradas en formato JSON cuando sea apropiado
- Razonamiento clínico paso a paso

DISCLAIMERS IMPORTANTES:
- Esta información es solo educativa y no reemplaza consulta médica
- En emergencias, contactar servicios de emergencia inmediatamente
- Siempre buscar atención médica profesional para diagnóstico y tratamiento

INSTRUCCIONES DE RESPUESTA:
- Proporciona razonamiento clínico detallado
- Estructura la información de manera clara
- Incluye recomendaciones específicas basadas en evidencia
- Adapta el nivel de detalle al tipo de usuario"""
        
        return base_prompt
    
    async def generate_streaming_response(self, query: str, context: Dict[str, Any] = None) -> str:
        """Genera respuesta médica con streaming en tiempo real"""
        
        if context is None:
            context = {}
        
        # Analizar query
        user_type = self.detect_user_type(query)
        urgency_level = self.detect_urgency_level(query)
        extracted_context = self.extract_medical_context(query)
        
        # Combinar contextos
        full_context = {**context, **extracted_context}
        
        # Crear prompt del sistema
        system_prompt = self.create_medical_system_prompt(user_type, urgency_level, full_context)
        
        # Configurar herramientas si es necesario
        tools = []
        if urgency_level != "emergency":  # En emergencias, respuesta directa
            tools = [
                {
                    "type": "builtin_function",
                    "function": {
                        "name": "$web_search"
                    }
                }
            ]
        
        # Crear mensajes
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        print(f"\n🩺 MedeX ({user_type.upper()}) - Urgencia: {urgency_level.upper()}")
        print("🤔 Analizando...")
        
        try:
            # Generar respuesta con streaming
            stream = self.client.chat.completions.create(
                model="kimi-k2-0711-preview",  # Modelo más avanzado
                messages=messages,
                temperature=0.6,  # Recomendado para K2
                max_tokens=4096,  # Suficiente para respuestas completas
                stream=True,
                tools=tools if tools else None
            )
            
            full_response = ""
            reasoning_content = ""
            is_reasoning = False
            
            print(f"\n💬 Respuesta MedeX:")
            print("-" * 60)
            
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta:
                    delta = chunk.choices[0].delta
                    
                    # Verificar si hay contenido de razonamiento
                    if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                        if not is_reasoning:
                            is_reasoning = True
                            print("🧠 Razonamiento médico:")
                            print("─" * 40)
                        reasoning_content += delta.reasoning_content
                        print(delta.reasoning_content, end="", flush=True)
                    
                    # Contenido principal
                    if delta.content:
                        if is_reasoning:
                            is_reasoning = False
                            print("\n" + "─" * 40)
                            print("📋 Respuesta clínica:")
                            print("─" * 40)
                        
                        full_response += delta.content
                        print(delta.content, end="", flush=True)
            
            print("\n" + "-" * 60)
            return full_response
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return f"Error en el sistema MedeX: {e}"
    
    async def analyze_medical_image(self, image_path: str, clinical_context: str) -> str:
        """Analiza imágenes médicas con Kimi Vision"""
        
        try:
            # Leer y codificar imagen
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            file_ext = Path(image_path).suffix.lower()
            
            # Detectar tipo de usuario del contexto
            user_type = self.detect_user_type(clinical_context)
            
            # Crear prompt para análisis de imagen
            if user_type == "professional":
                system_prompt = """Eres MedeX, especialista en análisis de imágenes médicas.

PROTOCOLO DE ANÁLISIS PROFESIONAL:
- Descripción detallada de hallazgos observables
- Interpretación técnica usando terminología médica apropiada
- Diagnósticos diferenciales basados en hallazgos imagenológicos
- Correlación clínica recomendada
- Estudios complementarios sugeridos
- Limitaciones del análisis por IA

Proporciona análisis técnico detallado para profesionales médicos."""
                
                user_prompt = f"""Analiza esta imagen médica con el siguiente contexto clínico:

CONTEXTO CLÍNICO: {clinical_context}

Proporciona un análisis profesional detallado incluyendo:
1. Técnica y calidad de la imagen
2. Hallazgos normales identificados
3. Hallazgos anormales específicos
4. Diagnósticos diferenciales imagenológicos
5. Correlación clínica recomendada
6. Estudios adicionales sugeridos

Incluye disclaimers sobre limitaciones del análisis por IA."""
            
            else:
                system_prompt = """Eres MedeX, asistente médico que ayuda a pacientes a entender sus estudios médicos.

PROTOCOLO PARA PACIENTES:
- Explicaciones claras y comprensibles
- Evitar alarmar innecesariamente
- Enfatizar importancia de consulta médica
- Lenguaje simple y empático

Ayuda al paciente a entender su estudio médico."""
                
                user_prompt = f"""Ayuda a explicar esta imagen médica de manera comprensible:

CONTEXTO: {clinical_context}

Proporciona una explicación clara que incluya:
1. Qué tipo de estudio es
2. Qué se puede observar en términos generales
3. Importancia de discutir con el médico
4. Qué preguntas hacer al médico tratante

Usa lenguaje simple y evita crear ansiedad innecesaria."""
            
            # Configurar mensajes con imagen
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
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ]
                }
            ]
            
            print(f"🔍 Analizando imagen médica...")
            print(f"📊 Tipo de usuario: {user_type}")
            
            # Generar análisis
            response = self.client.chat.completions.create(
                model="kimi-k2-0711-preview",
                messages=messages,
                temperature=0.3,  # Menor temperatura para precisión médica
                max_tokens=2048
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error analizando imagen médica: {e}"
    
    async def generate_structured_diagnosis(self, query: str) -> DiagnosticResponse:
        """Genera diagnóstico estructurado en formato JSON"""
        
        user_type = self.detect_user_type(query)
        urgency_level = self.detect_urgency_level(query)
        context = self.extract_medical_context(query)
        
        system_prompt = f"""Eres MedeX, sistema de IA médica. Genera un análisis médico estructurado.

INSTRUCCIONES:
- Analiza la consulta médica proporcionada
- Proporciona respuesta en formato JSON válido
- Adapta el nivel de detalle al tipo de usuario: {user_type}
- Considera nivel de urgencia: {urgency_level}

FORMATO DE RESPUESTA JSON:
{{
    "analysis": {{
        "chief_complaint": "Motivo de consulta principal",
        "symptoms": ["síntoma1", "síntoma2"],
        "duration": "duración de síntomas",
        "severity": "leve/moderado/severo",
        "patient_type": "{user_type}",
        "urgency_level": "{urgency_level}",
        "differential_diagnosis": ["diagnóstico1", "diagnóstico2"],
        "recommended_actions": ["acción1", "acción2"],
        "red_flags": ["bandera roja1", "bandera roja2"]
    }},
    "clinical_reasoning": "Razonamiento clínico detallado",
    "treatment_plan": ["plan1", "plan2"],
    "follow_up": ["seguimiento1", "seguimiento2"],
    "education": ["educación1", "educación2"],
    "warnings": ["advertencia1", "advertencia2"]
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model="kimi-k2-0711-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.4,
                max_tokens=3072,
                response_format={"type": "json_object"}
            )
            
            # Parsear respuesta JSON
            json_response = json.loads(response.choices[0].message.content)
            
            # Crear objetos estructurados
            analysis = MedicalAnalysis(**json_response["analysis"])
            diagnostic_response = DiagnosticResponse(
                analysis=analysis,
                clinical_reasoning=json_response["clinical_reasoning"],
                treatment_plan=json_response["treatment_plan"],
                follow_up=json_response["follow_up"],
                education=json_response["education"],
                warnings=json_response["warnings"]
            )
            
            return diagnostic_response
            
        except Exception as e:
            # Fallback si JSON falla
            return DiagnosticResponse(
                analysis=MedicalAnalysis(
                    chief_complaint=query[:100],
                    symptoms=[],
                    duration="No especificada",
                    severity="No determinada",
                    patient_type=user_type,
                    urgency_level=urgency_level,
                    differential_diagnosis=[],
                    recommended_actions=["Consultar con médico"],
                    red_flags=[]
                ),
                clinical_reasoning=f"Error en análisis estructurado: {e}",
                treatment_plan=["Consultar profesional médico"],
                follow_up=["Seguimiento médico apropiado"],
                education=["Buscar atención médica"],
                warnings=["Error en sistema, buscar atención médica"]
            )

# Función de demostración
async def demonstrate_ultimate_medex():
    """Demostración del sistema MedeX Ultimate"""
    
    print("🚀 INICIANDO MEDEX ULTIMATE SYSTEM")
    print("=" * 80)
    
    api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
    medex = UltimateMedeXSystem(api_key)
    
    # Casos de prueba
    test_cases = [
        {
            "name": "Emergencia Cardíaca - Profesional",
            "query": "Paciente de 55 años, diabético, con dolor precordial de 2 horas de evolución, diaforesis y disnea"
        },
        {
            "name": "Consulta Paciente - Rutina",
            "query": "Me duele la cabeza desde hace 3 días, es un dolor como pulsátil"
        },
        {
            "name": "Consulta Diabetes - Profesional",
            "query": "Protocolo de manejo para paciente con diabetes tipo 2 y HbA1c de 8.5%"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📋 CASO {i}: {case['name']}")
        print("=" * 60)
        
        response = await medex.generate_streaming_response(case['query'])
        
        print(f"\n✅ Respuesta generada: {len(response)} caracteres")
        print("=" * 60)
        
        if i < len(test_cases):
            input("\nPresiona Enter para continuar al siguiente caso...")

if __name__ == "__main__":
    asyncio.run(demonstrate_ultimate_medex())