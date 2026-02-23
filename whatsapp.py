from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)