   # test_import.py
import os
print(os.getcwd()) # Current working directory
import sys
print(sys.path) # Your Python path
try:
    import shared.models #If shared is at the correct location. This will import the module
    print("Import successful!")
except ImportError as e:
       print(f"Import failed: {e}")
