param(
    [string]$VPS_USER = "efran",
    [string]$VPS_HOST = "192.168.1.38",
    [string]$DEPLOY_DIR = "~/veterinaria_deploy",
    [string]$COMPOSE_FILE = "docker-compose.prod.yml"
)

$ErrorActionPreference = "Stop"

function Write-Step { param($msg) Write-Host "`n[STEP] $msg" -ForegroundColor Cyan }
function Write-OK   { param($msg) Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Fail { param($msg) Write-Host "  [ERROR] $msg" -ForegroundColor Red; exit 1 }

$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
$PACKAGE_NAME = "veterinaria_backend.tar.gz"
$PACKAGE_PATH = Join-Path $PROJECT_ROOT $PACKAGE_NAME

Write-Step "Verificando conexion SSH al VPS (${VPS_USER}@${VPS_HOST})..."
$sshTest = ssh -o ConnectTimeout=5 -o BatchMode=yes "${VPS_USER}@${VPS_HOST}" "echo ok" 2>&1
if ($LASTEXITCODE -ne 0) { Write-Fail "No se puede conectar al VPS. Verifica que la clave SSH este configurada." }
Write-OK "Conexion SSH exitosa"

Write-Step "Empaquetando backend (excluyendo .venv, venv, __pycache__, uploads, *.db)..."
Push-Location $PROJECT_ROOT
tar -czf $PACKAGE_NAME `
    --exclude="back_veterinaria/.venv" `
    --exclude="back_veterinaria/venv" `
    --exclude="back_veterinaria/__pycache__" `
    --exclude="back_veterinaria/uploads" `
    --exclude="back_veterinaria/*.db" `
    --exclude="back_veterinaria/.env" `
    --exclude=".git" `
    back_veterinaria `
    docker-compose.prod.yml
Pop-Location

if (-not (Test-Path $PACKAGE_PATH)) { Write-Fail "No se genero el paquete tar.gz" }
$sizeKB = [math]::Round((Get-Item $PACKAGE_PATH).Length / 1KB, 1)
Write-OK "Paquete creado: $PACKAGE_NAME ($sizeKB KB)"

Write-Step "Subiendo paquete al VPS ($DEPLOY_DIR)..."
ssh "${VPS_USER}@${VPS_HOST}" "mkdir -p $DEPLOY_DIR"
scp $PACKAGE_PATH "${VPS_USER}@${VPS_HOST}:${DEPLOY_DIR}/${PACKAGE_NAME}"
if ($LASTEXITCODE -ne 0) { Write-Fail "Error en SCP" }
Write-OK "Paquete subido correctamente"

Remove-Item $PACKAGE_PATH -Force
Write-OK "Paquete local eliminado"

Write-Step "Extrayendo y levantando contenedores en el VPS..."
$REMOTE_CMD = "set -e; cd $DEPLOY_DIR; echo '[VPS] Extrayendo...'; tar -xzf $PACKAGE_NAME; echo '[VPS] Copiando .env.prod...'; if [ -f ~/.env.prod.veterinaria ]; then cp ~/.env.prod.veterinaria .env.prod; echo '[VPS] .env.prod copiado'; fi; echo '[VPS] Iniciando Docker Compose...'; docker compose -f $COMPOSE_FILE up -d --build --remove-orphans; echo '[VPS] Estado:'; docker compose -f $COMPOSE_FILE ps; echo '[VPS] Despliegue completado'"

ssh "${VPS_USER}@${VPS_HOST}" $REMOTE_CMD
if ($LASTEXITCODE -ne 0) { Write-Fail "Error durante el despliegue remoto" }

Write-Host "`n[DONE] Despliegue finalizado exitosamente" -ForegroundColor Green
Write-Host "  API:    https://api-veterinaria.efranjs.com" -ForegroundColor Yellow
Write-Host "  Health: https://api-veterinaria.efranjs.com/api/health" -ForegroundColor Yellow
Write-Host "  Docs:   https://api-veterinaria.efranjs.com/docs" -ForegroundColor Yellow
