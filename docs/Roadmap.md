Let me provide you with the complete roadmap directly in this chat. The document artifact is ready for your team to edit and reference.

---

## **STEP-BY-STEP IMPLEMENTATION ROADMAP (4 Weeks)**

### **WEEK 1: Perception & Extraction Foundation**

**Goal:** Build the ability to process documents end-to-end, outputting structured JSON + bounding boxes

**Key deliverables:**
1. **Document loader** - accepts PDF, JPG, PNG from upload/API
2. **Preprocessing pipeline** - deskew, denoise, binarize, upscale using OpenCV
3. **Dual OCR system** - Tesseract + EasyOCR with character-level alignment and ensemble confidence
4. **Vision LLM fallback** - for low-confidence segments, handwriting, tables (use Claude with vision)
5. **Pydantic schemas** - define Invoice, Contract, PO data structures (configurable, no hardcoded types)
6. **Extraction with confidence** - use instructor library for structured extraction with per-field confidence blending OCR confidence + LLM self-report + format validity

**Output:** Upload a skewed invoice photo → get back:
```json
{
  "vendor_name": {"value": "Acme Corp", "confidence": 0.98, "source": "ocr"},
  "invoice_date": {"value": "2024-11-15", "confidence": 0.95},
  "total_amount": {"value": 5000.00, "confidence": 0.87},
  "bounding_boxes": [{page: 1, bbox: [0.1, 0.2, 0.9, 0.5], text: "..."}]
}
```

**Tech stack focus:** PyMuPDF, Tesseract, EasyOCR, OpenCV, instructor + Pydantic, Claude API

---

### **WEEK 2: Validation Logic & Knowledge Layer Setup**

**Goal:** Build the validation rules engine and hybrid search indexing

**Key deliverables:**
1. **Type validation** - Pydantic + cross-field math checks (invoice total = sum of line items)
2. **Business rules engine** - vendor list validation, amount ranges, standard terms checks
3. **Anomaly detection** - flag invoices deviating from historical patterns per vendor
4. **Chunking strategies** - implement three approaches:
   - Fixed-size chunks (testing baseline)
   - Structure-aware chunks (sections + clauses)
   - Semantic chunks (break on topic shifts)
5. **Hybrid search indexing** - setup PostgreSQL + pgvector + BM25 for contracts
6. **Metadata extraction** - attach vendor, doc_type, approval_status, OCR_confidence to every chunk

**Output:** 
- Uploaded contracts are indexed and searchable
- Invoices pass basic validation rules
- System can run queries: "payment terms for Vendor X"

**Tech stack focus:** PostgreSQL, pgvector, text-embedding-3-small, instructor library, Redis for caching

---

### **WEEK 3: Integration - The Headline Feature**

**Goal:** Wire contract-aware validation + create end-to-end flow

**Key deliverables:**
1. **Contract check (Stage 3d)** - for each invoice:
   - Look up vendor's contracts via metadata filter
   - Run hybrid queries for: "payment terms", "pricing schedule", "price cap", "late fees", "auto-renewal"
   - LLM compares invoice fields to retrieved clauses → structured findings: `{rule, status: ok|violation|unclear, evidence_chunk_ids}`
   - Route based on findings: clean → auto-approve, violation → detailed review

2. **Query router** - LLM classifies questions:
   - Structured ("total spend with Vendor X in Q3?") → SQL
   - Semantic ("what are indemnity terms?") → RAG
   - Hybrid → both

3. **Cited answers** - retrieval + reranking + grounded generation with `[n]` citations
   - Citation verification: LLM-as-judge checks claim-to-citation fidelity
   - Answer confidence score (retrieval quality + citation coverage + completeness + OCR confidence)

4. **Review UI** (Streamlit MVP) - side-by-side invoice + contract view with:
   - Confidence color coding
   - Bbox highlighting on PDFs
   - Inline edit capability
   - Keyboard shortcuts for approve/reject

5. **Feedback logging** - capture: original value → new value, reviewer, error type

**Output:** End-to-end demo:
1. Upload skewed invoice photo
2. See validation banner: "Payment terms Net-15 conflict with Contract §4.2 (Net-45)" [highlighted PDF region]
3. Reviewer corrects low-confidence field → logged
4. Ask: "Which vendors have auto-renewal clauses expiring this year?"
5. Get answer with verified citations

**Tech stack focus:** FastAPI, Claude API (vision + structured output), Streamlit (or React for polish), Celery for async processing

---

### **WEEK 4: Evaluation, Analytics, Deployment, Polish**

**Goal:** Measure performance, automate setup, finalize demo

**Key deliverables:**
1. **Three evaluation suites:**
   - **Perception**: OCR CER (character error rate) per engine + ensemble, extraction F1 per field per doc type
   - **Retrieval & answers**: 50+ question golden set (lookups, multi-hop, no-answer, structured vs. semantic) → correctness, faithfulness, citation accuracy, chunking-strategy delta
   - **End-to-end**: Synthetic invoice-contract pairs with **seeded violations** (10–20% contain intentional discrepancies) → measure detection recall, false-alarm rate

2. **Dataset assembly:**
   - **Contracts**: 5–10 from CUAD + synthetic variations
   - **Invoices**: 70% clean, 10% term violations, 10% price violations, 10% expired contracts
   - **Degradation**: apply blur, rotation, noise to simulate bad scans

3. **Analytics dashboard** - charts for:
   - Auto-approval rate + accuracy
   - Accuracy by field + vendor
   - Hybrid vs. dense-only retrieval delta
   - Cost per document
   - Processing time per stage

4. **Docker + compose** - single `docker-compose up` to spin up: PostgreSQL, pgvector, MinIO, Redis, Celery, FastAPI, Streamlit

5. **Demo script recording** (< 4 min) - walking through the full scenario

6. **Resume narrative** - quantified metrics (X% F1, Y% violation catch rate, Z% auto-approval, A% faithfulness)

---

## **Success Metrics (Targets)**

| Metric | Target | Why |
|--------|--------|-----|
| **Extraction accuracy (field-level F1)** | ≥ 95% on approved invoices | Shows clean path is reliable |
| **Auto-approval rate** | 60–70% | Real-world feasible (rest go to review) |
| **Contract violation detection (recall)** | ≥ 90% | Must catch payment term + pricing mismatches |
| **False-alarm rate** | ≤ 5% | Don't send good invoices to review unnecessarily |
| **Retrieval faithfulness** | ≥ 90% | RAG answers must match contract intent |
| **Citation accuracy** | ≥ 90% | Citations must point to correct contract sections |
| **Hybrid vs. dense-only delta** | +15–25% F1 | Justify combining BM25 + embeddings |
| **Processing time per document** | < 30 sec (avg) | Practical for 5,000/month workload |

---

## **Why This Dataset Mix Matters for Your Portfolio**

**Invoices alone:** "Built invoice extraction with OCR"  
**Contracts + Invoices:** "Built contract-aware intelligent validation engine catching compliance violations, with hybrid search retrieval and LLM-grounded answers at 90%+ faithfulness"

The second narrative gets you interviews. The contracts provide:
- Complex extraction challenges (legal language, varied structure)
- Meaningful retrieval scenarios (hybrid search shows its worth)
- Realistic validation logic (contract compliance is a real, sticky problem)
- Seeded violations prove the system works (not just extracted data, but enforced rules)

---

**Your artifact is ready.** I've created a Claude Docs document where you can refine this roadmap with your team, add timelines, assign tasks, and track progress. The document link is at the top of this conversation.