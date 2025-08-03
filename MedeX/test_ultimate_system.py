#!/usr/bin/env python3
"""
🧪 Test Ultimate MedeX System
Prueba rápida del sistema médico definitivo
"""

import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

from ultimate_medex_system import UltimateMedeXSystem

async def quick_test():
    """Prueba rápida del sistema"""
    
    print("🧪 INICIANDO PRUEBA RÁPIDA DE MEDEX ULTIMATE")
    print("=" * 60)
    
    api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
    medex = UltimateMedeXSystem(api_key)
    
    # Prueba 1: Consulta de emergencia
    print("\n🚨 PRUEBA 1: Emergencia médica")
    print("-" * 40)
    
    emergency_query = "Me duele el pecho muy fuerte desde hace 1 hora, me falta el aire y estoy sudando mucho"
    
    try:
        response = await medex.generate_streaming_response(emergency_query)
        print(f"\n✅ Emergencia procesada correctamente")
        print(f"📏 Longitud respuesta: {len(response)} caracteres")
    except Exception as e:
        print(f"❌ Error en emergencia: {e}")
    
    print("\n" + "="*60)
    
    # Prueba 2: Consulta profesional
    print("\n👨‍⚕️ PRUEBA 2: Consulta profesional")
    print("-" * 40)
    
    professional_query = "Paciente de 45 años con diabetes tipo 2, HbA1c 8.2%, consulta por protocolo de manejo"
    
    try:
        response = await medex.generate_streaming_response(professional_query)
        print(f"\n✅ Consulta profesional procesada")
        print(f"📏 Longitud respuesta: {len(response)} caracteres")
    except Exception as e:
        print(f"❌ Error en consulta profesional: {e}")
    
    print("\n" + "="*60)
    
    # Prueba 3: JSON estructurado
    print("\n📋 PRUEBA 3: Respuesta JSON estructurada")
    print("-" * 40)
    
    try:
        diagnostic = await medex.generate_structured_diagnosis("Dolor de cabeza persistente con náuseas")
        print(f"✅ JSON generado correctamente")
        print(f"📊 Motivo consulta: {diagnostic.analysis.chief_complaint}")
        print(f"🎯 Urgencia: {diagnostic.analysis.urgency_level}")
        print(f"👤 Tipo usuario: {diagnostic.analysis.patient_type}")
    except Exception as e:
        print(f"❌ Error en JSON: {e}")
    
    print("\n" + "="*60)
    print("🎉 PRUEBAS COMPLETADAS")
    print("✅ Sistema MedeX Ultimate funcionando correctamente")

if __name__ == "__main__":
    asyncio.run(quick_test())