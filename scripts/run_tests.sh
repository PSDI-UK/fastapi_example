#!/bin/bash

export LOG_LEVEL="CRITICAL"
export MODE="TEST"
coverage run --branch -m pytest -s tests/ -W ignore::DeprecationWarning

# coverage report
