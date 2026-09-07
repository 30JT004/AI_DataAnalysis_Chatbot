import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.5-flash")

user_input = input("You: ")

prompt = f"""
You are helping manage an AI assistant's memory.

Look at what the user said:

"{user_input}"

Decide whether this contains useful personal information
that should be remembered for future conversations.

Remember things such as:
- Name
- Long-term interests
- Skills they are learning
- Preferences
- Long-term goals

Do NOT remember:
- Casual conversation
- Temporary information
- Questions the user asks
- Random facts

If it should be remembered, respond EXACTLY like this:

REMEMBER: <the useful information>

If it should not be remembered, respond EXACTLY:

NO_MEMORY
"""

response = model.generate_content(prompt)

print("Gemini:", response.text)