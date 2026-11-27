#!/usr/bin/env python3
"""
DocuMind Project Setup Script

This script initializes the project structure, creates necessary directories,
and generates base configuration files.

Usage:
    python scripts/setup_project.py
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create all necessary project directories"""

    base_path = Path(__file__).parent.parent

    directories = [
        'src',
        'src/models',
        'src/data',
        'src/utils',
        'src/config',
        'notebooks/exploratory',
        'notebooks/experiments',
        'models/checkpoints',
        'models/weights',
        'tests/unit',
        'tests/integration',
        'docs/api',
        'docs/guides',
        'docs/results',
        'scripts',
        'logs',
    ]

    print("📁 Creating directories...")
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")

    return base_path

def create_init_files(base_path):
    """Create __init__.py files for Python packages"""

    init_dirs = [
        'src',
        'src/models',
        'src/data',
        'src/utils',
        'src/config',
        'tests',
    ]

    print("\n🐍 Creating Python package files...")
    for directory in init_dirs:
        init_file = base_path / directory / '__init__.py'
        init_file.touch(exist_ok=True)
        print(f"  ✓ {directory}/__init__.py")

def create_requirements_txt(base_path):
    """Create requirements.txt"""

    requirements = """# Core dependencies
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
click==8.1.6

# Development
jupyter==1.0.0
ipython==8.14.0
pytest==7.4.0
black==23.7.0
flake8==6.0.0
pylint==2.17.5
"""

    req_file = base_path / 'requirements.txt'
    if not req_file.exists():
        with open(req_file, 'w') as f:
            f.write(requirements)
        print("✓ requirements.txt")
    else:
        print("⚠ requirements.txt already exists")

def create_gitignore(base_path):
    """Create .gitignore"""

    gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Data & Models
*.pth
*.pt
models/checkpoints/*
models/weights/*
!models/.gitkeep

# Logs
logs/
*.log

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db
"""

    gitignore_file = base_path / '.gitignore'
    if not gitignore_file.exists():
        with open(gitignore_file, 'w') as f:
            f.write(gitignore)
        print("✓ .gitignore")
    else:
        print("⚠ .gitignore already exists")

def create_config_file(base_path):
    """Create src/config/config.py"""

    config_content = '''"""Global configuration for DocuMind"""

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
'''

    config_file = base_path / 'src' / 'config' / 'config.py'
    if not config_file.exists():
        with open(config_file, 'w') as f:
            f.write(config_content)
        print("✓ src/config/config.py")
    else:
        print("⚠ src/config/config.py already exists")

def create_placeholder_files(base_path):
    """Create placeholder files for key modules"""

    files_to_create = {
        'src/data/dataset.py': '"""Dataset loaders for different document types"""\n',
        'src/data/utils.py': '"""Data utility functions"""\n',
        'src/models/base_model.py': '"""Base model architectures"""\n',
        'src/models/trainer.py': '"""Training utilities and trainer class"""\n',
        'src/utils/metrics.py': '"""Evaluation metrics for document understanding"""\n',
    }

    print("\n📄 Creating module files...")
    for file_path, content in files_to_create.items():
        full_path = base_path / file_path
        if not full_path.exists():
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"  ✓ {file_path}")
        else:
            print(f"  ⚠ {file_path} already exists")

def create_summary(base_path):
    """Create setup summary"""

    print("\n" + "="*60)
    print("✅ PROJECT INITIALIZATION COMPLETE")
    print("="*60)

    print("\n📂 Project Structure:")
    print(f"  Root: {base_path}")
    print("  ├── src/              (source code)")
    print("  ├── data/             (datasets)")
    print("  ├── notebooks/        (experiments)")
    print("  ├── models/           (checkpoints & weights)")
    print("  ├── tests/            (test suites)")
    print("  ├── docs/             (documentation)")
    print("  ├── scripts/          (utility scripts)")
    print("  └── logs/             (training logs)")

    print("\n📋 Next Steps:")
    print("  1. Install dependencies:")
    print("     pip install -r requirements.txt")
    print("\n  2. Run integration tests:")
    print("     python tests/test_pipeline.py")
    print("\n  3. Explore data:")
    print("     jupyter notebook notebooks/01_data_exploration.ipynb")
    print("\n  4. Check configuration:")
    print("     cat src/config/config.py")

    print("\n📚 Documentation:")
    print("  • INITIALIZATION.md  - Complete setup guide")
    print("  • data/DATA_INDEX.md - Dataset documentation")
    print("  • README.md          - Project overview")

def main():
    """Main setup function"""

    print("="*60)
    print("🚀 DocuMind - Project Setup")
    print("="*60)

    try:
        # Create directories
        base_path = create_directories()

        # Create Python package files
        create_init_files(base_path)

        # Create configuration files
        print("\n⚙️  Creating configuration files...")
        create_requirements_txt(base_path)
        create_gitignore(base_path)
        create_config_file(base_path)

        # Create placeholder modules
        create_placeholder_files(base_path)

        # Summary
        create_summary(base_path)

        print("\n✨ Setup complete! You're ready to start development.")

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
