#!/usr/bin/env python
"""
Entry point for the SC Flask web application.
"""
from .aq_dashboard import create_app

APP = create_app()
