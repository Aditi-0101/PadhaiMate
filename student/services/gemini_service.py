from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_explanation(class_level, subject, level, weak_topics):
    prompt = f"""
You are an experienced teacher.

Student details:
- Class: {class_level}
- Subject: {subject}
- Learning Level: {level}
- Weak Topics: {", ".join(weak_topics)}

Explain the weak topics clearly.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        # 🔁 FALLBACK (dev mode)
        return f"""
⚠️ AI temporarily unavailable.

Topic: {weak_topics[0]}

🔹 What is Force?
Force is a push or a pull that can change:
• the shape of an object
• the speed of an object
• the direction of motion
• or stop/start motion

Example:
Pushing a door to open it or kicking a football are examples of force.

🔹 What is Motion?
Motion means a change in position of an object with time.
If an object moves from one place to another, it is said to be in motion.

🔹 Newton’s Laws of Motion (Simple Explanation)

1️⃣ First Law (Law of Inertia):
An object will remain at rest or in uniform motion unless an external force acts on it.
Example: A book on a table stays still until you push it.

2️⃣ Second Law:
Force = Mass × Acceleration (F = m × a)
Heavier objects need more force to move.
Example: Pushing a loaded cart is harder than an empty cart.

3️⃣ Third Law:
For every action, there is an equal and opposite reaction.
Example: When you jump, the ground pushes you upward.

🔹 Key Takeaway:
Force causes motion, changes motion, or stops motion.

[VISUAL IDEA]
Show:
• a ball being pushed
• a moving car
• action–reaction arrows

📌 Tip for Quiz:
Remember definitions + real-life examples.
"""