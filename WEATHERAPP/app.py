from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Replace with your real API key from openweathermap.org
API_KEY = "e96183ff5c085404d3b25846e03fc184"

def get_outfit(temp, condition):
    if temp >= 30:
        outfit = " Wear light cotton clothes, shorts and sunglasses!"
    elif temp >= 20:
        outfit = " Wear comfortable clothes like a t-shirt and jeans!"
    elif temp >= 10:
        outfit = "Wear a jacket or sweater!"
    else:
        outfit = " Wear a heavy coat, scarf and gloves!"
    if "rain" in condition.lower():
        outfit += " Don't forget your  umbrella!"
    return outfit

def get_farmer_tip(temp, condition, humidity, rain_chance):
    if rain_chance >= 70:
        return " High chance of rain today! Avoid harvesting. Good day for planting. Keep equipment dry!"
    elif rain_chance >= 40:
        return " Moderate chance of rain. Water crops lightly in morning. Be ready to cover sensitive plants!"
    elif temp >= 35:
        return " Very hot and dry day! Water crops early morning or evening. Protect sensitive plants!"
    elif humidity >= 80:
        return " High humidity! Watch out for fungal diseases. Ensure good drainage in your farm!"
    elif temp >= 25:
        return " Great day for harvesting and drying crops! Good sunshine for solar drying!"
    else:
        return " Moderate weather. Good day for general farm maintenance and weeding!"

def get_activity(temp, condition, rain_chance):
    if rain_chance >= 70:
        return " High chance of rain! Stay indoors. Great day for reading, cooking, or indoor exercises!"
    elif rain_chance >= 40:
        return " Rain possible today! Plan indoor activities but keep an eye on the weather!"
    elif temp >= 35:
        return " Too hot for outdoor activities! Try swimming or stay in a cool place!"
    elif temp >= 25:
        return " Perfect day for outdoor sports, picnics, or visiting the park!"
    else:
        return " Nice day for a walk, jogging, or sightseeing!"

def get_health_tip(temp, condition, humidity, rain_chance):
    if rain_chance >= 70:
        return "Rainy day ahead! Avoid getting wet to prevent cold and flu. Keep warm and dry!"
    elif temp >= 35:
        return " Extreme heat! Drink at least 3 litres of water. Avoid going out between 12pm-3pm!"
    elif temp >= 30:
        return "Hot day! Stay hydrated with at least 8 glasses of water. Wear sunscreen outside!"
    elif humidity >= 80:
        return " High humidity! People with asthma should be careful. Stay in ventilated areas!"
    else:
        return " Good weather for your health! Great day for outdoor exercise and fresh air!"

def get_rain_alert(rain_chance):
    if rain_chance >= 80:
        return " Heavy rain expected today! Carry an umbrella and avoid flooded areas!"
    elif rain_chance >= 60:
        return "Good chance of rain today! Keep an umbrella handy!"
    elif rain_chance >= 40:
        return "Rain possible today! Keep an eye on the sky!"
    elif rain_chance >= 20:
        return " Small chance of rain! Probably a dry day!"
    else:
        return "Very unlikely to rain today! Enjoy the dry weather!"

@app.route("/", methods=["GET", "POST"])
def weather():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form["city"]

        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        try:
            current_response = requests.get(current_url)
            current_data = current_response.json()

            print("API Response:", current_data)

            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()

            if current_data["cod"] == 200:
                temp = current_data["main"]["temp"]
                condition = current_data["weather"][0]["description"]
                humidity = current_data["main"]["humidity"]
                feels_like = current_data["main"]["feels_like"]
                wind_speed = current_data["wind"]["speed"]
                country = current_data["sys"]["country"]

                rain_chance = 0
                forecast_days = []

                if forecast_data.get("list"):
                    first_forecast = forecast_data["list"][0]
                    rain_chance = int(first_forecast.get("pop", 0) * 100)

                    seen_dates = []
                    for item in forecast_data["list"]:
                        date = item["dt_txt"].split(" ")[0]
                        if date not in seen_dates and len(seen_dates) < 3:
                            seen_dates.append(date)
                            day_rain = int(item.get("pop", 0) * 100)
                            day_temp = round(item["main"]["temp"])
                            day_condition = item["weather"][0]["description"].title()
                            forecast_days.append({
                                "date": date,
                                "temp": day_temp,
                                "condition": day_condition,
                                "rain_chance": day_rain
                            })

                weather_data = {
                    "city": city.title(),
                    "country": country,
                    "temp": round(temp),
                    "condition": condition.title(),
                    "humidity": humidity,
                    "feels_like": round(feels_like),
                    "wind_speed": wind_speed,
                    "rain_chance": rain_chance,
                    "rain_alert": get_rain_alert(rain_chance),
                    "outfit": get_outfit(temp, condition),
                    "farmer_tip": get_farmer_tip(temp, condition, humidity, rain_chance),
                    "activity": get_activity(temp, condition, rain_chance),
                    "health_tip": get_health_tip(temp, condition, humidity, rain_chance),
                    "forecast": forecast_days
                }
            else:
                error = "City not found! Please check the city name."
                print("Error from API:", current_data)

        except Exception as e:
            error = "Something went wrong! Please try again."
            print("Exception:", e)

    return render_template("weather.html", weather=weather_data, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4500))
    app.run(host="0.0.0.0", port=4500, debug=True)
