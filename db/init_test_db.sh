#!/bin/bash
# psql -U postgres -c "CREATE DATABASE test_db;"
psql -U postgres -d test_db -f schema.sql

# psql -U postgres -c "CREATE USER test_user WITH PASSWORD 'test_password';
# GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user;"
