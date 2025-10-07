"""
Controller for handling Green API webhook notifications.
Receives incoming WhatsApp messages and processes them.
"""

from fastapi import APIRouter, HTTPException, Request
from src.models.webhook import GreenAPIWebhook
from typing import Dict, Any
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/webhook",
    summary="Receive WhatsApp webhook notifications",
    description="Endpoint for receiving incoming WhatsApp messages from Green API webhook"
)
async def receive_webhook(request: Request) -> Dict[str, str]:
   
    try:
        # Get raw JSON data
        data = await request.json()
        
        # Try alternative parsing for direct webhook format
        if "typeWebhook" in data:
            type_webhook = data.get("typeWebhook")
                
            if type_webhook == "incomingMessageReceived":
                sender_data = data.get("senderData", {})
                message_data = data.get("messageData", {})
                    
                sender = sender_data.get("sender", "")
                phone_number = sender.replace("@c.us", "")
                    
                if not phone_number.startswith("+"):
                    phone_number = f"+{phone_number}"
                    
                text_message_data = message_data.get("textMessageData", {})
                message_text = text_message_data.get("textMessage", "")
                    
                # Output to console
                # print("=" * 60)
                # print(f"📱 НОВОЕ СООБЩЕНИЕ ИЗ WHATSAPP")
                # print(f"📞 Номер телефона: {phone_number}")
                # print(f"💬 Сообщение: {message_text}")
                # print("=" * 60)

                profile = (requests.get("http://51.250.42.45:2025/ai/getProfile", json={"client_phone": phone_number})).json()
                
                if profile: # если профиль есть, то обрабатываем сообщение
                    print(f"📞 Номер телефона: {phone_number}")
                    print(f"💬 Сообщение: {message_text}")
                    requests.post("http://51.250.42.45:2025/ai/processConversation", json={"client_phone": phone_number, "message": message_text})

                return {"status": "ok", "message": "Webhook received and processed"}
            
         # If we can't parse it, just acknowledge receipt
        logger.warning("Received webhook in unknown format")
        return {"status": "ok", "message": "Webhook received"}
            
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        # Still return 200 to avoid webhook retries
        return {"status": "error", "message": f"Error: {str(e)}"}


@router.get(
    "/webhook",
    summary="Webhook verification endpoint",
    description="Used by some services to verify webhook endpoint is accessible"
)
async def verify_webhook() -> Dict[str, str]:
    """
    Verification endpoint for webhook.
    Some services send GET requests to verify the endpoint is working.
    
    Returns:
        Dict confirming webhook is active
    """
    return {"status": "ok", "message": "Webhook endpoint is active"}
