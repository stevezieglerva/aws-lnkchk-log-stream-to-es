echo off

git diff

set /p msg="Enter commit message: "
echo %msg%

git add --all
git commit -m "%msg%"
git push

