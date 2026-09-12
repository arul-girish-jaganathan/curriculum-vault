#!/usr/bin/env python3
"""
Curriculum Maintenance Toolkit
================================

Core library for analyzing, validating, and maintaining the curriculum-vault repository.
Provides reusable functions for all maintenance operations.

Usage:
    from curriculum_tools import RepositoryAnalyzer
    analyzer = RepositoryAnalyzer("/path/to/curriculum-vault")
    analysis = analyzer.analyze()
    analyzer.export_reports()
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
import hashlib


class RepositoryAnalyzer:
    """Comprehensive curriculum repository analyzer."""
    
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.stats = {
            "analysis_timestamp": datetime.now().isoformat(),
            "repository_root": str(self.repo_root),
            "total_files": 0,
            "total_directories": 0,
            "total_markdown_files": 0,
            "empty_markdown_files": 0,
            "placeholder_files": 0,
            "meaningful_content_files": 0,
            "index_files": 0,
        }
        self.files = []
        self.wikilinks_found = []
        self.wikilinks_broken = []
        self.duplicate_candidates = defaultdict(list)
        self.orphaned_notes = []
        self.domains = {}
        self.file_hashes = {}
        
    def analyze(self) -> Dict:
        """Run complete analysis pipeline."""
        print("🔍 Starting comprehensive repository analysis...")
        self._walk_filesystem()
        self._analyze_markdown_content()
        self._extract_wikilinks()
        self._validate_wikilinks()
        self._detect_duplicates()
        self._detect_orphans()
        self._analyze_domains()
        print("✅ Analysis complete")
        return self._get_summary()
    
    def _walk_filesystem(self):
        """Walk and catalog all files."""
        print("  📁 Walking filesystem...")
        for root, dirs, files in os.walk(self.repo_root):
            # Skip hidden and generated directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            rel_root = Path(root).relative_to(self.repo_root)
            if str(rel_root) != '.':
                self.stats["total_directories"] += 1
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                self.stats["total_files"] += 1
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.repo_root)
                
                file_info = {
                    "path": str(rel_path),
                    "name": file,
                    "directory": str(Path(root).relative_to(self.repo_root)),
                    "size": file_path.stat().st_size,
                    "extension": file_path.suffix,
                }
                
                if file.endswith('.md'):
                    self.stats["total_markdown_files"] += 1
                    file_info["is_markdown"] = True
                else:
                    file_info["is_markdown"] = False
                
                self.files.append(file_info)
    
    def _analyze_markdown_content(self):
        """Analyze content of Markdown files."""
        print("  📝 Analyzing Markdown content...")
        for file_info in self.files:
            if not file_info.get("is_markdown"):
                continue
            
            path = self.repo_root / file_info["path"]
            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
                file_info["content_length"] = len(content)
                file_info["line_count"] = len(content.split('\n'))
                
                # Check if empty
                is_empty = len(content.strip()) == 0
                file_info["is_empty"] = is_empty
                if is_empty:
                    self.stats["empty_markdown_files"] += 1
                    file_info["category"] = "empty"
                    continue
                
                # Check if placeholder/template
                is_placeholder = self._is_placeholder(content, file_info["path"])
                if is_placeholder:
                    self.stats["placeholder_files"] += 1
                    file_info["category"] = "placeholder"
                else:
                    self.stats["meaningful_content_files"] += 1
                    file_info["category"] = "meaningful"
                
                # Check if index/navigation
                if self._is_index_file(file_info["name"], content):
                    self.stats["index_files"] += 1
                    file_info["is_index"] = True
                
                # Hash content for duplicate detection
                self.file_hashes[file_info["path"]] = hashlib.md5(content.encode()).hexdigest()
                
            except Exception as e:
                file_info["error"] = str(e)
    
    def _is_placeholder(self, content: str, path: str) -> bool:
        """Detect placeholder/template-only content."""
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        
        # Filter out structure-only lines
        meaningful = [l for l in lines if not (
            l.startswith('#') or
            l in ['---', '~~~', '```', '> '] or
            l.lower() in ['todo', 'wip', 'placeholder', 'under construction', 'to be filled'] or
            l.startswith('- ') and len(l) < 40  # Short bullet points
        )]
        
        # Very short content is placeholder
        if len(meaningful) < 5:
            return True
        
        # Check for common placeholder patterns
        placeholder_patterns = [
            r'TODO:|FIXME:|XXX:',
            r'\[placeholder\]|\[wip\]|\[draft\]',
            r'coming soon|not yet written|to be added'
        ]
        
        for pattern in placeholder_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _is_index_file(self, filename: str, content: str) -> bool:
        """Detect if file is an index/navigation file."""
        index_patterns = [
            'index', 'readme', 'chapter_index', 'topic_map', 
            'complete_topic_map', 'navigation', '_index'
        ]
        
        if any(pattern in filename.lower() for pattern in index_patterns):
            return True
        
        # Check content patterns
        if '[[' in content and ('Chapter' in content or 'Topic' in content):
            return True
        
        return False
    
    def _extract_wikilinks(self):
        """Extract all Obsidian wikilinks from Markdown files."""
        print("  🔗 Extracting wikilinks...")
        wikilink_pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
        
        for file_info in self.files:
            if not file_info.get("is_markdown"):
                continue
            
            path = self.repo_root / file_info["path"]
            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
                matches = re.findall(wikilink_pattern, content)
                
                if matches:
                    file_info["wikilinks"] = []
                    for target, display_text in matches:
                        link_info = {
                            "target": target.strip(),
                            "display_text": display_text.strip() if display_text else target.strip(),
                            "source_file": file_info["path"],
                        }
                        file_info["wikilinks"].append(link_info)
                        self.wikilinks_found.append(link_info)
            except Exception as e:
                file_info["wikilink_error"] = str(e)
    
    def _validate_wikilinks(self):
        """Check which wikilinks point to nonexistent files."""
        print("  ✔️  Validating wikilinks...")
        
        # Build set of valid note names
        valid_notes = set()
        for file_info in self.files:
            if file_info.get("is_markdown"):
                # Add stem (filename without extension)
                stem = Path(file_info["path"]).stem
                valid_notes.add(stem)
        
        # Check each wikilink
        for link in self.wikilinks_found:
            target = link["target"]
            # Extract target filename (remove path prefix if present)
            target_stem = Path(target).stem
            
            if target_stem not in valid_notes:
                self.wikilinks_broken.append({
                    "source_file": link["source_file"],
                    "target": target,
                    "target_stem": target_stem,
                })
    
    def _detect_duplicates(self):
        """Find potentially duplicate canonical topics."""
        print("  🔀 Detecting duplicates...")
        
        # Group by normalized name
        name_groups = defaultdict(list)
        for file_info in self.files:
            if not file_info.get("is_markdown") or file_info.get("is_empty"):
                continue
            
            stem = Path(file_info["path"]).stem
            # Normalize: lowercase, replace underscores/hyphens with spaces
            normalized = stem.lower().replace('_', ' ').replace('-', ' ')
            name_groups[normalized].append(file_info["path"])
        
        # Find groups with multiple files
        for normalized, paths in name_groups.items():
            if len(paths) > 1:
                self.duplicate_candidates[normalized] = paths
    
    def _detect_orphans(self):
        """Find substantive notes not linked from anywhere."""
        print("  🏝️  Detecting orphaned notes...")
        
        # Collect files that are linked to
        linked_files = set()
        for link in self.wikilinks_found:
            target_stem = Path(link["target"]).stem
            linked_files.add(target_stem)
        
        # Find meaningful files that aren't linked and aren't special
        special_files = {'readme', 'index', 'chapter_index', 'topic_map', 'coverage_audit', 'source_backbone'}
        
        for file_info in self.files:
            if not file_info.get("is_markdown"):
                continue
            if file_info.get("category") != "meaningful":
                continue
            
            stem = Path(file_info["path"]).stem
            if stem.lower() in special_files:
                continue
            if stem in linked_files:
                continue
            if 'inventory' in file_info["path"].lower():
                continue
            
            self.orphaned_notes.append({
                "path": file_info["path"],
                "size": file_info.get("size", 0),
                "lines": file_info.get("line_count", 0),
            })
    
    def _analyze_domains(self):
        """Analyze domain structure."""
        print("  🏗️  Analyzing domains...")
        
        # Identify domains (top-level directories under 01_Concepts/01_Technical)
        technical_root = self.repo_root / "01_Concepts" / "01_Technical"
        if technical_root.exists():
            for domain_dir in technical_root.iterdir():
                if domain_dir.is_dir() and not domain_dir.name.startswith('.'):
                    domain_name = domain_dir.name
                    md_files = list(domain_dir.rglob("*.md"))
                    
                    # Categorize files in this domain
                    domain_files = [f for f in self.files 
                                   if f["path"].startswith(f"01_Concepts/01_Technical/{domain_name}/")]
                    
                    self.domains[domain_name] = {
                        "file_count": len(domain_files),
                        "markdown_count": len([f for f in domain_files if f.get("is_markdown")]),
                        "empty_count": len([f for f in domain_files if f.get("is_empty")]),
                        "meaningful_count": len([f for f in domain_files if f.get("category") == "meaningful"]),
                        "placeholder_count": len([f for f in domain_files if f.get("category") == "placeholder"]),
                        "files": [f["path"] for f in domain_files],
                    }
    
    def _get_summary(self) -> Dict:
        """Get analysis summary."""
        return {
            "metadata": {
                "analysis_timestamp": self.stats["analysis_timestamp"],
                "repository_root": str(self.repo_root),
            },
            "statistics": self.stats,
            "wikilinks": {
                "total_found": len(self.wikilinks_found),
                "broken": len(self.wikilinks_broken),
                "broken_links": self.wikilinks_broken[:100],  # First 100
            },
            "duplicates": {
                "total_candidates": len(self.duplicate_candidates),
                "candidates": dict(self.duplicate_candidates),
            },
            "orphans": {
                "total": len(self.orphaned_notes),
                "notes": sorted(self.orphaned_notes, key=lambda x: x.get("lines", 0), reverse=True)[:50],
            },
            "domains": self.domains,
        }
    
    def export_json(self, output_path: str = "00_Index/_Repository_Inventory/curriculum_analysis.json") -> Path:
        """Export full analysis as JSON."""
        output_file = self.repo_root / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        summary = self._get_summary()
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"  ✅ Analysis exported to {output_path}")
        return output_file
    
    def export_broken_links_report(self, output_path: str = "00_Index/_Repository_Inventory/broken_wikilinks.md") -> Path:
        """Export broken wikilinks as Markdown report."""
        output_file = self.repo_root / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        report = f"""# Broken Wikilinks Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

**Total Broken Links:** {len(self.wikilinks_broken)}

## Broken Links by Source File

"""
        
        # Group by source file
        by_source = defaultdict(list)
        for link in self.wikilinks_broken:
            by_source[link["source_file"]].append(link)
        
        for source_file in sorted(by_source.keys()):
            links = by_source[source_file]
            report += f"\n### `{source_file}`\n\n"
            for link in links:
                report += f"- **Target:** `{link['target']}`\n"
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        print(f"  ✅ Broken links report exported to {output_path}")
        return output_file
    
    def export_summary_report(self, output_path: str = "00_Index/_Repository_Inventory/curriculum_status.md") -> Path:
        """Export human-readable summary report."""
        output_file = self.repo_root / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        s = self.stats
        
        report = f"""# Curriculum Repository Status Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Overview Statistics

| Metric | Count |
|--------|-------|
| Total Files | {s['total_files']} |
| Total Directories | {s['total_directories']} |
| **Markdown Files** | **{s['total_markdown_files']}** |
| Empty Markdown Files | {s['empty_markdown_files']} |
| Placeholder Files | {s['placeholder_files']} |
| **Meaningful Content Files** | **{s['meaningful_content_files']}** |
| Index/Navigation Files | {s['index_files']} |

## Quality Metrics

- **Broken Wikilinks:** {len(self.wikilinks_broken)} / {len(self.wikilinks_found)}
- **Orphaned Notes:** {len(self.orphaned_notes)} meaningful files without incoming links
- **Duplicate Candidates:** {len(self.duplicate_candidates)} potential duplicates

## Domain Coverage

"""
        
        if self.domains:
            report += "\n### Technical Domains (01_Concepts/01_Technical)\n\n"
            report += "| Domain | Files | Markdown | Meaningful | Placeholder | Empty |\n"
            report += "|--------|-------|----------|------------|-------------|-------|\n"
            
            for domain_name in sorted(self.domains.keys()):
                d = self.domains[domain_name]
                report += f"| `{domain_name}` | {d['file_count']} | {d['markdown_count']} | {d['meaningful_count']} | {d['placeholder_count']} | {d['empty_count']} |\n"
        
        report += f"\n## Observations\n\n"
        if s['meaningful_content_files'] == 0:
            report += "- ⚠️ **No meaningful content yet** — repository is in skeleton phase\n"
        else:
            coverage_pct = (s['meaningful_content_files'] / max(s['total_markdown_files'], 1)) * 100
            report += f"- ℹ️ **Content coverage:** ~{coverage_pct:.1f}% of Markdown files contain meaningful content\n"
        
        if len(self.wikilinks_broken) > 0:
            pct = (len(self.wikilinks_broken) / len(self.wikilinks_found)) * 100 if self.wikilinks_found else 0
            report += f"- ⚠️ **Broken wikilinks:** {len(self.wikilinks_broken)} ({pct:.1f}% of {len(self.wikilinks_found)} total)\n"
        
        if len(self.duplicate_candidates) > 0:
            report += f"- ℹ️ **Potential duplicates:** {len(self.duplicate_candidates)} groups to review\n"
        
        if len(self.orphaned_notes) > 0:
            report += f"- ℹ️ **Orphaned notes:** {len(self.orphaned_notes)} meaningful files without incoming links\n"
        
        with open(output_file, 'w') as f:
            f.write(report)
        
        print(f"  ✅ Summary report exported to {output_path}")
        return output_file


def main():
    import sys
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    analyzer = RepositoryAnalyzer(repo_root)
    analysis = analyzer.analyze()
    
    # Export reports
    analyzer.export_json()
    analyzer.export_broken_links_report()
    analyzer.export_summary_report()
    
    # Print console summary
    s = analysis["statistics"]
    print(f"\n📊 Summary:\n")
    print(f"  Total Markdown: {s['total_markdown_files']}")
    print(f"  Meaningful Content: {s['meaningful_content_files']}")
    print(f"  Empty/Placeholder: {s['empty_markdown_files'] + s['placeholder_files']}")
    print(f"  Broken Wikilinks: {len(analysis['wikilinks']['broken_links'])}")
    print(f"  Orphaned Notes: {analysis['orphans']['total']}")
    print(f"  Duplicate Candidates: {analysis['duplicates']['total_candidates']}")


if __name__ == "__main__":
    main()
