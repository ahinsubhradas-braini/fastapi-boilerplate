# Imports fastapi dependices
from fastapi import Depends

# Imports from project or 3rd party libary dependices
from core.db.db_config import DbAdmin
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db.db_config import get_db
from sqlalchemy import and_, func, or_, select, delete
from src.apps.v1.users.models.user import User, Resources, Role, UserRoles, RoleResources
class UserService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def create_super_admin(self,name: str = "Super Admin",mail: str = ""):
        """
        Create a default super admin user if none exist.
        """
        try:
            existing_super_admin_role =await self.db.execute(select(Role).where(Role.name == "super_admin"))

            if not existing_super_admin_role:
                
                # Remove all existing resources
                await self.db.execute(select(delete(Resources)))
                # Create super admin resources first: Later we will take all resource from json file
                super_admin_resources = [
                    {"get_users"}, 
                    {"create_user"},
                    {"update_user"},
                    {"delete_user"}
                ]
                
                # We can avoid for loop here, but for clarity we are using for loop
                for resource in super_admin_resources:
                    create_resources_for_super_admin = Resources(
                        name=resource,
                        description=f"Permission to {resource.replace('_', ' ')}"
                    )
                    self.db.add(create_resources_for_super_admin)
                    await self.db.commit()
                    await self.db.refresh(create_resources_for_super_admin)
                
                # Create super admin role
                create_super_admin_role = Role(
                    name="super_admin",
                    description="Role with all permissions"
                )
                self.db.add(create_super_admin_role)
                await self.db.commit()

                # Assign role to resources: RoleResources
                get_superadmin_role = await self.db.execute(select(Role).where(Role.name == "super_admin"))
                
                fetch_all_resources = await self.db.execute(select(Resources))
                all_resources = fetch_all_resources.scalars().all()

                for resource in all_resources:
                    assign_role_to_resources = RoleResources(
                        role_id=get_superadmin_role.scalars().first().id,
                        resource_id=resource.id
                    )
                    self.db.add(assign_role_to_resources)
                    await self.db.commit()

                # Create super admin user
                create_super_admin_user = User(
                    username=name,
                    email=mail if mail else "superadmin@yopmail.com"
                )

                self.db.add(create_super_admin_user)
                await self.db.commit()

                # Assign super admin role to the user
                get_super_admin_user = await self.db.execute(select(User).where(User.email == (mail if mail else "superadmin@yopmailcom")))

                assign_role_to_super_admin_user = UserRoles(
                    user_id=get_super_admin_user.scalars().first().id,
                    role_id=get_superadmin_role.scalars().first().id
                )
                self.db.add(assign_role_to_super_admin_user)
                await self.db.commit()
        except Exception as e:
            print("Error creating super admin user:", e)