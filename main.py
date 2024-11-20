import os
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

os.environ['GOOGLE_API_KEY'] = "AIzaSyAss9bhYoHWfQHMsFe7J54e_JTQUN7Fpd0"

gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-002")

# response = gemini_model.invoke("Give me a Birthday Message")

message_template = """I am a {role}. Give me {number} WhatsApp message for {occasion} for my {message_for} and 
her/his name is {name}. following this format: 

Topic: {occasion}

Message {number}:
    - message 
================================================================================


please follow the instructions:
1. Make sure name is included in message 
2. Add some related emojis 

"""

message_prompt = PromptTemplate(template=message_template,
                                input_variables=['role', 'number', 'occasion', 'message_for', 'name'])

# prompt = message_template.format(role="Employee", number=5, occasion="Anniversary", message_for="Boss",
# name="Abhijit")

# print(prompt)

message_chain = message_prompt | gemini_model

st.header("WhatsApp Message Generator")

st.subheader("Generator WhatsApp Messages for your Love ones...")

user_role = st.selectbox(
    "You are:",
    ["Select who you are...", "Brother", "Sister", "Father", "Mother", "Employee", "Boss"]
)

num_messages = st.number_input(
    "Number of Messages:",
    min_value=1,
    max_value=10,
    value=2,
    step=1
)

occasion = st.radio(
    "Occasion:",
    ["Birthday", "Anniversary"]
)

recipient_role = st.selectbox(
    "Message for:",
    ["Select for whom this message is for...", "Brother", "Sister", "Father", "Mother", "Employee", "Boss"]
)

recipient_name = st.text_input("Name:")

if st.button("Generate Message"):    
    if user_role == "Select who you are...":
        st.warning("Please Select who you are.")
    elif recipient_role == "Select for whom this message is for...":
        st.warning("Please Select for whom this message is for.")
    elif not recipient_name.strip():
        st.warning("Please enter a name to generate a message.")
    else:
        response = message_chain.invoke(
            {"role": user_role, "number": num_messages, "occasion": occasion, "message_for": recipient_role,
             "name": recipient_name})
        st.success(response.content)
