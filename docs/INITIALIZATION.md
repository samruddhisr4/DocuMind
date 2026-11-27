# DocuMind - Project Initialization Guide

**Status**: 🚀 Setup Phase  
**Last Updated**: 2026-11-27  
**Target**: Complete project initialization and first working model

---

## 📋 Initialization Checklist

### Phase 1: Environment & Dependencies ⏱️ 30 mins
- [ ] Create Python environment
- [ ] Install core dependencies
- [ ] Verify setup

### Phase 2: Project Structure ⏱️ 15 mins
- [ ] Create source directories
- [ ] Create notebook directories
- [ ] Create model directories

### Phase 3: Data Pipeline ⏱️ 45 mins
- [ ] Create data loader classes
- [ ] Implement data preprocessing
- [ ] Test data loading

### Phase 4: Baseline Model ⏱️ 2 hours
- [ ] Setup training framework
- [ ] Create baseline model architecture
- [ ] Implement training loop

### Phase 5: Testing & Validation ⏱️ 1 hour
- [ ] Create evaluation metrics
- [ ] Test on sample data
- [ ] Generate initial results

---

## Phase 1: Environment & Dependencies Setup

### Step 1.1: Create Python Environment

**Using venv (Recommended for simplicity)**:
```bash
cd /Users/sam/Downloads/DocuMind/DocuMind
python3 -m venv venv
source venv/bin/activate
```

**Using conda (If preferred)**:
```bash
conda create -n documind python=3.10 -y
conda activate documind
```

### Step 1.2: Create requirements.txt

Create file: `requirements.txt`

```
# Core dependencies
numpy==1.24.3
pandas==2.0.3
scipy==1.11.0

# Deep Learning
torch==2.0.1
torchvision==0.15.2
torchtext==0.15.2

# Computer Vision & OCR
opencv-python==4.8.0.74
Pillow==10.0.0
pytesseract==0.3.10

# Data processing
scikit-learn==1.3.0
matplotlib==3.7.2
seaborn==0.12.2

# Utilities
tqdm==4.65.0
pyyaml==6.0
python-dotenv==1.0.0

# Development
jupyter==1.0.0
ipython==8.14.0
pytest==7.4.0
black==23.7.0
```

### Step 1.3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 1.4: Verify Installation

```bash
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"
python -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
```

✅ **Phase 1 Complete** - If all versions print without errors

---

## Phase 2: Project Structure Setup

### Step 2.1: Create Source Code Directory

```bash
mkdir -p src/{models,data,utils,config}
mkdir -p notebooks/{exploratory,experiments}
mkdir -p models/{checkpoints,weights}
mkdir -p tests/{unit,integration}
mkdir -p docs/{api,guides,results}
```

### Step 2.2: Create Directory Structure

**Create**: `src/__init__.py`
```python
"""DocuMind - Document Understanding & Information Extraction"""

__version__ = "0.1.0"
__author__ = "Sanyam Jain"
```

**Create**: `src/config/__init__.py`
```python
"""Configuration management"""
```

**Create**: `src/models/__init__.py`
```python
"""Model architectures and components"""
```

**Create**: `src/data/__init__.py`
```python
"""Data loading and preprocessing"""
```

**Create**: `src/utils/__init__.py`
```python
"""Utility functions"""
```

### Step 2.3: Create Main Configuration File

**Create**: `src/config/config.py`
```python
"""Global configuration for DocuMind"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "data"
MODELS_ROOT = PROJECT_ROOT / "models"
CHECKPOINTS_ROOT = MODELS_ROOT / "checkpoints"

# Dataset paths
SROIE_DATA = DATA_ROOT / "invoices" / "sroie"
SROIE_IMAGES = SROIE_DATA / "images"
SROIE_ANNOTATIONS = SROIE_DATA / "annotations"
SROIE_TEXTS = SROIE_DATA / "texts"

CUAD_DATA = DATA_ROOT / "cuad"
TRAIN_DATA = DATA_ROOT / "train"

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
```

### Step 2.4: Verify Structure

```bash
tree src/ -L 2
tree notebooks/
tree models/
```

✅ **Phase 2 Complete** - Directory structure created

---

## Phase 3: Data Pipeline Setup

### Step 3.1: Create Dataset Loader

**Create**: `src/data/dataset.py`
```python
"""Dataset loaders for different document types"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import cv2
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image

class SROIEDataset(Dataset):
    """SROIE Invoice Dataset - 626 invoices with annotations"""
    
    def __init__(self, 
                 images_dir: Path,
                 annotations_dir: Path,
                 texts_dir: Path,
                 transform=None,
                 max_samples: int = None):
        """
        Args:
            images_dir: Path to images folder
            annotations_dir: Path to annotations (CSV) folder
            texts_dir: Path to text data (JSON) folder
            transform: Image transformations
            max_samples: Limit dataset size (for testing)
        """
        self.images_dir = Path(images_dir)
        self.annotations_dir = Path(annotations_dir)
        self.texts_dir = Path(texts_dir)
        self.transform = transform or transforms.ToTensor()
        
        # Get all invoice IDs
        self.invoice_ids = sorted([
            f.replace('.jpg', '') 
            for f in os.listdir(self.images_dir)
            if f.endswith('.jpg')
        ])
        
        if max_samples:
            self.invoice_ids = self.invoice_ids[:max_samples]
    
    def __len__(self):
        return len(self.invoice_ids)
    
    def __getitem__(self, idx: int) -> Dict:
        """Load single invoice with all associated data"""
        invoice_id = self.invoice_ids[idx]
        
        # Load image
        img_path = self.images_dir / f"{invoice_id}.jpg"
        image = Image.open(img_path).convert('RGB')
        
        # Load annotations (bounding boxes)
        anno_path = self.annotations_dir / f"{invoice_id}.csv"
        boxes = self._load_annotations(anno_path)
        
        # Load text data (extracted information)
        text_path = self.texts_dir / f"{invoice_id}.json"
        with open(text_path, 'r') as f:
            text_data = json.load(f)
        
        # Apply transformations
        if self.transform:
            image = self.transform(image)
        
        return {
            'invoice_id': invoice_id,
            'image': image,
            'boxes': boxes,
            'text_data': text_data,
            'img_size': np.array(Image.open(img_path).size)
        }
    
    def _load_annotations(self, anno_path: Path) -> List[Dict]:
        """Parse CSV annotation file"""
        boxes = []
        with open(anno_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 9:
                    # Format: x1,y1,x2,y2,x3,y3,x4,y4,text
                    coords = [float(row[i]) for i in range(8)]
                    text = row[8] if len(row) > 8 else ""
                    boxes.append({
                        'coords': coords,
                        'text': text
                    })
        return boxes


def get_sroie_dataloader(images_dir: Path,
                        annotations_dir: Path,
                        texts_dir: Path,
                        batch_size: int = 32,
                        shuffle: bool = True,
                        num_workers: int = 4,
                        max_samples: int = None) -> DataLoader:
    """Create SROIE dataset and dataloader"""
    
    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    dataset = SROIEDataset(
        images_dir=images_dir,
        annotations_dir=annotations_dir,
        texts_dir=texts_dir,
        transform=transform,
        max_samples=max_samples
    )
    
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return dataloader, dataset
```

### Step 3.2: Create Data Utilities

**Create**: `src/data/utils.py`
```python
"""Data utility functions"""

import os
from pathlib import Path
from typing import Tuple, List
import numpy as np
import json

def get_dataset_statistics(images_dir: Path,
                          annotations_dir: Path,
                          texts_dir: Path) -> Dict:
    """Compute dataset statistics"""
    
    num_images = len([f for f in os.listdir(images_dir) if f.endswith('.jpg')])
    num_annotations = len([f for f in os.listdir(annotations_dir) if f.endswith('.csv')])
    num_texts = len([f for f in os.listdir(texts_dir) if f.endswith('.json')])
    
    # Sample text data for field statistics
    text_fields = {'company': [], 'date': [], 'address': [], 'total': []}
    
    for text_file in list(os.listdir(texts_dir))[:50]:  # Sample first 50
        with open(texts_dir / text_file, 'r') as f:
            data = json.load(f)
            for field in text_fields.keys():
                if field in data:
                    text_fields[field].append(len(str(data[field])))
    
    return {
        'num_images': num_images,
        'num_annotations': num_annotations,
        'num_texts': num_texts,
        'text_field_stats': {
            field: {
                'avg_length': np.mean(lengths) if lengths else 0,
                'max_length': np.max(lengths) if lengths else 0
            }
            for field, lengths in text_fields.items()
        }
    }

def split_dataset(images_dir: Path,
                 train_ratio: float = 0.8,
                 val_ratio: float = 0.1,
                 test_ratio: float = 0.1,
                 seed: int = 42) -> Tuple[List, List, List]:
    """Split dataset into train/val/test"""
    
    np.random.seed(seed)
    
    all_files = sorted([f.replace('.jpg', '') 
                       for f in os.listdir(images_dir) 
                       if f.endswith('.jpg')])
    
    np.random.shuffle(all_files)
    
    total = len(all_files)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    return (
        all_files[:train_end],
        all_files[train_end:val_end],
        all_files[val_end:]
    )
```

### Step 3.3: Test Data Loading

**Create**: `notebooks/01_data_exploration.ipynb` (or `.py` for quick test)

```python
# Quick test script
import sys
sys.path.insert(0, '/Users/sam/Downloads/DocuMind/DocuMind')

from pathlib import Path
from src.config.config import SROIE_IMAGES, SROIE_ANNOTATIONS, SROIE_TEXTS
from src.data.dataset import get_sroie_dataloader
from src.data.utils import get_dataset_statistics, split_dataset

# 1. Check dataset statistics
print("=" * 50)
print("DATASET STATISTICS")
print("=" * 50)
stats = get_dataset_statistics(SROIE_IMAGES, SROIE_ANNOTATIONS, SROIE_TEXTS)
print(f"Images: {stats['num_images']}")
print(f"Annotations: {stats['num_annotations']}")
print(f"Text files: {stats['num_texts']}")

# 2. Split dataset
print("\n" + "=" * 50)
print("DATASET SPLIT")
print("=" * 50)
train, val, test = split_dataset(SROIE_IMAGES)
print(f"Train: {len(train)} samples")
print(f"Validation: {len(val)} samples")
print(f"Test: {len(test)} samples")

# 3. Test dataloader
print("\n" + "=" * 50)
print("TESTING DATALOADER")
print("=" * 50)
dataloader, dataset = get_sroie_dataloader(
    SROIE_IMAGES, SROIE_ANNOTATIONS, SROIE_TEXTS,
    batch_size=4, num_workers=0, max_samples=10
)

for batch in dataloader:
    print(f"Batch size: {len(batch['image'])}")
    print(f"Image shape: {batch['image'].shape}")
    print(f"Sample invoice ID: {batch['invoice_id'][0]}")
    print(f"Number of boxes: {len(batch['boxes'][0])}")
    print(f"Text data: {batch['text_data'][0]}")
    break

print("\n✅ Data pipeline working correctly!")
```

✅ **Phase 3 Complete** - Data pipeline created and tested

---

## Phase 4: Baseline Model Setup

### Step 4.1: Create Base Model Architecture

**Create**: `src/models/base_model.py`
```python
"""Base model architectures"""

import torch
import torch.nn as nn
import torchvision.models as models

class TextDetectionModel(nn.Module):
    """Baseline model for text detection (bounding box prediction)"""
    
    def __init__(self, num_boxes: int = 100):
        super().__init__()
        
        # ResNet50 backbone
        backbone = models.resnet50(pretrained=True)
        self.features = nn.Sequential(*list(backbone.children())[:-2])
        
        # Detection head
        self.detection_head = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_boxes * 8)  # 8 coordinates per box
        )
    
    def forward(self, x):
        features = self.features(x)
        boxes = self.detection_head(features)
        return boxes

class InformationExtractionModel(nn.Module):
    """Baseline model for key information extraction"""
    
    def __init__(self, num_classes: int = 4):
        super().__init__()
        
        # Pretrained ResNet50
        backbone = models.resnet50(pretrained=True)
        self.features = nn.Sequential(*list(backbone.children())[:-1])
        
        # Classification head for key fields
        self.classifier = nn.Sequential(
            nn.Linear(2048, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        features = self.features(x).squeeze(-1).squeeze(-1)
        logits = self.classifier(features)
        return logits
```

### Step 4.2: Create Training Module

**Create**: `src/models/trainer.py`
```python
"""Training utilities and trainer class"""

import torch
import torch.nn as nn
from torch.optim import Adam
from tqdm import tqdm
from pathlib import Path
import json

class ModelTrainer:
    """Trainer for document understanding models"""
    
    def __init__(self, 
                 model: nn.Module,
                 device: str = 'cuda' if torch.cuda.is_available() else 'cpu',
                 learning_rate: float = 1e-4,
                 checkpoint_dir: Path = None):
        
        self.model = model.to(device)
        self.device = device
        self.optimizer = Adam(model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()
        self.checkpoint_dir = checkpoint_dir or Path('./models/checkpoints')
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        self.history = {'train_loss': [], 'val_loss': []}
    
    def train_epoch(self, train_loader):
        """Train for one epoch"""
        self.model.train()
        total_loss = 0
        
        for batch in tqdm(train_loader, desc="Training"):
            images = batch['image'].to(self.device)
            # For testing - simplified loss
            # In real scenario, you'd use actual targets
            
            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = torch.tensor(0.0).to(self.device)  # Placeholder
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        avg_loss = total_loss / len(train_loader)
        self.history['train_loss'].append(avg_loss)
        return avg_loss
    
    def save_checkpoint(self, epoch: int, name: str = 'checkpoint'):
        """Save model checkpoint"""
        path = self.checkpoint_dir / f"{name}_epoch_{epoch}.pth"
        torch.save({
            'epoch': epoch,
            'model_state': self.model.state_dict(),
            'optimizer_state': self.optimizer.state_dict(),
            'history': self.history
        }, path)
        print(f"Checkpoint saved: {path}")
    
    def load_checkpoint(self, path: Path):
        """Load model checkpoint"""
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state'])
        self.history = checkpoint['history']
        print(f"Checkpoint loaded: {path}")
```

✅ **Phase 4 Complete** - Baseline model architecture created

---

## Phase 5: Testing & Validation

### Step 5.1: Create Evaluation Metrics

**Create**: `src/utils/metrics.py`
```python
"""Evaluation metrics for document understanding"""

import numpy as np
from typing import List, Dict

def calculate_iou(box1, box2):
    """Calculate Intersection over Union (IoU) for bounding boxes"""
    # Simplified IoU calculation
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    
    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)
    
    if inter_x_max < inter_x_min or inter_y_max < inter_y_min:
        return 0.0
    
    inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = box1_area + box2_area - inter_area
    
    return inter_area / union_area if union_area > 0 else 0.0

def evaluate_detection(predictions: List[Dict], 
                      ground_truth: List[Dict],
                      iou_threshold: float = 0.5) -> Dict:
    """Evaluate text detection performance"""
    
    tp = fp = fn = 0
    
    for pred, gt in zip(predictions, ground_truth):
        pred_boxes = pred['boxes']
        gt_boxes = gt['boxes']
        
        matched = set()
        for pb in pred_boxes:
            best_iou = 0
            best_idx = -1
            for idx, gb in enumerate(gt_boxes):
                if idx in matched:
                    continue
                iou = calculate_iou(pb, gb)
                if iou > best_iou:
                    best_iou = iou
                    best_idx = idx
            
            if best_iou >= iou_threshold:
                tp += 1
                matched.add(best_idx)
            else:
                fp += 1
        
        fn += len(gt_boxes) - len(matched)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': tp,
        'fp': fp,
        'fn': fn
    }
```

### Step 5.2: Create Test Script

**Create**: `tests/test_pipeline.py`
```python
"""Integration tests for data pipeline and models"""

import sys
import os
sys.path.insert(0, '/Users/sam/Downloads/DocuMind/DocuMind')

from pathlib import Path
from src.config.config import SROIE_IMAGES, SROIE_ANNOTATIONS, SROIE_TEXTS, CHECKPOINTS_ROOT
from src.data.dataset import get_sroie_dataloader
from src.models.base_model import TextDetectionModel, InformationExtractionModel
from src.models.trainer import ModelTrainer
import torch

def test_data_pipeline():
    """Test data loading"""
    print("\n" + "="*60)
    print("TEST 1: Data Pipeline")
    print("="*60)
    
    dataloader, dataset = get_sroie_dataloader(
        SROIE_IMAGES, SROIE_ANNOTATIONS, SROIE_TEXTS,
        batch_size=4, num_workers=0, max_samples=10
    )
    
    print(f"✓ Dataset size: {len(dataset)}")
    print(f"✓ Dataloader batches: {len(dataloader)}")
    
    for batch in dataloader:
        print(f"✓ Batch image shape: {batch['image'].shape}")
        print(f"✓ Sample loaded successfully")
        break
    
    return True

def test_model_initialization():
    """Test model creation"""
    print("\n" + "="*60)
    print("TEST 2: Model Initialization")
    print("="*60)
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Test detection model
    det_model = TextDetectionModel(num_boxes=100)
    det_model.to(device)
    print(f"✓ Detection model created ({device})")
    print(f"  Parameters: {sum(p.numel() for p in det_model.parameters()):,}")
    
    # Test extraction model
    ext_model = InformationExtractionModel(num_classes=4)
    ext_model.to(device)
    print(f"✓ Extraction model created ({device})")
    print(f"  Parameters: {sum(p.numel() for p in ext_model.parameters()):,}")
    
    return True

def test_forward_pass():
    """Test forward pass"""
    print("\n" + "="*60)
    print("TEST 3: Forward Pass")
    print("="*60)
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    dataloader, _ = get_sroie_dataloader(
        SROIE_IMAGES, SROIE_ANNOTATIONS, SROIE_TEXTS,
        batch_size=4, num_workers=0, max_samples=5
    )
    
    model = TextDetectionModel()
    model.to(device)
    model.eval()
    
    for batch in dataloader:
        images = batch['image'].to(device)
        with torch.no_grad():
            outputs = model(images)
        
        print(f"✓ Input shape: {images.shape}")
        print(f"✓ Output shape: {outputs.shape}")
        print(f"✓ Forward pass successful")
        break
    
    return True

def test_trainer():
    """Test training loop"""
    print("\n" + "="*60)
    print("TEST 4: Trainer Setup")
    print("="*60)
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    model = TextDetectionModel()
    trainer = ModelTrainer(model, device=device, checkpoint_dir=CHECKPOINTS_ROOT)
    
    print(f"✓ Trainer initialized")
    print(f"✓ Device: {device}")
    print(f"✓ Checkpoint directory: {CHECKPOINTS_ROOT}")
    
    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DOCUMIND - INTEGRATION TESTS")
    print("="*60)
    
    tests = [
        ("Data Pipeline", test_data_pipeline),
        ("Model Init", test_model_initialization),
        ("Forward Pass", test_forward_pass),
        ("Trainer Setup", test_trainer),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, "PASSED" if result else "FAILED"))
        except Exception as e:
            print(f"\n✗ Error: {e}")
            results.append((name, "FAILED"))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, status in results:
        symbol = "✓" if status == "PASSED" else "✗"
        print(f"{symbol} {name}: {status}")
    
    all_passed = all(status == "PASSED" for _, status in results)
    if all_passed:
        print("\n✅ All tests passed! Project is ready for development.")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
```

✅ **Phase 5 Complete** - Testing framework created

---

## 🚀 Quick Start Execution

### Run Complete Initialization:

```bash
cd /Users/sam/Downloads/DocuMind/DocuMind

# 1. Create environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create project structure (run from Python)
python scripts/setup_project.py

# 4. Run integration tests
python tests/test_pipeline.py

# 5. Explore data with notebook
jupyter notebook notebooks/01_data_exploration.ipynb
```

---

## 📊 Expected Output After Initialization

```
✅ All tests passed! Project is ready for development.
  ✓ Data Pipeline: PASSED
  ✓ Model Init: PASSED
  ✓ Forward Pass: PASSED
  ✓ Trainer Setup: PASSED

Ready to:
  - Train baseline models
  - Experiment with architectures
  - Evaluate on test set
  - Build production pipelines
```

---

## 📝 Next Steps After Initialization

Once initialization is complete:

1. **Train Baseline Models** - Run training on SROIE data
2. **Evaluate Performance** - Test on held-out test set
3. **Experiment** - Try different architectures and parameters
4. **Document Results** - Log results in `docs/results/`
5. **Iterate** - Improve based on evaluation metrics

---

## 🔗 Quick Reference

| Component | Location | Purpose |
|-----------|----------|---------|
| Configuration | `src/config/config.py` | Global settings |
| Datasets | `src/data/dataset.py` | Data loading |
| Models | `src/models/base_model.py` | Architectures |
| Training | `src/models/trainer.py` | Training loop |
| Metrics | `src/utils/metrics.py` | Evaluation |
| Tests | `tests/test_pipeline.py` | Integration tests |
| Data | `data/DATA_INDEX.md` | Dataset info |

---

**Last Updated**: 2026-11-27  
**Status**: 🚀 Ready for Phase 1 Execution
