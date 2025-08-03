#!/usr/bin/env python3
"""
Prueba simple y directa del sistema MedeX
"""

import asyncio
from openai import OpenAI

async def simple_test():
    print("🧪 Prueba simple de conexión")
    
    client = OpenAI(
        api_key="sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK",
        base_url="https://api.moonshot.ai/v1"
    )
    
    try:
        # Prueba sin streaming
        print("📡 Probando conexión básica...")
        response = client.chat.completions.create(
            model="kimi-k2-0711-preview",
            messages=[
                {"role": "system", "content": "Eres MedeX, un asistente médico."},
                {"role": "user", "content": "Hola, soy un paciente con dolor de cabeza"}
            ],
            temperature=0.6,
            max_tokens=200
        )
        
        print("✅ Respuesta recibida:")
        print(response.choices[0].message.content)
        
        # Prueba con streaming
        print("\n🔄 Probando streaming...")
        stream = client.chat.completions.create(
            model="kimi-k2-0711-preview",
            messages=[
                {"role": "system", "content": "Eres MedeX, un asistente médico."},
                {"role": "user", "content": "¿Qué puede causar dolor de cabeza?"}
            ],
            temperature=0.6,
            max_tokens=300,
            stream=True
        )
        
        print("💬 Respuesta streaming:")
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        
        print("\n\n✅ Sistema funcionando correctamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(simple_test())