import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_explanation(class_level, subject, level, weak_topics):
    prompt = f"""
You are an experienced teacher.

Student details:
- Class: {class_level}
- Subject: {subject}
- Learning Level: {level}
- Weak Topics: {", ".join(weak_topics)}

Explain the weak topics clearly.

While explaining:
- Use very simple language suitable for the student's level
- Include 1–2 visual-style explanations (describe them clearly)
- Use analogies (daily life examples)
- Break concepts step-by-step

When you include a visual, clearly label it as:
[VISUAL IDEA]

End with 3 short key takeaways.
"""

    model = genai.GenerativeModel("gemini-1.0-pro")

    response = model.generate_content(prompt)

    return response.text
