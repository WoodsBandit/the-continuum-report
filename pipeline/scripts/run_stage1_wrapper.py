#!/usr/bin/env python3
"""Wrapper to run stage1 with correct imports."""
import sys
import os

# Set up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
sys.path.insert(0, os.path.join(script_dir, 'lib'))

# Fix relative imports in lib modules
import config
import logging_config

# Patch the modules so relative imports work
sys.modules['lib'] = type(sys)('lib')
sys.modules['lib.config'] = config
sys.modules['lib.logging_config'] = logging_config

# Now import and run
if __name__ == "__main__":
    # Re-execute run_stage1 with fixed imports
    exec(open(os.path.join(script_dir, 'run_stage1.py')).read())
