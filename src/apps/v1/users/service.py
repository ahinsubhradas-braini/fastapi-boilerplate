# Imports from project or 3rd party libary dependices
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, or_, select, delete
from src.apps.v1.users.models.user import User, Resources, Role, UserRoles, RoleResources
class UserService:
    async def create_super_admin(db: AsyncSession,mail: str):
        """
        Create a default super admin user if none exist.
        """
        try:
            existing_super_admin_role =await db.execute(select(Role).where(Role.name == "super_admin"))
            print("existing_super_admin_role:",existing_super_admin_role)

            if not existing_super_admin_role.scalars().first():
                print("1111111111")
                # Create super admin resources first: Later we will take all resource from json file
                super_admin_resources = [
                    {"get_users"}, 
                    {"create_user"},
                    {"update_user"},
                    {"delete_user"}
                ]
                print("333333333333")
                # We can avoid for loop here, but for clarity we are using for loop
                for resource in super_admin_resources:
                    resource_name = list(resource)[0]
                    print("44444444444")
                    create_resources_for_super_admin = Resources(
                        name=resource_name,
                        description=f"Permission to {resource_name.replace('_', ' ')}"
                    )
                    db.add(create_resources_for_super_admin)
                    await db.commit()
                    print("4.5 ===>")
                
                # Create super admin role
                create_super_admin_role = Role(
                    name="super_admin",
                    description="Role with all permissions"
                )
                db.add(create_super_admin_role)
                await db.commit()
                print("555555555555")
                # Assign role to resources: RoleResources
                get_superadmin_role = await db.execute(select(Role).where(Role.name == "super_admin"))
                
                fetch_all_resources = await db.execute(select(Resources))
                all_resources = fetch_all_resources.scalars().all()
                print("66666666666")
                for resource in all_resources:
                    assign_role_to_resources = RoleResources(
                        role_id=get_superadmin_role.scalars().first().id,
                        resource_id=resource.id
                    )
                    print("88888888888")
                    db.add(assign_role_to_resources)
                    await db.commit()

                # Create super admin user
                create_super_admin_user = User(
                    full_name="Super Admin",
                    first_name="Super",
                    last_name="Admin",
                    username=mail,
                    email=mail if mail else "superadmin@yopmail.com"
                )
                print("99999999999")
                db.add(create_super_admin_user)
                await db.commit()

                # Assign super admin role to the user
                get_super_admin_user = await db.execute(select(User).where(User.email == (mail if mail else "superadmin@yopmailcom")))
                print("100000000000000")
                assign_role_to_super_admin_user = UserRoles(
                    user_id=get_super_admin_user.scalars().first().id,
                    role_id=get_superadmin_role.scalars().first().id
                )
                db.add(assign_role_to_super_admin_user)
                await db.commit()
        except Exception as e:
            print("Error creating super admin user:", e)