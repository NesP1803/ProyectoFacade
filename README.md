# Full-Stack Facade Pattern Demo (Flask + React + TypeScript)

This repository demonstrates the **Facade design pattern** using an academic e-commerce scenario.

## Structure

- `backend/services/` → subsystem services (`ProductService`, `PaymentService`, `NotificationService`)
- `backend/facade/` → facade class (`OrderFacade`)
- `backend/controllers/` → API controller (`POST /process`)
- `frontend/api/` → API facade (`ApiFacade`)
- `frontend/hooks/` → hook/service layer (`useOrderProcessor`)
- `frontend/components/` → UI component (`OrderDemo`)

## Run backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

## UML (text-based)

```text
Client (OrderDemo component)
    |
    v
Frontend ApiFacade (apiFacade.ts)
    |
    v
Backend Controller (/process)
    |
    v
OrderFacade (process_order)
    |--------> ProductService
    |--------> PaymentService
    \--------> NotificationService
```
