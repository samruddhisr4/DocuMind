#!/usr/bin/env python3
"""
Generate synthetic invoices with optional degradation for OCR testing.
Creates both clean and degraded (blur, rotation, noise) versions.
"""

import random
import json
from pathlib import Path
from datetime import datetime, timedelta

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    import numpy as np
except ImportError:
    print("Error: PIL and numpy are required. Install with: pip install Pillow numpy")
    exit(1)


class InvoiceGenerator:
    """Generate synthetic invoice images with optional degradation."""

    def __init__(self, width=800, height=1050):
        self.width = width
        self.height = height
        self.vendors = [
            "Acme Corp", "TechVendor Inc", "Global Supplies Ltd",
            "FastShip Solutions", "Premium Services Co", "Office Materials Ltd"
        ]
        self.items = [
            ("Widget Pack", (10, 500)),
            ("Gadget Kit", (50, 1000)),
            ("Service Hours", (100, 2000)),
            ("Consulting", (500, 5000)),
            ("License Fee", (1000, 10000)),
            ("Support Package", (200, 2000)),
        ]

    def generate(self, invoice_id, vendor_idx=None, include_violation=None):
        """
        Generate a clean invoice image.

        Args:
            invoice_id: Unique invoice ID
            vendor_idx: Which vendor to use (random if None)
            include_violation: Type of violation to include ('term', 'price', None)
        """
        vendor = self.vendors[vendor_idx or random.randint(0, len(self.vendors)-1)]

        img = Image.new('RGB', (self.width, self.height), color='white')
        draw = ImageDraw.Draw(img)

        y = 50
        line_height = 40

        # Header
        draw.text((50, y), "INVOICE", fill='black', font=None)
        y += int(line_height * 1.5)

        # Invoice details
        invoice_date = datetime.now() - timedelta(days=random.randint(1, 30))
        invoice_num = f"INV-2024-{invoice_id:05d}"

        draw.text((50, y), f"Invoice #: {invoice_num}", fill='black')
        y += line_height
        draw.text((50, y), f"Date: {invoice_date.strftime('%Y-%m-%d')}", fill='black')
        y += line_height
        draw.text((50, y), f"Vendor: {vendor}", fill='black')
        y += line_height
        draw.text((50, y), f"Bill To: Acme Buyer Inc", fill='black')
        y += int(line_height * 1.5)

        # Line items
        draw.text((50, y), "ITEMS:", fill='black')
        y += line_height

        total = 0
        num_items = random.randint(2, 4)

        for _ in range(num_items):
            item_name, (min_qty, max_qty) = random.choice(self.items)
            qty = random.randint(1, 5)
            unit_price = random.randint(min_qty, max_qty)
            amount = qty * unit_price
            total += amount

            draw.text((70, y), f"{item_name} - Qty: {qty} @ ${unit_price}: ${amount}", fill='black')
            y += line_height

        # Payment terms
        y += line_height
        payment_term = "Net-45"
        if include_violation == 'term':
            payment_term = "Net-15"

        draw.text((50, y), f"Payment Terms: {payment_term}", fill='black')
        y += line_height
        draw.text((50, y), f"Due Date: {(invoice_date + timedelta(days=45)).strftime('%Y-%m-%d')}", fill='black')
        y += int(line_height * 1.5)

        # Total
        total_to_show = total
        if include_violation == 'price':
            total_to_show = int(total * 1.5)

        draw.text((50, y), f"TOTAL: ${total_to_show}", fill='black', font=None)

        # Footer
        y = self.height - 100
        draw.text((50, y), "Thank you for your business!", fill='gray')
        y += line_height
        draw.text((50, y), "Contact: vendor@example.com", fill='gray')

        return img, {
            'invoice_id': invoice_id,
            'invoice_number': invoice_num,
            'vendor': vendor,
            'date': invoice_date.strftime('%Y-%m-%d'),
            'total': total if include_violation != 'price' else int(total * 1.5),
            'payment_term': payment_term,
            'violation': include_violation,
        }

    def apply_degradation(self, image, degradation_type='blur'):
        """Apply degradation to simulate poor scans."""
        if degradation_type == 'blur':
            return image.filter(ImageFilter.GaussianBlur(radius=2))

        elif degradation_type == 'rotation':
            angle = random.randint(-10, 10)
            return image.rotate(angle, expand=True, fillcolor='white')

        elif degradation_type == 'lowcontrast':
            enhancer = ImageEnhance.Contrast(image)
            return enhancer.enhance(0.6)

        elif degradation_type == 'noise':
            arr = np.array(image, dtype=np.float32)
            noise_factor = 0.05
            random_noise = np.random.random(arr.shape)

            arr[random_noise < noise_factor/2] = 255
            arr[random_noise > 1 - noise_factor/2] = 0

            return Image.fromarray(arr.astype('uint8'))

        elif degradation_type == 'faded':
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(0.8)
            enhancer = ImageEnhance.Contrast(image)
            return enhancer.enhance(0.7)

        return image


def generate_invoice_dataset(output_dir, num_invoices=100, degradations=None):
    """
    Generate a complete invoice test dataset.

    Args:
        output_dir: Output directory for invoices
        num_invoices: Total number of invoices to generate
        degradations: List of degradation types to apply
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / 'clean').mkdir(exist_ok=True)
    (output_dir / 'degraded').mkdir(exist_ok=True)
    (output_dir / 'violations').mkdir(exist_ok=True)

    degradations = degradations or ['blur', 'rotation', 'noise', 'lowcontrast']

    print("=" * 80)
    print("GENERATING SYNTHETIC INVOICES")
    print("=" * 80)

    generator = InvoiceGenerator()
    ground_truth = []

    num_clean = int(num_invoices * 0.70)
    num_degraded = int(num_invoices * 0.20)
    num_violations = num_invoices - num_clean - num_degraded

    print(f"\nGenerating {num_invoices} invoices:")
    print(f"  Clean: {num_clean} (no OCR challenges)")
    print(f"  Degraded: {num_degraded} (blur, rotation, noise)")
    print(f"  Violations: {num_violations} (intentional compliance issues)")

    # Generate clean invoices
    print(f"\nGenerating clean invoices...")
    for i in range(num_clean):
        img, metadata = generator.generate(i)
        img_path = output_dir / 'clean' / f'invoice_{i:04d}.jpg'
        img.save(img_path, 'JPEG', quality=95)

        metadata['file'] = str(img_path)
        metadata['category'] = 'clean'
        ground_truth.append(metadata)

        if (i + 1) % 25 == 0:
            print(f"  Generated {i + 1}/{num_clean}...")

    # Generate degraded invoices
    print(f"\nGenerating degraded invoices...")
    for i in range(num_degraded):
        invoice_id = num_clean + i
        img, metadata = generator.generate(invoice_id)

        for degradation in degradations:
            degraded_img = generator.apply_degradation(img, degradation)
            img_path = output_dir / 'degraded' / f'invoice_{invoice_id:04d}_{degradation}.jpg'
            degraded_img.save(img_path, 'JPEG', quality=95)

            meta_copy = metadata.copy()
            meta_copy['file'] = str(img_path)
            meta_copy['category'] = 'degraded'
            meta_copy['degradation'] = degradation
            ground_truth.append(meta_copy)

        if (i + 1) % 25 == 0:
            print(f"  Generated {i + 1}/{num_degraded}...")

    # Generate violation invoices
    print(f"\nGenerating violation invoices...")
    violation_types = ['term', 'price', 'term', 'price']

    for i in range(num_violations):
        invoice_id = num_clean + num_degraded + i
        violation_type = violation_types[i % len(violation_types)]

        img, metadata = generator.generate(invoice_id, include_violation=violation_type)
        img_path = output_dir / 'violations' / f'invoice_{invoice_id:04d}_{violation_type}_violation.jpg'
        img.save(img_path, 'JPEG', quality=95)

        metadata['file'] = str(img_path)
        metadata['category'] = 'violations'
        metadata['violation_type'] = violation_type
        ground_truth.append(metadata)

        if (i + 1) % 10 == 0:
            print(f"  Generated {i + 1}/{num_violations}...")

    # Save ground truth
    gt_path = output_dir / 'ground_truth.json'
    with open(gt_path, 'w') as f:
        json.dump(ground_truth, f, indent=2)

    print(f"\n✓ Successfully generated {len(ground_truth)} invoice images")
    print(f"  Clean: {output_dir}/clean")
    print(f"  Degraded: {output_dir}/degraded")
    print(f"  Violations: {output_dir}/violations")
    print(f"  Ground truth: {gt_path}")

    return ground_truth


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate synthetic invoices for OCR testing')
    parser.add_argument('--output', default='./data/invoices', help='Output directory')
    parser.add_argument('--count', type=int, default=100, help='Number of invoices to generate')
    parser.add_argument('--degradations', nargs='+',
                        default=['blur', 'rotation', 'noise', 'lowcontrast', 'faded'],
                        help='Types of degradation to apply')

    args = parser.parse_args()

    dataset = generate_invoice_dataset(args.output, args.count, args.degradations)

    print("\n" + "=" * 80)
    print("Done! Invoices ready for OCR testing and extraction training.")
    print("=" * 80)
