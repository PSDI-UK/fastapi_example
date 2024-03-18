#!/bin/bash

export LOG_LEVEL="DEBUG"
export MODE="DEV"
hypercorn --bind 0.0.0.0:80 src.main:app