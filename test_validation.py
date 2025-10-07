#!/usr/bin/env python3
"""
Простой тест валидации моделей
"""

from src.models.whatsapp_message import WhatsAppImagesRequest
from pydantic import ValidationError

def test_validation():
    print("🧪 Тестирование валидации модели WhatsAppImagesRequest")
    print("=" * 60)
    
    # Тест 1: Корректные данные
    try:
        valid_request = WhatsAppImagesRequest(
            recipient="+1234567890",
            image_urls=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            caption="Test caption"
        )
        print("✅ Тест 1 (корректные данные): ПРОШЕЛ")
    except ValidationError as e:
        print(f"❌ Тест 1 (корректные данные): ПРОВАЛЕН - {e}")
    
    # Тест 2: Неверный формат номера телефона
    try:
        invalid_request = WhatsAppImagesRequest(
            recipient="1234567890",  # Без +
            image_urls=["https://example.com/image1.jpg"],
            caption="Test caption"
        )
        print("❌ Тест 2 (неверный номер): ПРОВАЛЕН - валидация не сработала")
    except ValidationError as e:
        print("✅ Тест 2 (неверный номер): ПРОШЕЛ - валидация сработала")
        print(f"   Ошибка: {e.errors()[0]['msg']}")
    
    # Тест 3: Пустой список изображений
    try:
        invalid_request = WhatsAppImagesRequest(
            recipient="+1234567890",
            image_urls=[],  # Пустой список
            caption="Test caption"
        )
        print("❌ Тест 3 (пустой список): ПРОВАЛЕН - валидация не сработала")
    except ValidationError as e:
        print("✅ Тест 3 (пустой список): ПРОШЕЛ - валидация сработала")
        print(f"   Ошибка: {e.errors()[0]['msg']}")
    
    # Тест 4: Неверный URL
    try:
        invalid_request = WhatsAppImagesRequest(
            recipient="+1234567890",
            image_urls=["not-a-valid-url"],  # Неверный URL
            caption="Test caption"
        )
        print("❌ Тест 4 (неверный URL): ПРОВАЛЕН - валидация не сработала")
    except ValidationError as e:
        print("✅ Тест 4 (неверный URL): ПРОШЕЛ - валидация сработала")
        print(f"   Ошибка: {e.errors()[0]['msg']}")

if __name__ == "__main__":
    test_validation()