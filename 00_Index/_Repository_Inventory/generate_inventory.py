#!/usr/bin/env python3
"""
Repository Inventory Generator for curriculum-vault

Performs a comprehensive, programmatic analysis of the repository structure.
Generates:
  - inventory.json: Machine-readable inventory data
  - inventory_summary.md: Human-readable summary report
  - curriculum_map.md: Actual curriculum hierarchy
  - analysis_stats.csv: Key statistics
  - broken_links.json: Broken wikilink analysis
  - duplicate_candidates.json: Potential duplicate topics
"""

import os
import json
import csv
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class RepositoryInventory:
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.stats = {
            "total_files": 0,
            "total_directories": 0,
            "total_markdown_files": 0,
            "empty_markdown_files": 0,
            "small_placeholder_files": 0,
            "meaningful_content_files": 0,
            "template_only_files": 0,
        }
        self.markdown_files = []
        self.directory_structure = defaultdict(list)
        self.all_wikilinks = set()
        self.broken_wikilinks = []
        self.potential_duplicates = defaultdict(list)
        self.files_by_directory = defaultdict(int)
        self.orphaned_notes = []
        
    def analyze(self):
        """Run full analysis pipeline."""
        print("🔍 Starting repository inventory analysis...")
        self._walk_repository()
        self._analyze_markdown_files()
        self._check_wikilinks()
        self._detect_duplicates()
        self._detect_orphans()
        print("✅ Analysis complete")
        
    def _walk_repository(self):
        """Walk repository and collect file/directory stats."""
        print("  📁 Walking repository structure...")
        for root, dirs, files in os.walk(self.repo_root):
            # Skip hidden dirs and vendor/generated content
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            rel_root = Path(root).relative_to(self.repo_root)
            if str(rel_root) != '.':
                self.stats["total_directories"] += 1
            
            for file in files:
                if file.startswith('.'):
                    continue
                self.stats["total_files"] += 1
                file_path = Path(root) / file
                self.files_by_directory[str(rel_root)] += 1
                
                if file.endswith('.md'):
                    self.stats["total_markdown_files"] += 1
                    self.markdown_files.append({
                        "path": str(file_path.relative_to(self.repo_root)),
                        "size": file_path.stat().st_size,
                        "name": file,
                    })
                    
    def _analyze_markdown_files(self):
        """Analyze content of each Markdown file."""
        print("  📝 Analyzing Markdown file contents...")
        for file_info in self.markdown_files:
            path = self.repo_root / file_info["path"]
            
            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
                file_info["lines"] = len(content.split('\n'))
                file_info["is_empty"] = len(content.strip()) == 0
                
                if file_info["is_empty"]:
                    self.stats["empty_markdown_files"] += 1
                    file_info["category"] = "empty"
                elif file_info["size"] < 200:
                    self.stats["small_placeholder_files"] += 1
                    file_info["category"] = "small_placeholder"
                elif self._is_template_only(content):
                    self.stats["template_only_files"] += 1
                    file_info["category"] = "template_only"
                else:
                    self.stats["meaningful_content_files"] += 1
                    file_info["category"] = "meaningful"
                    
                # Extract wikilinks
                wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
                file_info["wikilinks"] = wikilinks
                self.all_wikilinks.update(wikilinks)
                
            except Exception as e:
                file_info["error"] = str(e)
                
    def _is_template_only(self, content: str) -> bool:
        """Check if file contains only template text/headings."""
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        # Filter out headings, whitespace, basic template text
        meaningful_lines = [l for l in lines if not (
            l.startswith('#') or
            l in ['---', '~~~', '```'] or
            l.lower() in ['todo', 'wip', 'placeholder', 'to be filled', 'under construction']
        )]
        return len(meaningful_lines) < 3
        
    def _check_wikilinks(self):
        """Validate wikilinks point to real files."""
        print("  🔗 Checking wikilink validity...")
        
        # Build set of valid note names (without .md)
        valid_notes = set()
        for file_info in self.markdown_files:
            # Extract filename without extension
            name = Path(file_info["path"]).stem
            valid_notes.add(name)
            # Also add with domain prefix
            parts = Path(file_info["path"]).parts
            for i in range(len(parts) - 1):
                valid_notes.add(parts[-1].replace('.md', ''))
        
        # Check each wikilink
        for file_info in self.markdown_files:
            for link in file_info.get("wikilinks", []):
                link_target = link.split('|')[0].strip()  # Remove display text
                # Remove any path components for matching
                link_name = Path(link_target).stem
                
                if link_name not in valid_notes:
                    self.broken_wikilinks.append({
                        "source_file": file_info["path"],
                        "target": link_target,
                        "resolved_name": link_name,
                    })
                    
    def _detect_duplicates(self):
        """Find potential duplicate canonical topics."""
        print("  🔀 Detecting potential duplicates...")
        
        # Group files by simplified name
        name_groups = defaultdict(list)
        for file_info in self.markdown_files:
            # Extract meaningful name
            name = Path(file_info["path"]).stem
            # Normalize for grouping
            normalized = name.lower().replace('_', ' ').replace('-', ' ')
            name_groups[normalized].append(file_info["path"])
        
        # Find groups with multiple files
        for normalized, files in name_groups.items():
            if len(files) > 1:
                self.potential_duplicates[normalized] = files
                
    def _detect_orphans(self):
        """Find potentially orphaned substantive notes (not linked from anywhere)."""
        print("  🏝️  Detecting orphaned notes...")
        
        # Files that are linked to
        linked_files = set()
        for file_info in self.markdown_files:
            for link in file_info.get("wikilinks", []):
                linked_files.add(link.split('|')[0].strip())
        
        # Find substantive files that aren't linked and aren't index/README
        for file_info in self.markdown_files:
            if file_info.get("category") == "meaningful":
                name = Path(file_info["path"]).stem
                if (name not in linked_files and 
                    not name.endswith('Index') and 
                    not name.startswith('README') and
                    'inventory' not in file_info["path"].lower()):
                    self.orphaned_notes.append({
                        "path": file_info["path"],
                        "size": file_info["size"],
                        "lines": file_info.get("lines", 0),
                    })
    
    def export_json(self, output_path: str = "00_Index/_Repository_Inventory/inventory.json"):
        """Export inventory as JSON."""
        output_file = self.repo_root / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        inventory = {
            "metadata": {
                "repository": str(self.repo_root),
                "analysis_timestamp": __import__('datetime').datetime.now().isoformat(),
            },
            "statistics": self.stats,
            "files_by_directory": dict(self.files_by_directory),
            "markdown_files": self.markdown_files,
            "broken_wikilinks": self.broken_wikilinks,
            "potential_duplicates": dict(self.potential_duplicates),
            "orphaned_notes": self.orphaned_notes,
        }
        
        with open(output_file, 'w') as f:
            json.dump(inventory, f, indent=2)
        print(f"  ✅ Inventory saved to {output_path}")
        return inventory
    
    def export_summary_markdown(self, output_path: str = "00_Index/_Repository_Inventory/inventory_summary.md"):
        """Export human-readable summary."""
        output_file = self.repo_root / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        summary = f"""# Repository Inventory Summary

**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Overview

| Metric | Count |
|--------|-------|
| Total Files | {self.stats['total_files']} |
| Total Directories | {self.stats['total_directories']} |
| **Markdown Files** | **{self.stats['total_markdown_files']}** |
| Empty Markdown Files | {self.stats['empty_markdown_files']} |
| Small Placeholder Files (<200B) | {self.stats['small_placeholder_files']} |
| Template-Only Files | {self.stats['template_only_files']} |
| **Meaningful Content Files** | **{self.stats['meaningful_content_files']}** |

## File Categories

### Empty Files ({self.stats['empty_markdown_files']})
"""
        for file_info in self.markdown_files:
            if file_info.get("category") == "empty":
                summary += f"\n- `{file_info['path']}`"
        
        summary += f"\n\n### Small Placeholders ({self.stats['small_placeholder_files']})\n"
        for file_info in self.markdown_files:
            if file_info.get("category") == "small_placeholder":
                summary += f"\n- `{file_info['path']}` ({file_info['size']} bytes)"
        
        summary += f"\n\n### Template-Only Files ({self.stats['template_only_files']})\n"
        for file_info in self.markdown_files:
            if file_info.get("category") == "template_only":
                summary += f"\n- `{file_info['path']}`"
        
        summary += f"\n\n## Broken Wikilinks ({len(self.broken_wikilinks)})\n"
        for link_info in self.broken_wikilinks[:50]:  # First 50
            summary += f"\n- **Source:** `{link_info['source_file']}`"
            summary += f"\n  **Target:** `{link_info['target']}`"
        if len(self.broken_wikilinks) > 50:
            summary += f"\n\n... and {len(self.broken_wikilinks) - 50} more (see broken_links.json)"
        
        summary += f"\n\n## Potential Duplicates ({len(self.potential_duplicates)})\n"
        for normalized_name, files in sorted(self.potential_duplicates.items())[:20]:
            summary += f"\n### {normalized_name}\n"
            for file in files:
                summary += f"  - `{file}`\n"
        if len(self.potential_duplicates) > 20:
            summary += f"\n... and {len(self.potential_duplicates) - 20} more (see duplicate_candidates.json)"
        
        summary += f"\n\n## Orphaned Substantive Notes ({len(self.orphaned_notes)})\n"
        for note_info in sorted(self.orphaned_notes, key=lambda x: x['lines'], reverse=True)[:30]:
            summary += f"\n- `{note_info['path']}` ({note_info['lines']} lines, {note_info['size']} bytes)"
        if len(self.orphaned_notes) > 30:
            summary += f"\n\n... and {len(self.orphaned_notes) - 30} more (see inventory.json)"
        
        summary += f"\n\n## Top Directories by File Count\n"
        for dir_path, count in sorted(self.files_by_directory.items(), key=lambda x: x[1], reverse=True)[:20]:
            summary += f"\n- `{dir_path or '.'}`: {count} files"
        
        with open(output_file, 'w') as f:
            f.write(summary)
        print(f"  ✅ Summary saved to {output_path}")
    
    def export_curriculum_map(self, output_path: str = "00_Index/_Repository_Inventory/curriculum_map.md"):
        """Export curriculum hierarchy under 01_Concepts/01_Technical."""
        output_file = self.repo_root / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        technical_root = self.repo_root / "01_Concepts" / "01_Technical"
        
        curriculum_map = "# Curriculum Map: 01_Concepts/01_Technical\n\n"
        curriculum_map += "**Generated:** " + __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + "\n\n"
        curriculum_map += "## Domain Structure\n\n"
        
        # Walk technical directory
        if technical_root.exists():
            domains = sorted([d for d in technical_root.iterdir() if d.is_dir()])
            for domain in domains:
                domain_name = domain.name
                md_files = list(domain.glob("*.md"))
                
                curriculum_map += f"### {domain_name}\n"
                curriculum_map += f"- Files: {len(md_files)}\n"
                
                # List files in domain
                for md_file in sorted(md_files):
                    size = md_file.stat().st_size
                    curriculum_map += f"  - `{md_file.name}` ({size} bytes)\n"
                
                # Check for subdirectories
                subdirs = [d for d in domain.iterdir() if d.is_dir() and not d.name.startswith('.')]
                if subdirs:
                    curriculum_map += f"  - Subdirectories: {len(subdirs)}\n"
                    for subdir in sorted(subdirs)[:10]:
                        sub_files = list(subdir.glob("*.md"))
                        curriculum_map += f"    - `{subdir.name}/`: {len(sub_files)} files\n"
                    if len(subdirs) > 10:
                        curriculum_map += f"    - ... and {len(subdirs) - 10} more\n"
                
                curriculum_map += "\n"
        else:
            curriculum_map += "⚠️ **01_Concepts/01_Technical directory not found**\n"
        
        with open(output_file, 'w') as f:
            f.write(curriculum_map)
        print(f"  ✅ Curriculum map saved to {output_path}")
    
    def export_stats_csv(self, output_path: str = "00_Index/_Repository_Inventory/analysis_stats.csv"):
        """Export key statistics as CSV."""
        output_file = self.repo_root / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            for key, value in self.stats.items():
                writer.writerow([key.replace('_', ' ').title(), value])
            writer.writerow(["Broken Wikilinks", len(self.broken_wikilinks)])
            writer.writerow(["Potential Duplicates", len(self.potential_duplicates)])
            writer.writerow(["Orphaned Notes", len(self.orphaned_notes)])
        print(f"  ✅ Statistics saved to {output_path}")
    
    def export_broken_links_json(self, output_path: str = "00_Index/_Repository_Inventory/broken_links.json"):
        """Export broken links as JSON."""
        output_file = self.repo_root / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump({
                "total_broken": len(self.broken_wikilinks),
                "broken_links": self.broken_wikilinks,
            }, f, indent=2)
        print(f"  ✅ Broken links saved to {output_path}")
    
    def export_duplicates_json(self, output_path: str = "00_Index/_Repository_Inventory/duplicate_candidates.json"):
        """Export duplicate candidates as JSON."""
        output_file = self.repo_root / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump({
                "total_groups": len(self.potential_duplicates),
                "duplicates": dict(self.potential_duplicates),
            }, f, indent=2)
        print(f"  ✅ Duplicate candidates saved to {output_path}")


if __name__ == "__main__":
    import sys
    
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    inventory = RepositoryInventory(repo_root)
    inventory.analyze()
    
    # Export all formats
    inventory.export_json()
    inventory.export_summary_markdown()
    inventory.export_curriculum_map()
    inventory.export_stats_csv()
    inventory.export_broken_links_json()
    inventory.export_duplicates_json()
    
    print("\n📊 Inventory generation complete!")
    print(f"  Total files: {inventory.stats['total_files']}")
    print(f"  Markdown files: {inventory.stats['total_markdown_files']}")
    print(f"  Meaningful content: {inventory.stats['meaningful_content_files']}")
    print(f"  Broken wikilinks: {len(inventory.broken_wikilinks)}")
    print(f"  Potential duplicates: {len(inventory.potential_duplicates)}")
    print(f"  Orphaned notes: {len(inventory.orphaned_notes)}")
