# -*- coding: utf-8 -*-

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!", 200

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    try:
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
        client = Groq(api_key=GROQ_API_KEY)
        
        incoming_msg = request.values.get("Body", "").strip()
        
        RESTAURANT_INFO = """
You are a helpful chatbot assistant for Spice Garden Restaurant in Hyderabad.
Only answer questions related to this restaurant. Be friendly, warm and helpful.

MENU:
Starters: Veg Samosa - Rs80, Paneer Tikka - Rs180, Chicken Wings - Rs220
Main Course: Dal Makhani - Rs160, Butter Chicken - Rs250, Paneer Butter Masala - Rs200
Rice & Breads: Steamed Rice - Rs80, Butter Naan - Rs40, Jeera Rice - Rs100
Desserts: Gulab Jamun - Rs80, Ice Cream - Rs100, Kheer - Rs90
Drinks: Lassi - Rs60, Cold Coffee - Rs80, Fresh Lime Soda - Rs50

TIMINGS: Monday to Sunday, 11:00 AM to 11:00 PM
LOCATION: Banjara Hills, Hyderabad
CONTACT: +91 98765 43210
"""
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": RESTAURANT_INFO},
                {"role": "user", "content": incoming_msg}
            ],
            max_tokens=300
        )
        
        reply_text = response.choices[0].message.content
        resp = MessagingResponse()
        resp.message(reply_text)
        return str(resp)

    except Exception as e:
        resp = MessagingResponse()
        resp.message(f"Error: {str(e)}")
        return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
