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
@app.get("/stats")
async def get_waste_stats():
    """API Dashboard: Thống kê số lượng rác thải đã phân loại"""
    try:
        # 1. Sử dụng Aggregation để nhóm theo nhãn 'result' và đếm số lượng
        pipeline = [
            {"$group": {"_id": "$result", "count": {"$sum": 1}}}
        ]
        results = list(collection.aggregate(pipeline))
        
        # 2. Tính tổng số lượng tất cả các mẫu rác
        total = sum(item['count'] for item in results)
        
        # 3. Định dạng lại dữ liệu trả về cho Dashboard
        stats_detail = [
            {
                "label": item['_id'], 
                "count": item['count'],
                "percentage": f"{(item['count'] / total) * 100:.2f}%" if total > 0 else "0%"
            } for item in results
        ]
        
        return {
            "total_classified": total,
            "statistics": stats_detail,
            "status": "Success"
        }
    except Exception as e:
        print(f"Lỗi thống kê: {e}")
        return {"status": "Error", "message": str(e)}