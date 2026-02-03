from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.schemas import RequerimientoCreate, RequerimientoUpdate
from app.services.historial_service import registrar_historial

router = APIRouter()

@router.get("/")
def listar_requerimientos():
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT * FROM requerimientos_empresariales
                ORDER BY fecha_creacion DESC
            """)
            return cur.fetchall()


@router.post("/")
def crear_requerimiento(data: RequerimientoCreate):
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("""
                INSERT INTO requerimientos_empresariales
                (empresa_nit, tipo_solicitud, prioridad, descripcion, estado)
                VALUES (%s,%s,%s,%s,'nuevo')
                RETURNING id
            """, (data.empresa_nit, data.tipo_solicitud, data.prioridad, data.descripcion))
            nuevo = cur.fetchone()
        con.commit()
    return {"id": nuevo["id"], "status": "created"}


@router.put("/{req_id}")
def actualizar_requerimiento(req_id: int, data: RequerimientoUpdate):
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("SELECT estado FROM requerimientos_empresariales WHERE id=%s", (req_id,))
            anterior = cur.fetchone()
            if not anterior:
                raise HTTPException(404, "No existe")

            cur.execute("""
                UPDATE requerimientos_empresariales
                SET estado=%s, prioridad=%s, responsable_id=%s, resolucion=%s
                WHERE id=%s
            """, (data.estado, data.prioridad, data.responsable_id, data.resolucion, req_id))
        con.commit()

    registrar_historial(req_id, "system", anterior["estado"], data.estado, "Actualizado vía microservicio")

    return {"status": "updated"}
