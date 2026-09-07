#import google.generativeai as genai
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

#Configure Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.5-flash"
#Cretae the model
#model =  genai.GenerativeModel("gemini-3.5-flash")

response_schema = {
   "type":"object",
   "properties":{
      "answer":{ "type":"string" },
      "memory":{ "type":"string" }
   },
   "required": ["answer","memory"]
}

#model = genai.GenerativeModel(
#   "gemini-3.5-flash",
#   generation_config={
#      "response_mime_type": "appplication/json",
#      "response_schema": response_schema
#   }
#)

#Load saved memeory
memory=""

if os.path.exists("memory.txt"):
   with open("memory.txt", "r", encoding="utf-8") as file:
      memory = file.read()

#Start the chat
MODEL = "gemini-3.5-flash"

system_instruction = f"""
You are a helpful AI assistant and a patient teacher.

Explain technical concepts clearly and simply,
especially for someone learning programming,
data analytics, aand data engineering.


When explaining difficult concepts,
use simple exaples and analogies.

Do not unnecessarily overcomplicate your answers.

Here is the user's saved memory:

{memory}

Use this memory when it is relevant to the conversation.
"""

print("Chatbot is ready! Type 'exit' to stop.")

#Stores the conversation for saving
conversation=[]

#Functon to save a memory
def save_memory(new_memory):
   with open("memory.txt", "a", encoding="utf-8") as file:
      file.write(new_memory + "\n")

   print("Chatbot: I'll remember that!")

#Function to check if something should be remembered
def check_memory (user_input):
   prompt = f"""

Look at the user's message.
Decide whether it contains useful long-term information
about the user that should be remembered.

Examples:
-name
-interest
-goals
-things they are learning
-skills
-preference

Do not remember temporary or casual information.

User message:
"{user_input}"

If it is worth remembering, reply exactly like this:

Remember: <short description>

Otherwise reply exactly:

NO
"""
   
   response = model.generate_content(prompt)
   return response.text.strip()

#Function to save conversation
def save_conversation(conversation):
   os.makedirs("conversations", exist_ok=True)

   filename = datetime.now().strftime("chat_%Y-%m-%d_%H_%M_%S.txt")
   filepath = os.path.join("conversations", filename)

   with open(filepath, "w", encoding="utf-8") as file:
      for message in conversation:
         file.write(message + "\n")

   print(f"Chatbot: Conversation saved to {filepath}")


#Reading Memory file
def load_memory_file():
   """Safely load memory.txt, creating it if missing."""
   if not os.path.exists("memory.txt"):
      open("memory.txt","w",encoding="utf-8").close()
      return ""
   try:
      with open("memory.txt", "r", encoding="utf-8") as file:
         return file.read()
   except OSError as e:
      print(f"Chatbot: Couldn't read memory file ({e}). Starting fresh.")
      return ""

#Main chatbot loop
while True:

   user_input = input("You: ")

   #Save conversation
   if user_input.lower() == "/save":
     save_conversation(conversation)
     continue

   #Exit
   if user_input.lower() =='exit':
      print("Chatbot: Goodbye!")
      break

   #Help
   if user_input.lower() == '/help':
    print("""
    Available commands:
     
     /help  -Show available commands
     /save  -Save conversation
     /clear -Clear conversation memory
     /load  -Load a previous conversation
     exit   -Exit the chatbot
     """)
    continue

   #Load previous conversation
   if user_input.lower() == "/load":
     files = os.listdir("conversations")

     if not files:
        print("Chatbot: No saved conversations found.")
        continue

     print("Saved conversations: ")
     
     for i, file in enumerate(files):
        print(f"{i+1}.{file}")

     choice = input("Enter the numberof the conversation to load : ")

     try:
        choice = int(choice) -1
        filepath = os.path.join("conversations", files[choice])

        with open(filepath, "r", encoding="utf-8") as file:
           old_conversation = file.read()

        chat = model.start_chat(history=[
           {
              "role" : "user",
              "parts" : [
                 f""" Here is a previous conversation with the user:
                 {old_conversation}
               Use this conversation as context for thr current conversation
            """
              ]
           },
           {
              "role":"model",
              "parts":["Understood. I will use the previous conversation as cotext."]
           }])
        print("Chatbot: Previous conversation loaded!")

     except (ValueError, IndexError): 
         print("Chatbot: Invalid selection.")

     continue

   #Remembering conversation
   if user_input.lower().startswith("/remember"):
     new_memory = user_input[10:].strip()

     if not new_memory:
        print("Chatbot: Please tell me what you want me to remember.")
        continue

     existing_memory = load_memory_file()

     if new_memory in existing_memory:
        print("Chatbot: I already remember that!")
     else:
        save_memory(new_memory)

     continue

   #Clear conversation
   if user_input.lower() == "/clear":
      chat = model.start_chat(history=[])
      conversation.clear()
      print("Chatbot: Conversation cleared!")
      continue

   #Send response to Gemini

  #response = chat.send_message(user_input)
  #print("Chatbot: ", response.text)

   response = client.models.generate_content(
       model=MODEL,
      contents=user_input,
      config=types.GenerateContentConfig(
         system_instruction=system_instruction,
         response_mime_type="application/json",
         response_schema=response_schema
      )
   )


   #Convert Gemini's JSON response into python data
   result = response.parsed

   answer = result["answer"]
   new_memory = result["memory"]



   #Save new memory if Gemini found useful information
   if new_memory:
     existing_memory = load_memory_file()

     if new_memory not in existing_memory:
         save_memory(new_memory)
         print("Chatbot : Memory updated!")

   #Display response
   print("Chatbot :", answer)

   #Start conversation
   conversation.append("You: " + user_input)
   conversation.append("Chatbot: " + response.text)