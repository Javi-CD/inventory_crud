@echo off
echo Creating executable..

rem switch to the root directory of the project
cd ..

rem Create build directory if it doesn't exist
if not exist build mkdir build

rem Run PyInstaller with all required parameters
pyinstaller --clean ^
    --onefile ^
    --windowed ^
    --name "InventoryManager" ^
    --add-data "src/db/inventory.db;src/db" ^
    --add-data "assets/login_img.webp;assets" ^
    --distpath "build" ^
    main.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo Build completed successfully!
    echo Your executable is available at: build\InventoryManager.exe
) else (
    echo Build failed with error code: %ERRORLEVEL%
)

pause