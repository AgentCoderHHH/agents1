@echo off
curl.exe -X POST "http://localhost:3001/execute" -H "Content-Type: application/json" -d "{\"topic\": \"Planning Agent in agentic world\", \"reasoning_effort\": \"balanced\"}"
pause 