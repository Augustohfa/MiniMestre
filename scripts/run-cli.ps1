# Runs the CLI using the src layout
$env:PYTHONPATH = "$PSScriptRoot\..\src"
python -m unimestre.cli.main
