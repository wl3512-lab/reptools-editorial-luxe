#!/usr/bin/env python3
"""Verify that all modified Jinja2 templates compile without syntax errors."""

import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError

# Template files to check
TEMPLATES_TO_VERIFY = [
    'home.html',
    'products.html',
    'tools.html',
    'order.html',
    'measurements.html',
    'contact.html',
    'tutorial.html',
    'privacy.html',
    'terms.html',
]

def verify_templates():
    """Load and compile each template."""
    template_dir = Path(__file__).parent / 'templates'

    # Create Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(template_dir)))

    results = {}
    failed = []

    for template_name in TEMPLATES_TO_VERIFY:
        template_path = template_dir / template_name

        if not template_path.exists():
            results[template_name] = f"SKIP (file not found: {template_path})"
            continue

        try:
            # This triggers template parsing/compilation
            env.get_template(template_name)
            results[template_name] = "PASS"
        except TemplateSyntaxError as e:
            results[template_name] = f"FAIL: {e.message} (line {e.lineno})"
            failed.append(template_name)
        except Exception as e:
            results[template_name] = f"ERROR: {str(e)}"
            failed.append(template_name)

    # Print results
    print("\n" + "="*70)
    print("JINJA2 TEMPLATE COMPILATION VERIFICATION")
    print("="*70 + "\n")

    for template_name in TEMPLATES_TO_VERIFY:
        status = results.get(template_name, "UNKNOWN")
        symbol = "✓" if status == "PASS" else "✗" if "FAIL" in status or "ERROR" in status else "○"
        print(f"{symbol} {template_name:30} {status}")

    print("\n" + "="*70)
    if failed:
        print(f"RESULT: {len(failed)} template(s) failed to compile")
        print("="*70)
        return 1
    else:
        print(f"RESULT: All {len(TEMPLATES_TO_VERIFY)} templates compiled successfully")
        print("="*70)
        return 0

if __name__ == '__main__':
    sys.exit(verify_templates())
