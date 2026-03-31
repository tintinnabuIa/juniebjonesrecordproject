#!/usr/bin/env bash

python3 "${SCRIPT_DIR}/discogs-xml2db/run.py" --bz2 --output="${SCRIPT_DIR}/discogs-xml2db/csv_dir" "${SCRIPT_DIR}/discogs-xml2db/discogs_dumps" --export="artist" --export="label" --export="master" --export "release"
# in order: compress resulting csvs, where to put csvs, export from this dir, export these items

# change defaults in postgresql.conf to be for the user
sed -i'' -e "s/postgres/$(whoami)/" -e "s/pgpass/$(whoami)/" "${SCRIPT_DIR}/discogs-xml2db/postgresql/postgresql.conf"
# make the user (with privileges) and database; password awful because
# not valuable public db, but should change if code use expanded
sudo -u postgres psql <<EOF
DROP DATABASE IF EXISTS "discogs" WITH (FORCE);
DROP USER IF EXISTS $(whoami);
CREATE USER $(whoami) WITH SUPERUSER PASSWORD '$(whoami)';
CREATE DATABASE "discogs" WITH OWNER = $(whoami);
EOF

# create database tables
python3 "${SCRIPT_DIR}/discogs-xml2db/postgresql/psql.py" < "${SCRIPT_DIR}/discogs-xml2db/postgresql/sql/CreateTables.sql"

# import csv files
python3 "${SCRIPT_DIR}/discogs-xml2db/postgresql/importcsv.py" ${SCRIPT_DIR}/discogs-xml2db/csv_dir/*

# configure primary keys and constraints, build indexes
python3 "${SCRIPT_DIR}/discogs-xml2db/postgresql/psql.py" < "${SCRIPT_DIR}/discogs-xml2db/postgresql/sql/CreatePrimaryKeys.sql"
python3 "${SCRIPT_DIR}/discogs-xml2db/postgresql/psql.py" < "${SCRIPT_DIR}/discogs-xml2db/postgresql/sql/CreateFKConstraints.sql"
python3 "${SCRIPT_DIR}/discogs-xml2db/postgresql/psql.py" < "${SCRIPT_DIR}/discogs-xml2db/postgresql/sql/CreateIndexes.sql"


