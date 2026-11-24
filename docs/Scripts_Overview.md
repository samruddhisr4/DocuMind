# Scripts Overview

Quick reference for all utility scripts in the `/scripts/` directory.

## Available Scripts

### 1. `extract_cuad.py` - Extract CUAD Contracts

**Purpose:** Convert CUAD JSON files (train_separate_questions.json + test.json) into individual contract files with metadata.

**Usage:**
```bash
python scripts/extract_cuad.py \
    --train data/train_separate_questions.json \
    --test data/test.json \
    --output contracts/cuad
```

**Output:**
```
contracts/cuad/
├── training/
│   ├── contract_0000.txt           # Full contract text
│   ├── contract_0000_metadata.json # {title, split, qa_count, text_length}
│   ├── contract_0000_qa.json       # Q&A pairs for extraction training
│   ├── contract_0001.txt
│   └── ... (408 total)
└── test/
    ├── contract_0408.txt
    ├── contract_0408_metadata.json
    ├── contract_0408_qa.json
    └── ... (102 total)
```

**When to run:** 
- Week 1: To prepare CUAD contracts for indexing and retrieval testing
- Before: Running extraction model training

**What it does:**
- ✓ Extracts 408 training + 102 test contracts
- ✓ Preserves full text for indexing
- ✓ Saves Q&A pairs as ground truth for extraction models
- ✓ Saves metadata (title, split, counts) for easy reference

---

### 2. `generate_invoices.py` - Generate Synthetic Invoices

**Purpose:** Create synthetic invoice images with optional degradations (blur, rotation, noise) for OCR testing.

**Usage:**
```bash
# Generate 100 invoices with all degradations
python scripts/generate_invoices.py \
    --output data/invoices \
    --count 100 \
    --degradations blur rotation noise lowcontrast faded
```

**Output:**
```
data/invoices/
├── clean/                           # 70 clean invoices (no OCR challenges)
│   ├── invoice_0000.jpg
│   ├── invoice_0001.jpg
│   └── ... (70 total)
├── degraded/                        # 20 invoices with 5 degradation types each = 100 images
│   ├── invoice_0070_blur.jpg
│   ├── invoice_0070_rotation.jpg
│   ├── invoice_0070_noise.jpg
│   ├── invoice_0070_lowcontrast.jpg
│   ├── invoice_0070_faded.jpg
│   ├── invoice_0071_blur.jpg
│   └── ... (100 total degraded versions)
├── violations/                      # 10 invoices with intentional violations
│   ├── invoice_0090_term_violation.jpg     # Payment term mismatch
│   ├── invoice_0091_price_violation.jpg    # Price exceeds contract cap
│   └── ... (10 total)
└── ground_truth.json                # Metadata for all images
```

**Configuration:**
```python
# Default split (100 invoices):
# 70% clean (no OCR challenges)
# 20% degraded (blur, rotation, noise, lowcontrast, faded)
# 10% violations (term mismatches, price violations)

# Degradation types:
# - 'blur': Gaussian blur (radius=2)
# - 'rotation': Random ±10° rotation
# - 'noise': Salt-and-pepper noise
# - 'lowcontrast': Reduced contrast (60%)
# - 'faded': Reduced brightness + contrast
```

**When to run:**
- Week 1: To prepare OCR test dataset
- Week 2: To create violation-seeded dataset

**What it does:**
- ✓ Generates realistic invoice images with structured data
- ✓ Applies multiple degradations per invoice
- ✓ Creates violation invoices with intentional mismatches
- ✓ Saves ground truth JSON with metadata
- ✓ Includes vendor, date, total, payment terms per invoice

**Example ground_truth.json:**
```json
[
  {
    "invoice_id": 0,
    "invoice_number": "INV-2024-00000",
    "vendor": "Acme Corp",
    "date": "2024-11-24",
    "total": 5000,
    "payment_term": "Net-45",
    "violation": null,
    "file": "data/invoices/clean/invoice_0000.jpg",
    "category": "clean"
  },
  {
    "invoice_id": 70,
    "invoice_number": "INV-2024-00070",
    "vendor": "TechVendor Inc",
    "date": "2024-11-23",
    "total": 3500,
    "payment_term": "Net-45",
    "violation": null,
    "file": "data/invoices/degraded/invoice_0070_blur.jpg",
    "category": "degraded",
    "degradation": "blur"
  },
  {
    "invoice_id": 90,
    "invoice_number": "INV-2024-00090",
    "vendor": "Global Supplies Ltd",
    "date": "2024-11-22",
    "total": 7500,
    "payment_term": "Net-15",
    "violation": "term",
    "file": "data/invoices/violations/invoice_0090_term_violation.jpg",
    "category": "violations",
    "violation_type": "term"
  }
]
```

---

## Usage in Implementation Timeline

### Week 1: OCR Testing
```bash
# 1. Extract CUAD contracts
python scripts/extract_cuad.py --train data/train_separate_questions.json --test data/test.json

# 2. Generate synthetic invoices for OCR baseline
python scripts/generate_invoices.py --output data/invoices --count 50

# 3. Download real invoice datasets (SROIE, CORD)
# See Dataset_Guide.md for URLs

# 4. Run OCR comparison on all three sources
# - SROIE (real scans)
# - Synthetic clean (baseline)
# - Synthetic degraded (robustness testing)
```

### Week 2: Extraction Training & Validation Rules
```bash
# 1. Use CUAD Q&A pairs from extract_cuad.py output
#    Load from: contracts/cuad/training/contract_*_qa.json

# 2. Use synthetic invoices as extraction training data
#    Load from: data/invoices/ground_truth.json
```

### Week 3: Integration Testing
```bash
# 1. Use contracts from extract_cuad.py output for indexing
# 2. Use invoices (clean + degraded) for contract validation
# 3. Seed violations using ground_truth.json
```

### Week 4: Evaluation
```bash
# Run evaluation on:
# - OCR: SROIE + synthetic degraded → CER comparison
# - Extraction: CUAD Q&A pairs + synthetic invoices → F1 scores
# - Validation: Violation invoices vs. contracts → recall/precision
# - Retrieval: CUAD contracts indexed, test semantic queries
```

---

## Script Parameters Reference

### extract_cuad.py
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--train` | `./data/train_separate_questions.json` | Training contracts JSON |
| `--test` | `./data/test.json` | Test contracts JSON |
| `--output` | `./contracts/cuad` | Output directory |

### generate_invoices.py
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output` | `./data/invoices` | Output directory |
| `--count` | `100` | Total invoices to generate |
| `--degradations` | `blur rotation noise lowcontrast faded` | Degradation types |

---

## Quick Start

```bash
# 1. Extract contracts (408 train + 102 test)
cd /Users/sam/Downloads/DocuMind/DocuMind
python scripts/extract_cuad.py

# 2. Generate synthetic invoices (70 clean + 20 degraded + 10 violations)
python scripts/generate_invoices.py --count 100

# 3. Check outputs
ls -lah contracts/cuad/training | head -10
ls -lah data/invoices/clean | head -10
cat data/invoices/ground_truth.json | jq '.[0:3]'
```

---

## Troubleshooting

**Q: Script fails with "Module not found"**
```bash
pip install Pillow numpy
```

**Q: Generated invoices look strange / corrupted**
- Check PIL is installed: `python -c "from PIL import Image; print(Image.PIL_VERSION)"`
- Try with smaller degradation values in generate_invoices.py

**Q: CUAD extraction takes too long**
- Normal for 510 contracts. Progress prints every 50 contracts.
- Takes ~30 seconds total on modern hardware.

**Q: How do I use ground_truth.json from generated invoices?**
```python
import json

with open('data/invoices/ground_truth.json') as f:
    invoices = json.load(f)

# Filter by category
clean = [inv for inv in invoices if inv['category'] == 'clean']
degraded = [inv for inv in invoices if inv['category'] == 'degraded']
violations = [inv for inv in invoices if inv['category'] == 'violations']

# Get specific violation type
term_violations = [inv for inv in violations if inv['violation_type'] == 'term']
```

