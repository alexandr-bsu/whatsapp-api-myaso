# Быстрый старт - Webhook для WhatsApp

## Что было реализовано

✅ **Webhook endpoint** для получения сообщений из WhatsApp через Green API  
✅ **Вывод в консоль** номера телефона и текста сообщения  
✅ **Pydantic модели** для валидации данных webhook  
✅ **Документация API** в Swagger UI  

## Быстрый запуск

### 1. Запустите сервер

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

или

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Проверьте, что сервер работает

Откройте в браузере: http://localhost:8000

Должен вернуться JSON:
```json
{
  "status": "ok",
  "service": "WhatsApp Messaging API",
  "version": "1.0.0",
  "webhook_enabled": true
}
```

### 3. Протестируйте webhook локально

Используйте тестовый скрипт:
```bash
python test_webhook.py
```

Или отправьте тестовый запрос через curl:
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d "{\"typeWebhook\":\"incomingMessageReceived\",\"senderData\":{\"sender\":\"1234567890@c.us\"},\"messageData\":{\"textMessageData\":{\"textMessage\":\"Тестовое сообщение\"}}}"
```

**В консоли сервера должно появиться:**
```
============================================================
📱 НОВОЕ СООБЩЕНИЕ ИЗ WHATSAPP
📞 Номер телефона: +1234567890
💬 Сообщение: Тестовое сообщение
============================================================
```

### 4. Настройте webhook в Green API

Для получения реальных сообщений из WhatsApp:

1. Сделайте сервер доступным из интернета (используйте ngrok для тестирования):
   ```bash
   ngrok http 8000
   ```

2. Скопируйте публичный URL (например: `https://abc123.ngrok.io`)

3. Перейдите в [консоль Green API](https://console.green-api.com/)

4. Выберите ваш инстанс → Настройки → Webhook

5. Укажите URL webhook:
   ```
   https://abc123.ngrok.io/webhook
   ```

6. Включите уведомление "incomingMessageReceived"

7. Сохраните настройки

### 5. Отправьте тестовое сообщение

Отправьте сообщение на ваш номер WhatsApp (подключенный к Green API) с любого другого номера.

### 6. Протестируйте отправку изображений

Используйте тестовый скрипт для отправки изображений:
```bash
python examples/send_images_example.py
```

Или отправьте запрос через curl:
```bash
curl -X POST http://localhost:8000/send-images \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "+1234567890",
    "image_urls": [
      "https://picsum.photos/400/300?random=1",
      "https://picsum.photos/400/300?random=2"
    ],
    "caption": "Тестовые изображения из API! 📸"
  }'
```

**В консоли сервера должно появиться:**
```
============================================================
📱 НОВОЕ СООБЩЕНИЕ ИЗ WHATSAPP
📞 Номер телефона: +79001234567
💬 Сообщение: Привет!
============================================================
```

## Доступные endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/webhook` | Прием webhook от Green API |
| GET | `/webhook` | Проверка доступности webhook |
| POST | `/send-message` | Отправка сообщения в WhatsApp |
| POST | `/send-images` | Отправка нескольких изображений по URL |
| POST | `/processConversation` | Обработка входящего сообщения |
| GET | `/` | Статус API |
| GET | `/docs` | Swagger UI документация |

## Просмотр документации API

После запуска сервера откройте:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Структура проекта

```
src/
├── controllers/
│   ├── webhook_controller.py      ← Обработка webhook
│   └── conversation_controller.py
├── models/
│   ├── webhook.py                 ← Модели данных webhook
│   ├── whatsapp_message.py
│   └── conversation.py
├── services/
│   ├── whatsapp_service.py
│   └── message_receiver.py
├── config/
│   └── settings.py
└── main.py                        ← Главный файл приложения
```

## Что делать дальше?

### Добавить обработку сообщений
Отредактируйте `src/controllers/webhook_controller.py`:

```python
# После вывода в консоль добавьте свою логику:
if webhook.body.typeWebhook == "incomingMessageReceived":
    # ... извлечение данных ...
    
    # Ваша бизнес-логика:
    # - Сохранить в базу данных
    # - Отправить в AI чатбот
    # - Отправить автоответ
    # - Интеграция с CRM
```

### Добавить автоответ
```python
from src.services.whatsapp_service import send_whatsapp_message
from src.models.whatsapp_message import WhatsAppMessageRequest

# После получения сообщения:
auto_reply = WhatsAppMessageRequest(
    recipient=phone_number,
    message="Спасибо за ваше сообщение! Мы скоро ответим."
)
await send_whatsapp_message(auto_reply)
```

### Сохранить в базу данных
```python
# Добавьте модель БД и сохраните сообщение:
await save_message_to_db(
    phone_number=phone_number,
    message=message_text,
    timestamp=webhook.body.timestamp
)
```

## Troubleshooting

### Сервер не запускается
```bash
# Проверьте установлены ли зависимости:
pip install -r requirements.txt

# Проверьте порт:
netstat -an | findstr :8000
```

### Webhook не принимает сообщения
- ✅ Проверьте, что сервер запущен
- ✅ Проверьте URL в настройках Green API
- ✅ Убедитесь, что сервер доступен из интернета (используйте ngrok)
- ✅ Проверьте логи сервера на наличие ошибок

### Сообщения не отображаются
- ✅ Проверьте консоль сервера, а не консоль где запущен test_webhook.py
- ✅ Убедитесь, что typeWebhook = "incomingMessageReceived"

## Дополнительная документация

- [WEBHOOK_SETUP.md](./WEBHOOK_SETUP.md) - Полная инструкция по настройке webhook
- [README.md](./README.md) - Общая документация проекта

## Поддержка

Если возникли вопросы:
1. Проверьте логи сервера
2. Откройте `/docs` для интерактивного тестирования API
3. Изучите документацию Green API: https://green-api.com/docs/




