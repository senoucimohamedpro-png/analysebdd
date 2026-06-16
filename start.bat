@echo off
REM Lance le backend (FastAPI) et le frontend (Vite dev server) en une seule commande.
setlocal

set ROOT=%~dp0

echo === Installation des dependances backend (si besoin) ===
cd "%ROOT%backend"
python -m pip install -r requirements.txt

echo === Installation des dependances frontend (si besoin) ===
cd "%ROOT%frontend"
if not exist node_modules (
    npm install
)

echo === Demarrage du backend (http://127.0.0.1:8000) ===
cd "%ROOT%"
start "Backend - FastAPI" cmd /k python -m uvicorn backend.main:app --reload --port 8000

echo === Demarrage du frontend (http://127.0.0.1:5173) ===
cd "%ROOT%frontend"
start "Frontend - Vite" cmd /k npm run dev

echo.
echo Application lancee : ouvrez http://127.0.0.1:5173 dans votre navigateur.
endlocal
