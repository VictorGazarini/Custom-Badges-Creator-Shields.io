# test-local.ps1 - Smoke test for local app (PowerShell)
# Usage: Open PowerShell in project root and run: .\test-local.ps1

$baseUrl = 'http://localhost:5000'

function Test-Health {
    try {
        $r = Invoke-RestMethod -Uri "$baseUrl/api/healthz" -TimeoutSec 5
        Write-Host "[OK] Health:" ($r | ConvertTo-Json -Compress)
        return $true
    } catch {
        Write-Host "[FAIL] Health check failed: $_"
        return $false
    }
}

function Test-Generate {
    $body = @{ label='BUILD'; message='PASSING'; color='brightgreen' } | ConvertTo-Json
    try {
        $r = Invoke-RestMethod -Method POST -Uri "$baseUrl/api/generate" -ContentType 'application/json' -Body $body -TimeoutSec 5
        Write-Host "[OK] Generate:" ($r | ConvertTo-Json -Compress)
        return $true
    } catch {
        Write-Host "[FAIL] Generate failed: $_"
        return $false
    }
}

Write-Host "== Local smoke test: $baseUrl =="

if (Test-Health) {
    Test-Generate | Out-Null
    Write-Host "SMOKE TEST: OK (service responding)"
    exit 0
}

# If health failed, try to use Docker to start the container
Write-Host "Service not responding. Trying to start via Docker (if available)..."

$dockerAvailable = $false
try { docker version > $null 2>&1; $dockerAvailable = $true } catch { $dockerAvailable = $false }

if (-not $dockerAvailable) {
    Write-Host "Docker not available. Start the app (venv) or enable Docker, then re-run this script."
    exit 2
}

# Check existing container
$cid = docker ps -a --filter "name=custom-shields-creator" --format "{{.ID}}"
if ($cid) {
    $status = docker ps --filter "name=custom-shields-creator" --format "{{.Status}}"
    if (-not $status) {
        Write-Host "Starting existing container..."
        docker start custom-shields-creator | Out-Null
    } else {
        Write-Host "Container already running: $status"
    }
} else {
    Write-Host "Building image and running container... (this may take a minute)"
    if (-not (Test-Path -Path "Dockerfile")) { Write-Host "Dockerfile not found in current folder"; exit 3 }
    $buildOk = (docker build -t custom-shields-creator .) -eq 0
    if (-not $buildOk) { Write-Host "Docker build failed"; exit 4 }
    docker run --rm -d -p 5000:5000 --name custom-shields-creator custom-shields-creator | Out-Null
}

# wait for service
Write-Host "Waiting for service to become available..."
for ($i=0; $i -lt 20; $i++) {
    Start-Sleep -s 1
    if (Test-Health) {
        Test-Generate | Out-Null
        Write-Host "SMOKE TEST: OK (service started via Docker)"
        exit 0
    }
}

Write-Host "Service did not become available. Check container logs: docker logs custom-shields-creator --tail 200"
exit 5
