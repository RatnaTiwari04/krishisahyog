from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import json
from datetime import datetime, timedelta
import random
import os
import google.generativeai as genai
from config import Config

app = Flask(__name__)
CORS(app)

# Configure Gemini AI
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  

# Agricultural context for better AI responses
AGRICULTURE_CONTEXT = """
You are an expert agricultural AI assistant helping farmers in India. You have deep knowledge about:
- Indian crops (rice, wheat, cotton, sugarcane, pulses, etc.)
- Soil management and fertilizers
- Pest and disease control
- Weather patterns and seasonal farming
- Market prices and crop profitability
- Sustainable farming practices
- Government schemes for farmers

Always provide practical, actionable advice. Keep responses concise but informative.
Consider Indian farming conditions, monsoons, and local agricultural practices.
"""

# Simulated ML Models and Data
class AgriPredictor:
    def __init__(self):
        self.crop_database = {
            'rice': {'ph_range': [5.5, 7.0], 'moisture_range': [40, 60], 'temp_range': [20, 35]},
            'wheat': {'ph_range': [6.0, 7.5], 'moisture_range': [30, 50], 'temp_range': [15, 25]},
            'cotton': {'ph_range': [5.8, 8.0], 'moisture_range': [35, 55], 'temp_range': [21, 32]},
            'sugarcane': {'ph_range': [6.0, 7.5], 'moisture_range': [45, 65], 'temp_range': [26, 32]}
        }
        
        self.market_prices = {
            'rice': {'current': 2500, 'trend': 'up', 'change': 5.2},
            'wheat': {'current': 2200, 'trend': 'stable', 'change': 1.1},
            'cotton': {'current': 7800, 'trend': 'up', 'change': 8.7},
            'sugarcane': {'current': 350, 'trend': 'down', 'change': -2.3}
        }

    def get_soil_data(self, location):
        # Simulate soil data from satellite APIs
        return {
            'ph': round(random.uniform(5.5, 8.0), 1),
            'moisture': round(random.uniform(30, 70), 1),
            'nitrogen': round(random.uniform(200, 400), 1),
            'phosphorus': round(random.uniform(50, 150), 1),
            'potassium': round(random.uniform(100, 300), 1),
            'organic_matter': round(random.uniform(1.5, 4.0), 2)
        }

    def predict_crops(self, location, soil_type, farm_size):
        soil_data = self.get_soil_data(location)
        suitable_crops = []
        
        for crop, requirements in self.crop_database.items():
            ph_score = 1 if requirements['ph_range'][0] <= soil_data['ph'] <= requirements['ph_range'][1] else 0.5
            moisture_score = 1 if requirements['moisture_range'][0] <= soil_data['moisture'] <= requirements['moisture_range'][1] else 0.5
            
            suitability_score = (ph_score + moisture_score) / 2
            
            if suitability_score > 0.5:
                yield_estimate = self.estimate_yield(crop, farm_size, suitability_score)
                profit_estimate = self.estimate_profit(crop, yield_estimate)
                
                suitable_crops.append({
                    'crop': crop,
                    'suitability_score': round(suitability_score * 100, 1),
                    'estimated_yield': yield_estimate,
                    'estimated_profit': profit_estimate,
                    'sustainability_score': round(random.uniform(75, 95), 1),
                    'market_trend': self.market_prices[crop]['trend']
                })
        
        return sorted(suitable_crops, key=lambda x: x['suitability_score'], reverse=True)

    def estimate_yield(self, crop, farm_size, suitability_score):
        base_yields = {'rice': 4.5, 'wheat': 3.2, 'cotton': 1.5, 'sugarcane': 65}
        return round(base_yields.get(crop, 2.0) * farm_size * suitability_score, 2)

    def estimate_profit(self, crop, yield_amount):
        return round(yield_amount * self.market_prices[crop]['current'], 0)

# Initialize predictor
predictor = AgriPredictor()

@app.route('/api/analyze_farm', methods=['POST'])
def analyze_farm():
    data = request.json
    location = data.get('location')
    soil_type = data.get('soil_type')
    farm_size = float(data.get('farm_size', 1))
    
    # Get soil analysis
    soil_data = predictor.get_soil_data(location)
    
    # Get crop recommendations
    crop_recommendations = predictor.predict_crops(location, soil_type, farm_size)
    
    # Get weather forecast
    weather_data = get_weather_forecast(location)
    
    return jsonify({
        'status': 'success',
        'soil_analysis': soil_data,
        'crop_recommendations': crop_recommendations,
        'weather_forecast': weather_data,
        'analysis_timestamp': datetime.now().isoformat()
    })

@app.route('/api/detect_disease', methods=['POST'])
def detect_disease():
    # Simulate ML disease detection
    diseases = [
        {
            'disease': 'Early Blight',
            'confidence': 87.5,
            'treatment': 'Apply copper-based fungicide, ensure proper ventilation',
            'prevention': 'Crop rotation, avoid overhead watering'
        },
        {
            'disease': 'Late Blight',
            'confidence': 92.3,
            'treatment': 'Remove affected leaves, apply metalaxyl fungicide',
            'prevention': 'Improve air circulation, avoid wet foliage'
        },
        {
            'disease': 'Leaf Spot',
            'confidence': 78.9,
            'treatment': 'Prune affected areas, apply neem oil',
            'prevention': 'Proper spacing, morning watering'
        }
    ]
    
    detected_disease = random.choice(diseases)
    
    return jsonify({
        'status': 'success',
        'detection_result': detected_disease,
        'additional_info': {
            'severity': random.choice(['Low', 'Medium', 'High']),
            'spread_risk': random.choice(['Low', 'Medium', 'High']),
            'economic_impact': f"₹{random.randint(5000, 25000)} potential loss if untreated"
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat_response():
    data = request.json
    user_message = data.get('message', '')
    language = data.get('language', 'en')
    location = data.get('location', 'India')
    
    try:
        # Create a comprehensive prompt for any question
        prompt = f"""
        You are AgriSmart AI, an intelligent assistant with expertise in agriculture, but you can help with any question.

        Primary Focus: Agriculture, farming, crops, livestock, rural development
        Secondary: General knowledge, technology, science, business, weather, etc.
        
        User Context:
        - Location: {location}
        - Language preference: {language}
        
        User Question: {user_message}
        
        Instructions:
        - If it's agriculture-related: Provide expert farming advice with Indian context
        - If it's general knowledge: Provide accurate, helpful information
        - If language is not English: Respond in the requested language ({language})
        - Keep responses conversational and helpful
        - Be practical and actionable
        - Limit response to 200 words for better readability
        
        Respond naturally and helpfully to: {user_message}
        """
        
        # Generate response using Gemini
        response = model.generate_content(prompt)
        ai_response = response.text.strip()
        
        # Fallback if response is empty
        if not ai_response:
            ai_response = get_emergency_fallback(user_message, language)
            
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        ai_response = get_emergency_fallback(user_message, language)
    
    return jsonify({
        'status': 'success',
        'response': ai_response,
        'timestamp': datetime.now().isoformat(),
        'source': 'gemini_ai',
        'language': language
    })

def get_emergency_fallback(user_message, language):
    """Emergency fallback when Gemini API completely fails"""
    if language == 'hi':
        return "मैं आपकी सहायता करने के लिए यहाँ हूँ। कृपया दोबारा प्रयास करें या अपना प्रश्न दूसरे तरीके से पूछें।"
    elif language == 'ta':
        return "நான் உங்களுக்கு உதவ இங்கே இருக்கிறேன். தயவுசெய்து மீண்டும் முயற்சிக்கவும் அல்லது உங்கள் கேள்வியை வேறு வழியில் கேளுங்கள்."
    else:
        return "I'm here to help you with any question! Please try asking again or rephrase your question. I can help with farming, general knowledge, or anything else you'd like to know."
    """Fallback responses when Gemini API is unavailable"""
    user_msg_lower = user_message.lower()
    
    # English responses
    fallback_responses = {
        'weather': "Based on current weather patterns, I recommend checking soil moisture levels and adjusting irrigation schedule accordingly. Monitor local weather forecasts for the next 7 days.",
        'fertilizer': "For optimal growth, consider using balanced NPK fertilizer. Current soil analysis suggests checking nitrogen levels. Apply based on soil test results.",
        'irrigation': "Your crops need watering based on soil moisture. Check moisture at 6-inch depth. Water early morning or evening to reduce evaporation.",
        'disease': "Upload an image of affected crops for accurate disease identification. Common signs include leaf spots, wilting, or discoloration.",
        'market': "Current market trends show price fluctuations. Consider timing your harvest based on local mandi prices. Check government MSP rates.",
        'rice': "Rice cultivation requires proper water management. Maintain 2-3 inches of standing water during vegetative growth. Apply urea in split doses.",
        'cotton': "Cotton needs well-drained soil and careful pest monitoring. Watch for bollworm attacks. Use IPM practices for sustainable cultivation.",
        'default': "I'm here to help with your agricultural needs. Ask about crops, weather, diseases, fertilizers, or market prices for your location."
    }
    
    # Hindi responses
    hindi_responses = {
        'weather': "मौसम के आधार पर मिट्टी की नमी जांचें और सिंचाई का समय निर्धारित करें। अगले 7 दिनों का मौसम पूर्वानुमान देखें।",
        'fertilizer': "अच्छी फसल के लिए संतुलित NPK उर्वरक का प्रयोग करें। मिट्टी परीक्षण के आधार पर नाइट्रोजन की मात्रा तय करें।",
        'irrigation': "मिट्टी की नमी के आधार पर सिंचाई करें। 6 इंच गहराई में नमी जांचें। सुबह या शाम को पानी दें।",
        'disease': "सटीक बीमारी पहचान के लिए पौधे की तस्वीर अपलोड करें। पत्तियों पर धब्बे या मुरझाना आम लक्षण हैं।",
        'market': "बाजार की कीमतों में उतार-चढ़ाव हो रहा है। स्थानीय मंडी भाव देखकर फसल बेचने का समय तय करें।",
        'default': "मैं आपकी खेती संबंधी मदद के लिए यहाँ हूँ। फसल, मौसम, बीमारी, या बाजार भाव के बारे में पूछें।"
    }
    
    # Determine response based on keywords
    response_text = fallback_responses.get('default')
    if language == 'hi':
        response_text = hindi_responses.get('default')
        for keyword in hindi_responses:
            if keyword in user_msg_lower or keyword in user_message:
                response_text = hindi_responses[keyword]
                break
    else:
        for keyword in fallback_responses:
            if keyword in user_msg_lower:
                response_text = fallback_responses[keyword]
                break
    
    return response_text

@app.route('/api/market_data', methods=['GET'])
def get_market_data():
    return jsonify({
        'status': 'success',
        'market_prices': predictor.market_prices,
        'last_updated': datetime.now().isoformat()
    })

@app.route('/api/weather/<location>', methods=['GET'])
def get_weather_by_location(location):
    weather_data = get_weather_forecast(location)
    return jsonify({
        'status': 'success',
        'location': location,
        'weather_data': weather_data
    })

def get_weather_forecast(location):
    # Simulate weather API data
    forecasts = []
    base_temp = random.randint(25, 35)
    
    for i in range(7):
        date = datetime.now() + timedelta(days=i)
        temp = base_temp + random.randint(-5, 5)
        
        forecasts.append({
            'date': date.strftime('%Y-%m-%d'),
            'temperature': temp,
            'humidity': random.randint(60, 90),
            'rainfall': random.randint(0, 20),
            'condition': random.choice(['sunny', 'cloudy', 'rainy', 'partly_cloudy'])
        })
    
    return forecasts

@app.route('/api/sensor_data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    # Store sensor data (in production, use database)
    sensor_data = {
        'device_id': data.get('device_id'),
        'temperature': data.get('temperature'),
        'humidity': data.get('humidity'),
        'soil_moisture': data.get('soil_moisture'),
        'ph': data.get('ph'),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify({
        'status': 'success',
        'message': 'Sensor data received',
        'data_stored': sensor_data
    })

@app.route('/api/recommendations/<crop>', methods=['GET'])
def get_crop_recommendations(crop):
    recommendations = {
        'rice': {
            'planting_season': 'June-July',
            'harvesting_season': 'November-December',
            'water_requirements': 'High (1200-1500mm)',
            'fertilizer_schedule': [
                {'stage': 'Transplanting', 'fertilizer': 'NPK 10-26-26', 'quantity': '2 bags/acre'},
                {'stage': 'Tillering', 'fertilizer': 'Urea', 'quantity': '1 bag/acre'},
                {'stage': 'Panicle initiation', 'fertilizer': 'DAP', 'quantity': '0.5 bag/acre'}
            ],
            'pest_management': 'Monitor for stem borer, use pheromone traps'
        },
        'cotton': {
            'planting_season': 'April-June',
            'harvesting_season': 'October-February',
            'water_requirements': 'Medium (800-1200mm)',
            'fertilizer_schedule': [
                {'stage': 'Sowing', 'fertilizer': 'NPK 12-32-16', 'quantity': '2 bags/acre'},
                {'stage': 'Squaring', 'fertilizer': 'Urea', 'quantity': '1.5 bags/acre'},
                {'stage': 'Flowering', 'fertilizer': 'Potash', 'quantity': '0.5 bag/acre'}
            ],
            'pest_management': 'Regular monitoring for bollworm, use IPM practices'
        }
    }
    
    return jsonify({
        'status': 'success',
        'crop': crop,
        'recommendations': recommendations.get(crop, {})
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)