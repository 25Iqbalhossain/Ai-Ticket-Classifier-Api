from app.core.config import settings
from app.services.ml_model import train_and_save

if __name__ == "__main__":
    train_and_save(settings.MODEL_PATH)
    print("Model trained and saved:", settings.MODEL_PATH)
