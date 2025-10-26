from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from utils.translator import translate_text
from utils.weather import get_weather
import google.generativeai as genai
import pyttsx3
import tempfile
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# 🔑 Setup Gemini API
genai.configure(api_key="AIzaSyDZaPRR-K5ZzFKsF1LhB74OUT5SgJM7X8k")

app = FastAPI(title="AgroMind AI Backend (Gemini Edition)")


@app.get("/")
def home():
    return {"message": "🌾 AgroMind Gemini Backend Running!"}


# 🌾 GEMINI AI CHAT
@app.post("/api/chat")
async def chat(query: str = Form(...)):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"You are AgroMind AI — an intelligent agriculture assistant. Reply in a friendly and helpful tone.\nUser: {query}"
        response = model.generate_content(prompt)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Gemini Error: {e}"

    voice_path = await text_to_voice(reply)
    return JSONResponse({"reply": reply, "voice_url": voice_path})


# 🌿 LEAF ANALYZER (same as before)
@app.post("/api/leaf")
async def analyze_leaf(file: UploadFile):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).resize((224, 224))
        img = np.expand_dims(np.array(img) / 255.0, axis=0)

        interpreter = tf.lite.Interpreter(model_path="model/leaf_model.tflite")
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        interpreter.set_tensor(input_details[0]['index'], img.astype(np.float32))
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        pred = np.argmax(output_data)

        with open("model/labels.txt") as f:
            labels = f.read().splitlines()
        result = labels[pred]

        return {"disease": result}
    except Exception as e:
        return {"error": str(e)}


# 🔊 Text-to-Speech
async def text_to_voice(text):
    tts = pyttsx3.init()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save_to_file(text, fp.name)
        tts.runAndWait()
        return fp.name
