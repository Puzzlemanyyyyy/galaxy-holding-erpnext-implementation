# Guía rápida de instalación

Esta guía resume los pasos esenciales para desplegar el stack completo de Galaxy Holding utilizando Docker Compose.

## 1. Requisitos previos
- Docker y Docker Compose instalados.
- DNS o entradas en `/etc/hosts` apuntando a los dominios locales (`galaxy.local`, `galaxy.erp.local`, `n8n.local`).
- Variables de entorno definidas en `docker/.env` (copiar desde `docker/.env.example`).
- Credenciales para Microsoft 365 y claves API necesarias (OpenAI, Verifactu, etc.).

## 2. Preparación del entorno
1. Clonar el repositorio y situarse en la carpeta raíz.
2. Copiar el archivo `.env` de ejemplo: `cp docker/.env.example docker/.env`.
3. Editar `docker/.env` con las credenciales reales y hostnames.
4. Revisar/ajustar las configuraciones en `configs/` si se personalizan puertos o dominios.

## 3. Despliegue de la infraestructura
```bash
docker-compose --env-file docker/.env -f docker/docker-compose.yml up -d
```

Verificar que todos los contenedores estén saludables (`docker ps`).

## 4. Bootstrap de ERPNext
Ejecutar los scripts de inicialización para crear compañías, roles y datos maestros:
```bash
docker exec -it galaxy-erpnext python3 /scripts/setup_companies.py --site galaxy.local
docker exec -it galaxy-erpnext python3 /scripts/setup_roles_permissions.py --site galaxy.local
docker exec -it galaxy-erpnext python3 /scripts/setup_erp_crm.py --site galaxy.local --verifactu-api-key <sandbox-key>
```

## 5. Importación de workflows n8n
1. Acceder a `http://n8n.local:5678`.
2. Importar los archivos desde `n8n_workflows/`.
3. Configurar las credenciales (Microsoft 365, Webhooks, OpenAI, etc.).

## 6. Validaciones finales
- Acceder a `http://galaxy.local` y verificar login con credenciales administrativas.
- Revisar que la configuración multi-compañía esté aplicada.
- Ejecutar flujos críticos (facturación intercompany, reportes con IA, notificaciones Teams).

> Para detalles extendidos consultar el documento `/docs/galaxy_master_document`.
