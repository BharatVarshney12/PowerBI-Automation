"""
Clear saved authentication session
Run this if you want to force a fresh login
"""

import os
from pathlib import Path

auth_state_path = Path(__file__).parent / 'data' / 'auth_state.json'

if auth_state_path.exists():
 os.remove(auth_state_path)
 print(f" Cleared saved session: {auth_state_path}")
 print("Next test run will require fresh login")
else:
 print("ℹ No saved session found - already cleared")
