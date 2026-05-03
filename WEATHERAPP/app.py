from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = "e96183ff5c085404d3b25846e03fc184"

def get_outfit(temp, condition):
    if temp >= 30:
        outfit = "Wear light cotton clothes, shorts and sunglasses!"
    elif temp >= 20:
        outfit = "Wear comfortable clothes like a t-shirt and jeans!"
    elif temp >= 10:
        outfit = "Wear a jacket or sweater!"
    else:
        outfit = "Wear a heavy coat, scarf and gloves!"
    if "rain" in condition.lower():
        outfit += " Don't forget your  umbrella!"
    return outfit

def get_farmer_tip(temp, condition, humidity):
    if "rain" in condition.lower():
        return "Good day for planting! Rain will water your crops naturally. Avoid using pesticides today!"
    elif temp >= 35:
        return "Very hot day! Water your crops early morning or evening. Protect sensitive plants from direct sun!"
    elif humidity >= 80:
        return "High humidity today! Watch out for fungal diseases on crops. Ensure good drainage!"
    elif temp >= 25 and "clear" in condition.lower():
        return "Great day for harvesting and drying crops! Good sunshine for solar drying!"
    else:
        return "Moderate weather today. Good day for general farm maintenance and weeding!"

def get_activity(temp, condition):
    if "rain" in condition.lower():
        return "Stay indoors! Great day for reading, cooking, or indoor exercises!"
    elif temp >= 35:
        return "Too hot for outdoor activities! Try swimming or stay in a cool place!"
    elif temp >= 25 and "clear" in condition.lower():
        return "Perfect day for outdoor sports, picnics, or visiting the park!"
    elif temp >= 20:
        return "Nice day for a walk, jogging, or sightseeing!"
    else:
        return "☕ Cool weather! Perfect for a warm drink and light indoor activities!"

def get_health_tip(temp, condition, humidity):
    if temp >= 35:
        return "Extreme heat! Drink at least 3 litres of water. Avoid going out between 12pm-3pm. Watch for heat exhaustion!"
    elif temp >= 30:
        return "Hot day! Stay hydrated with at least 8 glasses of water. Wear sunscreen if going outside!"
    elif "rain" in condition.lower():
        return "Rainy day! Avoid getting wet to prevent cold and flu. Keep warm and dry!"
    elif humidity >= 80:
        return "High humidity! People with asthma or breathing issues should be careful. Stay in ventilated areas!"
    else:
        return "Good weather for your health! Great day for outdoor exercise and fresh air!"

@app.route("/", methods=["GET", "POST"])
def weather():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] == 200:
                temp = data["main"]["temp"]
                condition = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                feels_like = data["main"]["feels_like"]
                wind_speed = data["wind"]["speed"]
                country = data["sys"]["country"]

                weather_data = {
                    "city": city.title(),
                    "country": country,
                    "temp": round(temp),
                    "condition": condition.title(),
                    "humidity": humidity,
                    "feels_like": round(feels_like),
                    "wind_speed": wind_speed,
                    "outfit": get_outfit(temp, condition),
                    "farmer_tip": get_farmer_tip(temp, condition, humidity),
                    "activity": get_activity(temp, condition),
                    "health_tip": get_health_tip(temp, condition, humidity)
                }
            else:
                error = "City not found! Please check the city name."
        except:
            error = "Something went wrong! Please try again."

    return render_template("weather.html", weather=weather_data, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port, debug=False)