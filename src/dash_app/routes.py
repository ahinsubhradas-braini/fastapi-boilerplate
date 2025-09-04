# Import python core libary dependices
import os

# Imports from project or 3rd party libary dependices
from fastapi import APIRouter, Request, HTTPException
from starlette.responses import HTMLResponse
from src.core.config import get_settings
from src.core.db.seeds.seeder import seed_data
from src.apps.v1.users.service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.database_dependencies import get_async_session
from fastapi import Depends

settings = get_settings()

router = APIRouter(include_in_schema=False)

@router.get("/dev_dash")
async def dash_login_page():
    return HTMLResponse(
        """
    <h2>Developer Dashboard</h2>
    <button onclick="runSeeder()">Seed Data and Process</button>
    <button onclick="openPopup()">Add Super Admin</button>
    <div id="output" style="margin-top: 20px;"></div>
    
    # Popup modal for adding super admin
    <!-- Popup Modal -->
    <div id="popup" style="display:none; position:fixed; top:30%; left:40%; background:white; padding:20px; border:1px solid #ccc;">
        <h3>Add Super Admin</h3>
        <input type="email" id="superAdminEmail" placeholder="Enter Super Admin Email" style="width: 100%; padding:5px;" />
        <br><br>
        <button onclick="submitSuperAdmin()">Submit</button>
        <button onclick="closePopup()">Cancel</button>
    </div>

    
    # To seeding data
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

        function openPopup() {
            document.getElementById('popup').style.display = 'block';
        }

        function closePopup() {
            document.getElementById('popup').style.display = 'none';
        }

        async function submitSuperAdmin() {
            const email = document.getElementById('superAdminEmail').value;
            if (!email) {
                alert("Please enter a valid email.");
                return;
            }
            try {
                const response = await fetch('/dev_dash/add-super-admin', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ email: email })
                });
                if (response.ok) {
                    alert("Super Admin added successfully!");
                } else {
                    const err = await response.json();
                    alert("Error: " + err.detail);
                }
            } catch (error) {
                alert("Request failed: " + error.message);
            }
            closePopup();
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
        print("Error during seeding:", e)

@router.post("/dev_dash/add-super-admin")
async def add_super_admin(request: Request,db: AsyncSession = Depends(get_async_session)):
    try:
        form_data = await request.form()
        email = form_data.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email is required.")
        else:
            await UserService.create_super_admin(db,email)
    except Exception as e:
        print("Error during adding super admin:", e)
