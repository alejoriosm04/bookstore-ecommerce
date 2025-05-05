para iniciar la base de datos y crear las tablas:

flask shell
>>> from extensions import db
>>> db.create_all()
