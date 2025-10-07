# Настройка Webhook для получения сообщений из WhatsApp

## Описание

Webhook позволяет получать сообщения из WhatsApp в реальном времени, без необходимости постоянного опроса API (polling). Green API автоматически отправляет уведомления на ваш сервер при получении новых сообщений.

## Шаги настройки

### 1. Запустите ваше приложение

Убедитесь, что ваше FastAPI приложение запущено и доступно из интернета:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 2. Сделайте сервер доступным из интернета

Для локальной разработки можно использовать:

#### Вариант A: ngrok (рекомендуется для тестирования)
```bash
# Установите ngrok: https://ngrok.com/
ngrok http 8000
```

После запуска ngrok покажет публичный URL, например: `https://abc123.ngrok.io`

#### Вариант B: Развертывание на сервере
Разверните приложение на облачном сервере (AWS, DigitalOcean, Heroku и т.д.)

### 3. Настройте Webhook в Green API

1. Перейдите в личный кабинет Green API: https://console.green-api.com/
2. Выберите ваш инстанс WhatsApp
3. Перейдите в раздел "Настройки" → "Webhook"
4. Укажите URL вашего webhook endpoint:
   ```
   https://ваш-домен.com/webhook
   ```
   или если используете ngrok:
   ```
   https://abc123.ngrok.io/webhook
   ```

5. Выберите типы уведомлений для отправки:
   - ✅ **incomingMessageReceived** (обязательно)
   - Остальные по желанию

6. Сохраните настройки

### 4. Проверьте работу webhook

#### Метод 1: Отправьте тестовое сообщение
1. Отправьте сообщение на ваш номер WhatsApp (подключенный к Green API)
2. В консоли приложения должно появиться:
   ```
   ============================================================
   📱 НОВОЕ СООБЩЕНИЕ ИЗ WHATSAPP
   📞 Номер телефона: +1234567890
   💬 Сообщение: Привет!
   ============================================================
   ```

#### Метод 2: Проверьте endpoint
Откройте в браузере:
```
https://ваш-домен.com/webhook
```
Должен вернуться JSON:
```json
{
  "status": "ok",
  "message": "Webhook endpoint is active"
}
```

## Формат получаемых данных

Webhook endpoint получает данные в следующем формате:

```json
{
  "typeWebhook": "incomingMessageReceived",
  "instanceData": {
    "idInstance": 1234567,
    "wid": "79001234567@c.us",
    "typeInstance": "whatsapp"
  },
  "timestamp": 1234567890,
  "idMessage": "BAE5F...",
  "senderData": {
    "chatId": "79001234567@c.us",
    "sender": "79001234567@c.us",
    "senderName": "Имя отправителя"
  },
  "messageData": {
    "typeMessage": "textMessage",
    "textMessageData": {
      "textMessage": "Текст сообщения"
    }
  }
}
```

## Доступные Endpoints

### POST /webhook
Основной endpoint для получения webhook уведомлений от Green API.

**Использование:**
- Автоматически вызывается Green API при получении нового сообщения
- Выводит в консоль номер телефона и текст сообщения
- Возвращает подтверждение получения

### GET /webhook
Endpoint для проверки доступности webhook.

**Использование:**
- Проверить работоспособность webhook
- Некоторые сервисы используют GET запросы для верификации

### POST /processConversation
Endpoint для обработки сообщений (можно использовать для своей бизнес-логики).

**Пример запроса:**
```json
{
  "client_phone": "+1234567890",
  "message": "Привет"
}
```

## Отладка

### Проверка логов
Логи приложения выводят информацию о получаемых webhook:
```
INFO:     Received webhook data: {...}
INFO:     Processed message from +1234567890: Привет
```

### Тестирование локально
Отправьте тестовый POST запрос:
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "typeWebhook": "incomingMessageReceived",
    "senderData": {
      "sender": "1234567890@c.us"
    },
    "messageData": {
      "textMessageData": {
        "textMessage": "Тестовое сообщение"
      }
    }
  }'
```

## Безопасность

### Рекомендации:
1. **Используйте HTTPS** для production окружения
2. **Добавьте аутентификацию** (например, проверку токена в заголовках)
3. **Ограничьте IP адреса** только для Green API серверов
4. **Валидируйте входящие данные** (уже реализовано через Pydantic)

### Пример добавления проверки токена:
```python
from fastapi import Header, HTTPException

@router.post("/webhook")
async def receive_webhook(
    request: Request,
    x_webhook_token: str = Header(None)
):
    if x_webhook_token != settings.webhook_secret:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # ... остальной код
```

## Переключение с Polling на Webhook

Если ранее использовался polling (автоматический опрос API), его можно отключить:

1. Удалите или закомментируйте код запуска message_receiver в main.py
2. Webhook будет основным способом получения сообщений

## Troubleshooting

### Webhook не получает сообщения
- ✅ Проверьте, что URL webhook правильно указан в настройках Green API
- ✅ Убедитесь, что сервер доступен из интернета
- ✅ Проверьте логи приложения на наличие ошибок
- ✅ Убедитесь, что в Green API включен тип уведомлений "incomingMessageReceived"

### Ошибки при получении данных
- ✅ Проверьте формат входящих данных в логах
- ✅ Убедитесь, что модели Pydantic соответствуют структуре данных

### Сообщения приходят с задержкой
- ✅ Убедитесь, что используется именно webhook, а не polling
- ✅ Проверьте скорость интернет-соединения сервера

## API Documentation

После запуска приложения доступна интерактивная документация:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc




