# Notes-app
A basic note-taking app written in Python.

## Getting Started

### Direct Downloads

**Windows (MSI installer)**  
[Download latest MSI](https://github.com/Shadowniko1/Notes-app/releases/latest/download/notes-app.msi)

**Other operating systems (Linux, macOS, etc.)**  
Direct download assets are published on the latest release page:  
[Browse latest release assets](https://github.com/Shadowniko1/Notes-app/releases/latest)

### Build It Yourself (from source)
If your platform does not have a prebuilt release, run the app from source.

1. Install Python and confirm it is available:
```bash
python3 --version
```
If needed, install Python from [python.org](https://www.python.org/downloads/).

2. Clone the repository:
```bash
git clone https://github.com/Shadowniko1/Notes-app.git
cd Notes-app
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```
If you get a permissions error:
```bash
pip3 install -r requirements.txt --user
```

4. Run the app:
```bash
python3 main.py
```

### Platform-Specific Notes

**macOS**  
If Tkinter is missing:
```bash
brew install python-tk
```

**Linux (Fedora/RHEL)**  
```bash
sudo dnf install python3-tkinter
```

**BSD**  
```bash
pkg install py311-tkinter
```
Replace `py311` with your installed Python version.
