-- Sets up the Postgres DB for development

-- Create database
CREATE EXTENSION IF NOT EXISTS dblink;

DO $$
BEGIN
   IF EXISTS (SELECT FROM pg_database WHERE datname = 'wya_dev_db') THEN
      RAISE NOTICE 'Database already exists';
   ELSE
      PERFORM dblink_exec('dbname=' || current_database()
                        , 'CREATE DATABASE wya_dev_db');
   END IF;
END $$;

-- Create 'dev' user
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'wya_dev') THEN
        CREATE USER wya_dev WITH PASSWORD 'wya_dev_password';
    ELSE
        RAISE NOTICE 'User wya_dev already exists';
    END IF;
END $$;

GRANT ALL PRIVILEGES ON DATABASE wya_dev_db TO wya_dev;
