#!/usr/bin/env bash
# deploy_backend.sh
# ============================================================
#  Script de despliegue del Backend Veterinaria → VPS
#  Uso: bash scripts/deploy_backend.sh
#  Requiere: ssh, scp, tar configurados con clave SSH
# ============================================================

set -euo pipefail

# ── Config (edita si es necesario) ───────────────────────────
VPS_USER="${VPS_USER:-efran}"
VPS_HOST="${VPS_HOST:-192.168.1.38}"
DEPLOY_DIR="${DEPLOY_DIR:-~/veterinaria_deploy}"
COMPOSE_FILE="docker-compose.prod.yml"
PACKAGE_NAME="veterinaria_backend.tar.gz"

# ── Helpers ───────────────────────────────────────────────────
BOLD='\033[1m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; RED='\033[0;31m'; NC='\033[0m'
step()  { echo -e "\n${CYAN}${BOLD}🔹 $1${NC}"; }
ok()    { echo -e "  ${GREEN}✅ $1${NC}"; }
fail()  { echo -e "  ${RED}❌ $1${NC}"; exit 1; }

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACKAGE_PATH="$PROJECT_ROOT/$PACKAGE_NAME"

# ── 1. Verificar SSH ─────────────────────────────────────────
step "Verificando conexión SSH al VPS ($VPS_USER@$VPS_HOST)..."
ssh -o ConnectTimeout=5 -o BatchMode=yes "$VPS_USER@$VPS_HOST" "echo ok" \
  || fail "No se puede conectar al VPS. Verifica la clave SSH."
ok "Conexión SSH exitosa"

# ── 2. Empaquetar backend ─────────────────────────────────────
step "Empaquetando backend (excluyendo .venv, venv, __pycache__, uploads, *.db)..."
cd "$PROJECT_ROOT"
tar -czf "$PACKAGE_NAME" \
  --exclude="back_veterinaria/.venv" \
  --exclude="back_veterinaria/venv" \
  --exclude="back_veterinaria/__pycache__" \
  --exclude="back_veterinaria/app/__pycache__" \
  --exclude="back_veterinaria/uploads" \
  --exclude="back_veterinaria/*.db" \
  --exclude="back_veterinaria/.env" \
  --exclude=".git" \
  back_veterinaria \
  "$COMPOSE_FILE"

SIZE_KB=$(du -k "$PACKAGE_PATH" | cut -f1)
ok "Paquete creado: $PACKAGE_NAME (${SIZE_KB} KB)"

# ── 3. Subir al VPS ──────────────────────────────────────────
step "Subiendo paquete al VPS ($DEPLOY_DIR)..."
ssh "$VPS_USER@$VPS_HOST" "mkdir -p $DEPLOY_DIR"
scp "$PACKAGE_PATH" "$VPS_USER@$VPS_HOST:$DEPLOY_DIR/$PACKAGE_NAME"
ok "Paquete subido correctamente"

# ── 4. Limpiar paquete local ──────────────────────────────────
rm -f "$PACKAGE_PATH"
ok "Paquete local eliminado"

# ── 5. Desplegar en VPS ──────────────────────────────────────
step "Extrayendo y levantando contenedores en el VPS..."
ssh "$VPS_USER@$VPS_HOST" bash <<REMOTE
set -e
cd $DEPLOY_DIR
echo '[VPS] Extrayendo paquete...'
tar -xzf $PACKAGE_NAME
echo '[VPS] Copiando .env.prod si existe en home...'
if [ -f ~/.env.prod.veterinaria ]; then
  cp ~/.env.prod.veterinaria .env.prod
  echo '[VPS] .env.prod copiado desde home'
fi
echo '[VPS] Levantando Docker Compose (producción)...'
docker compose -f $COMPOSE_FILE up -d --build --remove-orphans
echo '[VPS] Estado de contenedores:'
docker compose -f $COMPOSE_FILE ps
echo '[VPS] ✅ Despliegue completado'
REMOTE

echo -e "\n${GREEN}${BOLD}🚀 Despliegue finalizado exitosamente${NC}"
echo -e "   API:    ${CYAN}https://api-veterinaria.efranjs.com${NC}"
echo -e "   Health: ${CYAN}https://api-veterinaria.efranjs.com/api/health${NC}"
echo -e "   Docs:   ${CYAN}https://api-veterinaria.efranjs.com/docs${NC}"
