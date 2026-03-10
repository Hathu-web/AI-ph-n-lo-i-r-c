import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import os
import warnings

# ==============================
# TẮT WARNING KHÔNG CẦN THIẾT
# ==============================
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

# ==============================
# FIX LỖI KERAS 3 (groups)
# ==============================
class PatchedDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
    def __init__(self, **kwargs):
        kwargs.pop("groups", None)
        super().__init__(**kwargs)


# ==============================
# PATH MODEL
# ==============================
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "models", "keras_model.h5")

# Phải đúng thứ tự labels.txt của Teachable Machine
LABELS = ["Plastic", "Papper", "Metal", "Other"]

# ==============================
# LOAD MODEL GLOBAL
# ==============================
GLOBAL_MODEL = None

try:
    GLOBAL_MODEL = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False,
        custom_objects={"DepthwiseConv2D": PatchedDepthwiseConv2D}
    )

    print(">>> [AI ENGINE] Model đã nạp thành công!")
    print(">>> Input shape:", GLOBAL_MODEL.input_shape)

except Exception as e:
    print(">>> [AI ENGINE ERROR] Không thể load model:", e)
    GLOBAL_MODEL = None


# ==============================
# HÀM PREDICT
# ==============================
def predict_waste(image_data):

    if GLOBAL_MODEL is None:
        print(">>> Model chưa được load")
        return "Unknown", 0.0

    try:
        # ==============================
        # LOAD ẢNH
        # ==============================
        image = Image.open(image_data).convert("RGB")

        # Resize đúng chuẩn Teachable Machine
        image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)

        image_array = np.asarray(image)

        # Normalize [-1,1]
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Shape đúng cho model
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        # ==============================
        # PREDICT
        # ==============================
        prediction = GLOBAL_MODEL.predict(data, verbose=0)

        index = int(np.argmax(prediction))
        confidence = float(prediction[0][index])

        # ==============================
        # KIỂM TRA LABEL
        # ==============================
        if index >= len(LABELS):
            print(">>> Index vượt quá LABELS:", index)
            return "Unknown", confidence

        label = LABELS[index]

        print(f">>> Prediction: {label} ({confidence:.2f})")

        return label, confidence

    except Exception as e:
        print(f">>> [AI ENGINE ERROR] Lỗi khi dự đoán: {e}")
        return "Unknown", 0.0