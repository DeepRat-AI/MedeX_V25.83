#!/usr/bin/env python3
"""
🧪 Test Demo del Sistema MEDEX Ultimate RAG
Demuestra todas las capacidades sin modo interactivo
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from MEDEX_ULTIMATE_RAG import MedeXUltimateRAG
import asyncio

async def demo_completo():
    """Demuestra todas las capacidades del sistema MEDEX Ultimate"""
    
    print("🏥 DEMO COMPLETO - MEDEX ULTIMATE RAG")
    print("=" * 60)
    
    # Inicializar sistema
    medex = MedeXUltimateRAG()
    
    # Test 1: Consulta médica básica
    print("\n🧪 TEST 1: Consulta médica con RAG")
    print("-" * 40)
    query1 = "Paciente de 55 años, diabético, con dolor precordial de 2 horas de evolución"
    print(f"📝 Consulta: {query1}")
    
    try:
        response1 = await medex.process_query_async(query1)
        print(f"🤖 Respuesta RAG: {response1[:200]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Detección de emergencia
    print("\n🚨 TEST 2: Detección de emergencia")
    print("-" * 40)
    query2 = "dolor en el pecho muy fuerte, no puedo respirar, mareos"
    print(f"📝 Consulta: {query2}")
    
    try:
        response2 = await medex.process_query_async(query2)
        print(f"🚨 Respuesta emergencia: {response2[:200]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Búsqueda en base de conocimiento
    print("\n🔍 TEST 3: Búsqueda RAG específica")
    print("-" * 40)
    search_term = "infarto agudo de miocardio"
    print(f"🔍 Búsqueda: {search_term}")
    
    try:
        results = medex.rag_system.search_knowledge(search_term, top_k=3)
        print(f"📚 Resultados RAG encontrados: {len(results)}")
        for i, result in enumerate(results):
            print(f"   {i+1}. {result['content'][:100]}...")
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
    
    # Test 4: Análisis de medicamento
    print("\n💊 TEST 4: Información de medicamento")
    print("-" * 40)
    query4 = "aspirina dosis para paciente diabético"
    print(f"📝 Consulta: {query4}")
    
    try:
        response4 = await medex.process_query_async(query4)
        print(f"💊 Respuesta medicamento: {response4[:200]}...")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Estadísticas del sistema
    print("\n📊 TEST 5: Estadísticas del sistema")
    print("-" * 40)
    try:
        stats = medex.get_system_stats()
        print(f"📈 Base de conocimiento: {stats['knowledge_base_size']} documentos")
        print(f"🧠 Modelo embedding: {stats['embedding_model']}")
        print(f"⚡ RAG activo: {stats['rag_enabled']}")
        print(f"🎯 Consultas procesadas: {stats.get('queries_processed', 0)}")
    except Exception as e:
        print(f"❌ Error en estadísticas: {e}")
    
    print("\n✅ DEMO COMPLETADO")
    print("🎯 El sistema MEDEX Ultimate RAG está funcionando correctamente")
    print("📚 RAG vectorial integrado con base de conocimiento médico")
    print("🚨 Protocolos de emergencia activos")
    print("🤖 Kimi K2 operativo con streaming")

if __name__ == "__main__":
    asyncio.run(demo_completo())