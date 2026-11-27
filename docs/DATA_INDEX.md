# Data Index - DocuMind Project

**Last Updated**: 2026-11-27  
**Location**: `/Users/sam/Downloads/DocuMind/DocuMind/data/`

---

## Overview

The data folder contains three main dataset categories:
1. **CUAD** - Contract Understanding Attentive Dataset
2. **TRAIN** - Training and test datasets for model development
3. **INVOICES** - Scanned invoice and receipt images with annotations

**Total Size**: ~460 MB

---

## 📁 Directory Structure

```
data/
├── cuad/                          # Contract Understanding Attentive Dataset
│   └── CUADv1.json               # Main CUAD dataset (38 MB)
│
├── train/                         # Training & Test Data
│   ├── test.json                 # Test dataset (7 MB)
│   └── train_separate_questions.json  # Training questions (33 MB)
│
├── invoices/                      # Invoice & Receipt Images
│   └── sroie/                    # ICDAR 2019 SROIE Dataset
│       ├── images/              # 626 invoice JPG images (340 MB)
│       ├── annotations/         # 626 bounding box CSV files (2.5 MB)
│       ├── texts/               # 626 OCR JSON files (2.4 MB)
│       ├── README.md            # Original SROIE documentation
│       └── LICENSE              # Dataset license
│
└── DATA_INDEX.md                 # This file (updated with each change)
```

---

## 📊 Dataset Details

### 1. CUAD Dataset (`cuad/`)

**File**: `CUADv1.json` (38 MB)

**Purpose**: Contract Understanding Attentive Dataset for legal document understanding

**Format**: JSON  
**Records**: Multiple contract documents with annotations

**Usage**: Legal document analysis, contract parsing, information extraction

---

### 2. Training Data (`train/`)

**Files**:
- `test.json` (7 MB) - Test dataset for model evaluation
- `train_separate_questions.json` (33 MB) - Training dataset with questions

**Purpose**: Model training and evaluation

**Format**: JSON  
**Usage**: Training document understanding and QA models

---

### 3. Invoice Dataset (`invoices/sroie/`)

**Source**: [ICDAR-2019-SROIE](https://github.com/zzzDavid/ICDAR-2019-SROIE)

**Total Records**: 626 invoices

**Files**:
- **images/** (340 MB) - 626 scanned invoice JPG images
  - Format: JPEG, 463×1013 pixels, ~96KB each
  - Naming: `000.jpg` to `625.jpg`
  
- **annotations/** (2.5 MB) - 626 bounding box CSV files
  - Format: CSV with coordinates and text content
  - Naming: `000.csv` to `625.csv`
  
- **texts/** (2.4 MB) - 626 OCR extraction JSON files
  - Format: JSON with structured data (company, date, address, total)
  - Naming: `000.json` to `625.json`

**File Correspondence**: Each invoice has 3 matching files with the same ID number

**Usage**: 
- OCR and document analysis
- Text localization and detection
- Information extraction
- Invoice parsing pipelines

---

## 🔄 Data Changes & Updates

### 2026-11-27 - Initial Organization
- ✅ Organized JSON files into `cuad/` and `train/` folders
- ✅ Downloaded SROIE invoice dataset (626 images + annotations)
- ✅ Organized invoice data with clean structure (images, annotations, texts)
- ✅ Created unified DATA_INDEX.md for documentation

---

## 📈 Statistics

| Dataset | Type | Count | Size |
|---------|------|-------|------|
| CUAD | Contracts | - | 38 MB |
| Test | JSON | 1 file | 7 MB |
| Train | JSON | 1 file | 33 MB |
| Invoices | Images | 626 | 340 MB |
| Invoices | Annotations | 626 | 2.5 MB |
| Invoices | Text Data | 626 | 2.4 MB |
| **TOTAL** | - | - | **~460 MB** |

---

## 💡 Quick Access

### Load CUAD Dataset (Python)
```python
import json

with open('/Users/sam/Downloads/DocuMind/DocuMind/data/cuad/CUADv1.json', 'r') as f:
    cuad = json.load(f)
```

### Load Training Data (Python)
```python
import json

test = json.load(open('/Users/sam/Downloads/DocuMind/DocuMind/data/train/test.json'))
train = json.load(open('/Users/sam/Downloads/DocuMind/DocuMind/data/train/train_separate_questions.json'))
```

### Access Invoice Data (Python)
```python
import json
from PIL import Image

# Load image
img = Image.open('/Users/sam/Downloads/DocuMind/DocuMind/data/invoices/sroie/images/000.jpg')

# Load annotations
with open('/Users/sam/Downloads/DocuMind/DocuMind/data/invoices/sroie/annotations/000.csv') as f:
    annotations = f.read()

# Load text data
with open('/Users/sam/Downloads/DocuMind/DocuMind/data/invoices/sroie/texts/000.json') as f:
    text_data = json.load(f)
```

---

## 📝 Notes

- All datasets are organized by type for easy access
- One unified index file (this file) tracks all changes
- Invoice data includes original SROIE README and LICENSE
- No unnecessary duplicate documentation files
- All files maintain correspondence through ID matching

---

## 🔗 References

- **CUAD Dataset**: Contract Understanding Attentive Dataset
- **SROIE**: Scanned Receipts OCR and Information Extraction (ICDAR 2019)
- **GitHub**: https://github.com/zzzDavid/ICDAR-2019-SROIE

