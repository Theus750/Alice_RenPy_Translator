$ErrorActionPreference = "Stop"

Set-Location -LiteralPath (Join-Path $PSScriptRoot "..")

python -m PyInstaller --clean --noconfirm packaging\alice.spec

Write-Host "Executável criado em dist\Alice.exe"
