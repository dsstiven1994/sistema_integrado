from app.database import get_connection

def registrar_historial(requerimiento_id, usuario, estado_ant, estado_nuevo, comentario):
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("""
                INSERT INTO requerimientos_historial
                (requerimiento_id, usuario, estado_anterior, estado_nuevo, comentario)
                VALUES (%s,%s,%s,%s,%s)
            """, (requerimiento_id, usuario, estado_ant, estado_nuevo, comentario))
        con.commit()
