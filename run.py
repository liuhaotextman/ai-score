import uvicorn
import sys
import asyncio
import os

if __name__ == "__main__":
    # Fix for Windows: Force SelectorEventLoopPolicy for psycopg compatibility
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Run Uvicorn via code
    # reload=True enables auto-reload on code changes
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
