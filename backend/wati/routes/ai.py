from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
import os
import httpx
from ..oauth2 import get_current_user


router = APIRouter(prefix="/ai", tags=["AI"])


class GenerateTemplateRequest(BaseModel):
    customer_name: str | None = None
    product_name: str | None = None
    intent: str | None = None  # e.g., "order_update", "payment_reminder", "welcome"
    notes: str | None = None
    api_key_override: Optional[str] = None


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class CRMChatRequest(BaseModel):
    messages: list[ChatMessage]
    situation: Optional[str] = None
    tone: Optional[str] = None
    api_key_override: Optional[str] = None


class CRMChatResponse(BaseModel):
    reply: str
    usage: Optional[dict] = None


OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


SYSTEM_PROMPT = (
    "You are a helpful CRM assistant creating personalized WhatsApp template messages. "
    "Analyze the customer context and agent notes to create relevant, engaging responses. "
    "Return ONLY a valid JSON object with this structure: "
    "{\"components\": [{\"type\": \"header\", \"parameters\": [{\"type\": \"text\", \"text\": \"Header Text\"}]}, "
    "{\"type\": \"body\", \"parameters\": [{\"type\": \"text\", \"text\": \"Main message body\"}]}, "
    "{\"type\": \"footer\", \"parameters\": [{\"type\": \"text\", \"text\": \"Footer text\"}]}, "
    "{\"type\": \"button\", \"parameters\": [{\"type\": \"quick_reply\", \"text\": \"Reply button\"}]}]}. "
    "Personalize based on customer name and conversation context. Keep professional but warm."
)


def build_user_prompt(payload: GenerateTemplateRequest) -> str:
    prompt_parts = []
    
    # Start with the main request
    prompt_parts.append("Create a personalized WhatsApp template message.")
    
    # Add customer context if available
    if payload.customer_name:
        prompt_parts.append(f"Customer name: {payload.customer_name}")
    
    if payload.product_name:
        prompt_parts.append(f"Product/service: {payload.product_name}")
    
    if payload.intent:
        prompt_parts.append(f"Purpose: {payload.intent}")
    
    # Add detailed notes/context - this is the key part
    if payload.notes:
        prompt_parts.append(f"Context and instructions:\n{payload.notes}")
    
    # Add formatting reminder
    prompt_parts.append("\nCreate an appropriate header, body message, and if relevant, a footer and quick reply button. Make it conversational and specific to this situation.")
    
    return "\n\n".join(prompt_parts)


@router.post("/generate-template")
async def generate_template(req: GenerateTemplateRequest, user=Depends(get_current_user)):
    api_key = req.api_key_override or OPENAI_API_KEY

    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(req)},
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"},
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(f"{OPENAI_BASE_URL}/chat/completions", headers=headers, json=body)
            resp.raise_for_status()
            data = resp.json()

        content = data["choices"][0]["message"]["content"]
        # Ensure content is a JSON-compatible string
        return {"template": content}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


CRM_SYSTEM_PROMPT = (
    "You are a senior CRM specialist helping an agent craft messages for customers via WhatsApp. "
    "Respond with concise, empathetic, and action-oriented copy. "
    "Incorporate available context about the customer or scenario."
)


@router.post("/chat", response_model=CRMChatResponse)
async def crm_chat(req: CRMChatRequest, user=Depends(get_current_user)):
    api_key = req.api_key_override or OPENAI_API_KEY

    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    system_prompt = CRM_SYSTEM_PROMPT
    if req.tone:
        system_prompt += f" Use a {req.tone.lower()} tone."

    messages_payload = [{"role": "system", "content": system_prompt}]

    if req.situation:
        messages_payload.append({
            "role": "user",
            "content": f"Here is the CRM situation to consider:\n{req.situation.strip()}",
        })

    # Limit conversation history to last 12 exchanges to avoid overly long prompts
    for message in req.messages[-12:]:
        messages_payload.append({
            "role": message.role,
            "content": message.content,
        })

    if len(messages_payload) == 1:
        raise HTTPException(status_code=400, detail="At least one message is required")

    body = {
        "model": OPENAI_MODEL,
        "messages": messages_payload,
        "temperature": 0.6,
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{OPENAI_BASE_URL}/chat/completions", headers=headers, json=body
            )
            resp.raise_for_status()
            data = resp.json()

        content = data["choices"][0]["message"]["content"].strip()
        usage = data.get("usage")

        return CRMChatResponse(reply=content, usage=usage)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


