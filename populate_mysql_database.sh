#! /bin/bash

# CREATE DATABASE tawos
# CREATE USER 'tawos'@'localhost' IDENTIFIED BY 'tawospass';
# GRANT ALL PRIVILEGES ON tawos.* TO 'tawos'@'localhost';
# FLUSH PRIVILEGES;

mysql -u tawos -p tawos < TAWOS.sql