#!/usr/bin/env python3
"""
Quick domain scanner - identifies domains and their state WITHOUT modification.
"""
import os
from pathlib import Path
from collections import defaultdict

def scan_domains(repo_root="."):
    """Scan all technical domains and report their state."""
    technical_root = Path(repo_root) / "01_Concepts" / "01_Technical"
    
    if not technical_root.exists():
        print(f"❌ Technical root not found: {technical_root}")
        return {}
    
    domains = {}
    
    for domain_dir in sorted(technical_root.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith('.'):
            continue
        
        domain_name = domain_dir.name
        md_files = list(domain_dir.rglob("*.md"))
        
        # Categorize files
        empty = 0
        meaningful = 0
        placeholder = 0
        index = 0
        other = 0
        
        file_list = []
        
        for md_file in md_files:
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
                rel_path = md_file.relative_to(domain_dir)
                
                if len(content.strip()) == 0:
                    empty += 1
                    category = "empty"
                elif ("00_Chapter_Index" in md_file.name or 
                      "README" in md_file.name or
                      "index" in md_file.name.lower()):
                    index += 1
                    category = "index"
                elif len(content.split('\n')) < 10 or "TODO" in content or "placeholder" in content.lower():
                    placeholder += 1
                    category = "placeholder"
                else:
                    meaningful += 1
                    category = "meaningful"
                
                file_list.append({
                    "path": str(rel_path),
                    "category": category,
                    "size": md_file.stat().st_size,
                })
            except Exception as e:
                other += 1
        
        domains[domain_name] = {
            "path": f"01_Concepts/01_Technical/{domain_name}",
            "total_files": len(md_files),
            "empty": empty,
            "placeholder": placeholder,
            "meaningful": meaningful,
            "index": index,
            "other": other,
            "files": file_list,
        }
    
    return domains


if __name__ == "__main__":
    import sys
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print("\n" + "="*80)
    print("DOMAIN INVENTORY SCAN")
    print("="*80)
    
    domains = scan_domains(repo_root)
    
    # Report by domain
    processed = set()  # Assume 01_C was processed
    processed.add("01_C")
    
    print(f"\n✅ PROCESSED: {', '.join(sorted(processed))}")
    
    print(f"\n📊 UNPROCESSED DOMAINS:\n")
    
    unprocessed = [(name, info) for name, info in sorted(domains.items()) 
                   if name not in processed]
    
    for idx, (domain_name, info) in enumerate(unprocessed, 1):
        print(f"{idx}. {domain_name}")
        print(f"   Path: {info['path']}")
        print(f"   Files: {info['total_files']} (meaningful: {info['meaningful']}, "
              f"placeholder: {info['placeholder']}, empty: {info['empty']}, "
              f"index: {info['index']})")
        
        # Show sample meaningful files
        meaningful_files = [f for f in info['files'] if f['category'] == 'meaningful']
        if meaningful_files:
            print(f"   Sample content: {', '.join(f['path'] for f in meaningful_files[:3])}")
        
        print()

