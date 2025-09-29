@echo off
echo CS50 AI Crossword Project Submission Script
echo ==========================================
echo.

echo Setting up Git repository...
git init

echo.
echo Configuring Git with your details...
git config user.name "Abduep53"
git config user.email "abduyusufbek.2@gmail.com"

echo.
echo Adding all project files...
git add .

echo.
echo Committing files...
git commit -m "Submit crossword project for CS50 AI"

echo.
echo Adding remote repository...
git remote add origin https://github.com/me50/Abduep53.git

echo.
echo Creating required branch...
git checkout -b ai50/projects/2024/x/crossword

echo.
echo Pushing to GitHub...
git push -u origin ai50/projects/2024/x/crossword

echo.
echo ==========================================
echo Submission complete!
echo Check your progress at: https://cs50.me/cs50ai
echo ==========================================
pause
