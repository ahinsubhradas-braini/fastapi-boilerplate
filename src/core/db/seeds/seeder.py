from src.apps.v1.app_settings.service import AppSettingsService

async def seed_data():
    """
    Seed initial data into the database.
    """
    print("<========= Seeding initial data ==============>")
    service = AppSettingsService(db)
    await AppSettingsService.create_app_settings()
    
    print("Data seeding completed.")
    return "Data seeding completed."

