#!/bin/bash
# Run curriculum analysis
cd /tmp/repo_analysis || mkdir -p /tmp/repo_analysis
cd /tmp/repo_analysis

# Initialize a minimal Python environment and run the analyzer
python3 << 'EOF'
import sys
sys.path.insert(0, '/tmp/repo_analysis')

# Import the analyzer
import subprocess
import os

# Clone or check the repo (simplified for this context)
repo_root = "/tmp/curriculum-vault"
if not os.path.exists(repo_root):
    subprocess.run(["git", "clone", "--depth", "1", 
                   "https://github.com/arul-girish-jaganathan/curriculum-vault.git",
                   repo_root], check=False)

# Copy the tools
tools_src = os.path.join(repo_root, "00_Index/_Repository_Inventory/curriculum_tools.py")
if os.path.exists(tools_src):
    # Add to path and import
    sys.path.insert(0, os.path.dirname(tools_src))
    from curriculum_tools import RepositoryAnalyzer
    
    # Run analysis
    analyzer = RepositoryAnalyzer(repo_root)
    analysis = analyzer.analyze()
    
    # Print domain breakdown
    print("\n" + "="*70)
    print("DOMAIN ANALYSIS REPORT")
    print("="*70)
    
    domains = analysis.get("domains", {})
    for domain in sorted(domains.keys()):
        info = domains[domain]
        print(f"\nDomain: {domain}")
        print(f"  Files: {info['file_count']}")
        print(f"  Markdown: {info['markdown_count']}")
        print(f"  Meaningful: {info['meaningful_count']}")
        print(f"  Placeholder: {info['placeholder_count']}")
        print(f"  Empty: {info['empty_count']}")
    
    # Export reports
    analyzer.export_json()
    analyzer.export_summary_report()
    analyzer.export_broken_links_report()

EOF
