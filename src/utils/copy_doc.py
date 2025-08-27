import os
import pathlib
import subprocess
from platform import system

def copy_document(path: str) -> None:
    """
    Copies a document file to the system clipboard based on the platform.
    This copies a reference to the file, allowing it to be pasted into applications.
    """
    filepath = pathlib.Path(path)
    if not filepath.is_file():
        raise FileNotFoundError(f"The file was not found at the specified path: {path}")

    # Use the absolute path to avoid issues with relative paths in shell commands
    abs_path = str(filepath.resolve())
    _system = system().lower()

    if _system == "windows":
        # PowerShell is the simplest and most reliable way to copy a file object
        command = f'powershell -Command "Set-Clipboard -Path \'{abs_path}\'"'
        subprocess.run(command, check=True, shell=True)

    elif _system == "darwin":  # macOS
        # AppleScript can set the clipboard to a POSIX file object
        os.system(f"osascript -e 'set the clipboard to (POSIX file \"{abs_path}\")'")

    elif _system == "linux":
        # This requires 'copyq' to be installed (e.g., sudo apt install copyq)
        os.system(f"copyq copy 'file:{abs_path}'")
        
    else:
        raise Exception(f"Unsupported System: {_system}")