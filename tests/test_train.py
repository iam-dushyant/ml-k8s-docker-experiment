from pathlib import Path
import json

from src.train import train_model, MODEL_PATH, META_PATH

def test_train_model_and_metadata():
    train_model()
    # Check if the model file exists
    assert MODEL_PATH.exists(), f"Model file {MODEL_PATH} does not exist."

    # Check if the metadata file exists
    assert META_PATH.exists(), f"Metadata file {META_PATH} does not exist."

    # Load the metadata and check its contents
    metadata = json.loads(META_PATH.read_text())
    assert "model_name" in metadata, "Metadata missing 'model_name'."
    assert "version" in metadata, "Metadata missing 'version'."
    assert "framework" in metadata, "Metadata missing 'framework'."
    assert "test_accuracy" in metadata, "Metadata missing 'test_accuracy'."