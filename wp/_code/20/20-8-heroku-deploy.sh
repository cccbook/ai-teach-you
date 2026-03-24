#!/bin/bash
set -e

echo "Deploying to Heroku..."

git add .
git commit -m "Deploy"
git push heroku main

heroku run python -m alembic upgrade head

heroku restart
