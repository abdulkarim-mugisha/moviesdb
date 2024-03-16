CREATE USER 'admin1'@'localhost' IDENTIFIED BY 'admin1pw';
CREATE USER 'client1'@'localhost' IDENTIFIED BY 'client1pw';
-- Can add more users or refine permissions
GRANT ALL PRIVILEGES ON moviesdb.* TO 'admin1'@'localhost';
GRANT SELECT ON moviesdb.* TO 'client1'@'localhost';
FLUSH PRIVILEGES;
