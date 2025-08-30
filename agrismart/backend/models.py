import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pickle
import os

class DiseaseDetectionModel:
    def __init__(self):
        self.model = None
        self.diseases = [
            'Healthy', 'Early Blight', 'Late Blight', 'Leaf Spot', 
            'Bacterial Wilt', 'Mosaic Virus', 'Powdery Mildew'
        ]
    
    def train_model(self):
        # Simulated training data (replace with real dataset)
        X = np.random.rand(1000, 100)  # Image features
        y = np.random.randint(0, len(self.diseases), 1000)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        # Save model
        with open('disease_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
    
    def predict_disease(self, image_features):
        if self.model is None:
            self.load_model()
        
        prediction = self.model.predict([image_features])[0]
        confidence = np.max(self.model.predict_proba([image_features]))
        
        return {
            'disease': self.diseases[prediction],
            'confidence': round(confidence * 100, 1)
        }
    
    def load_model(self):
        try:
            with open('disease_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            self.train_model()

class CropPredictionModel:
    def __init__(self):
        self.yield_model = None
        self.suitability_model = None
    
    def train_models(self):
        # Generate synthetic training data
        # Features: pH, moisture, temperature, nitrogen, phosphorus, potassium
        X = np.random.rand(1000, 6)
        X[:, 0] = X[:, 0] * 3 + 5  # pH 5-8
        X[:, 1] = X[:, 1] * 40 + 30  # Moisture 30-70
        X[:, 2] = X[:, 2] * 20 + 15  # Temperature 15-35
        X[:, 3] = X[:, 3] * 300 + 100  # Nitrogen 100-400
        X[:, 4] = X[:, 4] * 100 + 50   # Phosphorus 50-150
        X[:, 5] = X[:, 5] * 200 + 100  # Potassium 100-300
        
        # Yield prediction (tons per hectare)
        y_yield = np.random.rand(1000) * 5 + 1
        
        # Suitability score (0-100)
        y_suitability = np.random.rand(1000) * 100
        
        # Train models
        self.yield_model = GradientBoostingRegressor(random_state=42)
        self.suitability_model = GradientBoostingRegressor(random_state=42)
        
        self.yield_model.fit(X, y_yield)
        self.suitability_model.fit(X, y_suitability)
        
        # Save models
        with open('yield_model.pkl', 'wb') as f:
            pickle.dump(self.yield_model, f)
        with open('suitability_model.pkl', 'wb') as f:
            pickle.dump(self.suitability_model, f)
    
    def predict_crop_performance(self, soil_data, weather_data):
        if self.yield_model is None or self.suitability_model is None:
            self.load_models()
        
        features = np.array([
            soil_data['ph'],
            soil_data['moisture'],
            weather_data['temperature'],
            soil_data['nitrogen'],
            soil_data['phosphorus'],
            soil_data['potassium']
        ]).reshape(1, -1)
        
        yield_prediction = self.yield_model.predict(features)[0]
        suitability_score = self.suitability_model.predict(features)[0]
        
        return {
            'predicted_yield': round(yield_prediction, 2),
            'suitability_score': round(min(100, max(0, suitability_score)), 1)
        }
    
    def load_models(self):
        try:
            with open('yield_model.pkl', 'rb') as f:
                self.yield_model = pickle.load(f)
            with open('suitability_model.pkl', 'rb') as f:
                self.suitability_model = pickle.load(f)
        except FileNotFoundError:
            self.train_models()

class WeatherPredictor:
    def __init__(self):
        self.model = None
    
    def predict_weather(self, location_features, days_ahead=7):
        # Simulate weather prediction
        predictions = []
        base_temp = np.random.randint(20, 35)
        
        for day in range(days_ahead):
            temp = base_temp + np.random.randint(-5, 5)
            humidity = np.random.randint(50, 90)
            rainfall = np.random.randint(0, 30)
            
            predictions.append({
                'day': day + 1,
                'temperature': temp,
                'humidity': humidity,
                'rainfall': rainfall,
                'condition': self._get_weather_condition(temp, humidity, rainfall)
            })
        
        return predictions
    
    def _get_weather_condition(self, temp, humidity, rainfall):
        if rainfall > 10:
            return 'rainy'
        elif humidity > 80:
            return 'cloudy'
        elif temp > 30:
            return 'hot_sunny'
        else:
            return 'pleasant'

# Initialize models
disease_detector = DiseaseDetectionModel()
crop_predictor = CropPredictionModel()
weather_predictor = WeatherPredictor()

def analyze_crop_image(image_path):
    """Analyze crop image for disease detection"""
    # Simulate image processing and feature extraction
    image_features = np.random.rand(100)
    return disease_detector.predict_disease(image_features)

def get_crop_recommendations(soil_data, weather_data, location):
    """Get crop recommendations based on conditions"""
    crops = ['rice', 'wheat', 'cotton', 'sugarcane', 'maize']
    recommendations = []
    
    for crop in crops:
        performance = crop_predictor.predict_crop_performance(soil_data, weather_data)
        
        recommendations.append({
            'crop': crop,
            'suitability_score': performance['suitability_score'],
            'predicted_yield': performance['predicted_yield'],
            'estimated_profit': performance['predicted_yield'] * np.random.randint(2000, 8000),
            'sustainability_score': np.random.randint(70, 95)
        })
    
    return sorted(recommendations, key=lambda x: x['suitability_score'], reverse=True)

if __name__ == "__main__":
    # Train models if running directly
    print("Training disease detection model...")
    disease_detector.train_model()
    
    print("Training crop prediction models...")
    crop_predictor.train_models()
    
    print("Models trained and saved successfully!")