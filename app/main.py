from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from app.ai_engine import predict_waste
import datetime
import io
import json


# Import DB
from app.database import collection  

app = FastAPI(title="AI Waste Classifier API")


# ===================== TEST API =====================
@app.post("/test")
def test_api():
    data = {"from": "swagger"}
    collection.insert_one(data)
    return {"msg": "inserted"}


# ===================== CLASSIFY =====================
@app.post("/classify")
async def classify_waste(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image_io = io.BytesIO(image_bytes)

        label, confidence = predict_waste(image_io)

        data = {
            "filename": file.filename,
            "result": label,
            "confidence": round(confidence * 100, 2),
            "time": datetime.datetime.now()
        }

        collection.insert_one(data)

        return {
            "result": label,
            "confidence": f"{round(confidence * 100, 2)}%",
            "status": "Success"
        }

    except Exception as e:
        return {"status": "Error", "message": str(e)}


# ===================== HISTORY =====================
@app.get("/history")
def get_history():
    history = list(collection.find().sort("time", -1).limit(10))

    for item in history:
        item["_id"] = str(item["_id"])

    return history


# ===================== STATS =====================
@app.get("/stats")
async def get_waste_stats():
    try:
        pipeline = [
            {"$group": {"_id": "$result", "count": {"$sum": 1}}}
        ]

        results = list(collection.aggregate(pipeline))
        total = sum(item['count'] for item in results)

        stats_detail = [
            {
                "label": item['_id'],
                "count": item['count'],
                "percentage": f"{(item['count'] / total) * 100:.2f}%" if total > 0 else "0%"
            }
            for item in results
        ]

        return {
            "total_classified": total,
            "statistics": stats_detail,
            "status": "Success"
        }

    except Exception as e:
        return {"status": "Error", "message": str(e)}


# ===================== DASHBOARD =====================
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Waste AI Dashboard</title>

    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body {
            background: #f4f7f6;
            font-family: 'Segoe UI', sans-serif;
        }
        .header {
            background: linear-gradient(135deg, #00c853, #009624);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 0 0 25px 25px;
        }
        .card {
            border: none;
            border-radius: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        }
    </style>
</head>

<body>

<div class="header">
    <h1>♻️ AI Waste Classifier</h1>
    <p>Dashboard phân tích dữ liệu từ MongoDB Atlas</p>
</div>

<div class="container mt-4">

    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card p-4 text-center">
                <h5>Tổng số mẫu</h5>
                <h1 class="text-success">{total}</h1>
            </div>
        </div>

        <div class="col-md-8">
            <div class="card p-4">
                <canvas id="barChart"></canvas>
            </div>
        </div>
    </div>

    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card p-4 text-center">
                <h5>Tỷ lệ rác (%)</h5>
                <canvas id="pieChart"></canvas>
            </div>
        </div>
    </div>

</div>

<script>
    const stats = {stats_json};

    const labels = stats.map(s => s.label);
    const counts = stats.map(s => s.count);

    const colors = [
        '#4CAF50',
        '#2196F3',
        '#FF9800',
        '#E91E63',
        '#9C27B0'
    ];

    // BAR CHART
    new Chart(document.getElementById('barChart'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Số lượng',
                data: counts,
                backgroundColor: colors
            }]
        }
    });

    // PIE CHART
    new Chart(document.getElementById('pieChart'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: colors
            }]
        }
    });
</script>

</body>
</html>
"""


@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    try:
        pipeline = [
            {"$group": {"_id": "$result", "count": {"$sum": 1}}}
        ]

        results = list(collection.aggregate(pipeline))
        total = sum(item['count'] for item in results)

        stats_detail = [
            {"label": item['_id'], "count": item['count']}
            for item in results
        ]

        return DASHBOARD_TEMPLATE.format(
            total=total,
            stats_json=json.dumps(stats_detail)
        )

    except Exception as e:
        return f"<h1>Error: {e}</h1>"