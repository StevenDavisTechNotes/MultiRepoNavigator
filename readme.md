# Multi Repo Navigator

<!-- cspell: ignore venv pycache childitem pytest reshim pyright -->

## Overview

Modern IDEs do a great job of navigating the code within one projects.  Maintaining file relationships across multiple repositories in different languages is a challenge.  This project is an attempt to create a tool to help with that.

## Installation

Copy the folder `testing_example` to `~/src/testing_example` or `(Join-Path $Env:UserProfile 'src' 'testing_example')` since that is where the seeded configuration will look.

```sh

### Python with py and venv

```ps1
rm venv -r # to remove the venv folder
get-childitem src -include __pycache__ -recurse | remove-item -Force -Recurse
py -3.12 -m venv venv 
.\venv\Scripts\Activate.ps1
python --version
python -c "import sys; print(sys.executable)"
.\venv\Scripts\python.exe -m pip install --upgrade pip
pip install -r .\requirements.txt
pytest -x -vv src
clear && flake8 src && node_modules/.bin/pyright src
```

### Python with asdf and venv

```sh
touch .tool-versions
asdf local python 3.12.4
python3 -V
echo "Expect Python 3.12.4"

rm -rf ./venv
find src | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
asdf reshim python 3.12.4
python --version
python -m venv venv
source venv/bin/activate

pip install --upgrade pip
asdf reshim python 3.12.4
pip install wheel && pip install -r requirements.txt

clear && flake8 src && py3clean src && ./node_modules/.bin/pyright src
```

### for asdf and Javascript

```sh
asdf local nodejs 20.9.0
npm install
```

### Sqlite Tools

To view and edit the database directly

#### Download and install the Sqlite Tools

##### For Windows

- Navigate to [https://www.sqlite.org/download.html](Sqlite Downloads)
- Install the sqlite-tools-win32-x86-3360000.zip to `C:\Programs\Sqlite`
- Add `C:\Programs\Sqlite` to your path using Edit Environment Variables for Your Account
- Close and reopen your terminal

##### For Linux

`sudo apt-get install sqlite3`

## Development

Please take a look at this [readme.md](src\web_ui\readme.md)
