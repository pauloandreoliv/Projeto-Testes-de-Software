import pytest
import sys
import os
import warnings 
warnings.filterwarnings('ignore') #Ignorar warning do firebase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests')))

if __name__ == "__main__":
    pytest.main(['tests'])
