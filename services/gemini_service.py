from google import genai
import os
import json

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_trip_plan(data):
    try:
        prompt = f"""
        Create a detailed travel plan for:
        Destination: {data['destination']}
        Days: {data['days']}
        Budget: ₹{data['budget']}
        Group: {data['group_type']}
        Style: {data['vibe']}

        Return ONLY valid JSON.
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        # Fallback demo plan (NO API NEEDED)
        demo_plan = {
            "summary": f"A wonderful {data['days']}-day trip to {data['destination']} with a {data['vibe']} experience.",
            "total_cost": int(data["budget"] * 0.8),
            "cost_breakdown": [
                {"category": "Stay", "amount": int(data["budget"] * 0.4)},
                {"category": "Food", "amount": int(data["budget"] * 0.2)},
                {"category": "Transport", "amount": int(data["budget"] * 0.15)},
                {"category": "Activities", "amount": int(data["budget"] * 0.05)}
            ],
            "itinerary": [
                {
                    "day": i + 1,
                    "title": f"Explore Day {i + 1}",
                    "activities": [
                        {
                            "time": "09:00 AM",
                            "location": f"Main Attraction {i + 1}",
                            "description": "Explore local sightseeing spots and enjoy the culture.",
                            "estimatedCost": 1000
                        },
                        {
                            "time": "02:00 PM",
                            "location": "Local Restaurant",
                            "description": "Enjoy local cuisine.",
                            "estimatedCost": 800
                        }
                    ]
                }
                for i in range(data["days"])
            ],
            "tips": [
                "Carry cash and ID.",
                "Start early to avoid crowds.",
                "Try local food specialties."
            ]
        }

        return json.dumps(demo_plan)