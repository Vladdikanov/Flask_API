#!/bin/bash
set -e


flask db upgrade b97977d331b4  

python start.py