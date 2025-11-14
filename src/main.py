from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from typing import List, Optional
import requests
from src.models.whatsapp_message import WhatsAppMessageRequest, WhatsAppFileRequest
from src.services.whatsapp_service import send_whatsapp_message, send_whatsapp_file
from src.controllers.webhook_controller import router as webhook_router
from src.models.whatsapp_message import ResetConversationRequest

app = FastAPI(
    title="WhatsApp Messaging API", 
    description="API to send and receive messages from WhatsApp accounts via Green API.", 
    version="1.0.0"
)

# Include routers
app.include_router(webhook_router, tags=["Webhook"])


@app.post("/send-message", summary="Send a WhatsApp message", response_description="Message sent successfully")
async def send_message(request: WhatsAppMessageRequest):
    """
    Send a WhatsApp message to a recipient.
    """
    response = await send_whatsapp_message(request)
    return response


@app.post("/sendFile", summary="Send multiple images to WhatsApp", response_description="File sent successfully")
async def send_images(request: WhatsAppFileRequest):
    """
    Send multiple file to a WhatsApp recipient using image URLs.
    
    - **recipient**: Phone number in international format (e.g., +1234567890)
    - **image_urls**: List of image URLs to send
    - **caption**: Optional caption for the first image
    """
    response = await send_whatsapp_file(request)
    return response

    
@app.get("/", summary="Health check", description="Check if the API is running")
async def health_check():
    """
    Health check endpoint to verify the API is operational.
    """
    return {
        "status": "ok",
        "service": "WhatsApp Messaging API",
        "version": "1.0.0",
        "webhook_enabled": True
    } 


@app.delete("/resetConversation", summary="Reset conversation", description="Reset conversation for a client")
async def reset_conversation(request: ResetConversationRequest):
    """
    Reset conversation for a client
    """
    requests.delete('http://51.250.42.45:2025/ai/resetConversation', json=request.model_dump())
    requests.post('http://51.250.42.45:2025/ai/initConversation', json=request.model_dump())

    return {
        "status": "ok",
        "message": "Conversation reset successfully"
    }