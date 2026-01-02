import os
import uvicorn
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. Cargar la clave
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: No se encontró la API KEY en el archivo .env")

app = FastAPI()

# 2. Configurar permisos (CORS) para que Angular pueda entrar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Usamos la conexión directa (REST API) porque es compatible con todo
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": request.message}]
        }]
    }

    try:
        # Enviamos el mensaje a Google
        response = requests.post(url, json=payload)
        response.raise_for_status() # Avisa si hay error
        
        data = response.json()
        
        # Sacamos el texto limpio de la respuesta
        reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
        
        return {"reply": reply_text}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)