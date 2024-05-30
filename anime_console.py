from neo4j import GraphDatabase

# Configuración de conexión a Neo4j
uri = "bolt://3.219.33.20:7687"
user = "neo4j"
password = "farads-photos-tablets"

driver = GraphDatabase.driver(uri, auth=(user, password))

def consulta_base_datos(tx):
    query = """
    MATCH (a:Anime)
    OPTIONAL MATCH (a)-[:ES_DE]->(g:Genero)
    OPTIONAL MATCH (a)-[:PRODUCIDA_POR]->(e:Estudio)
    OPTIONAL MATCH (a)-[:SE_EMITIO]->(y:Year)
    OPTIONAL MATCH (a)-[:VOZ]->(actor:Actor)
    OPTIONAL MATCH (a)-[:CREADO_POR]->(c:Manga)
    OPTIONAL MATCH (a)-[:TIPO]->(t:Tipo)
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

def consulta_favoritos(tx, username):
    query = """
    MATCH (u:User {username: $username})-[:LE_GUSTA]->(a:Anime)
    OPTIONAL MATCH (a)-[:ES_DE]->(g:Genero)
    OPTIONAL MATCH (a)-[:PRODUCIDA_POR]->(e:Estudio)
    OPTIONAL MATCH (a)-[:SE_EMITIO]->(y:Year)
    OPTIONAL MATCH (a)-[:VOZ]->(actor:Actor)
    OPTIONAL MATCH (a)-[:CREADO_POR]->(c:Manga)
    OPTIONAL MATCH (a)-[:TIPO]->(t:Tipo)
    RETURN a.nombre as nombre, collect(distinct g.nombre) as generos, 
           e.nombre as estudio, y.nombre as ano, collect(distinct actor.nombre) as actores, 
           c.nombre as creador, t.nombre as tipo
    """
    result = tx.run(query, username=username)
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

def agregar_favorito(tx, username, nombre_anime):
    query_check = """
    MATCH (u:User {username: $username})-[:LE_GUSTA]->(a:Anime {nombre: $anime_name})
    RETURN a
    """
    query_add = """
    MATCH (u:User {username: $username}), (a:Anime {nombre: $anime_name})
    MERGE (u)-[:LE_GUSTA]->(a)
    """
    result = tx.run(query_check, username=username, anime_name=nombre_anime)
    if result.single():
        return "Anime already in favorites"
    tx.run(query_add, username=username, anime_name=nombre_anime)
    return "Anime added to favorites"

def eliminar_favorito(tx, username, nombre_anime):
    query = """
    MATCH (u:User {username: $username})-[r:LE_GUSTA]->(a:Anime {nombre: $anime_name})
    DELETE r
    """
    tx.run(query, username=username, anime_name=nombre_anime)
    return "Anime removed from favorites"

def mostrar_recomendaciones(tx, username):
    all_animes_query = """
    MATCH (a:Anime)
    OPTIONAL MATCH (a)-[:ES_DE]->(g:Genero)
    OPTIONAL MATCH (a)-[:PRODUCIDA_POR]->(e:Estudio)
    OPTIONAL MATCH (a)-[:SE_EMITIO]->(y:Year)
    OPTIONAL MATCH (a)-[:VOZ]->(actor:Actor)
    OPTIONAL MATCH (a)-[:CREADO_POR]->(c:Manga)
    OPTIONAL MATCH (a)-[:TIPO]->(t:Tipo)
    RETURN a.nombre as nombre, collect(distinct g.nombre) as generos, 
           e.nombre as estudio, y.nombre as ano, collect(distinct actor.nombre) as actores, 
           c.nombre as creador, t.nombre as tipo
    """
    favorites_query = """
    MATCH (u:User {username: $username})-[:LE_GUSTA]->(a:Anime)
    OPTIONAL MATCH (a)-[:ES_DE]->(g:Genero)
    RETURN a.nombre as nombre, collect(distinct g.nombre) as generos
    """
    all_animes = tx.run(all_animes_query).data()
    favorites = tx.run(favorites_query, username=username).data()
    
    favorite_genres = set()
    for record in favorites:
        favorite_genres.update(record['generos'])
    
    recommendations = [anime for anime in all_animes if any(genre in favorite_genres for genre in anime['generos']) and anime['nombre'] not in [record['nombre'] for record in favorites]]
    return recommendations

def print_table(data, headers):
    col_widths = [max(len(str(row[i])) for row in data + [headers]) for i in range(len(headers))]
    
    header_row = " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
    separator_row = "-+-".join('-' * col_widths[i] for i in range(len(headers)))
    data_rows = [" | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))) for row in data]
    
    print(header_row)
    print(separator_row)
    for row in data_rows:
        print(row)

def main():
    with driver.session() as session:
        while True:
            print("\nMenú:")
            print("1. Consultar base de datos")
            print("2. Consultar favoritos")
            print("3. Agregar a favoritos")
            print("4. Eliminar de favoritos")
            print("5. Mostrar recomendaciones")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                animes = session.read_transaction(consulta_base_datos)
                headers = ["Nombre", "Tipo", "Géneros", "Estudio", "Año", "Actores", "Creador"]
                data = [
                    [anime['nombre'], anime['tipo'], ', '.join(anime['generos']), anime['estudio'], anime['ano'], ', '.join(anime['actores']), anime['creador']]
                    for anime in animes
                ]
                print("\nAnimes en la base de datos:")
                print_table(data, headers)
            elif opcion == '2':
                favoritos = session.read_transaction(consulta_favoritos, "Juan")
                headers = ["Nombre", "Tipo", "Géneros", "Estudio", "Año", "Actores", "Creador"]
                data = [
                    [anime['nombre'], anime['tipo'], ', '.join(anime['generos']), anime['estudio'], anime['ano'], ', '.join(anime['actores']), anime['creador']]
                    for anime in favoritos
                ]
                print("\nFavoritos de Juan:")
                print_table(data, headers)
            elif opcion == '3':
                nombre_anime = input("Ingrese el nombre del anime que desea agregar a favoritos: ")
                mensaje = session.write_transaction(agregar_favorito, "Juan", nombre_anime)
                print(mensaje)
            elif opcion == '4':
                nombre_anime = input("Ingrese el nombre del anime que desea eliminar de favoritos: ")
                mensaje = session.write_transaction(eliminar_favorito, "Juan", nombre_anime)
                print(mensaje)
            elif opcion == '5':
                recomendaciones = session.read_transaction(mostrar_recomendaciones, "Juan")
                headers = ["Nombre", "Tipo", "Géneros", "Estudio", "Año", "Actores", "Creador"]
                data = [
                    [anime['nombre'], anime['tipo'], ', '.join(anime['generos']), anime['estudio'], anime['ano'], ', '.join(anime['actores']), anime['creador']]
                    for anime in recomendaciones
                ]
                print("\nRecomendaciones:")
                print_table(data, headers)
            elif opcion == '6':
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == '__main__':
    main()