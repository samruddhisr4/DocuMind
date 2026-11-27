# Quick Start - Environment Setup

**Status**: ⏳ Dependencies installing...

## What You've Done ✅

```bash
✅ Created Python virtual environment
✅ Activated venv
✅ Upgraded pip, setuptools, wheel
✅ Started dependency installation (running in background)
```

## What's Installing 📦

Core packages being installed:
- torch (PyTorch) - Deep learning framework
- torchvision - Computer vision models
- opencv-python - Image processing
- pandas - Data manipulation
- numpy - Numerical computing
- scikit-learn - Machine learning
- matplotlib - Visualization
- jupyter - Notebooks
- ... and 15+ more

**Estimated time**: 5-15 minutes depending on internet speed

## Once Installation Completes ✅

### Verify Installation (2 mins)
```bash
# Already in venv? Just run:
python -c "import torch; import cv2; print('✓ All imports OK')"

# If not in venv, activate first:
cd /Users/sam/Downloads/DocuMind/DocuMind
source venv/bin/activate
python -c "import torch; import cv2; print('✓ All imports OK')"
```

### Next Steps (In Order)

#### 1. Implement Data Pipeline (20 mins)
```bash
# Edit these files to implement dataset loading:
# - src/data/dataset.py
# - src/data/utils.py
```

#### 2. Implement Models (30 mins)
```bash
# Edit these files to implement models:
# - src/models/base_model.py
# - src/models/trainer.py
```

#### 3. Run Tests (10 mins)
```bash
python tests/test_pipeline.py
```

#### 4. Explore Data (30 mins)
```bash
jupyter notebook
# Navigate to: notebooks/01_data_exploration.ipynb
```

#### 5. Train Baseline (1-2 hours)
```bash
# Create training notebook and run training
```

## Common Issues & Solutions

### "command not found: python"
**Solution**: Use `python3` instead (macOS only has python3)
```bash
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

### "command not found: pip"
**Solution**: Use python module directly
```bash
python -m pip install -r requirements.txt
```

### "command not found: jupyter"
**Solution**: It's installed, make sure venv is activated
```bash
source venv/bin/activate
jupyter notebook
```

### Virtual environment not activating
**Solution**: Check if venv exists
```bash
cd /Users/sam/Downloads/DocuMind/DocuMind
ls -la venv/        # Should show bin/, lib/, etc.
source venv/bin/activate
```

## Commands Reference

```bash
# Always start with:
cd /Users/sam/Downloads/DocuMind/DocuMind
source venv/bin/activate

# Then use:
python -m pip install package_name     # Install package
python -c "import package; print('✓')" # Test import
python script.py                        # Run script
jupyter notebook                        # Start Jupyter
pytest tests/                           # Run tests
```

## Project Location

```
/Users/sam/Downloads/DocuMind/DocuMind/
```

## Documentation

- **README.md** - Project overview
- **INITIALIZATION.md** - Complete setup guide
- **SETUP_STATUS.md** - What's been done
- **data/DATA_INDEX.md** - Dataset info

## Key Files to Edit After Setup

| File | What to do |
|------|-----------|
| src/data/dataset.py | Implement SROIEDataset class |
| src/data/utils.py | Implement helper functions |
| src/models/base_model.py | Implement model architectures |
| src/models/trainer.py | Implement training loop |

---

**Check installation progress**: Run the verify command above in a few minutes

**Having issues?** Check INITIALIZATION.md Phase 1 for detailed troubleshooting
