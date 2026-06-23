#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AMEVA OS: Smart Dynamic Test Runner
Enforce zero-hardcoding dynamic PYTHONPATH assembly and smart test-discovery based on git diff.
"""

import os
import sys
import subprocess
import argparse

def get_git_modified_files(repo_dir):
    """
    Get list of modified/untracked files using Git CLI.
    """
    try:
        # Get modified tracked files
        res1 = subprocess.run(
            ["git", "diff", "--name-only"], 
            cwd=repo_dir, capture_output=True, text=True, check=True
        )
        # Get untracked files
        res2 = subprocess.run(
            ["git", "status", "--porcelain"], 
            cwd=repo_dir, capture_output=True, text=True, check=True
        )
        
        modified = set()
        for line in res1.stdout.splitlines():
            if line.strip():
                modified.add(line.strip())
                
        for line in res2.stdout.splitlines():
            # Untracked files start with ??
            if line.startswith("??"):
                file_path = line[2:].strip()
                modified.add(file_path)
                
        return list(modified)
    except Exception as e:
        print(f"[WARN] Failed to read git status/diff: {e}")
        return []

def map_sources_to_tests(modified_files, tests_dir):
    """
    Map modified source filenames to corresponding test files in tests_dir.
    Example: src/utils/helper.py -> test_helper.py or test_utils.py
    """
    if not os.path.exists(tests_dir):
        return []
        
    all_test_files = []
    for root, _, files in os.walk(tests_dir):
        for f in files:
            if f.startswith("test_") and f.endswith(".py"):
                all_test_files.append(os.path.join(root, f))
                
    if not modified_files:
        return []
        
    target_tests = set()
    for m_file in modified_files:
        base_name = os.path.basename(m_file)
        name_without_ext, _ = os.path.splitext(base_name)
        
        # If the modified file itself is a test file, add directly
        if base_name.startswith("test_") and m_file.endswith(".py"):
            full_test_path = os.path.abspath(m_file)
            if os.path.exists(full_test_path):
                target_tests.add(full_test_path)
            continue
            
        # Scan for test files containing the source name keyword
        for test_file in all_test_files:
            test_base = os.path.basename(test_file)
            if name_without_ext.lower() in test_base.lower():
                target_tests.add(test_file)
                
    return list(target_tests)

def assemble_pythonpath(base_dir):
    """
    Dynamically scan the base directory for AMEVA projects and assemble PYTHONPATH.
    """
    paths = ["."]
    
    # Navigate to parent folder (c:\ameva) to dynamically discover subprojects
    parent_dir = os.path.abspath(os.path.join(base_dir, ".."))
    
    try:
        if os.path.exists(parent_dir):
            for item in os.listdir(parent_dir):
                full_path = os.path.join(parent_dir, item)
                if os.path.isdir(full_path) and (item.lower().startswith("ameva-") or "nexus" in item.lower()):
                    paths.append(full_path)
                    # Add inner src folder if present
                    src_path = os.path.join(full_path, "src")
                    if os.path.isdir(src_path):
                        paths.append(src_path)
    except Exception as e:
        print(f"[WARN] Error scanning parent AMEVA projects: {e}")
        
    # Append existing environment PYTHONPATH
    existing = os.environ.get("PYTHONPATH", "")
    sep = ";" if os.name == "nt" else ":"
    if existing:
        paths.extend(existing.split(sep))
        
    # Deduplicate and verify path existences
    unique_paths = []
    seen = set()
    for p in paths:
        abs_p = os.path.abspath(p)
        if abs_p not in seen and os.path.exists(abs_p):
            seen.add(abs_p)
            unique_paths.append(abs_p)
            
    return sep.join(unique_paths)

def main():
    parser = argparse.ArgumentParser(description="AMEVA Smart Dynamic Test Runner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Run all discoverable tests")
    group.add_argument("--modified", action="store_true", help="Run tests mapped to git-modified source files")
    parser.add_argument("--dir", default=".", help="Target project root directory (default: current)")
    parser.add_argument("--test-dir", default="tests", help="Tests subdirectory (default: tests)")
    
    args = parser.parse_args()
    project_dir = os.path.abspath(args.dir)
    tests_dir = os.path.join(project_dir, args.test_dir)
    
    print("==================================================")
    print("         AMEVA Smart Dynamic Test Runner")
    print("==================================================")
    
    # 1. Assemble PYTHONPATH dynamically
    dynamic_pythonpath = assemble_pythonpath(project_dir)
    print(f"[*] Dynamically assembled PYTHONPATH:")
    for path_item in dynamic_pythonpath.split(";" if os.name == "nt" else ":"):
        print(f"  - {path_item}")
        
    # Create child process environment
    env = os.environ.copy()
    env["PYTHONPATH"] = dynamic_pythonpath
    
    # 2. Determine target tests
    run_cmd = [sys.executable]
    
    if args.modified:
        print(f"\n[*] Mode: Modified source targets only")
        modified_files = get_git_modified_files(project_dir)
        if not modified_files:
            print("[Info] No git modified files detected. Skipping test execution.")
            sys.exit(0)
            
        print(f"  - Modified files detected: {len(modified_files)}")
        for f in modified_files:
            print(f"    - {f}")
            
        target_tests = map_sources_to_tests(modified_files, tests_dir)
        if not target_tests:
            print("[Info] No corresponding tests mapped to the modified files. Discovering all tests as fallback.")
            run_cmd.extend(["-m", "unittest", "discover", "-s", tests_dir])
        else:
            print(f"  - Mapped tests to execute: {len(target_tests)}")
            for t in target_tests:
                print(f"    - {os.path.relpath(t, project_dir)}")
            
            # Run specific test modules
            run_cmd.extend(["-m", "unittest"])
            for t in target_tests:
                run_cmd.append(t)
    else:
        print(f"\n[*] Mode: All tests")
        if not os.path.exists(tests_dir):
            print(f"[Error] Tests directory '{args.test_dir}' does not exist.")
            sys.exit(1)
        run_cmd.extend(["-m", "unittest", "discover", "-s", tests_dir])
        
    # 3. Execute the tests via subprocess
    print("\n[*] Launching unittest runner sub-process...")
    print(f"[*] Command: {' '.join(run_cmd)}\n")
    
    try:
        res = subprocess.run(run_cmd, env=env)
        sys.exit(res.returncode)
    except Exception as e:
        print(f"[Fatal] Failed to execute unittest subprocess: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
