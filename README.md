# DocuMind - Document Understanding & Information Extraction

**Status**: 🚀 Project Initialization  
**Last Updated**: 2026-11-27

## Overview

DocuMind is a comprehensive document understanding platform that combines OCR, layout analysis, and information extraction. It leverages multiple datasets (SROIE invoices, CUAD contracts, and custom training data) to build robust document processing models.

## 🎯 Project Goals

1. **OCR & Text Localization**: Accurately detect and recognize text in scanned documents
2. **Layout Understanding**: Parse document structure and identify key sections
3. **Information Extraction**: Extract structured data from documents (invoices, contracts, receipts)
4. **Document Classification**: Categorize documents by type and content
5. **Pipeline Integration**: Build end-to-end document processing pipelines

## 📊 Available Datasets

| Dataset | Type | Records | Size | Purpose |
|---------|------|---------|------|---------|
| **SROIE** | Invoice Images | 626 | 345 MB | OCR, text localization, information extraction |
| **CUAD** | Contract Docs | - | 38 MB | Contract understanding, legal document processing |
| **Training Data** | Mixed | - | 40 MB | Model training and testing |

See [data/DATA_INDEX.md](data/DATA_INDEX.md) for complete dataset documentation.

## 📁 Project Structure

```
DocuMind/
├── data/                      # All datasets (organized by type)
│   ├── invoices/sroie/       # 626 invoice images + annotations
│   ├── cuad/                 # Contract understanding dataset
│   ├── train/                # Training & test datasets
│   └── DATA_INDEX.md         # Dataset documentation
├── src/                       # Source code (to be created)
├── models/                    # Trained models (to be created)
├── notebooks/                 # Jupyter notebooks (to be created)
├── scripts/                   # Utility scripts
├── tests/                     # Unit tests (to be created)
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
├── environment.yml            # Conda environment
└── README.md                 # This file
```

## 🔄 Project Status

### ✅ Completed (Initialization Phase)
- [x] Data collection and organization (626 invoices + CUAD + training data)
- [x] Dataset preparation and indexing with documentation
- [x] Project structure created (27 directories, organized by purpose)
- [x] Python package setup (src/, tests/, notebooks/, models/)
- [x] Configuration system (src/config/config.py)
- [x] Requirements file (30+ dependencies)
- [x] Documentation (README, INITIALIZATION guide, SETUP_STATUS)
- [x] Code scaffolding (models, data loaders, trainer, metrics)
- [x] Setup automation (scripts/setup_project.py)

### 🔄 Next Phase (Development)
- [ ] Activate Python environment & install dependencies
- [ ] Implement data loading pipeline
- [ ] Implement baseline models
- [ ] Run integration tests
- [ ] Explore and visualize data
- [ ] Train baseline model on SROIE

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+** (macOS users: use `python3` command, not `python`)
- **pip** (comes with Python)
- **Virtual environment** (venv)

### Quick Initialization

For complete step-by-step initialization guide, see **[INITIALIZATION.md](INITIALIZATION.md)**

**Quick Setup (5 steps)**:
```bash
# 1. Navigate to project
cd /Users/sam/Downloads/DocuMind/DocuMind

# 2. Create virtual environment (macOS: use python3, not python)
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python -c "import torch; import cv2; print('✓ All imports OK')"

# 5. Run integration tests (after implementation)
python tests/test_pipeline.py
```

### macOS Python Setup Note
On macOS, only `python3` is available by default. If you get "command not found: python":
```bash
# Use python3 instead:
python3 --version          # Check version
python3 -m venv venv       # Create environment
python3 -m pip install -r requirements.txt  # Install (alternative)
```
Once the virtual environment is activated, you can use `python` normally.

### Key Directories

- **`data/`** - All datasets organized by type (see [data/DATA_INDEX.md](data/DATA_INDEX.md))
- **`src/`** - Source code (models, data loaders, utilities)
- **`notebooks/`** - Jupyter notebooks for exploration and experiments
- **`models/`** - Trained model weights and checkpoints
- **`scripts/`** - Setup and utility scripts
- **`tests/`** - Integration and unit tests

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) | ✅ Current setup progress (track your progress here) |
| [QUICK_START.md](QUICK_START.md) | 🚀 Quick reference commands |
| [SETUP_STATUS.md](SETUP_STATUS.md) | 📋 What's been completed |
| [INITIALIZATION.md](INITIALIZATION.md) | 📖 Complete setup guide (5+ phases) |
| [data/DATA_INDEX.md](data/DATA_INDEX.md) | 📊 Dataset documentation & statistics |
| [docs/](docs/) | 📚 Architecture guides and API docs |

## ⚙️ Configuration

Main configuration file: `src/config/config.py`

Key settings:
- Dataset paths (SROIE, CUAD, training data)
- Model hyperparameters (batch size, learning rate, epochs)
- Data loading parameters (image size, workers, splits)

Modify as needed for experiments.

## License

```
Copyright (c) 2019 Niansong Zhang, Songyi Yang, Shengjie Xiu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
