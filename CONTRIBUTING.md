
# Contributing to extrawest_ocpi

---

---

## Requirements

---

pyenv -> [installation guide](https://brain2life.hashnode.dev/how-to-install-pyenv-python-version-manager-on-ubuntu-2004)

Make sure to run after installation:
```bash
  pyenv update
```

python >= 3.11.1
```bash
  pyenv install 3.11.1
```

pipenv
```bash
  pip install pipenv
```


## Installation

---

Clone the project

```bash
  git clone https://github.com/extrawest/extrawest_ocpi.git
```

Go to the project directory

```bash
  cd extrawest_ocpi
```

Install dependencies

```bash
  pipenv --python 3.11.1
```

```bash
  pipenv update
```

Activate virtual environment:
```bash
  pipenv shell
```

Install pre-commit:
```bash
  pre-commit install
```


## Running Tests

---

To run tests, run the following command

```bash
  pytest
```
