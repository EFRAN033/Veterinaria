#!/usr/bin/env bash
# setup_cloudflare_vet.sh
# ============================================================
#  Configura el Cloudflare Tunnel para api-veterinaria.efranjs.com
#  ⚠️  Ejecutar UNA SOLA VEZ desde tu máquina local:
#      bash scripts/setup_cloudflare_vet.sh
#
#  Requiere: cloudflared instalado en el VPS, clave SSH lista
# ============================================================

set -euo pipefail

VPS_USER="efran"
VPS_HOST="192.168.1.38"
TUNNEL_UUID="07af7617-b07a-432b-9208-28ef8b78d892"
TUNNEL_HOSTNAME="api-veterinaria.efranjs.com"
TUNNEL_LOCAL_PORT="8000"
CLOUDFLARED_CONFIG="/etc/cloudflared/config.yml"

BOLD='\033[1m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'
step()  { echo -e "\n${CYAN}${BOLD}🔹 $1${NC}"; }
ok()    { echo -e "  ${GREEN}✅ $1${NC}"; }
warn()  { echo -e "  ${YELLOW}⚠️  $1${NC}"; }

step "Conectando al VPS y configurando Cloudflare Tunnel..."
ssh "$VPS_USER@$VPS_HOST" bash <<REMOTE
set -e

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Cloudflare Tunnel Setup — Veterinaria "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Paso 1: Crear ruta DNS en Cloudflare ─────────────────────
echo ""
echo "🔹 1/3 Registrando DNS: $TUNNEL_HOSTNAME → Túnel $TUNNEL_UUID"
cloudflared tunnel route dns $TUNNEL_UUID $TUNNEL_HOSTNAME \
  && echo "  ✅ DNS creado correctamente" \
  || echo "  ⚠️  El DNS ya existe o hubo un problema — verifica en Cloudflare Dashboard"

# ── Paso 2: Verificar estructura del config.yml ───────────────
echo ""
echo "🔹 2/3 Actualizando $CLOUDFLARED_CONFIG..."
CONFIG_FILE="$CLOUDFLARED_CONFIG"

if [ ! -f "\$CONFIG_FILE" ]; then
  echo "  ❌ No se encontró $CLOUDFLARED_CONFIG en el VPS."
  echo "     Asegúrate de que cloudflared está instalado y configurado."
  exit 1
fi

# Verificar si el hostname ya está en el config
if grep -q "$TUNNEL_HOSTNAME" "\$CONFIG_FILE"; then
  echo "  ⚠️  $TUNNEL_HOSTNAME ya existe en el config — omitiendo modificación"
else
  # Hacer backup
  sudo cp "\$CONFIG_FILE" "\${CONFIG_FILE}.bak.\$(date +%Y%m%d_%H%M%S)"
  echo "  📋 Backup creado"

  # Insertar el nuevo ingress ANTES del catch-all (http_status:404 o similar)
  # Usamos Python para manipular el YAML de forma segura
  sudo python3 - <<'PYEOF'
import yaml, sys

CONFIG_PATH = "$CLOUDFLARED_CONFIG"
NEW_INGRESS = {
    "hostname": "$TUNNEL_HOSTNAME",
    "service": "http://localhost:$TUNNEL_LOCAL_PORT"
}

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

if "ingress" not in config:
    config["ingress"] = []

# Insertar antes del catch-all (entrada sin hostname)
ingress = config["ingress"]
catch_all_idx = next(
    (i for i, r in enumerate(ingress) if "hostname" not in r),
    len(ingress)
)
ingress.insert(catch_all_idx, NEW_INGRESS)

with open(CONFIG_PATH, "w") as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

print("  ✅ Ingress añadido correctamente")
PYEOF
fi

# ── Paso 3: Reiniciar cloudflared ────────────────────────────
echo ""
echo "🔹 3/3 Reiniciando servicio cloudflared..."
sudo systemctl restart cloudflared
sleep 2
STATUS=\$(sudo systemctl is-active cloudflared)
if [ "\$STATUS" = "active" ]; then
  echo "  ✅ cloudflared está ACTIVO"
else
  echo "  ❌ cloudflared no está activo. Estado: \$STATUS"
  sudo systemctl status cloudflared --no-pager -l
  exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Configuración del túnel completada"
echo "  🌐 API disponible en: https://$TUNNEL_HOSTNAME"
echo "  🔍 Health check:      https://$TUNNEL_HOSTNAME/api/health"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
REMOTE

echo -e "\n${GREEN}${BOLD}✅ Setup de Cloudflare Tunnel finalizado${NC}"
echo -e "   URL de la API: ${CYAN}https://$TUNNEL_HOSTNAME${NC}"
