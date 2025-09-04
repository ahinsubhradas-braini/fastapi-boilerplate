# Import python core libary dependices
import os

# Imports from project or 3rd party libary dependices
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import HTMLResponse
from src.core.config import get_settings
from src.core.db.seeds.seeder import seed_data

settings = get_settings()

router = APIRouter(include_in_schema=False)

@router.get("/dev_dash")
async def dash_login_page():
    return HTMLResponse(
        """
    <h2>Developer Dashboard</h2>
    <button onclick="runSeeder()">Seed Data and Process</button>
    <div id="output" style="margin-top: 20px;"></div>
    
    <script>
        async function runSeeder() {
            const outputDiv = document.getElementById('output');
            outputDiv.innerHTML = 'Processing...';
            
            try {
                const response = await fetch('/dev_dash/run-seeder', {
                    method: 'POST'
                });
                outputDiv.innerHTML = `
                    <p>Data seeding completed!</p>
                `;
            } catch (error) {
                outputDiv.innerHTML = `<p>Error: ${error.message}</p>`;
            }
        }
    </script>
    """)

@router.post("/dev_dash/run-seeder")
async def run_seeder():
    try:
        # Call the seed_data function to seed initial data
        print("11111111111")
        await seed_data()

        return {"status": "success", "output": "Application settings created or already exist."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))