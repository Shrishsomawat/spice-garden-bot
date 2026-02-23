from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
import os

# Load .env only in local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

RESTAURANT_INFO = """
You are a helpful chatbot assistant for Spice Garden Restaurant in Hyderabad.
Only answer questions related to this restaurant. Be friendly, warm and helpful.

MENU:
Starters: Veg Samosa - ₹80, Paneer Tikka - ₹180, Chicken Wings - ₹220
Main Course: Dal Makhani - ₹160, Butter Chicken - ₹250, Paneer Butter Masala - ₹200
Rice & Breads: Steamed Rice - ₹80, Butter Naan - ₹40, Jeera Rice - ₹100
Desserts: Gulab Jamun - ₹80, Ice Cream - ₹100, Kheer - ₹90
Drinks: Lassi - ₹60, Cold Coffee - ₹80, Fresh Lime Soda - ₹50

TIMINGS: Monday to Sunday, 11:00 AM to 11:00 PM
LOCATION: Banjara Hills, Hyderabad
CONTACT: +91 98765 43210
"""

@app.route("/")
def home():
    return "Spice Garden Bot is running!", 200

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    try:
        incoming_msg = request.values.get("Body", "").strip()
        
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
        resp.message(f"Sorry, something went wrong: {str(e)}")
        return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
