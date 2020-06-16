from Database import Database

db = Database('test.db')
db.create_tables_if_not_exists()

with db.conn:
    id = db.insert_usuario('Jose 4')
    idp = db.insert_pedido(id, '16-06-2020', None)
    idz = db.insert_pizza('mediana', 15)
    idi = db.insert_ingrediente('anchoas', 'mediano', 2)
    x = db.insert_detalle(idp, idz, idi)
    db.update_precio_pedido(idp, 50.4)
    db.my_select("SELECT * FROM usuario;")
    db.my_select("SELECT * FROM pedido;")
    db.my_select("SELECT * FROM pizza;")
    db.my_select("SELECT * FROM ingrediente;")
    db.my_select("SELECT * FROM detalle;")