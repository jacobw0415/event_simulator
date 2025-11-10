@echo off
REM ============================================================
REM 🚀 Event Simulator 自動部署腳本
REM 位置: C:\Users\Admin\Documents\event_simulator
REM 功能: 停止、刪除、重新建置並啟動容器
REM ============================================================

cd /d "C:\Users\Admin\Documents\event_simulator"

echo.
echo [1/4] 🔻 停止舊容器...
docker compose stop event-simulator

echo.
echo [2/4] 🗑️  移除舊容器...
docker compose rm -f event-simulator

echo.
echo [3/4] 🏗️  重新建置映像檔（含最新 main.py / generator.py）...
docker compose build --no-cache event-simulator

echo.
echo [4/4] 🚀 啟動新版本容器...
docker compose up -d event-simulator

echo.
echo ✅ 部署完成，以下為最新 10 筆 log：
docker compose logs --tail=10 event-simulator

echo.
pause
