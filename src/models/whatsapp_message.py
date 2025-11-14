from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import Optional, List
import re

class WhatsAppMessageRequest(BaseModel):
    recipient: str = Field(..., description="The phone number of the recipient in international format, e.g., +1234567890.")
    message: str = Field(..., description="The text message to send.")
    media_url: Optional[HttpUrl] = Field(None, description="Optional URL to media (image, video, etc.) to send.") 
    
    @field_validator('recipient')
    @classmethod
    def validate_recipient(cls, v):
        if not v.startswith('+') or not v[1:].isdigit():
            raise ValueError('Recipient must be in international format, e.g., +1234567890')
        return v

class WhatsAppFileRequest(BaseModel):
    recipient: str = Field(..., description="The phone number of the recipient in international format, e.g., +1234567890.")
    file_url: HttpUrl = Field(..., description="List of image URLs to send.")
    caption: Optional[str] = Field(None, description="Optional caption for the images.")
    extension: str = Field(default='png', description="File extension" )
    
    @field_validator('recipient')
    @classmethod
    def validate_recipient(cls, v):
        if not v.startswith('+') or not v[1:].isdigit():
            raise ValueError('Recipient must be in international format, e.g., +1234567890')
        return v

class ResetConversationRequest(BaseModel):
    client_phone: str = Field(..., description="The phone number of the client in international format, e.g., +1234567890.")

