#!/usr/bin/env python3
"""
Test real MedeX responses with specific medical scenarios
"""

import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from pure_kimi_medex import PureKimiMedeX

async def test_medical_scenarios():
    """Test specific medical scenarios"""
    
    print("🧪 PROBANDO ESCENARIOS MÉDICOS REALES")
    print("=" * 60)
    
    api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
    
    # Test scenarios
    scenarios = [
        {
            "name": "Paciente - Dolor precordial",
            "query": "Me duele el pecho desde hace 2 horas y me falta el aire",
            "expected_type": "patient"
        },
        {
            "name": "Profesional - Síndrome coronario agudo",
            "query": "Paciente de 55 años, diabético, con dolor precordial de 2 horas de evolución, diaforesis y disnea",
            "expected_type": "professional"
        },
        {
            "name": "Paciente - Diabetes consulta",
            "query": "¿Qué es la diabetes tipo 2? Mi médico me dijo que la tengo",
            "expected_type": "patient"
        },
        {
            "name": "Profesional - Manejo diabetes",
            "query": "Protocolo de manejo para diabetes tipo 2 con HbA1c de 8.5%",
            "expected_type": "professional"
        }
    ]
    
    async with PureKimiMedeX(api_key) as medex:
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n📋 ESCENARIO {i}: {scenario['name']}")
            print(f"📝 Consulta: {scenario['query']}")
            print("🤔 Procesando...")
            
            try:
                response = await medex.generate_medical_response(scenario['query'])
                
                print(f"\n🩺 RESPUESTA:")
                print(f"{response}")
                print(f"\n✅ Longitud: {len(response)} caracteres")
                
                # Verify response quality
                if len(response) > 100:
                    print("✅ Respuesta completa generada")
                else:
                    print("⚠️  Respuesta parece incompleta")
                
                print("-" * 60)
                
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_medical_scenarios())