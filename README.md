# weather-app-rs

## Pre - Requisites
1. python 3.12
2. virtualenv (pip install virtualenv)

## Set up workspace
1. Run `git clone https://github.com/Sudeepto41/weather-app-rs.git` in git bash
2. cd into cloned directory
3. Open terminal in current directory
4. Run `cd weather-app-rs`.
5. Run `python -m venv .venv`.
6. Run `.\.venv\scripts\Activate.ps1` or `./.venv/scripts/Activate.bat`
7. Run `pip install -r reuirements.txt`

## Start dev server
1. Run `cd weather_app`
2. Run `python manage.py migrate`
3. Run `python manage.py makemigrations`
4. Run `python manage.py runserver`