@echo off
title Push Updates to GitHub
echo ========================================================
echo   Updating GitHub Repository:
echo   https://github.com/pvsairavish/Visual-Cryptography-image-sharing-Web-Tool.git
echo ========================================================
echo.

:: Initialize git repository if not already initialized
IF NOT EXIST ".git" (
    echo [1/5] Initializing Git repository...
    git init
) ELSE (
    echo [1/5] Git repository already initialized.
)

:: Set remote URL
echo [2/5] Configuring remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/pvsairavish/Visual-Cryptography-image-sharing-Web-Tool.git

:: Add all files (respecting .gitignore to omit venv and database)
echo [3/5] Staging files...
git add .

:: Commit
echo [4/5] Committing changes...
git commit -m "feat: upgrade to Streamlit v2.0 Studio with Obsidian Cyber UI, lossless XOR secret sharing, and entropy analysis"

:: Set branch to main and push
echo [5/5] Pushing to GitHub (main branch)...
git branch -M main
git push -u origin main --force

echo.
echo ========================================================
echo   Done! Check your repository at:
echo   https://github.com/pvsairavish/Visual-Cryptography-image-sharing-Web-Tool
echo ========================================================
pause
