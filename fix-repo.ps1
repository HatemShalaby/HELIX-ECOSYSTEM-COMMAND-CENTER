# --- 1. Rename Root Folders to Remove Spaces ---
$parent = "H:\AI Automation Engineering"
$oldRoot = "$parent\Command Center Project"
$newRoot = "$parent\Command_Center_Project"

If (Test-Path $newRoot) {
    Write-Host "Target folder already exists. Please confirm old folders before proceeding."
} ElseIf (Test-Path $oldRoot) {
    Rename-Item -Path $oldRoot -NewName "Command_Center_Project"
    Write-Host "Root folder renamed."
}

# --- 2. Navigate to 00_command_center Folder ---
$projectFolder = "$newRoot\00_command_center"
cd $projectFolder

# --- 3. Create .gitignore ---
$gitignoreContent = @"
# Python cache files
__pycache__/
*.pyc
*.pyo
*.pyd

# Compiled binaries
*.exe
*.out
*.dll
*.bin

# OS-specific files
.DS_Store
Thumbs.db
"@
Set-Content -Path ".gitignore" -Value $gitignoreContent
Write-Host ".gitignore created."

# --- 4. Remove Tracked Cache/Binary Files ---
git rm --cached -r __pycache__ | Out-Null
git rm --cached *.pyc,*.pyo,*.pyd,*.exe,*.out,*.dll,*.bin | Out-Null
Write-Host "Removed tracked Python cache and binary files from Git."

# --- 5. Create README.md ---
$readmeContent = @"
# Command Center Project

## Overview
This project provides tools and automation for AI-assisted engineering processes. It supports centralized command and control operations.

## Getting Started
1. Clone the repository
   git clone <repo-link>
2. Set up dependencies
   pip install -r requirements.txt
3. Usage instructions here...

## Features
- Centralized command interface
- Python automation scripts
- Modular architecture

## Contributing
Please submit issues and pull requests via GitHub.

## License
See LICENSE for details.
"@
Set-Content -Path "README.md" -Value $readmeContent
Write-Host "README.md created."

# --- 6. Create LICENSE (MIT Example) ---
$licenseContent = @"
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"@
Set-Content -Path "LICENSE" -Value $licenseContent
Write-Host "LICENSE created."

# --- 7. Add, Commit, and Push Changes ---
git add .gitignore README.md LICENSE
git add -A # Add all other changes
git commit -m "Repo maintenance: folder names, .gitignore, README, LICENSE"
git push
Write-Host "All fixes applied and changes pushed to GitHub."