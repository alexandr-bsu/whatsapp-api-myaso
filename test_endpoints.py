#!/usr/bin/env python3
"""
Тест доступности всех endpoints
"""

import requests

def test_endpoints():
    """
    Проверяет доступность всех endpoints
    """
    base_url = "http://51.250.42.45:2025"
    
    endpoints = [
        ("GET", "/", "Health check"),
        ("GET", "/docs", "Swagger UI"),
        ("POST", "/send-message", "Send message"),
        ("POST", "/send-images", "Send images"),
        ("POST", "/send-file", "Send file"),
        ("POST", "/webhook", "Webhook"),
        ("GET", "/webhook", "Webhook check")
    ]
    
    print("🔍 Проверка доступности endpoints")
    print("=" * 50)
    
    for method, endpoint, description in endpoints:
        url = f"{base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                # Для POST endpoints просто проверяем, что они существуют
                # Отправляем пустой запрос, ожидаем 422 (validation error) вместо 404
                response = requests.post(url, timeout=5)
            
            if response.status_code == 404:
                status = "❌ НЕ НАЙДЕН"
            elif response.status_code in [200, 422, 400]:  # 422 = validation error (endpoint exists)
                status = "✅ ДОСТУПЕН"
            else:
                status = f"⚠️  КОД {response.status_code}"
                
            print(f"{method:4} {endpoint:15} - {status:15} ({description})")
            
        except requests.exceptions.RequestException as e:
            print(f"{method:4} {endpoint:15} - ❌ ОШИБКА        ({description}) - {e}")

if __name__ == "__main__":
    test_endpoints()