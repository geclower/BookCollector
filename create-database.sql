CREATE DATABASE bookcollector;

CREATE USER book_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE bookcollector TO book_admin;

