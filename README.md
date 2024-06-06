# About

Parse Ableton Live project.

# Installation

```
python3.9 -m venv venv
. ./venv/Scripts/activate
POETRY_VIRTUALENVS_CREATE=false poetry install
```

# Usage

```
python -m blendals_parser.main parse <path to .als file>
```

# Bugs

Time signature parsing does not work. Can't find it in als file.
