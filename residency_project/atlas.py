import streamlit as st
import openai
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

# Set page configuration
st.set_page_config(page_title="ATLAS - YOUR PERSONAL NAVIGATOR", layout="wide", initial_sidebar_state="expanded")

AZURE_OPENAI_ENDPOINT = "endpoint"
AZURE_OPENAI_API_KEY = "key"
AZURE_OPENAI_DEPLOYMENT = "gpt-35-turbo"  # Your GPT-3.5 Turbo deployment name
AZURE_OPENAI_API_VERSION = "2023-12-01-preview"  # Update if necessary

# Function to generate a response using Azure OpenAI GPT-3.5 Turbo


@st.cache_resource
def load_model():
    openai.api_base = AZURE_OPENAI_ENDPOINT
    openai.api_key = AZURE_OPENAI_API_KEY
    openai.api_type = "azure"
    openai.api_version = AZURE_OPENAI_API_VERSION
    return openai

model = load_model()

def generate_response(question, chat_history):
    messages = [
        {
            "role": "user",
            "content": question,
        },
    ]
    if chat_history !="":
        template = f"""
            Given the earlier response provided by LLM: {chat_history}, your task is to generate a customized travel itenary depending on new request: {question}
        """
        print(template)
        messages = [
            {
                "role": "user",
                "content": template,
            },
        ]
    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=0.9
    )
    return response["choices"][0]["message"]["content"]

# @st.cache_resource
# def load_model():
#     # Update to use the advanced model
#     # model_id = "EleutherAI/gpt-neo-2.7B"
#     # model_id = "deepseek-ai/DeepSeek-R2-Distill-Qwen-2.5B"
#     # model_id = "deepseek-ai/DeepSeek-R2-Distill-Qwen-2.5B"
#     # model_id = "t5-small"
#     model_id = "microsoft/DialoGPT-medium"

#     model = AutoModelForCausalLM.from_pretrained(model_id,device_map="auto", torch_dtype="auto")
#     tokenizer = AutoTokenizer.from_pretrained(model_id)
#     return model, tokenizer

# model, tokenizer = load_model()

# # Function to generate bot response based on inputs
# def generate_response(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
#     outputs = model.generate(**inputs, max_new_tokens=1024, temperature=0.7, top_p=0.9, top_k=50, do_sample=True)
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response

st.session_state.theme = 'Dark'

# Apply custom CSS for dark theme with light text and military green accents

st.markdown("""
<style>
body { background-color: #1e1e1e; color: white; }
.stButton button { background-color: #4b5320; color: white; }
.stTextInput div, .stSelectbox div, .stNumberInput div { background-color: #333333; color: white; }
[data-testid="stAppViewContainer"] { background-color: #1e1e1e; }
[data-testid="stHeader"] { background-color: #1e1e1e; }
[data-testid="stSidebar"] { background-color: #333333; color: white; }
.stMarkdown p, .stMarkdown ul, .stMarkdown ol, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown { color: white; }
.css-1d391kg, .css-qrbaxs, .css-1cpxqw2, .css-1d6s8r7, .css-1q8dd3e, .css-1v3fvcr, .css-1n76uvr, .css-1cpxqw2 { color: white !important; }
.css-1cpxqw2, .css-1d6s8r7, .css-1q8dd3e { color: white !important; }
.css-1d6s8r7, .css-qrbaxs, .css-1cpxqw2, .css-1d391kg, .css-1n76uvr { background-color: #333333 !important; }
.stTextInput, .stSelectbox, .stNumberInput, .stSidebar { background-color: #333333; color: white; }
.stButton button:hover { background-color: #6b8e23; }
.title-box { background-color: #4b5320; padding: 5px; border-radius: 5px; }
.response-box { background-color: #333333; padding: 10px; border: 1px solid #4b5320; border-radius: 5px; color: white; }
.custom-message { text-align: left; font-size: 20px; color: #6b8e23; padding: 10px 0; }
.processing { text-align: center; font-size: 20px; color: #6b8e23; padding: 10px 0; }
.processing-followup { text-align: center; font-size: 20px; color: #6b8e23; padding: 10px 0; }
.processing-hidden { display: none; }
</style>
""", unsafe_allow_html=True)

# Page title and sidebar header
st.markdown("<div class='title-box'><h1 style='text-align: center; color: #faf7f7; font-size: 3em;'>🗺️ ATLAS - <span style='font-size:0.6em;'>YOUR PERSONAL NAVIGATOR</span></h1></div>", unsafe_allow_html=True)
st.sidebar.header("Select Your Preferences")

destination = st.sidebar.text_input("Enter your travel destination:")
travel_dates = st.sidebar.date_input("Select your travel dates", [])
travel_style = st.sidebar.multiselect("Travel Style", ["Adventure", "Luxury", "Budget", "Cultural", "Relaxation", "Business"])
budget = st.sidebar.number_input("Budget", min_value=0,step=100)
currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "JPY", "AUD", "Other"])
traveling_with = st.sidebar.selectbox("Traveling With", ["Solo", "Couple", "Family", "Friends"]) 
accommodation = st.sidebar.selectbox("Preferred Accommodation", ["Hotel", "Hostel", "Airbnb", "Other"])
dietary_preferences = st.sidebar.multiselect("Dietary Preferences", ["Vegetarian", "Vegan", "Halal", "Kosher", "Gluten-Free", "No Preference"])
landmarks = st.sidebar.text_area("Must-See Landmarks")
itinerary_style = st.sidebar.radio("Preferred Itinerary Style", ["Relaxed", "Balanced", "Packed Schedule"])
additional = st.sidebar.text_input("Any additional requirements for your trip?")

# Main content
# col1, col2 = st.columns([4, 3])
# with col1:
st.markdown(
    "<h3 style='text-align: center; font-size: 20px;'>Hi, I am Atlas🗺️. Let’s Customize Your Trip With Your Preferences 📅 🧳 🌎</h3>", 
    unsafe_allow_html=True
)

# Main content
if st.sidebar.button("PLAN NOW"):
    logging.info("Send button clicked.")
    st.markdown("<div class='processing'>🤔 Your best itenary is under construction 🚧....</div>", unsafe_allow_html=True)
    prompt = (
        f"Create a detailed travel itinerary for a group consisting of {traveling_with}, "
        f"focused on attractions, restaurants, and activities for a trip to {destination}, "
        f"starting on {str(travel_dates[0]) if travel_dates else 'a selected date'}, "
        f"lasting till {str(travel_dates[1]) if len(travel_dates) > 1 else 'the end date'}, "
        f"within a budget of {currency} {budget}. This should include daily timings, "
        f"preferences for {accommodation} accommodations, food preferences highlighting "
        f"{', '.join(dietary_preferences) if dietary_preferences else 'any cuisine'}. "
        f"Also, provide a travel checklist relevant to the destination "
        f"and duration. Consider these additional requirements from the user: {additional}."
    )
    logging.info(f"Prompt: {prompt}")
    response = generate_response(prompt)
    st.session_state.response = response
    if 'response' in st.session_state:
        logging.info("Displaying response.")
        st.markdown("""<style>.processing{display: none;}</style>""", unsafe_allow_html=True)
        response = st.session_state.response.replace("\\n", "\n")
        st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)

    # Follow-up input and send button
if 'response' in st.session_state and st.session_state.response:
    # Follow-up input and send button
    follow_up = st.text_input("Provide feedback or ask follow-up questions:")
    if st.button("Send Follow-Up"):
        logging.info("Send Follow-Up button clicked.")
        st.markdown("<div class='processing-followup'>🤔 Your follow-up request is being processed 🚧. Please wait...</div>", unsafe_allow_html=True)
        follow_up_response = generate_response(prompt=follow_up, history=st.session_state.response)
        st.session_state.response = follow_up_response
        follow_up_response = st.session_state.response.replace("\\n", "\n")
        logging.info(f"Follow-Up Response: {follow_up_response}")
        st.markdown("""<style>.processing-followup{display: none;}</style>""", unsafe_allow_html=True)
        st.markdown(f"<div class='response-box'>{follow_up_response}</div>", unsafe_allow_html=True)