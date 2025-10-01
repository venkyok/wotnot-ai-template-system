#!/usr/bin/env python3
"""
Railway Debug Script - Check what files exist and environment
"""
import os
import sys

print("=== RAILWAY DEBUG INFO ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

print("\n=== FILES IN CURRENT DIRECTORY ===")
try:
    files = os.listdir(".")
    for file in sorted(files):
        print(f"- {file}")
except Exception as e:
    print(f"Error listing files: {e}")

print("\n=== ENVIRONMENT VARIABLES ===")
railway_vars = {k: v for k, v in os.environ.items() if 'RAILWAY' in k or k in ['PORT', 'HOST']}
for key, value in sorted(railway_vars.items()):
    print(f"{key}: {value}")

print("\n=== TRYING TO IMPORT DIRECT_MAIN ===")
try:
    import direct_main
    print("✅ direct_main imported successfully")
    print(f"App object: {direct_main.app}")
except Exception as e:
    print(f"❌ Failed to import direct_main: {e}")

print("\n=== TRYING TO IMPORT WATI.MAIN ===")
try:
    from wati import main
    print("✅ wati.main imported successfully")
except Exception as e:
    print(f"❌ Failed to import wati.main: {e}")

print("=== END DEBUG INFO ===")