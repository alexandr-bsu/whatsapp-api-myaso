# API для отправки изображений в WhatsApp

## Описание

Endpoint `/send-images` позволяет отправлять несколько изображений по URL в WhatsApp через Green API. Изображения отправляются по одному, что обеспечивает надежность доставки.

## Endpoint

**POST** `/send-images`

## Параметры запроса

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `recipient` | string | Да | Номер телефона получателя в международном формате (например, +1234567890) |
| `image_urls` | array[string] | Да | Массив URL изображений для отправки (минимум 1 элемент) |
| `caption` | string | Нет | Подпись к изображениям (добавляется только к первому изображению) |

## Пример запроса

```json
{
  "recipient": "+1234567890",
  "image_urls": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.png",
    "https://example.com/image3.gif"
  ],
  "caption": "Вот несколько изображений для вас! 📸"
}
```

## Пример ответа

### Успешный ответ (200 OK)

```json
{
  "recipient": "+1234567890",
  "total_images": 3,
  "successful_sends": 3,
  "results": [
    {
      "image_url": "https://example.com/image1.jpg",
      "status": "sent",
      "message_id": "BAE55C7B8F341592",
      "response": {
        "idMessage": "BAE55C7B8F341592"
      }
    },
    {
      "image_url": "https://example.com/image2.png",
      "status": "sent",
      "message_id": "BAE58513B30A5EAB",
      "response": {
        "idMessage": "BAE58513B30A5EAB"
      }
    },
    {
      "image_url": "https://example.com/image3.gif",
      "status": "sent",
      "message_id": "BAE59A2C4D1B7F3E",
      "response": {
        "idMessage": "BAE59A2C4D1B7F3E"
      }
    }
  ]
}
```

### Частично успешный ответ (200 OK)

Если некоторые изображения не удалось отправить:

```json
{
  "recipient": "+1234567890",
  "total_images": 3,
  "successful_sends": 2,
  "results": [
    {
      "image_url": "https://example.com/image1.jpg",
      "status": "sent",
      "message_id": "BAE55C7B8F341592",
      "response": {
        "idMessage": "BAE55C7B8F341592"
      }
    },
    {
      "image_url": "https://example.com/broken-link.jpg",
      "status": "failed",
      "error": "Green API error for image 2: 400 - File not found"
    },
    {
      "image_url": "https://example.com/image3.gif",
      "status": "sent",
      "message_id": "BAE59A2C4D1B7F3E",
      "response": {
        "idMessage": "BAE59A2C4D1B7F3E"
      }
    }
  ]
}
```

## Коды ошибок

| Код | Описание | Пример ответа |
|-----|----------|---------------|
| 400 | Неверный формат номера телефона | `{"detail": "Recipient must be in international format, e.g., +1234567890"}` |
| 422 | Ошибка валидации данных | `{"detail": [{"msg": "List should have at least 1 item"}]}` |
| 502 | Не удалось отправить ни одного изображения | `{"detail": "Failed to send any images"}` |
| 500 | Внутренняя ошибка сервера | `{"detail": "Internal server error"}` |

## Примеры использования

### Python (requests)

```python
import requests

url = "http://localhost:8000/send-images"
payload = {
    "recipient": "+1234567890",
    "image_urls": [
        "https://picsum.photos/800/600?random=1",
        "https://picsum.photos/800/600?random=2"
    ],
    "caption": "Красивые изображения! 🖼️"
}

response = requests.post(url, json=payload)
print(response.json())
```

### cURL

```bash
curl -X POST "http://localhost:8000/send-images" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "+1234567890",
    "image_urls": [
      "https://picsum.photos/800/600?random=1",
      "https://picsum.photos/800/600?random=2"
    ],
    "caption": "Тестовые изображения"
  }'
```

### JavaScript (fetch)

```javascript
const response = await fetch('http://localhost:8000/send-images', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    recipient: '+1234567890',
    image_urls: [
      'https://picsum.photos/800/600?random=1',
      'https://picsum.photos/800/600?random=2'
    ],
    caption: 'Изображения из JavaScript! 🚀'
  })
});

const result = await response.json();
console.log(result);
```

## Особенности работы

### Поддерживаемые форматы изображений
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

### Ограничения
- Максимальный размер изображения: ~100 МБ (ограничение Green API)
- Изображения отправляются последовательно, не параллельно
- Подпись (caption) добавляется только к первому изображению
- URL должны быть публично доступными

### Рекомендации
- Используйте изображения оптимального размера (не более 2048x2048 пикселей)
- Убедитесь, что URL изображений доступны без авторизации
- Для большого количества изображений рассмотрите разбивку на несколько запросов

## Логирование

Все операции отправки логируются:

```
INFO: Image 1 sent successfully: BAE55C7B8F341592
INFO: Image 2 sent successfully: BAE58513B30A5EAB
ERROR: Green API error for image 3: 400 - File not found
```

## Интеграция с Green API

Endpoint использует метод `SendFileByUrl` Green API:
- URL: `{MEDIA_URL}/waInstance{ID_INSTANCE}/sendFileByUrl/{API_TOKEN_INSTANCE}`
- Метод: POST
- Формат: JSON
- **Важно**: Используется `MEDIA_URL` вместо `API_URL` согласно рекомендациям Green API

Каждое изображение отправляется отдельным запросом к Green API для обеспечения надежности доставки.

## Тестирование

Для тестирования endpoint используйте:

```bash
# Запуск тестового скрипта
python test_send_images.py

# Или используйте пример
python examples/send_images_example.py
```

## Swagger UI

После запуска сервера документация доступна по адресу:
- http://localhost:8000/docs

Там вы можете протестировать endpoint интерактивно.