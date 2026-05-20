from flask import request, jsonify
from database import get_db_connection
from middlewares.auth_middleware import token_required


def Create():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute( "INSERT INTO estados (estado, uf ) VALUES (%s, %s)",
        (data['estado'],data['uf'],)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Usuário criado'}), 201

def GetAll():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estados")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

def Delete(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM estados WHERE id = %s",[id],)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users), 401

def Put(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute( "UPDATE estados SET estado = %s , uf = %s WHERE id = %s",
        (data['estado'],data['uf'], id )
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'registro atualizado'}), 203

def GetById(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estados WHERE id = %s",[id],)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users) , 206
