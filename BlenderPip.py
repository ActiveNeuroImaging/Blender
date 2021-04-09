import sys
import os

python_exe = os.path.join(sys.prefix, 'bin', 'python3.7m')

import subprocess
 
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

subprocess.call([python_exe, "-m", "pip", "install", "nibabel"])

