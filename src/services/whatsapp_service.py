from src.models.whatsapp_message import WhatsAppMessageRequest, WhatsAppImagesRequest
from fastapi import HTTPException, UploadFile
from pydantic import HttpUrl
import logging
from src.config.settings import settings
import httpx
import requests
from typing import List, Optional

async def send_whatsapp_message(request: WhatsAppMessageRequest) -> dict:
    """
    Sending a WhatsApp message
    """
    # Example: Use settings.whatsapp_api_key in real API call
    # api_key = settings.whatsapp_api_key
    if not request.recipient.startswith('+') or not request.recipient[1:].isdigit():
        logging.error(f"Invalid recipient format: {request.recipient}")
        raise HTTPException(status_code=400, detail="Recipient must be in international format, e.g., +1234567890.")
    if not request.message.strip():
        logging.error("Message body is empty.")
        raise HTTPException(status_code=400, detail="Message body cannot be empty.")

    url = f"{settings.api_url}/waInstance{settings.id_instance}/sendMessage/{settings.api_token_instance}"
    payload = {
        "chatId": f"{request.recipient.replace('+', '')}@c.us",
        "message": request.message
    }
    if request.media_url:
        payload["file"] = str(request.media_url)  # Convert HttpUrl to string
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        logging.error(f"Green API error: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=502, detail=f"WhatsApp API error: {exc.response.text}")
    except Exception as exc:
        logging.error(f"Unexpected error: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error while sending WhatsApp message.")


async def send_whatsapp_image(request: WhatsAppImagesRequest) -> dict:
    url = f"{settings.api_url}/waInstance{settings.id_instance}/sendFileByUrl/{settings.api_token_instance}"

    payload = {
    "chatId": f"{request.recipient.replace('+', '')}@c.us", 
    "urlFile": str(request.image_url),  # Convert HttpUrl to string
    "fileName": "photo.png" 
    }
    
    if request.caption:
        payload["caption"] = request.caption

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as exc:
        logging.error(f"Green API error: {response.status_code} - {response.text}")
        raise HTTPException(status_code=502, detail=f"WhatsApp API error: {response.text}")
    except Exception as exc:
        logging.error(f"Unexpected error: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error while sending WhatsApp image.")
