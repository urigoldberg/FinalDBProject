# install and download mysql
# connect to mysql with: mysql -uroot
# https://www.a2hosting.com/kb/developer-corner/mysql/managing-mysql-databases-and-users-from-the-command-line

mysql> create database uni;
Query OK, 1 row affected (0.01 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| uni                |
+--------------------+
5 rows in set (0.00 sec)