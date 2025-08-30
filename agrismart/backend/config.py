import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys (add your actual API keys here)
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'demo_key')
    SATELLITE_API_KEY = os.getenv('SATELLITE_API_KEY', 'demo_key')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBvkWEZmriAs-20hWZ6z3iRj9cLUag0MdM')
    
    # External APIs
    WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather?units=metric&q="
    SOIL_GRIDS_URL = "https://rest.soilgrids.org/soilgrids/v2.0/properties/query"
    BHUVAN_API_URL = "https://bhuvan-app1.nrsc.gov.in/api"
    
    # Database Configuration (if using database)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///agrismart.db')
    
    # ML Model Paths
    MODEL_PATH = 'models/'
    DISEASE_MODEL = os.path.join(MODEL_PATH, 'disease_detection.pkl')
    CROP_MODEL = os.path.join(MODEL_PATH, 'crop_prediction.pkl')
    
    # File Upload Settings
    UPLOAD_FOLDER = 'uploads/'
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'हिंदी',
        'ta': 'தமிழ்',
        'te': 'తెలుగు',
        'bn': 'বাংলা',
        'gu': 'ગુજરાતી',
        'mr': 'मराठी',
        'kn': 'ಕನ್ನಡ'
    }
    
    # Crop Database
    CROP_INFO = {
        'rice': {
            'scientific_name': 'Oryza sativa',
            'optimal_ph': [5.5, 7.0],
            'water_requirement': 'High',
            'growing_season': 'Kharif',
            'maturity_period': '110-140 days'
        },
        'wheat': {
            'scientific_name': 'Triticum aestivum',
            'optimal_ph': [6.0, 7.5],
            'water_requirement': 'Medium',
            'growing_season': 'Rabi',
            'maturity_period': '110-130 days'
        },
        'cotton': {
            'scientific_name': 'Gossypium hirsutum',
            'optimal_ph': [5.8, 8.0],
            'water_requirement': 'Medium-High',
            'growing_season': 'Kharif',
            'maturity_period': '150-180 days'
        },
        'sugarcane': {
            'scientific_name': 'Saccharum officinarum',
            'optimal_ph': [6.0, 7.5],
            'water_requirement': 'High',
            'growing_season': 'Year-round',
            'maturity_period': '10-12 months'
        }
    }
    
    # Market Data Sources
    MARKET_APIS = {
        'agmarknet': 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070',
        'commodity': 'https://api.commodityapi.com/v1',
        'manual_prices': {
            'rice': 2500,
            'wheat': 2200,
            'cotton': 7800,
            'sugarcane': 350
        }
    }

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}