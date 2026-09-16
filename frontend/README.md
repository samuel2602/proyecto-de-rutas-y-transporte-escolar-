# Frontend de Gestión de Transporte

Aplicación Svelte + Vite para administrar rutas, estudiantes, conductores, vehículos, paraderos y registros de abordaje.

## Ejecución

1. Inicia la API en otra terminal desde la raíz del backend:

   ```powershell
   py -3.14 -m uvicorn main:app --reload
   ```

2. Copia `.env.example` a `.env` si la API se ejecuta en otra URL y ajusta `VITE_API_URL`.
3. Desde esta carpeta ejecuta:

   ```powershell
   npm install
   npm run dev
   ```

El panel se sirve en `http://localhost:5173`. La API ya permite solicitudes desde ese origen.

## Compilación

```powershell
npm run build
```
