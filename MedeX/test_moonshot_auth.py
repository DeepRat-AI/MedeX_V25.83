#!/usr/bin/env python3
"""
Test different Moonshot API authentication methods
"""

import asyncio
import aiohttp
import json

async def test_moonshot_api():
    """Test various Moonshot API configurations"""
    
    api_key = "sk-moXrSMVmgKFHiIB1cDi1BCq7EPJ0D6JeUI0URgR2m5DwcNlK"
    
    # Test different base URLs and authentication methods
    test_configs = [
        {
            "base_url": "https://api.moonshot.cn/v1",
            "headers": {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            "name": "Standard Bearer Token"
        },
        {
            "base_url": "https://api.moonshot.cn/v1",
            "headers": {"Authorization": f"sk {api_key}", "Content-Type": "application/json"},
            "name": "SK Prefix"
        },
        {
            "base_url": "https://api.moonshot.cn/v1",
            "headers": {"x-api-key": api_key, "Content-Type": "application/json"},
            "name": "X-API-Key Header"
        },
        {
            "base_url": "https://api.moonshot.cn",
            "headers": {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            "name": "Without /v1"
        }
    ]
    
    test_payload = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, test connection"}
        ],
        "max_tokens": 50,
        "temperature": 0.3
    }
    
    for config in test_configs:
        print(f"\n🧪 Testing: {config['name']}")
        print(f"   URL: {config['base_url']}/chat/completions")
        
        try:
            async with aiohttp.ClientSession(headers=config["headers"]) as session:
                async with session.post(
                    f"{config['base_url']}/chat/completions",
                    json=test_payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    
                    print(f"   Status: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        content = result["choices"][0]["message"]["content"]
                        print(f"   ✅ SUCCESS: {content[:50]}...")
                        return config, result
                    else:
                        error_text = await response.text()
                        print(f"   ❌ Error: {error_text}")
        
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    print("\n❌ All authentication methods failed")
    
    # Test if the API endpoint is reachable
    print("\n🌐 Testing basic connectivity...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.moonshot.cn") as response:
                print(f"   Base URL status: {response.status}")
    except Exception as e:
        print(f"   Base URL error: {e}")
    
    return None, None

if __name__ == "__main__":
    print("🚀 Testing Moonshot API Authentication Methods")
    print("=" * 60)
    
    result = asyncio.run(test_moonshot_api())
    
    if result[0]:
        print(f"\n✅ Working configuration found: {result[0]['name']}")
    else:
        print(f"\n❌ No working configuration found")
        print(f"   The API key might be invalid or the service might be unavailable")