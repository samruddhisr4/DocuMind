# DocuMind: Intelligent Document Processing + Contract-Aware Knowledge Platform

A combined project plan built from Project 14 (Multi-Modal Document Processor) and Project 6 (RAG Pipeline with Hybrid Search).

## 1. The idea

Project 14 (document processor) turns messy documents into **structured data**. Project 6 (RAG) turns a document corpus into **answers with citations**. Built separately, they're two demos. Combined, each fixes the other's weakness, and that makes a system companies would actually pay for.

**One-line pitch:** *A pipeline that ingests scanned and digital business documents (invoices, contracts, POs), extracts and validates structured data, indexes everything into a hybrid search system, and uses the indexed contracts to automatically validate incoming invoices, with human review where confidence is low.*

## 2. Use case: accounts payable and contract compliance

**Scenario:** A mid-size company receives about 5,000 vendor invoices a month, as PDFs, phone photos, and scans. It also holds hundreds of vendor contracts and purchase orders. Today, AP clerks do three things by hand:

1. Type invoice data into the ERP.
2. Check whether the invoice matches the contract (agreed rates, payment terms, price caps).
3. Answer questions like "What's our termination notice period with Vendor X?" by digging through PDFs.

**What DocuMind does:**

- Extracts invoice fields (vendor, line items, totals, dates) with per-field confidence.
- Retrieves the relevant contract clauses for that vendor and checks the invoice against them. For example: "Invoice says Net-15, but contract §4.2 says Net-45."
- Auto-approves clean documents and routes uncertain ones to a reviewer who sees the evidence side by side.
- Lets anyone ask natural-language questions across all processed documents, with verified citations.

## 3. Why the combination is stronger

| Synergy | What it means | Why it's impressive |
| --- | --- | --- |
| **Contract-aware validation** | The RAG engine acts as a *tool* for the validation engine. Invoice checks pull real contract clauses instead of relying on hardcoded rules. | Real multi-component reasoning; this is the headline feature. |
| **Extracted fields become retrieval metadata** | Vendor, date, doc type, and amount are stored with every chunk, enabling filtered hybrid search ("termination clauses in contracts with Vendor X signed after 2024"). | Fixes the biggest weakness of plain RAG: no structure awareness. |
| **Query router** | Structured questions ("total spend with Vendor X in Q3?") go to SQL. Semantic questions ("what are the indemnity terms?") go to hybrid RAG. Mixed questions use both. | Shows real system design, not a single-path demo. |
| **Layout-aware citations** | OCR bounding boxes are kept on every chunk, so a citation like \[2\] highlights the exact region on the original page image. | Verifiable answers; great demo moment. |
| **Confidence propagation** | OCR confidence feeds chunk confidence, which feeds retrieval weighting, which feeds answer confidence. A shaky scan produces a visibly less confident answer. | End-to-end uncertainty handling, which most systems skip. |
| **Unified feedback loop** | A reviewer's correction updates the database, the search index, the few-shot examples, and the eval dataset. | One correction improves four things. |
| **Gated indexing** | Only approved (or explicitly flagged "unverified") documents reach the search index. | Prevents garbage-in, garbage-out in RAG. |

## 4. Goals

**Product goals**

- Process PDFs, images, and scans end to end with no manual steps for clean documents.
- Auto-approve at least 60–70% of documents with at least 95% field-level accuracy on approved ones.
- Catch seeded contract/invoice discrepancies with high recall.
- Answer cross-document questions with at least 90% faithfulness and citation accuracy.

**Portfolio goals**

- Produce concrete numbers for your resume: accuracy, auto-approval rate, faithfulness, hybrid vs. dense-only delta, and time saved per document.
- Show the full AI engineering stack: CV/OCR, LLM extraction, retrieval, evaluation, async systems, and UI.

## 5. Architecture

```
                        ┌──────────────────────────────┐
  Upload / API / Email ─►  Ingestion API (FastAPI)     │
                        └──────────────┬───────────────┘
                                       │ store raw file (MinIO/S3), enqueue
                                       ▼
                        ┌──────────────────────────────┐
                        │  Celery + Redis task queue   │
                        └──────────────┬───────────────┘
                                       ▼
  ┌─────────────── STAGE 1: PERCEPTION ────────────────────────────┐
  │ Format detect → native text (PyMuPDF) or OCR path             │
  │ Preprocess (deskew, denoise, binarize, upscale)               │
  │ Dual OCR (Tesseract + EasyOCR) → ensemble merge               │
  │ Vision-LLM fallback for handwriting / tables / low confidence │
  │ OUTPUT: pages → text blocks + bboxes + OCR confidence         │
  └───────────────────────────────┬────────────────────────────────┘
                                  ▼
  ┌─────────────── STAGE 2: UNDERSTANDING ─────────────────────────┐
  │ Doc-type classifier (invoice / contract / PO / other)         │
  │ Schema-driven extraction (instructor + Pydantic, few-shot)    │
  │ Chunk-and-merge for long docs, conflict flagging              │
  │ Per-field confidence (OCR conf + LLM conf + format + agreement)│
  └───────────────────────────────┬────────────────────────────────┘
                                  ▼
  ┌─────────────── STAGE 3: VALIDATION ────────────────────────────┐
  │ 3a Type validation (Pydantic, cross-field math)               │
  │ 3b Business rules (vendor list, ranges, standard terms)       │
  │ 3c Anomaly detection (historical outliers per vendor)         │
  │ 3d CONTRACT CHECK  ◄──── calls Retrieval Engine (Stage 5)     │
  │ Routing: auto-approve / fast review / detailed review         │
  └──────────────┬───────────────────────────────┬─────────────────┘
                 │ needs review                  │ approved
                 ▼                               ▼
     ┌─────────────────────┐        ┌──────────────────────────────┐
     │ STAGE 4: REVIEW UI  │        │ STAGE 5: KNOWLEDGE LAYER     │
     │ Side-by-side view,  │ fixes  │ Chunking (3 strategies)      │
     │ bbox highlights,    ├───────►│ Embeddings + keyword index   │
     │ inline edit, queue  │        │ Dedup, metadata from Stage 2 │
     └─────────────────────┘        └───────────────┬──────────────┘
                                                    ▼
  ┌─────────────── STAGE 6: QUERY & ANSWER ───────────────────────┐
  │ Query router (SQL / RAG / both)                               │
  │ Hybrid retrieval: dense + BM25 → RRF → metadata filters       │
  │ Cross-encoder rerank → grounded generation with [n] citations │
  │ Citation verification (LLM-as-judge) + answer confidence      │
  │ "I don't know" handling                                       │
  └───────────────────────────────┬────────────────────────────────┘
                                  ▼
  ┌─────────────── STAGE 7: FEEDBACK & ANALYTICS ─────────────────┐
  │ Correction log → few-shot updates, threshold tuning,          │
  │ eval set growth, dashboards (auto-approve rate, accuracy…)    │
  └───────────────────────────────────────────────────────────────┘
```

**Storage layout**

- **PostgreSQL:** documents, pages, extractions, field-level confidence, validation results, corrections, and users. Structured data lives here, so SQL questions are cheap.
- **pgvector** (or Qdrant) for dense vectors, plus Postgres full-text search or `rank_bm25` for the sparse side. Using Postgres for both keeps metadata filters and vector search in a single query, and avoids keeping two indexes in sync.
- **MinIO/S3:** original files, page images, and processed text.
- **Redis:** queue and cache.

## 6. Key components in detail

### Stage 1: Perception (from Project 14)

- Text-density check per page chooses native extraction or OCR.
- Both OCR engines run on scanned pages. A character-level alignment picks the higher-confidence reading per segment.
- Pages with low ensemble confidence go to a vision LLM that returns text with structure preserved.
- Every step is logged (which preprocessing helped, which engine won), which feeds the OCR comparison analytics.
- **Addition:** keep the bounding boxes. They power citations and field highlighting later.

### Stage 2: Understanding (from Project 14)

- Pydantic schemas for `Invoice`, `Contract`, `PurchaseOrder`, loaded from config so new types need no code changes.
- The prompt says "extract only what's present, never infer," with 2–3 few-shot examples per type.
- Long contracts are chunked by section, extracted per chunk, then merged. Conflicts are flagged with source locations.
- Per-field confidence is a weighted blend of exact-match score, LLM self-report, chunk agreement, and format validity.

### Stage 3: Validation, including the new contract check

- 3a–3c are straight from Project 14.
- **3d Contract check (the new part):**
  1. Look up the vendor's contracts via a metadata filter (`vendor_id`, `doc_type=contract`, active dates).
  2. Run targeted hybrid queries: "payment terms," "pricing schedule," "price cap," "late fees," "auto-renewal."
  3. An LLM compares the invoice fields to the retrieved clauses and returns structured findings: `{rule, status: ok | violation | unclear, evidence_chunk_ids, explanation}`.
  4. Those findings feed routing. A violation sends the document to detailed review, with the clause shown next to the invoice.

### Stage 5: Knowledge layer (from Project 6)

- Three switchable chunking strategies (fixed, structure-aware, semantic). Contracts benefit from clause-level chunking, which makes a good experiment.
- Each chunk carries: source doc, page, bbox, section heading, doc type, vendor, dates, OCR confidence, and approval status.
- Near-duplicate detection at cosine similarity above 0.95. This matters here because contract amendments repeat a lot of text.

### Stage 6: Query and answer (from Project 6)

- **Router:** an LLM classifies each question as structured, semantic, or hybrid, then dispatches it.
- **Retrieval:** dense plus BM25, fused with configurable-weight RRF, then metadata filters, then cross-encoder rerank of the top 20 down to 5.
- **Generation:** answers only from context, with `[n]` citations. Each citation resolves to doc, page, and a highlighted region.
- **Verification:** an LLM-as-judge checks each claim-citation pair, and the answer gets a composite confidence score (retrieval, citation coverage, completeness, plus OCR confidence of the cited chunks).
- Below the confidence threshold, the system says what it found, what it didn't, and which documents to check manually.

### Stage 4 and 7: Review and feedback

- Side-by-side review with confidence colors and keyboard shortcuts.
- Each edit logs the original value, the new value, the reviewer, and whether it was an extraction error or a validation false positive.
- **Corrections trigger:** an index update for the corrected chunk, a few-shot candidate, a threshold-tuning data point, and a new eval test case.

## 7. Tech stack

| Layer | Choice |
| --- | --- |
| Language / API | Python 3.11+, FastAPI |
| OCR | Tesseract + EasyOCR, OpenCV for preprocessing, PyMuPDF for native PDFs |
| LLMs | Claude or GPT-4o with vision, structured output via `instructor` + Pydantic |
| Embeddings / rerank | `text-embedding-3-small` (or an open model like bge), a cross-encoder such as `bge-reranker` |
| Data | PostgreSQL + pgvector, MinIO, Redis |
| Async | Celery |
| Frontend | Streamlit for speed, React if you want polish (the bbox highlighting is easier in React) |
| Observability | Structured logs and per-stage timing/cost tracking (Langfuse optional) |
| Deployment | Docker + docker-compose |

## 8. Evaluation, the part that sets it apart

Build three suites and run them on every change:

1. **Perception and extraction:** field-level precision/recall/F1 per doc type, plus OCR character error rate for each engine vs. the ensemble vs. vision fallback.
2. **Retrieval and answers:** a 50+ question golden set covering lookups, multi-hop, no-answer, ambiguous, and structured-vs-semantic questions. Metrics are correctness, faithfulness, retrieval relevance, and citation accuracy. Include the chunking-strategy comparison and hybrid vs. dense-only.
3. **End to end (the unique one):** generate synthetic contract and invoice pairs, then **seed known discrepancies** (wrong payment terms, price over the cap, expired contract). Measure how many the contract check catches, and the false-alarm rate.

**Data sources:** CUAD (contract clauses), SROIE and FUNSD (receipts and forms), and synthetic invoices that you generate and degrade with blur, skew, and noise to simulate bad scans. Synthetic data gives you ground truth for free.

## 9. Build plan (about 4 weeks)

| Week | Focus | Deliverable |
| --- | --- | --- |
| **1** | Perception and schemas: loader, preprocessing, dual OCR, vision fallback, Pydantic schemas, extraction with confidence | Upload a scan and get structured JSON plus bboxes |
| **2** | Validation and knowledge layer: validation rules, anomaly detection, routing, chunking, hybrid index, rerank | Approved docs searchable with hybrid retrieval |
| **3** | Integration: contract-aware validation, query router, cited answers with verification, review UI | The headline demo flow works end to end |
| **4** | Feedback, evals, analytics, Docker, polish, demo | Numbers in hand, one-command setup, recorded walkthrough |

**Rule of thumb:** build the full vertical slice for one document type (invoices plus contracts for one vendor) before widening. A working end-to-end path beats ten half-built features.

## 10. Demo script (under 4 minutes)

1. Upload a skewed, noisy invoice photo and watch OCR and extraction run.
2. A validation banner appears: **"Payment terms Net-15 conflict with Contract §4.2 (Net-45)."** The clause is shown side by side, with the PDF region highlighted.
3. The reviewer fixes a low-confidence field, and the correction is logged.
4. Ask: "Which vendors have auto-renewal clauses expiring this year, and what did we pay them last quarter?" The router uses SQL plus RAG, and the answer comes back with verified citations.
5. Show the analytics dashboard: auto-approval rate, accuracy by field, and hybrid vs. dense-only.

## 11. Resume narrative

> "Built an end-to-end document intelligence platform that ingests scanned invoices and contracts, extracts structured data at **X% field-level F1**, validates invoices against contract clauses retrieved through hybrid search (catching **Y%** of seeded discrepancies), and auto-approves **Z%** of documents without human review. The RAG layer achieves **A% faithfulness** and **B% citation accuracy** on a 50-question eval suite, and a feedback loop turns every reviewer correction into improved prompts, thresholds, and test cases."

## 12. Risks and stretch goals

**Risks to manage**

- *Scope creep:* limit v1 to three doc types and one vendor family.
- *LLM cost:* cache results, use the vision fallback only on low-confidence pages, and track cost per document as a metric.
- *Eval leakage:* keep the golden set separate from few-shot examples.
- *PII:* mention redaction and access control in your write-up, even if you only implement a basic version.

**Stretch goals**

- Three-way match (invoice vs. PO vs. goods receipt).
- ERP export (CSV or a mock API).
- Email-inbox ingestion.
- Active learning: prioritize review of the documents the model is least sure about.
- Multi-language OCR.
