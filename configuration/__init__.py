from .celery import app as celery_app

__all__ = ("celery_app",)

# PyMySQL remplace mysqlclient (MySQL/MariaDB de XAMPP)
import pymysql

pymysql.version_info = (1, 4, 6, "final", 0)  # Django 4.2 exige mysqlclient >= 1.4.3
pymysql.install_as_MySQLdb()

