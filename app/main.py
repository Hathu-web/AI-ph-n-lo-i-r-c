from fastapi import FastAPI, UploadFile, File
from .database import collection
from .ai_engine import predict_waste # Import hàm AI vừa viết
import datetime
import io

app = FastAPI(title="AI Waste Classifier API")

@app.post("/classify")
async def classify_waste(file: UploadFile = File(...)):
    # 1. Đọc dữ liệu ảnh từ file upload
    image_bytes = await file.read()
    image_io = io.BytesIO(image_bytes)
    
    # 2. Gọi AI để phân loại
    label, confidence = predict_waste(image_io)
    
    # 3. Lưu kết quả vào MongoDB
    data = {
        "filename": file.filename,
        "result": label,
        "confidence": round(confidence * 100, 2), # Lưu dưới dạng %
        "time": datetime.datetime.now()
    }
    collection.insert_one(data)
    print("Saved to MongoDB:", data)
    return {
        "result": label, 
        "confidence": f"{round(confidence * 100, 2)}%", 
        "status": "Success"
    }
@app.get("/history")
def get_history():
    # Lấy 10 kết quả mới nhất từ MongoDB
    history = list(collection.find().sort("time", -1).limit(10))
    for item in history:
        item["_id"] = str(item["_id"]) # Chuyển ID của Mongo sang chuỗi để hiện thị
    return history