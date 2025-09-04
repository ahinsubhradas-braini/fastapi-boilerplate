from src.core.db.db_config import get_db
from src.apps.v1.app_settings.service import AppSettingsService

async def seed_data():
    """
    Seed initial data into the database.
    """
    print("<========= Seeding initial data ==============>")
    async with get_db() as db:
        await AppSettingsService.create_app_settings(db)
    
    print("Data seeding completed.")
    return "Data seeding completed."