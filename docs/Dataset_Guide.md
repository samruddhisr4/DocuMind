# DocuMind Dataset Guide

## Overview
This guide explains the contracts you already have (CUAD), where to get invoice images for OCR testing, and how to set up your complete dataset pipeline.

---

## Part 1: CUAD Dataset (Contracts) - What You Already Have

### Dataset Structure
You have **510 real legal contracts** in `/data/CUADv1.json`:

```
CUADv1.json (38MB)
├── version: "1.0"
└── data: [
    {
      "title": "LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT",
      "paragraphs": [
        {
          "context": "EXHIBIT 10.6\n\nDISTRIBUTOR AGREEMENT\n\nTHIS DISTRIBUTOR AGREEMENT (the 'Agreement') is made by and between Electric City Corp., a Delaware corporation ('Company') and Electric City of Illinois LLC ('Distributor') this 7th day of September, 1999.",
          "qas": [
            {
              "question": "Highlight the parts related to 'Document Name'",
              "id": "cuad_0__0_1",
              "answers": [
                {"text": "DISTRIBUTOR AGREEMENT", "answer_start": 32}
              ]
            },
            {
              "question": "Highlight the parts related to 'Parties'",
              "id": "cuad_0__0_2",
              "answers": [
                {"text": "Distributor", "answer_start": 215}
              ]
            }
          ]
        }
      ]
    }
  ]
```

### Contract Types in CUAD
The 510 contracts include:
- **Service Agreements** - SaaS, consulting, support services
- **Non-Disclosure Agreements (NDAs)** - confidentiality terms
- **Employment Agreements** - compensation, termination, benefits
- **Purchase Agreements** - pricing, delivery, payment terms
- **Master Service Agreements (MSAs)** - general terms & conditions
- **Supply Agreements** - vendor contracts with pricing schedules
- **License Agreements** - software licensing terms
- **Real Estate Agreements** - lease/property agreements

### Extracted Q&A Topics (Perfect for Training)
Each contract has Q&A pairs for these key clauses:
- `Document Name` - title of agreement
- `Parties` - entities involved
- `Effective Date` - when agreement starts
- `Termination Clause` - how to end agreement
- `Payment Terms` - Net-30, Net-45, etc.
- `Pricing Schedule` - cost structure
- `Price Cap` - maximum amounts
- `Auto-Renewal` - renewal conditions
- `Indemnity` - liability & protection clauses
- `Governing Law` - jurisdiction
- `Termination for Cause` - grounds for termination

### How to Use in DocuMind

#### Split 1: Training vs. Test
```python
# From CUADv1.json (510 contracts)
training_contracts = data['data'][:408]      # 408 for training extraction models
test_contracts = data['data'][408:510]       # 102 for testing (matches test.json)

# train_separate_questions.json has 408 entries (matches training split)
# test.json has 102 entries (matches test split)
```

#### Split 2: Select 5-10 for DocuMind Demo
For your Week 2-3 demo, pick 5-10 diverse contracts:
```python
demo_contracts = [
    "LIMEENERGYCO_09_09_1999-EX-10-DISTRIBUTOR AGREEMENT",        # Vendor agreement
    "NDA_Sample_Employment",                                        # Employment/confidentiality
    "ServiceAgreement_SaaS",                                        # Service/payment terms
    "MasterServiceAgreement",                                       # Complex MSA
    "PurchaseAgreement_Hardware"                                    # Procurement
]
```

#### Use Cases
1. **Stage 2 Extraction Training** - Train on CUAD Q&A pairs to extract contract elements
2. **Stage 5 Knowledge Layer** - Index CUAD contracts for retrieval testing
3. **Stage 6 Query & Answer** - Golden test set: "What are termination clauses in XYZ contract?"
4. **Stage 3d Validation** - Seed invoices with violations against CUAD payment terms

---

## Part 2: Invoice Datasets - Where to Get Images for OCR Testing

### Option 1: SROIE Dataset (Recommended for OCR Testing)
**What:** Scanned Receipts OCR and Information Extraction dataset  
**Size:** ~600 receipt images + annotations  
**Format:** JPG images + JSON ground truth  
**OCR Task:** Text recognition, field extraction

**Download:**
```bash
# Clone SROIE dataset
cd /Users/sam/Downloads/DocuMind/DocuMind/data
git clone https://github.com/SROIE/SROIE2019.git
# Navigate to: SROIE2019/0325updated.task1train(626p)/
# Contains: 626 receipt images, each with ground truth .txt file
```

**What You Get:**
- 626 receipt images (JPG format, various quality)
- Ground truth text for each image
- Field annotations: vendor, date, total, line items, etc.
- Perfect for OCR testing: Tesseract + EasyOCR comparison

**Use in DocuMind:**
- Week 1 OCR testing: use SROIE images to benchmark Tesseract vs. EasyOCR
- Week 1 Evaluation suite: measure OCR character error rate (CER)

### Option 2: Real Invoice Datasets (Paired with CUAD)

**Best sources for invoices matching CUAD contracts:**

| Dataset | Size | Format | Quality | URL |
|---------|------|--------|---------|-----|
| **SROIE** | 626 images | JPG + TXT | Realistic scans, varied angles/lighting | https://github.com/SROIE/SROIE2019 |
| **CORD** | 900 images | PNG + JSON | Detailed annotations, field-level labels | https://github.com/clovaai/cord |
| **LayoutLM Invoices** | 1000+ samples | Image + JSON | Professional invoices with bbox | https://github.com/microsoft/LayoutLM/tree/main/examples/invoice |
| **DocVQA** | 12k pages | PDF + Q&A pairs | Documents with questions | https://www.docvqa.org/ |
| **RVL-CDIP** | 400k images | Multi-class | 11M+ from dataset, includes invoices | https://www.cs.cmu.edu/~aharley/rvl-cdip/ |
| **Invoice2Data** | Templates + samples | PDF/JSON | Real invoice structures | https://github.com/invoice-x/invoice_formats |

**Why SROIE + CORD are best:**
- SROIE: Realistic scans showing OCR challenges (blur, rotation, shadows)
- CORD: Structured annotations (vendor, total, items) matching your extraction schema
- Both free, no licensing restrictions

**Download all at once:**
```bash
cd data/
git clone https://github.com/SROIE/SROIE2019.git sroie_data
git clone https://github.com/clovaai/cord.git cord_data
cp -r sroie_data/0325updated.task1train\(626p\)/ ./sroie_receipts/
cp -r cord_data/data/all/ ./cord_receipts/
```

### Option 3: Synthetic Invoice Generation (For Degradation Testing)
**Create realistic scanned invoices with controlled degradation**

```python
# Generate synthetic invoices with PIL/OpenCV
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

def generate_synthetic_invoice(output_path):
    """Generate a clean invoice image"""
    img = Image.new('RGB', (800, 1000), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add invoice content
    draw.text((50, 50), "INVOICE", fill='black', font=None)
    draw.text((50, 100), f"Invoice #: INV-2024-{random.randint(1000, 9999)}", fill='black')
    draw.text((50, 150), f"Date: 2024-11-{random.randint(1, 28):02d}", fill='black')
    draw.text((50, 200), "Vendor: Acme Corp", fill='black')
    
    # Add items
    y = 300
    for item in ["Item 1: Widget - $100.00", "Item 2: Gadget - $250.00", "Service: Labor - $150.00"]:
        draw.text((50, y), item, fill='black')
        y += 50
    
    draw.text((50, y+50), "TOTAL: $500.00", fill='black')
    
    img.save(output_path)
    return img

def degrade_invoice(image_path, degradation_type='blur'):
    """Apply degradation to simulate bad scans"""
    img = Image.open(image_path)
    
    if degradation_type == 'blur':
        return img.filter(ImageFilter.GaussianBlur(radius=2))
    elif degradation_type == 'noise':
        # Add salt-and-pepper noise
        import numpy as np
        arr = np.array(img)
        for _ in range(1000):
            x, y = random.randint(0, arr.shape[0]-1), random.randint(0, arr.shape[1]-1)
            arr[x, y] = [0, 0, 0]  # Random black spots
        return Image.fromarray(arr.astype('uint8'))
    elif degradation_type == 'rotation':
        return img.rotate(random.randint(-15, 15), expand=True, fillcolor='white')
    elif degradation_type == 'lowcontrast':
        # Reduce contrast to simulate poor scan
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(0.5)
    
    return img

# Generate test set: 50 invoices
for i in range(50):
    clean_path = f"/data/invoices/clean/invoice_{i:03d}.jpg"
    generate_synthetic_invoice(clean_path)
    
    # Create degraded versions
    degrade_invoice(clean_path, 'blur').save(f"/data/invoices/degraded/invoice_{i:03d}_blur.jpg")
    degrade_invoice(clean_path, 'rotation').save(f"/data/invoices/degraded/invoice_{i:03d}_rotated.jpg")
    degrade_invoice(clean_path, 'noise').save(f"/data/invoices/degraded/invoice_{i:03d}_noisy.jpg")
```

### Option 3: Real-World Invoice Sources
**If you need realistic invoice samples:**

1. **Sample Invoices (Free Templates)** - Download and convert to images:
   - Canva: https://www.canva.com/invoices/templates/
   - Microsoft Word: Invoice templates
   - Save as PDF → convert to JPG with ImageMagick

2. **Public Datasets:**
   - **FUNSD Dataset** - Form Understanding in Noisy Scanned Documents
   - **DocVQA** - Document Visual Question Answering (Infographics, invoices)
   - **RVL-CDIP** - Receipts and Invoices (11M+ document images)

3. **Generate from Scratch:**
   - Python libraries: `reportlab` (PDF generation), `PIL` (image creation)
   - Create realistic invoice templates with vendor names, line items, dates
   - Apply realistic degradations (page curl, shadow, fold lines)

---

## Part 3: Complete Dataset Structure for DocuMind

### Recommended Directory Layout
```
/data
├── contracts/
│   ├── cuad/                          # CUAD contracts (extracted from JSON)
│   │   ├── training/
│   │   │   ├── contract_001.txt
│   │   │   ├── contract_002.txt
│   │   │   └── ... (408 total)
│   │   └── test/
│   │       ├── contract_409.txt
│   │       └── ... (102 total)
│   │
│   └── demo/                          # 5-10 selected for demo
│       ├── vendor_agreement.txt
│       ├── nda.txt
│       └── ...
│
├── invoices/
│   ├── clean/                         # Clean, native PDFs/images
│   │   ├── invoice_001.jpg
│   │   ├── invoice_002.jpg
│   │   └── ... (70% of test set)
│   │
│   ├── degraded/                      # Scanned, skewed, noisy
│   │   ├── invoice_003_blur.jpg
│   │   ├── invoice_003_rotated.jpg
│   │   ├── invoice_003_noisy.jpg
│   │   └── ... (20% with OCR challenges)
│   │
│   └── violations/                    # Intentionally invalid
│       ├── invoice_term_violation.jpg (Net-15 vs Net-45)
│       ├── invoice_price_violation.jpg (exceeds cap)
│       └── invoice_expired.jpg (contract expired)
│
├── raw_json/
│   ├── CUADv1.json                    # 510 contracts
│   ├── test.json                      # 102 test samples
│   └── train_separate_questions.json  # 408 train samples
│
└── ground_truth/
    ├── invoices_gt.json               # OCR ground truth for invoices
    ├── extraction_gt.json             # Field extraction ground truth
    └── violations_gt.json             # Expected violations in test set
```

---

## Part 4: Processing Pipeline for CUAD → Usable Contracts

### Step 1: Extract CUAD to Individual Files
```python
import json
import os

with open('/data/raw_json/CUADv1.json', 'r') as f:
    data = json.load(f)

os.makedirs('/data/contracts/cuad/training', exist_ok=True)
os.makedirs('/data/contracts/cuad/test', exist_ok=True)

for idx, contract in enumerate(data['data']):
    split = 'training' if idx < 408 else 'test'
    
    output_path = f'/data/contracts/cuad/{split}/contract_{idx:03d}.txt'
    
    # Extract full text
    full_text = contract['paragraphs'][0]['context']
    
    with open(output_path, 'w') as f:
        f.write(full_text)
    
    print(f"Extracted: {contract['title']} → {output_path}")
```

### Step 2: Extract Q&A Pairs as Ground Truth
```python
import json

with open('/data/raw_json/CUADv1.json', 'r') as f:
    data = json.load(f)

ground_truth = []

for idx, contract in enumerate(data['data']):
    for para in contract['paragraphs']:
        for qa in para.get('qas', []):
            ground_truth.append({
                'contract_id': idx,
                'contract_title': contract['title'],
                'question': qa['question'],
                'answer': qa['answers'][0]['text'] if qa['answers'] else None,
                'answer_start': qa['answers'][0].get('answer_start') if qa['answers'] else None,
            })

with open('/data/ground_truth/extraction_gt.json', 'w') as f:
    json.dump(ground_truth, f, indent=2)

print(f"Extracted {len(ground_truth)} Q&A pairs for training")
```

### Step 3: Create Violations Dataset
```python
import json

# Seed violations: 10% of test invoices violate contracts
violations = [
    {
        'invoice_id': 'inv_001',
        'vendor': 'Acme Corp',
        'violation_type': 'payment_term',
        'invoice_term': 'Net-15',
        'contract_term': 'Net-45',
        'contract_id': 'contract_042',
        'severity': 'high'
    },
    {
        'invoice_id': 'inv_002',
        'vendor': 'Acme Corp',
        'violation_type': 'price_cap_exceeded',
        'invoice_amount': 15000.00,
        'contract_cap': 10000.00,
        'contract_id': 'contract_042',
        'severity': 'critical'
    },
]

with open('/data/ground_truth/violations_gt.json', 'w') as f:
    json.dump(violations, f, indent=2)
```

---

## Part 5: OCR Testing Strategy

### Test Dataset Composition (100 invoices)

| Category | Count | Purpose | Format | Challenge |
|----------|-------|---------|--------|-----------|
| Clean PDFs | 30 | Baseline OCR | Native PDF | Low noise |
| Clean Images | 20 | Standard JPG | JPG (200 DPI) | Moderate |
| Blurred Scans | 15 | OCR robustness | Gaussian blur | High noise |
| Rotated/Skewed | 15 | Geometric OCR | ±15° rotation | Preprocessing challenge |
| Low Contrast | 10 | Dark/faded scans | Low DPI, faded | Thresholding challenge |
| Handwritten | 10 | Vision LLM fallback | Mixed typed/handwritten | NLP challenge |

### OCR Comparison Methodology
```python
# Week 1: Compare OCR engines
import pytesseract
from easyocr import Reader

def compare_ocr_engines(image_path):
    """Benchmark Tesseract vs. EasyOCR"""
    
    # Tesseract
    tesseract_text = pytesseract.image_to_string(image_path)
    
    # EasyOCR
    reader = Reader(['en'])
    easyocr_results = reader.readtext(image_path)
    easyocr_text = '\n'.join([result[1] for result in easyocr_results])
    
    # Measure character error rate (CER)
    # CER = (insertions + deletions + substitutions) / reference_length
    
    return {
        'tesseract_text': tesseract_text,
        'easyocr_text': easyocr_text,
        'tesseract_confidence': pytesseract.image_to_pdf_or_hocr(image_path, lang='eng'),
        'ensemble_confidence': compute_alignment(tesseract_text, easyocr_text)
    }
```

---

## Part 6: Setup Instructions

### Download & Organize SROIE Dataset
```bash
# 1. Download SROIE
cd /Users/sam/Downloads/DocuMind/DocuMind/data
git clone https://github.com/SROIE/SROIE2019.git

# 2. Extract invoices (receipts)
cp -r SROIE2019/0325updated.task1train\(626p\)/ ./sroie_receipts/

# 3. Create invoice ground truth from SROIE
# SROIE images can be used as reference for real-world invoice formatting
```

### Generate Synthetic Invoices
```bash
# Install dependencies
pip install Pillow opencv-python numpy

# Run generation script (see Option 2 above)
python scripts/generate_invoices.py --count 50 --output_dir /data/invoices/
```

### Extract CUAD to Usable Format
```bash
# Run extraction script (see Part 4 above)
python scripts/extract_cuad.py \
    --input /data/raw_json/CUADv1.json \
    --output /data/contracts/cuad/
```

---

## Summary: What You Have & What You Need

| Component | Status | Location | Use Case |
|-----------|--------|----------|----------|
| **Contracts (510)** | ✅ Ready | `/data/CUADv1.json` | Knowledge base for validation & RAG |
| **Invoice Images** | ❌ Need to get | SROIE or synthetic | OCR testing, extraction training |
| **Degraded Invoices** | ❌ Need to generate | Synthetic pipeline | Robustness testing |
| **Ground Truth** | ✅ Partial (CUAD Q&A) | CUADv1.json | Training extraction models |
| **Violations Dataset** | ❌ Need to create | Synthetic | Validation testing (Week 2) |
| **Demo Dataset** | ✅ Partial (10 contracts) | CUAD subset | Live demo (Week 3) |

---

## Implementation Timeline

| Timeline | Task | Dataset | Output |
|----------|------|---------|--------|
| **NOW** | Download SROIE (626) + CORD (900) | Real invoice images | `/data/sroie_receipts/`, `/data/cord_receipts/` |
| **NOW** | Extract CUAD to individual files | 408 train + 102 test | `/contracts/cuad/training/`, `/contracts/cuad/test/` |
| **Week 1** | Extract SROIE/CORD OCR ground truth | SROIE + CORD | OCR baseline comparisons |
| **Week 1** | Generate 50 synthetic invoices (clean) | Synthetic | `/data/invoices/clean/` |
| **Week 1** | Create degraded versions (blur, rotation, noise) | Synthetic | `/data/invoices/degraded/` |
| **Week 2** | Create violation-seeded invoices | Synthetic + CUAD pairing | `/data/invoices/violations/` |
| **Week 3** | Integration testing (invoice vs. contract) | Mix of all above | Demo dataset ready |
| **Week 4** | Final evaluation dataset | Clean + degraded + violations | Evaluation suite runs |

## Next Steps

**Immediate (Do Today):**
```bash
cd /Users/sam/Downloads/DocuMind/DocuMind/data/

# 1. Download real invoice datasets
git clone https://github.com/SROIE/SROIE2019.git sroie_data
git clone https://github.com/clovaai/cord.git cord_data

# 2. Organize
mkdir -p invoices_real/sroie invoices_real/cord
cp -r sroie_data/0325updated.task1train\(626p\)/* invoices_real/sroie/
cp -r cord_data/data/all/* invoices_real/cord/

# 3. Extract CUAD
python ../scripts/extract_cuad.py --train train_separate_questions.json --test test.json --output ../contracts/cuad
```

**Week 1:**
1. Run extract_cuad.py script
2. Download SROIE + CORD datasets  
3. Run OCR comparison on SROIE images (Tesseract vs. EasyOCR)
4. Generate 50 synthetic clean invoices
5. Create 20 degraded versions per synthetic invoice

**Week 2:**
1. Create violation dataset (term mismatches, price violations)
2. Pair invoices with CUAD contracts
3. Build validation rules

**Week 3:**
1. Use complete mixed dataset for integration testing
2. Run contract-aware validation demo

**Week 4:**
1. Full evaluation: OCR + extraction + retrieval + validation
2. Measure accuracy, precision, recall across all datasets
