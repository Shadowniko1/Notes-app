# Notes-app
A basic note-taking app written in python

# Getting Started

## Windows
Click [Here](https://github.com/Shadowniko1/Notes-app/releases/latest/download/notes-app.exe) to download the latest Windows executable.

## Linux (Debian/Ubuntu)
Click [Here](https://github.com/Shadowniko1/Notes-app/releases/latest/download/notes-app.deb) to download the latest `.deb` package, then install it with:
```bash
sudo dpkg -i notes-app.deb
```

## macOS
Click [Here](https://github.com/Shadowniko1/Notes-app/releases/latest/download/notes-app) to download the latest macOS binary, then make it executable and run it:
```bash
chmod +x notes-app
./notes-app
```
> **Note:** If macOS blocks the app because it's from an unidentified developer, go to **System Settings → Privacy & Security** and click **Open Anyway**.

## Building from Source
For operating systems without a prebuilt release (Fedora, BSD, etc.), you can run directly from source.

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

**Linux (Fedora/RHEL)**
```bash
sudo dnf install python3-tkinter
```

**BSD**
```bash
pkg install py311-tkinter
```
*(Replace `py311` with your installed Python version.)*
