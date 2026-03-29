from pymongo import MongoClient

client = MongoClient("mongodb+srv://nhthu181005nvtroi2023_db_user:phanloairac@cluster0.xdbvgut.mongodb.net/waste_db")

db = client["waste_db"]
collection = db["classification_history"]

try:
    
    print("✅ INSERT OK")
except Exception as e:
    print("❌ ERROR:", e)