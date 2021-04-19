#!/bin/sh 
# Builds backend with no updates to front
cd backend
python3 wsgi.py
cd ..