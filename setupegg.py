#!/usr/bin/env python
"""Wrapper to run setup.py using setuptools."""

with open('setup.py') as f:
    exec(compile(f.read(), 'setup.py', 'exec'))
