import google.generativeai as genai
from config import Config
import json

class GeminiAgriculturalAI:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.conversation_history = []
    
    def get_agricultural_advice(self, user_message, context=None):
        """Get agricultural advice from Gemini AI"""
        
        # Build comprehensive prompt
        system_prompt = """
        You are AgriSmart AI, an expert agricultural assistant specifically designed for Indian farmers. 

        Your expertise includes:
        - Indian crops: Rice, Wheat, Cotton, Sugarcane, Maize, Pulses, Vegetables
        - Soil management: pH, nutrients, organic matter, drainage
        - Pest and disease management: IPM, organic solutions, chemical treatments
        - Weather-based farming: Monsoon patterns, seasonal crops, climate adaptation
        - Market intelligence: MSP, local mandi prices, crop economics
        - Government schemes: PM-KISAN, crop insurance, subsidies
        - Sustainable practices: Organic farming, water conservation, soil health

        Guidelines:
        - Provide practical, actionable advice
        - Consider Indian farming conditions and monsoon patterns
        - Suggest cost-effective solutions for small farmers
        - Include scientific reasoning but keep language simple
        - Mention relevant government schemes when applicable
        - Consider regional variations across India
        - Prioritize sustainable and eco-friendly practices
        
        Response format:
        - Keep responses under 200 words
        - Use bullet points for multiple recommendations
        - Include specific numbers/quantities when relevant
        - End with a practical next step
        """
        
        # Add context if available
        context_info = ""
        if context:
            if 'location' in context:
                context_info += f"Farmer location: {context['location']}\n"
            if 'soil_data' in context:
                context_info += f"Soil conditions: pH {context['soil_data'].get('ph')}, Moisture {context['soil_data'].get('moisture')}%\n"
            if 'weather' in context:
                context_info += f"Weather: {context['weather']}\n"
            if 'farm_size' in context:
                context_info += f"Farm size: {context['farm_size']} acres\n"
        
        full_prompt = f"{system_prompt}\n\n{context_info}\nFarmer question: {user_message}\n\nPlease provide helpful agricultural advice:"
        
        try:
            response = self.model.generate_content(full_prompt)
            return {
                'success': True,
                'response': response.text,
                'source': 'gemini_ai'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': self._get_fallback_response(user_message)
            }
    
    def analyze_crop_image(self, image_data, user_question="What disease or problem do you see in this crop?"):
        """Analyze crop images using Gemini Vision"""
        try:
            # Note: This requires gemini-pro-vision model
            vision_model = genai.GenerativeModel('gemini-pro-vision')
            
            prompt = """
            You are an expert plant pathologist and agricultural specialist. 
            Analyze this crop image and provide:
            
            1. Crop identification (if possible)
            2. Health assessment (healthy/diseased/stressed)
            3. Specific disease/pest identification (if any)
            4. Severity level (mild/moderate/severe)
            5. Treatment recommendations
            6. Prevention measures
            7. Expected recovery time
            
            Be specific about:
            - Fungicides/pesticides to use
            - Application rates and timing
            - Cultural practices to follow
            - When to consult local agricultural officer
            
            If you cannot identify the issue clearly, suggest what additional information would help.
            """
            
            response = vision_model.generate_content([prompt, image_data])
            return {
                'success': True,
                'response': response.text,
                'source': 'gemini_vision'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': self._get_image_fallback()
            }
    
    def get_multilingual_response(self, message, language_code):
        """Get response in specified language"""
        language_map = {
            'hi': 'Hindi (हिंदी)',
            'ta': 'Tamil (தமிழ்)',
            'te': 'Telugu (తెలుగు)',
            'bn': 'Bengali (বাংলা)',
            'gu': 'Gujarati (ગુજરાતી)',
            'mr': 'Marathi (मराठी)',
            'kn': 'Kannada (ಕನ್ನಡ)',
            'en': 'English'
        }
        
        if language_code == 'en':
            return self.get_agricultural_advice(message)
        
        language_name = language_map.get(language_code, 'English')
        
        prompt = f"""
        You are AgriSmart AI, an agricultural expert for Indian farmers.
        
        Please respond to this farming question in {language_name}:
        "{message}"
        
        Provide practical agricultural advice in {language_name}. 
        Keep the response under 150 words and focus on actionable solutions.
        Include relevant farming practices suitable for Indian conditions.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'response': response.text,
                'language': language_name,
                'source': 'gemini_multilingual'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': self._get_fallback_response(message, language_code)
            }
    
    def get_crop_recommendations(self, soil_data, weather_data, location, farm_size):
        """Get AI-powered crop recommendations"""
        
        prompt = f"""
        As an agricultural AI expert, recommend the best crops for these conditions:
        
        Location: {location}
        Farm Size: {farm_size} acres
        Soil pH: {soil_data.get('ph')}
        Soil Moisture: {soil_data.get('moisture')}%
        Temperature: {weather_data.get('temperature')}°C
        Humidity: {weather_data.get('humidity')}%
        
        Provide top 3 crop recommendations with:
        1. Crop name and variety
        2. Suitability score (out of 100)
        3. Expected yield per acre
        4. Estimated profit margin
        5. Key growing tips
        6. Market demand outlook
        7. Sustainability benefits
        
        Consider current season, local market conditions, and sustainable farming practices.
        Format as JSON for easy parsing.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'response': response.text,
                'source': 'gemini_recommendations'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': self._get_fallback_crops()
            }
    
    def _get_fallback_response(self, message, language='en'):
        """Fallback response when AI is unavailable"""
        fallbacks = {
            'en': "I'm here to help with your agricultural questions. Please try again or contact your local agricultural extension officer for immediate assistance.",
            'hi': "मैं आपकी कृषि संबंधी मदद के लिए यहाँ हूँ। कृपया दोबारा कोशिश करें या तत्काल सहायता के लिए स्थानीय कृषि अधिकारी से संपर्क करें।"
        }
        return fallbacks.get(language, fallbacks['en'])
    
    def _get_image_fallback(self):
        """Fallback for image analysis"""
        return {
            'disease': 'Unable to analyze image',
            'confidence': 0,
            'treatment': 'Please consult local agricultural expert or upload a clearer image',
            'prevention': 'Maintain good crop hygiene and monitor regularly'
        }
    
    def _get_fallback_crops(self):
        """Fallback crop recommendations"""
        return [
            {
                'crop': 'Rice',
                'suitability_score': 80,
                'estimated_yield': '4.5 tons/acre',
                'estimated_profit': '₹85,000',
                'notes': 'Good for high moisture soils'
            },
            {
                'crop': 'Cotton',
                'suitability_score': 75,
                'estimated_yield': '15 quintals/acre',
                'estimated_profit': '₹75,000',
                'notes': 'Suitable for well-drained soils'
            }
        ]

# Initialize global instance
gemini_ai = GeminiAgriculturalAI()