import os
import hashlib
import json

from pathlib import Path
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

MODEL_VERSION = os.getenv("MODEL_VERSION", "v2")
MODEL_DIR = Path("model") / MODEL_VERSION
MODEL_PATH = MODEL_DIR / "iris_rf.joblib"
META_PATH = MODEL_DIR / "metadata.json"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
accuracy = accuracy_score(y_test, model.predict(X_test))
joblib.dump(model, MODEL_PATH)

sha256 = hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()
metadata = {
    "model_name": "iris_random_forest",
    "version": MODEL_VERSION,
    "framework": "scikit-learn",
    "framework_version": "1.3.2",
    "model_path": str(MODEL_PATH),
    "sha256": sha256,
    "test_accuracy": round(float(accuracy), 4)
}

META_PATH.write_text(json.dumps(metadata, indent=2))
print(f"Model trained and saved to {MODEL_PATH}. Accuracy on test set: {accuracy:.4f}")
