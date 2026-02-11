import google.generativeai as genai
import os
import json

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use stable model
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_trip_plan(data):
    prompt = f"""
You are an expert AI travel planner.

Create a detailed travel plan with:
- Destination: {data['destination']}
- Duration: {data['days']} days
- Budget: ₹{data['budget']}
- Group type: {data['group_type']}
- Travel style: {data['vibe']}

IMPORTANT:
Return ONLY valid JSON.
Do NOT include explanations.
Do NOT include markdown.
Do NOT include extra text.

Use this exact structure:

{{
  "summary": "Short trip overview",
  "total_cost": number,
  "cost_breakdown": [
    {{ "category": "Stay", "amount": number }},
    {{ "category": "Food", "amount": number }},
    {{ "category": "Transport", "amount": number }},
    {{ "category": "Activities", "amount": number }}
  ],
  "itinerary": [
    {{
      "day": 1,
      "title": "Day title",
      "activities": [
        {{
          "time": "09:00",
          "location": "Place name",
          "description": "Activity description",
          "estimatedCost": number
        }}
      ]
    }}
  ],
  "tips": [
    "Helpful tip 1",
    "Helpful tip 2"
  ]
}}
"""

    response = model.generate_content(prompt)

    # Extract raw text
    raw_text = response.text.strip()

    # Clean potential markdown formatting
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]

    return raw_text