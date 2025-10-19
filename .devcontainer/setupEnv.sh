#!/bin/bash

# Install PIP
pip install --upgrade pip

# Install Poetry
pip install poetry

pip install poetry-plugin-export

# Configure Poetry
poetry env use python3.12

poetry config warnings.export false

poetry config virtualenvs.in-project true

# Todo: Poetry Install.
poetry install