# Style Transfer Markup

This is a small utility which I created for myself in order to work on Style Transfer project. It allows counting time statistics. 

## Installation

### Windows
```
python3 -m pip install -U pip
python3 -m venv venv
source ./venv/Scripts/activate
pip install -r requirements.txt
```

### Linux/MacOS on Intel
```
python3 -m pip install -U pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Installing PyQt5 on Mac M1

```
python3 -m pip install -U pip
python3 -m venv venv
source venv/bin/activate

PYQT5_VERSION=5.15.7_1
PYTHON=python3.9
brew install pyqt5
echo 'export PATH="/opt/homebrew/opt/qt@5/bin:$PATH"' >> ~/.zshrc
echo 'export PATH="/opt/homebrew/opt/pyqt@5/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

cp -r /opt/homebrew/Cellar/pyqt@5/$PYQT5_VERSION/lib/$PYTHON/site-packages/* ./venv/lib/$PYTHON/site-packages

pip install pandas
```