#!/bin/bash
psql -U postgres -c "CREATE DATABASE test_db;"
# psql -U postgres -c "CREATE USER test_user WITH PASSWORD 'test_password';"

# Grant all privileges on the database
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user;"
# Grant privileges on the schema (assuming schema name is 'public')
psql -U postgres -d test_db -c "GRANT USAGE, CREATE ON SCHEMA public TO test_user;"
# Grant privileges on all tables (existing and future)
psql -U postgres -d test_db -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO test_user;"
psql -U postgres -d test_db -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO test_user;"
# further priveleges
psql -U postgres -d test_db -c "GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO test_user;"
psql -U postgres -d test_db -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO test_user;"
# Note: you may need to edit the config file for test_user to allow
# login via password
# On ubuntu, this is usually located at /etc/postgresql/16/main/pg_hba.conf
# and you may need to change the line:
# local   all             postgres                                peer
# to:
# local   test_user             postgres                                md5