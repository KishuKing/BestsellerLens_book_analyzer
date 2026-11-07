from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from scraper import get_book_data_from_url

# Initialize the app and load the model once at startup
app = FastAPI(title="Book Popularity Predictor")
model = joblib.load('book_popularity_model.joblib')

# Define what the incoming request should look like
class URLInput(BaseModel):
    amazon_url: str

@app.post("/predict")
def predict_popularity(data: URLInput):
    # 1. Get the data from the URL
    book_features = get_book_data_from_url(data.amazon_url)
    
    # 2. Make the prediction
    prediction = model.predict(book_features)[0]
    probability = model.predict_proba(book_features)[0].max()
    
    # 3. Format the response
    result = "Top 50 Bestseller 🔥" if prediction == 1 else "Outside Top 50 📉"
    
    return {
        "book_title": book_features['book title'][0],
        "predicted_status": result,
        "confidence_score": f"{probability * 100:.2f}%",
        "extracted_features": {
            "price": book_features['book price'][0],
            "rating": book_features['rating'][0],
            "author": book_features['author'][0],
            "genre": book_features['genre'][0]
        }
    }