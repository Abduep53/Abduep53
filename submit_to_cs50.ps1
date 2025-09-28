# CS50 AI Crossword Project Submission Script
Write-Host "CS50 AI Crossword Project Submission Script" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Setting up Git repository..." -ForegroundColor Yellow
git init

Write-Host ""
Write-Host "Configuring Git with your details..." -ForegroundColor Yellow
git config user.name "Abduep53"
git config user.email "abduyusufbek.2@gmail.com"

Write-Host ""
Write-Host "Adding all project files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "Committing files..." -ForegroundColor Yellow
git commit -m "Submit crossword project for CS50 AI"

Write-Host ""
Write-Host "Adding remote repository..." -ForegroundColor Yellow
git remote add origin https://github.com/me50/Abduep53.git

Write-Host ""
Write-Host "Creating required branch..." -ForegroundColor Yellow
git checkout -b ai50/projects/2024/x/crossword

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin ai50/projects/2024/x/crossword

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Submission complete!" -ForegroundColor Green
Write-Host "Check your progress at: https://cs50.me/cs50ai" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Green
