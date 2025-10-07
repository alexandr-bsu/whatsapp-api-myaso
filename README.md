# WhatsApp Messaging API

A FastAPI-based service to send and receive messages from WhatsApp accounts using Green API.

## Features
- ✅ Send text and media messages to WhatsApp numbers
- ✅ Send files and images to WhatsApp numbers
- ✅ Send multiple images in a single request
- ✅ **Webhook support** - receive incoming WhatsApp messages in real-time
- ✅ Automatically receive incoming WhatsApp messages
- ✅ Process incoming messages through custom endpoint
- ✅ Console output for incoming messages with phone numbers
- ✅ Background task for continuous message polling (alternative to webhook)
- ✅ Input validation and error handling
- ✅ Modular, production-ready structure

## Endpoints

### POST `/send-message`
Send a WhatsApp message to a recipient.

**Request Body:**
```json
{
  "recipient": "+1234567890",
  "message": "Hello from FastAPI!",
  "media_url": "https://example.com/image.jpg"  // optional
}
```

**Response:**
```json
{
  "idMessage": "3EB0...",
  "status": "success"
}
```

### POST `/send-images`
Send multiple images to a WhatsApp recipient.

**Request Body:**
```json
{
  "recipient": "+1234567890",
  "caption": "Check out these images!",
  "image_urls": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg",
    "https://example.com/image3.jpg"
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Sent 3 images successfully",
  "responses": [
    {
      "idMessage": "3EB0...",
      "status": "sent"
    },
    // ... additional responses for each image
  ]
}
```

### POST `/send-file`
Send a file to a WhatsApp recipient using file upload.

**Form Parameters:**
- `recipient` (required): Phone number in international format (e.g., +1234567890)
- `file` (required): The file to send
- `caption` (optional): Caption for the file
- `file_name` (optional): Name of the file with extension

**Response:**
```json
{
  "idMessage": "3EB0...",
  "status": "sent"
}
```

### POST `/processConversation`
Process incoming WhatsApp messages from clients. This endpoint is automatically called when a message is received from WhatsApp.

**Request Body:**
```json
{
  "client_phone": "+1234567890",
  "message": "Hello, I need help"
}
```

**Response:**
```json
{
  "status": "success",
  "client_phone": "+1234567890",
  "message_received": "Hello, I need help",
  "processed_at": "2024-01-01T12:00:00"
}
```

### POST `/webhook`
**[NEW]** Webhook endpoint for receiving incoming WhatsApp messages from Green API in real-time.

**What it does:**
- Receives webhook notifications from Green API when new messages arrive
- Extracts phone number and message text
- Outputs to console in a formatted way:
  ```
  ============================================================
  📱 НОВОЕ СООБЩЕНИЕ ИЗ WHATSAPP
  📞 Номер телефона: +1234567890
  💬 Сообщение: Hello!
  ============================================================
  ```

**Setup Instructions:** See [WEBHOOK_SETUP.md](./WEBHOOK_SETUP.md) for detailed webhook configuration guide.

### GET `/webhook`
Webhook verification endpoint to check if the webhook is accessible.

### GET `/`
Health check endpoint showing API status and webhook status.

## Configuration

### Environment Variables
Create a `.env` file in the project root with your Green API credentials:

```env
ID_INSTANCE=your_green_api_id_instance_here
API_TOKEN_INSTANCE=your_green_api_token_instance_here
API_URL=https://api.green-api.com
```

### Getting Green API Credentials
1. Register at [Green API](https://green-api.com/)
2. Create an instance and get your `ID_INSTANCE` and `API_TOKEN_INSTANCE`
3. Scan QR code to connect your WhatsApp account
4. Add credentials to `.env` file

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your Green API credentials (see Configuration section)

3. Run the application:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## How It Works

### Sending Messages
Use the `/send-message` endpoint to send WhatsApp messages to any phone number.

### Sending Images
Use the `/send-images` endpoint to send multiple images to a WhatsApp recipient.

### Sending Files
Use the `/send-file` endpoint to send any file to a WhatsApp recipient.

### Receiving Messages

**Option 1: Webhook (Recommended)**
The recommended way to receive messages is via webhook:
1. Green API sends webhook notifications to your `/webhook` endpoint when messages arrive
2. Application extracts phone number and message text
3. Outputs to console with formatted display
4. Can be extended to trigger custom processing logic

**To set up webhook:** Follow the guide in [WEBHOOK_SETUP.md](./WEBHOOK_SETUP.md)

**Option 2: Polling (Alternative)**
If webhook is not set up, the application can poll Green API:
1. Polls Green API for incoming messages every 2 seconds
2. Extracts client phone number and message text
3. Forwards the message to `/processConversation` endpoint for processing
4. Deletes the processed notification from Green API queue

You can customize the message processing logic in `src/controllers/conversation_controller.py`.

## Docker Support

Build and run with Docker:

```bash
docker-compose up --build
```

## API Documentation
- Interactive Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure
```
src/
├── config/
│   └── settings.py                    # Configuration and environment variables
├── controllers/
│   ├── conversation_controller.py     # Conversation processing endpoint
│   └── webhook_controller.py          # Webhook endpoint for incoming messages
├── models/
│   ├── conversation.py                # Conversation models
│   ├── webhook.py                     # Webhook data models
│   └── whatsapp_message.py            # WhatsApp message models
├── services/
│   ├── message_receiver.py            # Incoming message polling service
│   └── whatsapp_service.py            # WhatsApp message sending service
└── main.py                            # FastAPI application and lifespan management
```

## Examples

See the `examples/` directory for usage examples:
- [Send Message Example](./examples/send_message_example.py)
- [Send Images Example](./examples/send_images_example.py)
- [Send File Example](./examples/send_file_example.py)

## Customization

### Add Custom Message Processing Logic
Edit `src/controllers/conversation_controller.py` in the `process_conversation` function:

```python
async def process_conversation(request: ProcessConversationRequest):
    # Add your custom logic here:
    # - Save to database
    # - Trigger AI chatbot
    # - Send automated reply
    # - Update CRM system
    # etc.
    
    logger.info(f"Processing message from {request.client_phone}: {request.message}")
    
    # Your code here...
    
    return ProcessConversationResponse(...)
```

## Error Handling
- All endpoints include comprehensive error handling
- Errors are logged with full context for debugging
- HTTP status codes follow REST conventions

## Logging
The application uses Python's standard logging module. Logs include:
- Incoming message notifications
- Message processing status
- API call results
- Error traces

## License
MIT