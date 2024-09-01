-- Sets up the Postgres DB for test

-- Create database
CREATE DATABASE IF NOT EXISTS wya_test_db;

-- Create 'test' user
CREATE USER IF NOT EXISTS 'wya_test'@'172.17.0.1' IDENTIFIED BY 'wya_test_pwd';

-- Give user privileges
GRANT ALL PRIVILEGES ON `wya_test_db`.* TO 'wya_test'@'172.17.0.1';
FLUSH PRIVILEGES;
