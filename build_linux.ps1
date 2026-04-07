# PowerShell Script to build Square Survivor for Linux using Docker

$ImageName = "square-survivor-linux-build"
$ContainerName = "square-survivor-build-temp"
$OutputDir = Join-Path (Get-Location) "dist/linux"

# 1. Ensure output directory exists
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
    Write-Host "Created directory: $OutputDir" -ForegroundColor Cyan
}

# 2. Build the Docker image
Write-Host "Building Docker image: $ImageName..." -ForegroundColor Yellow
docker build -t $ImageName -f Dockerfile.linux .

if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build failed!"
    exit 1
}

# 3. Create a temporary container to extract the binary
Write-Host "Extracting Linux binary..." -ForegroundColor Yellow
if (docker ps -a --format '{{.Names}}' | Select-String -Quiet $ContainerName) {
    docker rm $ContainerName | Out-Null
}

docker create --name $ContainerName $ImageName
docker cp "${ContainerName}:/app/dist/." $OutputDir
docker rm $ContainerName | Out-Null

Write-Host "`nBuild complete! The Linux binary is at: $OutputDir" -ForegroundColor Green
Write-Host "To run on Linux:" -ForegroundColor Green
Write-Host "1. chmod +x $OutputDir/SquareSurvivor" -ForegroundColor White
Write-Host "2. ./$OutputDir/SquareSurvivor" -ForegroundColor White
