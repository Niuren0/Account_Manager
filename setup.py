import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["mysql.connector"],
    "include_files": [
            ("icon.ico", "icon.ico")],
    "optimize": 2
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executable = [
    Executable(
        "main.py",
        base=base,
        icon="icon.ico"
    )
]

setup(
    name="Hesap Yöneticisi",
    version="1.0",
    description="Hesap Yöneticisi",
    options={"build_exe": build_exe_options},
    executables=executable
)
