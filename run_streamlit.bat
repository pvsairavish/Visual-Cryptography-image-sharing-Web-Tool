@echo off
title Visual Cryptography Streamlit App
echo ========================================================
echo   Launching Visual Cryptography Tool in Streamlit...
echo ========================================================
echo.

IF EXIST "venv\Scripts\streamlit.exe" (
    venv\Scripts\streamlit.exe run streamlit_app.py
) ELSE (
    streamlit run streamlit_app.py
)

pause

