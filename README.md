# Notes-app
A basic note-taking app written in python

# Getting Started

## Windows
Click [Here](https://github.com/Shadowniko1/Notes-app/releases/latest/download/notes-app.exe) to download the latest Windows executable

## Building from Source
building from source is required on operating systems other than Windows (MacOS, Linux, BSD, etc.)

### 1. Install Python

Check if Python is installed:

```bash
python3 --version
```
If you do not have Python installed, check how to install it [Here](https://www.python.org/downloads/).

### 2. Clone the Repository
```bash
git clone https://github.com/Shadowniko1/Notes-app.git
cd Notes-app
```

### 3. Install Dependencies
Install the required packages:
```bash
pip3 install -r requirements.txt
```

> **Note:** If you get a permissions error, try adding `--user` to the command:
> ```bash
> pip3 install -r requirements.txt --user
> ```

### 4. Run the App
```bash
python3 main.py
```

---

### Platform-Specific Notes

**macOS**
If you run into a Tkinter error, you may need to install it separately. The easiest way is via [Homebrew](https://brew.sh/):
```bash
brew install python-tk
```

**Linux (Debian/Ubuntu)**
```bash
sudo apt install python3-tk
```

**Linux (Fedora/RHEL)**
```bash
sudo dnf install python3-tkinter
```

**BSD**
```bash
pkg install py311-tkinter
```
*(Replace `py311` with your installed Python version.)*
