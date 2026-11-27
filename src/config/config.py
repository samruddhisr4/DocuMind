"""Global configuration for DocuMind"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "data"
MODELS_ROOT = PROJECT_ROOT / "models"
CHECKPOINTS_ROOT = MODELS_ROOT / "checkpoints"
LOGS_ROOT = PROJECT_ROOT / "logs"

# Dataset paths
SROIE_DATA = DATA_ROOT / "invoices" / "sroie"
SROIE_IMAGES = SROIE_DATA / "images"
SROIE_ANNOTATIONS = SROIE_DATA / "annotations"
SROIE_TEXTS = SROIE_DATA / "texts"

CUAD_DATA = DATA_ROOT / "cuad"
TRAIN_DATA = DATA_ROOT / "train"

# Ensure paths exist
for path in [CHECKPOINTS_ROOT, LOGS_ROOT]:
    path.mkdir(parents=True, exist_ok=True)

# Model configuration
class ModelConfig:
    """Model hyperparameters"""
    NUM_EPOCHS = 50
    BATCH_SIZE = 32
    LEARNING_RATE = 1e-4
    WEIGHT_DECAY = 1e-5
    DEVICE = "cuda"  # or "cpu"

# Data configuration
class DataConfig:
    """Data loading parameters"""
    TRAIN_SPLIT = 0.8
    VAL_SPLIT = 0.1
    TEST_SPLIT = 0.1
    NUM_WORKERS = 4
    SHUFFLE = True
    IMG_SIZE = (512, 512)  # Resize images to this size

# Project info
PROJECT_NAME = "DocuMind"
VERSION = "0.1.0"

# Logging
LOG_LEVEL = "INFO"
