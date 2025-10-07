"""
Pydantic models for Green API webhook incoming messages.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class TextMessageData(BaseModel):
    """Text message data from webhook."""
    textMessage: str = Field(..., description="The text content of the message")


class MessageData(BaseModel):
    """Message data structure from webhook."""
    typeMessage: str = Field(..., description="Type of message (textMessage, imageMessage, etc.)")
    textMessageData: Optional[TextMessageData] = Field(None, description="Text message data if type is textMessage")
    extendedTextMessageData: Optional[Dict[str, Any]] = Field(None, description="Extended text message data")


class SenderData(BaseModel):
    """Sender information from webhook."""
    chatId: str = Field(..., description="Chat ID of the sender")
    sender: str = Field(..., description="Sender phone number with @c.us suffix")
    senderName: Optional[str] = Field(None, description="Name of the sender")


class InstanceData(BaseModel):
    """Instance information from webhook."""
    idInstance: int = Field(..., description="Instance ID")
    wid: str = Field(..., description="WhatsApp ID")
    typeInstance: str = Field(..., description="Type of instance")


class WebhookBody(BaseModel):
    """Main webhook body structure from Green API."""
    typeWebhook: str = Field(..., description="Type of webhook event (e.g., incomingMessageReceived)")
    instanceData: InstanceData = Field(..., description="Instance information")
    timestamp: int = Field(..., description="Unix timestamp of the event")
    idMessage: str = Field(..., description="Unique message ID")
    senderData: SenderData = Field(..., description="Sender information")
    messageData: MessageData = Field(..., description="Message content and metadata")


class GreenAPIWebhook(BaseModel):
    """
    Complete webhook structure from Green API for incoming messages.
    This is the top-level model that receives the entire webhook payload.
    """
    receiptId: Optional[int] = Field(None, description="Receipt ID for acknowledgment")
    body: WebhookBody = Field(..., description="Main webhook data")




