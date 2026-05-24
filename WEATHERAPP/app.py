from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = "b5866edda460015fa992a786c0db2f46"

def get_crop_advice(crop, temp, condition, humidity, rain_chance):
    condition = condition.lower()
    is_rainy = rain_chance >= 60 or "rain" in condition
    is_hot = temp >= 35
    is_humid = humidity >= 80
    is_cold = temp < 15

    advice = {
        "Maize": {
            "good": " Great day for maize! Warm temperatures help growth. Check for stem borers and fall armyworm.",
            "rain": " Rain is good for maize! Ensure proper drainage to avoid waterlogging and root rot.",
            "hot": " Too hot for maize! Water early morning. Watch for leaf rolling and heat stress.",
            "humid": " High humidity! Watch for maize streak virus, northern leaf blight and grey leaf spot.",
            "cold": " Too cold for maize growth. Cover young plants if possible."
        },
        "Rice": {
            "good": " Good day for rice! Check water levels in paddies. Watch for blast disease.",
            "rain": " Rain benefits rice paddies! Monitor water levels carefully to avoid flooding.",
            "hot": " Hot day! Rice needs water. Maintain paddy water levels to cool roots.",
            "humid": " High humidity increases rice blast and brown spot risk! Apply fungicide.",
            "cold": " Rice prefers warm conditions. Cold may slow growth and affect grain filling."
        },
        "Sorghum": {
            "good": " Great day for sorghum! Drought tolerant but check for aphids and shoot fly.",
            "rain": " Moderate rain is good for sorghum. Too much water causes lodging.",
            "hot": " Sorghum tolerates heat well! Ensure adequate moisture for grain filling.",
            "humid": " Watch for grain mold and downy mildew in high humidity conditions.",
            "cold": " Sorghum prefers warm weather. Cold temperatures slow development."
        },
        "Millet": {
            "good": " Good day for millet! Very drought tolerant. Check for downy mildew.",
            "rain": " Light rain benefits millet. Heavy rain can cause lodging and grain damage.",
            "hot": " Millet handles heat well! One of the most heat tolerant cereals.",
            "humid": " Watch for downy mildew and smut diseases in humid conditions.",
            "cold": " Millet prefers warm conditions. Cold slows growth significantly."
        },
        "Fonio": {
            "good": " Good day for fonio! Highly tolerant of poor conditions. Check for birds.",
            "rain": " Light rain good for fonio. Avoid waterlogging as it damages roots.",
            "hot": " Fonio tolerates heat well! Ensure minimal moisture for growth.",
            "humid": " Watch for fungal diseases in humid conditions. Ensure good air circulation.",
            "cold": " Fonio prefers warm dry conditions. Cold may slow growth."
        },
        "Yam": {
            "good": " Good day for yam! Check stakes and ensure proper hilling.",
            "rain": " Rain is beneficial for yam! Ensure mounds are intact to avoid rotting.",
            "hot": " Hot day! Yam vines may wilt. Mulch around mounds to retain moisture.",
            "humid": " High humidity! Watch for yam mosaic virus and scale insects.",
            "cold": " Yams prefer warm conditions. Cover young vines if temperature drops."
        },
        "Cassava": {
            "good": " Good day for cassava! Check for mealybugs and cassava mosaic disease.",
            "rain": " Rain benefits cassava! Ensure good drainage to prevent root rot.",
            "hot": " Cassava tolerates heat well! One of the most drought tolerant crops.",
            "humid": " Watch for cassava bacterial blight and anthracnose in humid weather.",
            "cold": " Cassava prefers warm conditions. Cold temperatures slow growth."
        },
        "Cocoyam": {
            "good": " Good day for cocoyam! Prefers shade. Check for leaf blight.",
            "rain": " Rain is good for cocoyam! Ensure partial shade and good drainage.",
            "hot": " Too much sun damages cocoyam! Provide shade and water regularly.",
            "humid": " Watch for root rot and leaf blight in high humidity conditions.",
            "cold": " Cocoyam prefers warm humid conditions. Protect from cold."
        },
        "Sweet Potato": {
            "good": " Good day for sweet potato! Check for weevils and vine borers.",
            "rain": " Light rain good for sweet potato. Heavy rain causes root cracking.",
            "hot": " Sweet potato tolerates heat! Ensure adequate moisture for vine growth.",
            "humid": " Watch for scurf and black rot diseases in humid conditions.",
            "cold": " Sweet potato needs warm soil. Cold reduces yield significantly."
        },
        "Irish Potato": {
            "good": " Good day for Irish potato! Check for late blight and aphids.",
            "rain": " Watch for late blight in rainy conditions! Apply fungicide preventively.",
            "hot": " Too hot for Irish potato! Prefers cool conditions. Shade if possible.",
            "humid": " High humidity greatly increases late blight risk! Apply fungicide urgently!",
            "cold": " Cool conditions are ideal for Irish potato! Monitor for frost damage."
        },
        "Groundnut": {
            "good": " Perfect day for groundnuts! Good sunshine helps pod development.",
            "rain": " Too much rain causes aflatoxin in groundnuts! Ensure good drainage.",
            "hot": " Hot day! Groundnuts need moisture. Water if no rain expected.",
            "humid": " High humidity increases aflatoxin risk! Harvest promptly when ready.",
            "cold": " Groundnuts prefer warm weather. Growth may slow down today."
        },
        "Cowpea (Beans)": {
            "good": " Great day for cowpea! Check for pod borers and aphids.",
            "rain": " Light rain good for cowpea. Heavy rain causes flower drop.",
            "hot": " Cowpea tolerates heat well! One of Ghana's most heat tolerant legumes.",
            "humid": " Watch for cercospora leaf spot and bacterial blight in humid weather.",
            "cold": " Cowpea prefers warm conditions. Cold slows nitrogen fixation."
        },
        "Soybean": {
            "good": " Good day for soybean! Check for soybean rust and pod borers.",
            "rain": " Rain benefits soybean! Monitor for soybean rust in wet conditions.",
            "hot": " Hot temperatures during flowering reduce soybean yield. Water regularly.",
            "humid": " High humidity increases soybean rust risk! Apply fungicide if needed.",
            "cold": " Soybean prefers warm conditions. Cold slows nodule formation."
        },
        "Bambara Bean": {
            "good": " Good day for bambara bean! Very drought tolerant crop.",
            "rain": " Light rain benefits bambara bean. Avoid waterlogging.",
            "hot": " Bambara bean tolerates heat well! One of Ghana's traditional crops.",
            "humid": " Watch for leaf spot diseases in humid conditions.",
            "cold": " Bambara bean prefers warm dry conditions."
        },
        "Pigeon Pea": {
            "good": " Good day for pigeon pea! Drought tolerant perennial legume.",
            "rain": " Rain benefits pigeon pea! Good drainage prevents root rot.",
            "hot": " Pigeon pea tolerates heat well! Deep roots access subsoil moisture.",
            "humid": " Watch for phytophthora blight in high humidity conditions.",
            "cold": " Pigeon pea prefers warm conditions. Cold affects flowering."
        },
        "Cocoa": {
            "good": " Good day for cocoa! Check for black pod disease and capsids.",
            "rain": " Rain is good for cocoa! But watch for black pod disease in wet conditions.",
            "hot": " Too hot and dry for cocoa! Water young trees. Check for red spider mites.",
            "humid": " High humidity increases black pod disease risk! Apply copper fungicide.",
            "cold": " Cocoa prefers warm humid conditions. Monitor growth carefully."
        },
        "Oil Palm": {
            "good": " Good day for oil palm! Check for rhinoceros beetle and bunch rot.",
            "rain": " Rain benefits oil palm! Ensure good drainage around base of trees.",
            "hot": " Oil palm tolerates heat well! Ensure adequate water for young trees.",
            "humid": " Watch for ganoderma disease and vascular wilt in humid conditions.",
            "cold": " Oil palm prefers warm humid conditions. Cold reduces yield."
        },
        "Coconut": {
            "good": " Good day for coconut! Check for rhinoceros beetle and lethal yellowing.",
            "rain": " Rain benefits coconut! Ensure good drainage to prevent root rot.",
            "hot": " Coconut tolerates heat well! Coastal varieties handle heat best.",
            "humid": " Watch for bud rot and stem bleeding in humid conditions.",
            "cold": " Coconut needs warm conditions. Cold temperatures damage leaves."
        },
        "Rubber": {
            "good": " Good day for rubber tapping! Best tapping time is early morning.",
            "rain": " Don't tap rubber in rain! Wait for dry conditions. Check for phytophthora.",
            "hot": " Hot day! Early morning tapping recommended before heat builds up.",
            "humid": " High humidity increases phytophthora and Fomes root rot risk!",
            "cold": " Cool conditions slow latex flow. Wait for warmer part of day to tap."
        },
        "Shea": {
            "good": " Good day for shea! Check for flowering and fruit set on trees.",
            "rain": " Rain benefits shea trees! Avoid harvesting fallen nuts in mud.",
            "hot": " Shea tolerates heat well! Native to savanna regions of Ghana.",
            "humid": " Watch for fungal diseases on shea fruits in humid conditions.",
            "cold": " Shea prefers warm dry savanna conditions."
        },
        "Coffee": {
            "good": " Good day for coffee! Check for coffee berry borer and leaf rust.",
            "rain": " Rain benefits coffee! Watch for coffee leaf rust in wet conditions.",
            "hot": " Too hot for coffee! Prefers 18-24°C. Provide shade if possible.",
            "humid": " High humidity increases coffee leaf rust risk! Apply copper fungicide.",
            "cold": " Cool conditions slow coffee growth. Protect from frost."
        },
        "Cola Nut": {
            "good": " Good day for cola nut! Check for black pod and weevils.",
            "rain": " Rain benefits cola nut trees! Ensure good drainage around base.",
            "hot": " Cola nut prefers shade. Protect young trees from direct sun.",
            "humid": " Watch for pod rot in humid conditions. Ensure good air circulation.",
            "cold": " Cola nut prefers warm humid conditions of forest zones."
        },
        "Plantain": {
            "good": " Great day for plantain! Check for weevils and sigatoka disease.",
            "rain": " Rain benefits plantain! Ensure proper drainage around plants.",
            "hot": " Hot day! Plantain leaves may scorch. Water young plants regularly.",
            "humid": " High humidity increases sigatoka risk! Remove affected leaves.",
            "cold": " Plantain prefers warm conditions. Protect young suckers from cold."
        },
        "Banana": {
            "good": " Good day for banana! Check for banana weevil and panama disease.",
            "rain": " Rain benefits banana! Ensure drainage to prevent crown rot.",
            "hot": " Hot day! Water banana plants regularly. Watch for spider mites.",
            "humid": " High humidity increases sigatoka leaf spot risk! Remove infected leaves.",
            "cold": " Banana prefers warm conditions. Cold causes chilling injury."
        },
        "Mango": {
            "good": " Good day for mango! Check for mango hopper and anthracnose.",
            "rain": " Rain during flowering reduces mango yield! Watch for anthracnose.",
            "hot": " Mango tolerates heat well! Ensure young trees have adequate water.",
            "humid": " High humidity during flowering causes anthracnose! Apply fungicide.",
            "cold": " Cool weather promotes mango flowering! Good sign for next season."
        },
        "Pineapple": {
            "good": " Good day for pineapple! Check for mealybugs and heart rot.",
            "rain": " Light rain benefits pineapple. Heavy rain causes heart rot.",
            "hot": " Pineapple tolerates heat well! Check soil moisture levels.",
            "humid": "Watch for phytophthora heart rot and root rot in humid conditions.",
            "cold": " Pineapple prefers warm conditions. Cold delays fruit development."
        },
        "Pawpaw (Papaya)": {
            "good": " Good day for pawpaw! Check for papaya ringspot virus and fruit flies.",
            "rain": " Moderate rain good for pawpaw. Waterlogging kills plants quickly!",
            "hot": " Pawpaw tolerates heat! Ensure adequate water for fruit development.",
            "humid": " Watch for powdery mildew and anthracnose in humid conditions.",
            "cold": " Pawpaw is sensitive to cold. Protect young plants from temperature drops."
        },
        "Citrus (Orange, Lemon, Lime)": {
            "good": " Good day for citrus! Check for citrus greening and scale insects.",
            "rain": " Rain benefits citrus! Ensure good drainage to prevent root rot.",
            "hot": " Hot day! Water citrus trees deeply. Watch for spider mites.",
            "humid": " High humidity increases citrus canker and melanose risk!",
            "cold": " Cold damages citrus fruits and flowers. Cover young trees."
        },
        "Avocado": {
            "good": " Good day for avocado! Check for anthracnose and avocado lace bug.",
            "rain": " Moderate rain good for avocado. Waterlogging causes root rot!",
            "hot": " Avocado tolerates heat. Mulch around base to retain soil moisture.",
            "humid": " Watch for phytophthora root rot and anthracnose in humid weather.",
            "cold": " Avocado is sensitive to frost. Protect young trees from cold."
        },
        "Watermelon": {
            "good": " Great day for watermelon! Loves sunshine. Check for aphids and fusarium.",
            "rain": " Rain can cause fruit splitting! Ensure consistent moisture levels.",
            "hot": " Watermelon loves heat! Ensure adequate water for fruit development.",
            "humid": " Watch for powdery mildew and anthracnose in humid conditions.",
            "cold": " Watermelon needs warm soil. Cold stops growth completely."
        },
        "Guava": {
            "good": " Good day for guava! Check for fruit fly and wilt disease.",
            "rain": " Rain benefits guava! Ensure drainage to prevent root rot.",
            "hot": " Guava tolerates heat well! Hardy fruit tree for Ghana's climate.",
            "humid": " Watch for anthracnose and fruit rot in humid conditions.",
            "cold": " Guava prefers warm conditions. Young trees need protection from cold."
        },
        "Soursop": {
            "good": " Good day for soursop! Check for mealybugs and scale insects.",
            "rain": " Rain benefits soursop! Ensure good drainage around trees.",
            "hot": " Soursop prefers warm humid conditions typical of Ghana.",
            "humid": " Watch for anthracnose and fruit rot in high humidity.",
            "cold": " Soursop is sensitive to cold. Keep in warm locations."
        },
        "Tomato": {
            "good": " Good day for tomatoes! Check for early blight and aphids.",
            "rain": " Rain warning! Tomatoes hate excess water. Check for blossom end rot.",
            "hot": " Too hot! Tomatoes drop flowers above 35°C. Shade and water frequently.",
            "humid": " High humidity! High risk of late blight. Apply fungicide immediately!",
            "cold": " Cool weather slows tomato growth. Cover plants at night."
        },
        "Pepper (Chilli & Bell)": {
            "good": " Good day for pepper! Check for pepper weevil and anthracnose.",
            "rain": " Light rain good for pepper. Heavy rain causes flower and fruit drop.",
            "hot": " Pepper tolerates heat! Chilli varieties especially heat tolerant.",
            "humid": " Watch for phytophthora blight and cercospora leaf spot.",
            "cold": " Pepper prefers warm conditions. Cold causes stunting."
        },
        "Onion": {
            "good": " Good day for onion! Check for thrips and downy mildew.",
            "rain": " Onions hate excess rain! Increases purple blotch and downy mildew.",
            "hot": " Hot dry conditions are good for bulb development! Reduce watering.",
            "humid": " High humidity greatly increases disease risk in onions! Apply fungicide.",
            "cold": " Cool conditions promote onion leaf growth. Good for early stages."
        },
        "Garden Egg (Eggplant)": {
            "good": " Good day for garden egg! Check for epilachna beetle and fruit borer.",
            "rain": " Light rain benefits garden egg. Avoid waterlogging.",
            "hot": " Garden egg tolerates heat well! Water regularly in hot conditions.",
            "humid": " Watch for phomopsis blight and cercospora leaf spot.",
            "cold": " Garden egg prefers warm conditions. Cold causes stunting."
        },
        "Okra": {
            "good": " Great day for okra! Very heat tolerant. Check for okra mosaic virus.",
            "rain": " Light rain good for okra. Too much water causes root rot.",
            "hot": " Okra loves heat! One of Ghana's most heat tolerant vegetables.",
            "humid": " Watch for powdery mildew and cercospora leaf spot in humid weather.",
            "cold": " Okra needs warm conditions. Cold stops growth completely."
        },
        "Cabbage": {
            "good": " Good day for cabbage! Check for caterpillars and black rot.",
            "rain": " Rain can cause head splitting in mature cabbage! Harvest promptly.",
            "hot": " Too hot for cabbage! Prefers cooler conditions. Provide shade.",
            "humid": " Watch for downy mildew and alternaria leaf spot in humid weather.",
            "cold": " Cool conditions are ideal for cabbage! Best season to grow."
        },
        "Lettuce": {
            "good": " Good day for lettuce! Cool weather crop. Check for aphids.",
            "rain": " Moderate rain good for lettuce. Heavy rain causes tip burn.",
            "hot": " Too hot for lettuce! Goes to seed quickly. Grow in shade.",
            "humid": " Watch for downy mildew and bottom rot in humid conditions.",
            "cold": " Cool conditions are perfect for lettuce! Best growing weather."
        },
        "Cucumber": {
            "good": " Good day for cucumber! Check for downy mildew and cucumber beetles.",
            "rain": " Light rain benefits cucumber. Too much causes powdery mildew.",
            "hot": " Cucumber tolerates heat! Ensure adequate water for fruit development.",
            "humid": " High humidity increases downy mildew risk! Apply fungicide.",
            "cold": " Cucumber needs warm conditions. Cold causes wilting."
        },
        "Carrot": {
            "good": " Good day for carrot! Check for carrot fly and alternaria blight.",
            "rain": " Light rain good for carrot. Heavy rain causes forking and cracking.",
            "hot": " Too hot for best carrot quality. Roots become woody in heat.",
            "humid": " Watch for alternaria leaf blight in humid conditions.",
            "cold": " Cool conditions improve carrot sweetness! Good growing weather."
        },
        "Spring Onion": {
            "good": " Good day for spring onion! Fast growing. Check for thrips.",
            "rain": " Light rain good for spring onion. Avoid waterlogging.",
            "hot": " Spring onion tolerates heat. Ensure adequate moisture.",
            "humid": " Watch for downy mildew in humid conditions.",
            "cold": " Cool conditions suit spring onion well."
        },
        "Spinach": {
            "good": " Good day for spinach! Cool weather crop. Check for aphids.",
            "rain": " Moderate rain good for spinach. Ensure good drainage.",
            "hot": " Too hot for spinach! Goes to seed quickly in heat. Provide shade.",
            "humid": " Watch for downy mildew and cercospora in humid conditions.",
            "cold": " Cool conditions are ideal for spinach growth!"
        },
        "Kontomire (Cocoyam leaves)": {
            "good": " Good day for kontomire! Prefers partial shade. Check for leaf blight.",
            "rain": " Rain benefits kontomire! Ensure partial shade and good drainage.",
            "hot": " Provide shade for kontomire in hot conditions. Water regularly.",
            "humid": " Watch for taro leaf blight in humid conditions. Remove affected leaves.",
            "cold": " Kontomire prefers warm humid conditions. Protect from cold."
        },
        "Ginger": {
            "good": "🫚 Good day for ginger! Check for rhizome rot and shoot borer.",
            "rain": "🫚 Rain benefits ginger! Ensure good drainage to prevent rhizome rot.",
            "hot": "🫚 Ginger prefers partial shade in hot weather. Mulch to retain moisture.",
            "humid": "🫚 Watch for pythium rhizome rot in high humidity conditions.",
            "cold": "🫚 Ginger prefers warm humid conditions. Cold stops growth."
        },
        "Turmeric": {
            "good": "🫚 Good day for turmeric! Similar needs to ginger. Check for leaf blotch.",
            "rain": "🫚 Rain is good for turmeric! Ensure drainage to prevent rhizome rot.",
            "hot": "🫚 Turmeric tolerates heat with adequate moisture and partial shade.",
            "humid": "🫚 Watch for leaf blotch and rhizome rot in humid conditions.",
            "cold": "🫚 Turmeric prefers warm humid tropical conditions."
        },
        "Garlic": {
            "good": " Good day for garlic! Check for thrips and white rot.",
            "rain": " Garlic dislikes excess rain! Increases white rot and purple blotch.",
            "hot": " Hot dry conditions help bulb development! Reduce irrigation.",
            "humid": " High humidity greatly increases disease risk in garlic!",
            "cold": " Cool conditions promote garlic leaf growth. Good for early stages."
        },
        "Chilli Pepper": {
            "good": " Great day for chilli! Heat tolerant crop. Check for anthracnose.",
            "rain": " Light rain good for chilli. Heavy rain causes anthracnose on fruits.",
            "hot": " Chilli loves heat! One of Ghana's most heat tolerant crops.",
            "humid": " Watch for phytophthora blight in humid conditions.",
            "cold": " Chilli prefers warm conditions. Cold causes stunting."
        },
        "Cotton": {
            "good": " Good day for cotton! Check for bollworm and jassids.",
            "rain": " Light rain good for cotton. Heavy rain during boll opening causes damage.",
            "hot": " Cotton tolerates heat well! Warm dry conditions help boll development.",
            "humid": " Watch for boll rot and angular leaf spot in humid conditions.",
            "cold": " Cotton needs warm conditions. Cold slows germination and growth."
        }
    }

    if crop not in advice:
        return " Select a crop to get specific farming advice!"

    if is_rainy:
        return advice[crop]["rain"]
    elif is_hot:
        return advice[crop]["hot"]
    elif is_humid:
        return advice[crop]["humid"]
    elif is_cold:
        return advice[crop]["cold"]
    else:
        return advice[crop]["good"]

def get_outfit(temp, condition):
    condition = condition.lower()
    if temp >= 30:
        outfit = " Wear light cotton clothes, shorts and sunglasses!"
    elif temp >= 20:
        outfit = " Wear comfortable clothes like a t-shirt and jeans!"
    elif temp >= 10:
        outfit = " Wear a jacket or sweater!"
    else:
        outfit = " Wear a heavy coat, scarf and gloves!"
    if "rain" in condition:
        outfit += " Don't forget your umbrella!"
    return outfit

def get_farmer_tip(temp, condition, humidity, rain_chance):
    condition = condition.lower()
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
    condition = condition.lower()
    if rain_chance >= 70:
        return " High chance of rain! Stay indoors. Great day for reading, cooking, or indoor exercises!"
    elif rain_chance >= 40:
        return "Rain possible today! Plan indoor activities but keep an eye on the weather!"
    elif temp >= 35:
        return " Too hot for outdoor activities! Try swimming or stay in a cool place!"
    elif temp >= 25:
        return " Perfect day for outdoor sports, picnics, or visiting the park!"
    else:
        return " Nice day for a walk, jogging, or sightseeing!"

def get_health_tip(temp, condition, humidity, rain_chance):
    condition = condition.lower()
    if rain_chance >= 70:
        return " Rainy day ahead! Avoid getting wet to prevent cold and flu. Keep warm and dry!"
    elif temp >= 35:
        return " Extreme heat! Drink at least 3 litres of water. Avoid going out between 12pm-3pm!"
    elif temp >= 30:
        return " Hot day! Stay hydrated with at least 8 glasses of water. Wear sunscreen outside!"
    elif humidity >= 80:
        return " High humidity! People with asthma should be careful. Stay in ventilated areas!"
    else:
        return " Good weather for your health! Great day for outdoor exercise and fresh air!"

def get_rain_alert(rain_chance):
    if rain_chance >= 80:
        return "Heavy rain expected today! Carry an umbrella and avoid flooded areas!"
    elif rain_chance >= 60:
        return " Good chance of rain today! Keep an umbrella handy!"
    elif rain_chance >= 40:
        return "Rain possible today! Keep an eye on the sky!"
    elif rain_chance >= 20:
        return "Small chance of rain! Probably a dry day!"
    else:
        return "Very unlikely to rain today! Enjoy the dry weather!"

def get_disease_risks(temp, humidity, rain_chance):
    if humidity >= 80 and rain_chance >= 60:
        fungal_risk = 90
        fungal_level = "Very High"
        fungal_color = "#e74c3c"
    elif humidity >= 70 or rain_chance >= 40:
        fungal_risk = 60
        fungal_level = "Moderate"
        fungal_color = "#f39c12"
    else:
        fungal_risk = 20
        fungal_level = "Low"
        fungal_color = "#2ed573"

    if temp >= 30 and humidity >= 75:
        bacterial_risk = 85
        bacterial_level = "Very High"
        bacterial_color = "#e74c3c"
    elif temp >= 25 and humidity >= 60:
        bacterial_risk = 55
        bacterial_level = "Moderate"
        bacterial_color = "#f39c12"
    else:
        bacterial_risk = 15
        bacterial_level = "Low"
        bacterial_color = "#2ed573"

    if humidity >= 70 and temp >= 25:
        viral_risk = 75
        viral_level = "High"
        viral_color = "#e74c3c"
    elif humidity >= 55 or temp >= 20:
        viral_risk = 45
        viral_level = "Moderate"
        viral_color = "#f39c12"
    else:
        viral_risk = 10
        viral_level = "Low"
        viral_color = "#2ed573"

    if temp >= 28 and humidity >= 60:
        pest_risk = 88
        pest_level = "Very High"
        pest_color = "#e74c3c"
    elif temp >= 22 or humidity >= 50:
        pest_risk = 55
        pest_level = "Moderate"
        pest_color = "#f39c12"
    else:
        pest_risk = 18
        pest_level = "Low"
        pest_color = "#2ed573"

    if rain_chance >= 70 and humidity >= 75:
        root_risk = 85
        root_level = "Very High"
        root_color = "#e74c3c"
    elif rain_chance >= 50 or humidity >= 65:
        root_risk = 50
        root_level = "Moderate"
        root_color = "#f39c12"
    else:
        root_risk = 12
        root_level = "Low"
        root_color = "#2ed573"

    if humidity >= 85 and rain_chance >= 50:
        blight_risk = 92
        blight_level = "Very High"
        blight_color = "#e74c3c"
    elif humidity >= 70 or rain_chance >= 35:
        blight_risk = 58
        blight_level = "Moderate"
        blight_color = "#f39c12"
    else:
        blight_risk = 15
        blight_level = "Low"
        blight_color = "#2ed573"

    if rain_chance >= 60 and temp >= 25:
        weed_risk = 88
        weed_level = "Very High"
        weed_color = "#e74c3c"
    elif rain_chance >= 40 or temp >= 20:
        weed_risk = 52
        weed_level = "Moderate"
        weed_color = "#f39c12"
    else:
        weed_risk = 20
        weed_level = "Low"
        weed_color = "#2ed573"

    if rain_chance <= 10 and temp >= 35:
        drought_risk = 90
        drought_level = "Very High"
        drought_color = "#e74c3c"
    elif rain_chance <= 20 and temp >= 30:
        drought_risk = 55
        drought_level = "Moderate"
        drought_color = "#f39c12"
    else:
        drought_risk = 10
        drought_level = "Low"
        drought_color = "#2ed573"

    return {
        "fungal": {"risk": fungal_risk, "level": fungal_level, "color": fungal_color, "name": "Fungal Disease", "tip": "Apply fungicide and improve drainage"},
        "bacterial": {"risk": bacterial_risk, "level": bacterial_level, "color": bacterial_color, "name": "Bacterial Disease", "tip": "Use copper based sprays and remove infected plants"},
        "viral": {"risk": viral_risk, "level": viral_level, "color": viral_color, "name": "Viral Disease", "tip": "Control insect vectors and remove infected plants"},
        "pest": {"risk": pest_risk, "level": pest_level, "color": pest_color, "name": "Pest and Insects", "tip": "Apply appropriate pesticide and use traps"},
        "root_rot": {"risk": root_risk, "level": root_level, "color": root_color, "name": "Root Rot", "tip": "Improve drainage and avoid overwatering"},
        "blight": {"risk": blight_risk, "level": blight_level, "color": blight_color, "name": "Leaf Blight", "tip": "Remove affected leaves and apply fungicide"},
        "weed": {"risk": weed_risk, "level": weed_level, "color": weed_color, "name": "Weed Growth", "tip": "Weed regularly and use mulch to suppress weeds"},
        "drought": {"risk": drought_risk, "level": drought_level, "color": drought_color, "name": "Drought Stress", "tip": "Irrigate crops and use mulch to retain moisture"}
    }

@app.route("/", methods=["GET", "POST"])
def weather():
    weather_data = None
    error = None
    selected_crop = request.form.get("crop", "")
    selected_lang = request.form.get("lang", "en")

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

                disease_risks = get_disease_risks(temp, humidity, rain_chance)

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
                    "forecast": forecast_days,
                    "disease_risks": disease_risks,
                    "crop_advice": get_crop_advice(selected_crop, temp, condition, humidity, rain_chance) if selected_crop else None
                }
            else:
                error = "City not found! Please check the city name."
                print("API Error:", current_data)

        except Exception as e:
            error = "Something went wrong! Please try again."
            print("Exception:", e)

    return render_template("weather.html",
                          weather=weather_data,
                          error=error,
                          selected_crop=selected_crop,
                          selected_lang=selected_lang)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9200))
    app.run(host="0.0.0.0", port=port, debug=True)
