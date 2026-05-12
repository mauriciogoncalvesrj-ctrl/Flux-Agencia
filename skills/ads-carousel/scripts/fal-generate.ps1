# fal-generate.ps1
# Chama Fal.AI Recraft v3 via REST API para gerar imagens do padrao Flux.
# Uso:
#   .\fal-generate.ps1 -Prompt "texto" -OutFile "slide-1.png" [-Width 1080] [-Height 1350] [-Style "realistic_image"]
#
# Le FAL_KEY de:
#   1. $env:FAL_KEY
#   2. .env no diretorio atual
#   3. C:\Users\windows\.claude\projects\c--Users-windows--claude\docs\creative\flux-brand\.env

param(
    [Parameter(Mandatory=$true)][string]$Prompt,
    [Parameter(Mandatory=$true)][string]$OutFile,
    [int]$Width = 1080,
    [int]$Height = 1350,
    [string]$Style = "realistic_image",
    [string]$NegativePrompt = "",
    [string[]]$Colors = @()
)

# --- Resolver FAL_KEY ---
$falKey = $env:FAL_KEY
if (-not $falKey) {
    $envCandidates = @(
        (Join-Path (Get-Location) ".env"),
        "C:\Users\windows\.claude\projects\c--Users-windows--claude\docs\creative\flux-brand\.env"
    )
    foreach ($envPath in $envCandidates) {
        if (Test-Path $envPath) {
            $line = (Get-Content $envPath | Where-Object { $_ -match "^FAL_KEY=" } | Select-Object -First 1)
            if ($line) {
                $falKey = $line.Substring(8).Trim()
                break
            }
        }
    }
}

if (-not $falKey) {
    Write-Error "FAL_KEY nao encontrada (env var nem .env)."
    exit 1
}

# --- Payload Recraft v3 ---
# Endpoint: https://queue.fal.run/fal-ai/recraft-v3
# Recraft v3 suporta image_size {width, height}, style, colors (hex), negative_prompt
$payload = @{
    prompt = $Prompt
    image_size = @{ width = $Width; height = $Height }
    style = $Style
}
if ($NegativePrompt) { $payload.negative_prompt = $NegativePrompt }
if ($Colors.Count -gt 0) {
    $payload.colors = @($Colors | ForEach-Object {
        # Aceita "#C9A961" ou "201,169,97"
        if ($_ -match "^#([0-9A-Fa-f]{6})$") {
            $hex = $matches[1]
            @{
                r = [Convert]::ToInt32($hex.Substring(0,2), 16)
                g = [Convert]::ToInt32($hex.Substring(2,2), 16)
                b = [Convert]::ToInt32($hex.Substring(4,2), 16)
            }
        } else { $null }
    } | Where-Object { $_ })
}

$jsonBody = $payload | ConvertTo-Json -Depth 6 -Compress
$headers = @{
    "Authorization" = "Key $falKey"
    "Content-Type"  = "application/json"
}

Write-Host "[fal] Enviando para Recraft v3..."
Write-Host "[fal] Tamanho: ${Width}x${Height} | Style: $Style"

try {
    $submitUrl = "https://queue.fal.run/fal-ai/recraft-v3"
    $submit = Invoke-RestMethod -Uri $submitUrl -Method POST -Headers $headers -Body $jsonBody -TimeoutSec 60
} catch {
    Write-Error "[fal] Erro no submit: $($_.Exception.Message)"
    if ($_.ErrorDetails) { Write-Error $_.ErrorDetails.Message }
    exit 2
}

$requestId = $submit.request_id
$statusUrl = $submit.status_url
$responseUrl = $submit.response_url
Write-Host "[fal] request_id=$requestId — fazendo polling..."

# --- Polling ---
$maxAttempts = 60
$attempt = 0
$completed = $false
while (-not $completed -and $attempt -lt $maxAttempts) {
    Start-Sleep -Seconds 3
    $attempt++
    try {
        $status = Invoke-RestMethod -Uri $statusUrl -Method GET -Headers $headers -TimeoutSec 30
    } catch {
        Write-Host "[fal] Polling tentativa $attempt falhou: $($_.Exception.Message)"
        continue
    }
    if ($status.status -eq "COMPLETED") {
        $completed = $true
        Write-Host "[fal] Geracao completa (tentativa $attempt)."
    } elseif ($status.status -eq "FAILED") {
        Write-Error "[fal] Geracao falhou: $($status | ConvertTo-Json -Depth 5)"
        exit 3
    } else {
        Write-Host "[fal] Status: $($status.status) (tentativa $attempt/$maxAttempts)"
    }
}

if (-not $completed) {
    Write-Error "[fal] Timeout no polling apos $maxAttempts tentativas."
    exit 4
}

# --- Buscar resultado final ---
try {
    $result = Invoke-RestMethod -Uri $responseUrl -Method GET -Headers $headers -TimeoutSec 30
} catch {
    Write-Error "[fal] Erro ao buscar resultado: $($_.Exception.Message)"
    exit 5
}

$imageUrl = $result.images[0].url
if (-not $imageUrl) {
    Write-Error "[fal] Resposta sem URL de imagem: $($result | ConvertTo-Json -Depth 5)"
    exit 6
}

Write-Host "[fal] URL: $imageUrl"

# --- Download ---
$outDir = Split-Path $OutFile -Parent
if ($outDir -and -not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}
Invoke-WebRequest -Uri $imageUrl -OutFile $OutFile -TimeoutSec 60
Write-Host "[fal] Salvo: $OutFile"

# --- Output JSON para parseamento ---
$resultJson = @{
    request_id = $requestId
    image_url  = $imageUrl
    out_file   = $OutFile
    width      = $Width
    height     = $Height
    style      = $Style
} | ConvertTo-Json -Compress
Write-Output $resultJson
