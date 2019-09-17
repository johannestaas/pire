import os
import sys

rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [rootdir] + sys.path
