#!/usr/bin/env python3
"""
Debug Moonshot API - Find working authentication method
"""

import asyncio
import aiohttp
import json

async def debug_moonshot_api():
    """Debug Moonshot API with extensive testing"""
    
    api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
    
    # Test different endpoints and authentication methods
    test_configs = [
        # Standard OpenAI-compatible endpoints
        {
            "url": "https://api.moonshot.cn/v1/chat/completions",
            "headers": {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            "name": "Standard Bearer"
        },
        {
            "url": "https://api.moonshot.cn/v1/chat/completions", 
            "headers": {"Authorization": f"sk {api_key}", "Content-Type": "application/json"},
            "name": "SK Prefix"
        },
        {
            "url": "https://api.moonshot.cn/v1/chat/completions",
            "headers": {"x-api-key": api_key, "Content-Type": "application/json"},
            "name": "X-API-Key"
        },
        # Alternative endpoints
        {
            "url": "https://api.moonshot.cn/chat/completions",
            "headers": {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            "name": "Without /v1"
        },
        {
            "url": "https://api.moonshot.ai/v1/chat/completions",
            "headers": {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},  
            "name": ".ai domain"
        },
        # Kimi-specific endpoints
        {
            "url": "https://kimi.moonshot.cn/api/chat",
            "headers": {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            "name": "Kimi direct"
        }
    ]
    
    # Test payload
    payload = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": "Hello, test connection"}
        ],
        "max_tokens": 50,
        "temperature": 0.3
    }
    
    print("🔍 DEBUGGING MOONSHOT API AUTHENTICATION")
    print("=" * 60)
    
    for config in test_configs:
        print(f"\n🧪 Testing: {config['name']}")
        print(f"   URL: {config['url']}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config['url'],
                    headers=config['headers'],
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    
                    print(f"   Status: {response.status}")
                    response_text = await response.text()
                    
                    if response.status == 200:
                        result = json.loads(response_text)
                        content = result["choices"][0]["message"]["content"]
                        print(f"   ✅ SUCCESS: {content[:100]}...")
                        return config, result
                    else:
                        print(f"   ❌ Error: {response_text[:200]}...")
                        
                        # Try to parse error details
                        try:
                            error_json = json.loads(response_text)
                            if "error" in error_json:
                                print(f"   📋 Error details: {error_json['error']}")
                        except:
                            pass
        
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    # Test if we can reach the base URL at all
    print(f"\n🌐 Testing basic connectivity...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.moonshot.cn", timeout=aiohttp.ClientTimeout(total=10)) as response:
                print(f"   Base URL status: {response.status}")
                if response.status != 200:
                    text = await response.text()
                    print(f"   Response: {text[:200]}...")
    except Exception as e:
        print(f"   Base URL error: {e}")
    
    # Test alternative domains
    print(f"\n🔍 Testing alternative domains...")
    domains = ["api.moonshot.ai", "kimi.moonshot.cn", "api.kimi.cn"]
    for domain in domains:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://{domain}", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    print(f"   {domain}: {response.status}")
        except Exception as e:
            print(f"   {domain}: Error - {e}")
    
    return None, None

if __name__ == "__main__":
    result = asyncio.run(debug_moonshot_api())
    
    if result[0]:
        print(f"\n✅ WORKING CONFIGURATION FOUND: {result[0]['name']}")
        print(f"   URL: {result[0]['url']}")
    else:
        print(f"\n❌ NO WORKING CONFIGURATION FOUND")
        print(f"   Possible issues:")
        print(f"   1. API key is invalid or expired")
        print(f"   2. Service is temporarily unavailable") 
        print(f"   3. Different authentication method required")
        print(f"   4. Rate limiting or IP restrictions")