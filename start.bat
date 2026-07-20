@echo off
echo ========================================
echo    Sales Radar Dashboard
echo    Superstore Sales Analysis
echo ========================================
echo.
echo Starting server...
echo.
echo Access URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.
.venv\Scripts\streamlit run src\app.py
pause
