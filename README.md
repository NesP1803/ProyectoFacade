# ProyectoFacade

Proyecto demostrativo (backend + frontend) con una base de integración Factus API V2 en `backend/services/factus`.

## Factus V2 migration layer

Se implementó una capa de migración para Factus V2 con compatibilidad de rollback:

- Configuración versionada (`config.py`):
  - `FACTUS_API_VERSION` (default `v2`, fallback `v1`)
  - `FACTUS_SUPPORT_DOCUMENT_API_VERSION` (default `v1`)
  - `FACTUS_SUPPORT_ADJUSTMENT_API_VERSION` (default `v1`)
- Registro de endpoints (`endpoints.py`) por nombre lógico.
- Cliente HTTP (`client.py`) con manejo de errores y reintento controlado para `429`.
- Builder de payload Factura V2 (`payload_builder_v2.py`) para `payment_details[]` y precio neto.
- Builder de payload Nota Crédito V2 (`credit_note_payload_builder_v2.py`).
- Mapper de respuestas/estado (`response_mapper_v2.py`) para `estado_electronico` interno.
- Adaptador de descargas (`download_adapter.py`) para `pdf_base_64_encoded` y `xml_base_64_encoded`.

## Tests

```bash
cd backend
python -m unittest discover -s tests -v
```
