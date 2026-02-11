from flask import Flask, render_template, request
from services.gemini_service import generate_trip_plan
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/plan", methods=["POST"])
def plan_trip():
    try:
        # Collect form data
        data = {
            "destination": request.form.get("destination"),
            "days": int(request.form.get("days")),
            "budget": int(request.form.get("budget")),
            "group_type": request.form.get("people", "Solo"),
            "vibe": request.form.get("vibe", "Balanced"),
        }

        # Call Gemini service
        ai_response = generate_trip_plan(data)

        # Convert AI response to dictionary
        plan = json.loads(ai_response)

        # Budget check
        if plan["total_cost"] > data["budget"]:
            return render_template(
                "error.html",
                message="Your budget is insufficient for this trip."
            )

        # Calculate budget percentage (for progress bar if used)
        budget_percentage = round(
            (plan["total_cost"] / data["budget"]) * 100, 2
        )

        # Render result page
        return render_template(
            "result.html",
            destination=data["destination"],
            days=data["days"],
            people=data["group_type"],
            budget=data["budget"],
            total_cost=plan["total_cost"],
            itinerary=plan["itinerary"],
            cost_breakdown=plan["cost_breakdown"],
            tips=plan.get("tips", []),
            summary=plan.get("summary", ""),
            budget_percentage=budget_percentage
        )

    except Exception as e:
        # Print error in terminal for debugging
        print("ERROR:", e)

        return render_template(
            "error.html",
            message=str(e)
        )


if __name__ == "__main__":
    app.run(debug=True)