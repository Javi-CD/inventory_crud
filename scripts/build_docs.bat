@echo off
REM Build Sphinx documentation (HTML) for Inventory CRUD

REM Change to the documentation directory
cd ..\docs

REM Generates HTML documentation
sphinx-build -b html source .\build\index.html

REM Success message
if %ERRORLEVEL%==0 (
    echo Documentation built successfully! Output: docs\build\index.html
) else (
    echo Error building documentation.
)

pause
