# Description

The aim of this project is to cover by integration tests the web service AtomicBoard. The stage server is available by address 
[atomicboard.devman.org](http://atomicboard.devman.org).

Test list:
- load task list from server;
- edit exists task;
- mark task as closed;
- create new task
- drag'n'drop task (with helper from [this stackoverflow answer](https://stackoverflow.com/a/29381532));

# How to install

Just clone this repo, cd in cloned dir or download zip then unpack and cd in unpacked dir.

# Requirements

For any linux-based distributions with Python3 installed. Run on windows is the same if python3 added to your system PATH (check [python3 windows installation](http://docs.python-guide.org/en/latest/starting/install3/win/) guide).

This tests require a bunch of various technologies:
- python requirements:
    ```bash
    pip install -r requirements.txt
    ```
- PHANTOMJS requirements:
    ```bash
    npm i
    ```
    If npm is unavailable on your system please checkout [nodejs installation](https://nodejs.org/en/download/package-manager/) for various systems.

# How to run

To run tests input in console:
```bash
python3 tests.py
```

### Example output

```bash
 $ python3 tests.py
.....
----------------------------------------------------------------------
Ran 5 tests in 55.702s
OK
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

