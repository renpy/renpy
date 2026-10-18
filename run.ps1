# This builds out of date modules using mingw32, and then runs them.

$ErrorActionPreference = "Stop"

$env:RENPY_CYTHON = "cython"

$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$QUIET = if ($env:RENPY_QUIET) { $env:RENPY_QUIET } else { "--quiet" }
$BUILD_ONLY = $false
$CLEAN = $false

# Parse our own flags; stop at the first unknown argument.
while ($args.Count -gt 0) {
    switch ($args[0]) {
        "--build" { $BUILD_ONLY = $true; $args = $args[1..($args.Count - 1)] }
        "--clean" { $CLEAN = $true; $args = $args[1..($args.Count - 1)] }
        "--" { $args = $args[1..($args.Count - 1)]; break }
        default { break }
    }
    if ($args[0] -notin @("--build", "--clean", "--")) { break }
}

if ($CLEAN) {
    Remove-Item "$ROOT\*.cpython*.pyd" -ErrorAction SilentlyContinue
    Get-ChildItem "$ROOT\renpy" -Recurse -Filter "*.cpython*.pyd" |
    Remove-Item -ErrorAction SilentlyContinue
}

if ($env:RENPY_COVERAGE) {
    $variant = "renpy-coverage"
}
else {
    $variant = "renpy-run"
}

if ($env:RENPY_VIRTUAL_ENV) {
    . "$env:RENPY_VIRTUAL_ENV\Scripts\Activate.ps1"
}

if (-not $env:VIRTUAL_ENV) {
    if (Test-Path "$ROOT\.venv") {
        . "$ROOT\.venv\Scripts\Activate.ps1"
    }
    else {
        Write-Host "Please use 'uv sync' to create the virtual environment."
        exit 1
    }
}

$CPUS = (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors
$BUILD_J = @("--parallel", "$CPUS")

if (Test-Path "$ROOT\cubism") {
    $env:CUBISM = "$ROOT\cubism"
    if (-not $env:CUBISM_PLATFORM) {
        $env:CUBISM_PLATFORM = "windows/x86_64"
    }
    $env:PATH = "$env:CUBISM\Core\dll\$env:CUBISM_PLATFORM;$env:PATH"
}

Push-Location $ROOT
try {
    python setup.py $QUIET build_ext --compiler=mingw32 `
        -b "tmp/build/lib.$variant" -t "tmp/build/tmp.$variant" `
        --inplace @BUILD_J
    if ($LASTEXITCODE -ne 0) { exit 1 }
}
finally {
    Pop-Location
}

if ($BUILD_ONLY) {
    Write-Host "Ren'Py build complete."
    exit 0
}

python -X utf8 "$ROOT\renpy.py" @args
exit $LASTEXITCODE
