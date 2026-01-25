import google.generativeai as genai
import sys

print("PYTHON:", sys.executable)
print("GENAI:", genai.__file__)

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Hello PadhaiMate")

print("RESPONSE:", response.text)
