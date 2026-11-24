#!/usr/bin/env python3
"""
Extract CUAD dataset from your existing train/test split.
Works with: train_separate_questions.json (408) + test.json (102)
"""

import json
from pathlib import Path


def extract_cuad_split(train_json, test_json, output_dir='./contracts/cuad'):
    """
    Extract already-split CUAD contracts to individual text files.

    Args:
        train_json: Path to train_separate_questions.json (408 contracts)
        test_json: Path to test.json (102 contracts)
        output_dir: Output directory for extracted contracts
    """
    output_dir = Path(output_dir)
    training_dir = output_dir / 'training'
    test_dir = output_dir / 'test'

    # Create directories
    training_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("EXTRACTING CUAD DATASET (Train/Test Split)")
    print("=" * 80)

    # Load training data
    print(f"\nLoading training data from {train_json}...")
    with open(train_json, 'r') as f:
        train_data = json.load(f)

    train_contracts = train_data['data']
    print(f"Found {len(train_contracts)} training contracts")

    # Load test data
    print(f"Loading test data from {test_json}...")
    with open(test_json, 'r') as f:
        test_data = json.load(f)

    test_contracts = test_data['data']
    print(f"Found {len(test_contracts)} test contracts")

    # Extract training contracts
    print(f"\nExtracting training contracts...")
    for idx, contract in enumerate(train_contracts):
        _extract_single_contract(contract, idx, training_dir, 'train')
        if (idx + 1) % 50 == 0:
            print(f"  Extracted {idx + 1}/{len(train_contracts)}...")

    # Extract test contracts
    print(f"\nExtracting test contracts...")
    for idx, contract in enumerate(test_contracts):
        _extract_single_contract(contract, idx, test_dir, 'test')
        if (idx + 1) % 25 == 0:
            print(f"  Extracted {idx + 1}/{len(test_contracts)}...")

    print(f"\n✓ Successfully extracted all contracts")
    print(f"  Training: {training_dir} ({len(train_contracts)} contracts)")
    print(f"  Test: {test_dir} ({len(test_contracts)} contracts)")

    return {
        'training_count': len(train_contracts),
        'test_count': len(test_contracts),
        'output_dir': str(output_dir)
    }


def _extract_single_contract(contract, idx, output_dir, split):
    """Extract a single contract to files."""
    title = contract.get('title', f'contract_{idx:04d}')

    # Extract full text from paragraphs
    full_text_parts = []
    qa_data = []

    for para in contract.get('paragraphs', []):
        context = para.get('context', '')
        full_text_parts.append(context)

        # Collect Q&A pairs
        for qa in para.get('qas', []):
            qa_data.append({
                'question': qa.get('question'),
                'answer': qa.get('answers', [{}])[0].get('text') if qa.get('answers') else None,
            })

    full_text = '\n\n'.join(full_text_parts)

    # Save contract text
    contract_filename = f'contract_{idx:04d}.txt'
    contract_path = output_dir / contract_filename

    with open(contract_path, 'w', encoding='utf-8') as f:
        f.write(f"TITLE: {title}\n")
        f.write(f"INDEX: {idx} ({split})\n")
        f.write("=" * 80 + "\n\n")
        f.write(full_text)

    # Save metadata
    metadata_filename = f'contract_{idx:04d}_metadata.json'
    metadata_path = output_dir / metadata_filename

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump({
            'index': idx,
            'title': title,
            'split': split,
            'qa_count': len(qa_data),
            'text_length': len(full_text),
        }, f, indent=2)

    # Save Q&A pairs
    qa_filename = f'contract_{idx:04d}_qa.json'
    qa_path = output_dir / qa_filename

    with open(qa_path, 'w', encoding='utf-8') as f:
        json.dump(qa_data, f, indent=2)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Extract CUAD dataset (train/test split)')
    parser.add_argument('--train', default='./data/train_separate_questions.json', help='Training JSON file')
    parser.add_argument('--test', default='./data/test.json', help='Test JSON file')
    parser.add_argument('--output', default='./contracts/cuad', help='Output directory')

    args = parser.parse_args()

    result = extract_cuad_split(args.train, args.test, args.output)

    print("\n" + "=" * 80)
    print("Done! Contracts extracted and ready for use.")
    print("=" * 80)
