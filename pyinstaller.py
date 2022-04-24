"""
This is an example of using PyInstaller packager to build
executable from one of CEF Python's examples (wxpython.py).

See README-pyinstaller.md for installing required packages.

To package example type: `python pyinstaller.py`.
"""

import os
import platform
import shutil
import sys
from subprocess import Popen

try:
    import PyInstaller
except ImportError:
    PyInstaller = None
    raise SystemExit("Error: PyInstaller package missing. "
                     "To install type: pip install --upgrade pyinstaller")

EXE_EXT = ""
if platform.system() == "Windows":
    EXE_EXT = ".exe"
elif platform.system() == "Darwin":
    EXE_EXT = ".app"
elif platform.system() == "Linux":
    EXE_EXT = ""


def main():
    # Platforms supported
    if platform.system() not in ["Windows", "Darwin", "Linux"]:
        raise SystemExit("Error: Only Windows, Linux and Darwin platforms are "
                         "currently supported. See Issue #135 for details.")

    # Make sure nothing is cached from previous build.
    # Delete the build/ and dist/ directories.
    if os.path.exists("build/"):
        shutil.rmtree("build/")
    if os.path.exists("dist/"):
        shutil.rmtree("dist/")

    # Execute pyinstaller.
    # Note: the "--clean" flag passed to PyInstaller will delete
    #       global global cache and temporary files from previous
    #       runs. For example on Windows this will delete the
    #       "%appdata%/roaming/pyinstaller/bincache00_py27_32bit"
    #       directory.
    env = os.environ
    if "--debug" in sys.argv:
        env["CEFPYTHON_PYINSTALLER_DEBUG"] = "1"
    sub = Popen(["pyinstaller", "--clean", "prattle.spec"], env=env)
    sub.communicate()
    rcode = sub.returncode
    if rcode != 0:
        print("Error: PyInstaller failed, code=%s" % rcode)
        # Delete distribution directory if created
        if os.path.exists("dist/"):
            shutil.rmtree("dist/")
        sys.exit(1)


if __name__ == "__main__":
    main()