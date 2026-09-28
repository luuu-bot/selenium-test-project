@echo off
chcp 65001 >nul
echo 正在打开最新的测试报告...

cd /d "%~dp0reports"

:: 找到最新的 html 文件
for /f "delims=" %%i in ('dir /b /o-d *.html 2^>nul') do (
    start "" "%%i"
    goto :done
)

echo 没有找到报告文件，请先运行测试！
pause

:done
