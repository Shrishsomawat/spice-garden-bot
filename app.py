import streamlit as st
from groq import Groq

# ----- YOUR API KEY -----
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)



# ----- RESTAURANT DETAILS -----
RESTAURANT_NAME = "Spice Garden Restaurant"
RESTAURANT_INFO = """
You are a helpful chatbot assistant for Spice Garden Restaurant in Hyderabad.
Only answer questions related to this restaurant. Be friendly, warm and helpful.

Here is all the information you know:

MENU:
Starters: Veg Samosa - ₹80, Paneer Tikka - ₹180, Chicken Wings - ₹220
Main Course: Dal Makhani - ₹160, Butter Chicken - ₹250, Paneer Butter Masala - ₹200
Rice & Breads: Steamed Rice - ₹80, Butter Naan - ₹40, Jeera Rice - ₹100
Desserts: Gulab Jamun - ₹80, Ice Cream - ₹100, Kheer - ₹90
Drinks: Lassi - ₹60, Cold Coffee - ₹80, Fresh Lime Soda - ₹50

TIMINGS: Monday to Sunday, 11:00 AM to 11:00 PM
LOCATION: Banjara Hills, Hyderabad
CONTACT: +91 98765 43210
RESERVATION: Call between 10 AM - 9 PM to book a table

If someone asks something not related to the restaurant, politely say:
"I can only help with questions about Spice Garden Restaurant!"
"""

# ----- AI REPLY FUNCTION -----
def get_ai_reply(user_message, chat_history):
    try:
        # Build message history for context
        messages = [{"role": "system", "content": RESTAURANT_INFO}]
        
        for msg in chat_history[-6:]:
            if msg["role"] == "user":
                messages.append({"role": "user", "content": msg["content"]})
            else:
                messages.append({"role": "assistant", "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",

            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


# ----- WEB APP DESIGN -----
st.set_page_config(page_title="Spice Garden Chatbot", page_icon="🍛")

st.title("🍛 Spice Garden Restaurant")
st.subheader("Chat with us — we're here 24/7!")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "bot",
        "content": "👋 Welcome to Spice Garden Restaurant! I'm your AI assistant. Ask me anything about our menu, timings, location or reservations!"
    })

for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("Thinking..."):
        reply = get_ai_reply(user_input, st.session_state.messages)

    st.session_state.messages.append({"role": "bot", "content": reply})
    st.chat_message("assistant").write(reply)

