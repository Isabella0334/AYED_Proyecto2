from flask import Flask, jsonify, request
from neo4j import GraphDatabase

app = Flask(__name__)

# Configuración de conexión a Neo4j Sandbox
uri = "bolt://sandbox.neo4j.io:7687"  # Reemplaza con la URL de tu sandbox
user = "neo4j"  # Reemplaza con tu nombre de usuario
password = "your_sandbox_password"  # Reemplaza con tu contraseña

driver = GraphDatabase.driver(uri, auth=(user, password))

def get_animes(tx):
    query = """
    MATCH (a:Anime)-[:ES_DE]->(g:Genero),
          (a)-[:PRODUCIDA_POR]->(e:Estudio),
          (a)-[:SE_EMITIO]->(y:Year),
          (a)-[:VOZ]->(actor:Actor),
          (a)-[:CREADO_POR]->(c:Manga),
          (a)-[:TIPO]->(t:Tipo)
    RETURN a.nombre as nombre, collect(distinct g.nombre) as generos, 
           e.nombre as estudio, y.nombre as ano, collect(distinct actor.nombre) as actores, 
           c.nombre as creador, t.nombre as tipo
    """
    result = tx.run(query)
    animes = []
    for record in result:
        animes.append({
            "nombre": record["nombre"],
            "generos": record["generos"],
            "estudio": record["estudio"],
            "ano": record["ano"],
            "actores": record["actores"],
            "creador": record["creador"],
            "tipo": record["tipo"]
        })
    return animes

@app.route('/animes', methods=['GET'])
def animes():
    with driver.session() as session:
        animes = session.read_transaction(get_animes)
    return jsonify(animes)

@app.route('/animes', methods=['POST'])
def add_anime():
    data = request.get_json()
    query = """
    CREATE (a:Anime {nombre: $nombre, tipo: $tipo})
    WITH a
    UNWIND $generos AS genero
    MERGE (g:Genero {nombre: genero})
    CREATE (a)-[:ES_DE]->(g)
    WITH a
    MERGE (e:Estudio {nombre: $estudio})
    CREATE (a)-[:PRODUCIDA_POR]->(e)
    WITH a
    MERGE (y:Year {nombre: $ano})
    CREATE (a)-[:SE_EMITIO]->(y)
    WITH a
    UNWIND $actores AS actor
    MERGE (act:Actor {nombre: actor})
    CREATE (a)-[:VOZ]->(act)
    WITH a
    MERGE (c:Manga {nombre: $creador})
    CREATE (a)-[:CREADO_POR]->(c)
    WITH a
    MERGE (t:Tipo {nombre: $tipo})
    CREATE (a)-[:TIPO]->(t)
    """
    with driver.session() as session:
        session.run(query, data)
    return jsonify({'status': 'success'})

@app.route('/animes/<nombre>', methods=['PUT'])
def update_anime(nombre):
    data = request.get_json()
    query = """
    MATCH (a:Anime {nombre: $nombre})
    SET a += $data
    """
    params = {'nombre': nombre, 'data': data}
    with driver.session() as session:
        session.run(query, params)
    return jsonify({'status': 'success'})

@app.route('/animes/<nombre>', methods=['DELETE'])
def delete_anime(nombre):
    query = """
    MATCH (a:Anime {nombre: $nombre})
    DETACH DELETE a
    """
    with driver.session() as session:
        session.run(query, {'nombre': nombre})
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)