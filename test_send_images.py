#!/usr/bin/env python3
"""
Тестовый скрипт для проверки endpoint отправки изображений
"""

import requests
import json

def test_send_images_endpoint():
    """
    Тестирует endpoint /send-images
    """
    url = "http://localhost:8001/send-images"
    
    # Тестовые данные
    test_payload = {
        "recipient": "+79246506083",
        "image_urls": [
            "https://picsum.photos/400/300?random=1",
            "https://picsum.photos/400/300?random=2"
        ],
        "caption": "Тестовые изображения из API"
    }
    
    print("🧪 Тестирование endpoint /send-images")
    print("=" * 50)
    print(f"📤 Отправляем запрос:")
    print(json.dumps(test_payload, indent=2, ensure_ascii=False))
    print()
    
    try:
        response = requests.post(
            url,
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 Ответ сервера:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("\n✅ Тест прошел успешно!")
        else:
            print(f"\n❌ Тест не прошел. Код ошибки: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка соединения: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

def test_validation_errors():
    """
    Тестирует валидацию входных данных
    """
    url = "http://localhost:8001/send-images"
    
    print("\n🧪 Тестирование валидации данных")
    print("=" * 50)
    
    # Тест 1: Неверный формат номера телефона
    test_cases = [
        {
            "name": "Неверный формат номера телефона",
            "payload": {
                "recipient": "+79246506083",  # Без +
                "image_urls": ["https://picsum.photos/400/300?random=1"]
            }
        },
        {
            "name": "Пустой список изображений",
            "payload": {
                "recipient": "+79246506083",
                "image_urls": []
            }
        },
        {
            "name": "Неверный URL изображения",
            "payload": {
                "recipient": "+79246506083",
                "image_urls": ["not-a-valid-url"]
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 Тест: {test_case['name']}")
        try:
            response = requests.post(
                url,
                json=test_case['payload'],
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code != 200:
                print(f"Ошибка (ожидаемо): {response.json()}")
            else:
                print("⚠️  Неожиданно успешный ответ")
                
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    # Проверяем доступность сервера
    try:
        health_response = requests.get("http://localhost:8001/", timeout=5)
        if health_response.status_code == 200:
            print("✅ API сервер доступен")
            test_send_images_endpoint()
            test_validation_errors()
        else:
            print("❌ API сервер недоступен")
    except:
        print("❌ Не удается подключиться к API серверу")
        print("Убедитесь, что сервер запущен: uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")