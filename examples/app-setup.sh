#!/bin/sh

# quit on errors:
set -o errexit

# quit on unbound symbols:
set -o nounset

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

pip install -r requirements.txt

./app-teardown.sh

mkdir instance

# Create the database
flask db init
flask db create

flask npm

cd static
npm install
cd ..

flask collect -v
# AMD/RequireJS has been deprecated and will be removed in future versions
# flask assets build
flask webpack buildall

flask fixtures
flask run
