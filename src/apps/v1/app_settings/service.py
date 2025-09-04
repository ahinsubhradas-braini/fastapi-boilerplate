
# Import python core libary dependices
from fastapi import Depends

# Imports from project or 3rd party libary dependices
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.common.base_service import BaseService
from src.core.db.db_config import get_db
from src.apps.v1.app_settings.models.app_settings import AppSettings

class AppSettingsService(BaseService):
    def __init__(self, db):
        super().__init__(db) # calls BaseService.__init__(db)
    async def create_app_settings(self):
        """
        Create default application settings if they do not exist (async version).
        """
        print("<========= Create application settings ==============>")
        # Check if settings already exist with type 'default'
        try:
            new_application_settings = await self.db.execute(select(AppSettings).where(AppSettings.type == "default"))

            if not new_application_settings.scalars().first():
                deafault_settings = AppSettings(
                    type = "default",
                    data = {
                        "site_name":"My Application",
                        "maintenance_mode": False,
                    }
                )
                self.db.add(deafault_settings)
                await self.db.commit()
        except Exception as e:
            print("Error creating default application settings:", e)