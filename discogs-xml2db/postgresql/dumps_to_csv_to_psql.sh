#!/usr/bin/env bash

python3 run.py --bz2 --output=csv_dir "${SCRIPT_DIR}/discogs-xml2db/discogs_dumps" --export="artist" --export="label" --export="master" --export "release"
# in order: compress resulting csvs, where to put csvs, export from this dir, export these items

# change defaults in postgresql.conf to be for the user
sed "s/discogs/juniebjonesrecordproject/" -e "s/postgres/${whoami}/" -e "s/pgpass/${whoami}/" "${SCRIPT_DIR}/discogs-xml2db/postgresql/postgresql.conf"

# Create database tables
python3 "${SCRIPT_DIR}/discogs-xml2db/postgresql/psql.py" < "${SCRIPT_DIR}/discogs-xml2db/postgresql/sql/CreateTables.sql"

# Import CSV files
python3 "${SCRIPT_DIR}/discogs-xml2db/postgresql/importcsv.py" "/csvdir/*"

# Configure primary keys and constraints, build indexes
python3 "${SCRIPT_DIR}/discogs-xml2db/postgresql/psql.py" < "${SCRIPT_DIR}/discogs-xml2db/postgresql/sql/CreatePrimaryKeys.sql"
python3 "${SCRIPT_DIR}/discogs-xml2db/postgresql/psql.py" < "${SCRIPT_DIR}/discogs-xml2db/postgresql/sql/CreateFKConstraints.sql"
python3 "${SCRIPT_DIR}/discogs-xml2db/postgresql/psql.py" < "${SCRIPT_DIR}/discogs-xml2db/postgresql/sql/CreateIndexes.sql"


