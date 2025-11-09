"""
Migrate existing User records to UserAccount and UserProfile content instances.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from models.user import User
from models.content_type import ContentTypeModel, ContentInstanceModel
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Role mapping from old User.role to new UserProfile.role
ROLE_MAPPING = {
    "teacher": "teacher",
    "author": "content_author",
    "editor": "content_author",
    "knowledge_engineer": "admin",
    "admin": "admin"
}


def migrate_users():
    """Migrate User records to UserAccount and UserProfile instances."""
    print("=" * 80)
    print("MIGRATING USERS TO CONTENT TYPE SYSTEM")
    print("=" * 80)

    db = SessionLocal()

    try:
        # Get content type definitions
        user_account_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "UserAccount"
        ).first()
        user_profile_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "UserProfile"
        ).first()

        if not user_account_type or not user_profile_type:
            print("❌ ERROR: UserAccount or UserProfile content types not found!")
            return False

        print(f"\n✓ Found UserAccount content type: {user_account_type.id}")
        print(f"✓ Found UserProfile content type: {user_profile_type.id}")

        # Get all users
        users = db.query(User).all()
        print(f"\n✓ Found {len(users)} users to migrate")

        # Track migration results
        migrated_accounts = 0
        migrated_profiles = 0
        skipped = 0
        superusers = 0

        for user in users:
            print(f"\n{'=' * 60}")
            print(f"Processing user: {user.email} (ID: {user.id}, Role: {user.role})")

            # Check if user is superuser
            is_superuser = user.is_superuser
            if is_superuser:
                superusers += 1
                print(f"  ⚠️  SuperUser detected - will have cross-tenant access")

            # Generate user_id (use email as base for uniqueness)
            user_id = f"user-{user.id}"

            # Check if UserAccount already exists for this user
            existing_accounts = db.query(ContentInstanceModel).filter(
                ContentInstanceModel.content_type_id == user_account_type.id
            ).all()

            account_exists = False
            for acc in existing_accounts:
                if acc.data.get("email") == user.email:
                    account_exists = True
                    print(f"  ⚠️  UserAccount already exists for {user.email}")
                    break

            if not account_exists:
                # Create UserAccount instance
                account_data = {
                    "user_id": user_id,
                    "tenant_id": "default-tenant",  # All users start in default tenant
                    "primary_org_id": "default-org",  # All users start in default org
                    "email": user.email,
                    "locale": "en-US",
                    "status": "active" if user.is_active else "inactive"
                }

                account_instance = ContentInstanceModel(
                    id=str(uuid.uuid4()),
                    content_type_id=user_account_type.id,
                    data=account_data,
                    status="published",
                    created_by=user.id
                )

                db.add(account_instance)
                migrated_accounts += 1

                print(f"  ✓ Created UserAccount: {user_id}")
                print(f"    - Email: {user.email}")
                print(f"    - Tenant: {account_data['tenant_id']}")
                print(f"    - Org: {account_data['primary_org_id']}")
                print(f"    - Status: {account_data['status']}")

            # Check if UserProfile already exists
            existing_profiles = db.query(ContentInstanceModel).filter(
                ContentInstanceModel.content_type_id == user_profile_type.id
            ).all()

            profile_exists = False
            for prof in existing_profiles:
                if prof.data.get("user_id") == user_id:
                    profile_exists = True
                    print(f"  ⚠️  UserProfile already exists for {user_id}")
                    break

            if not profile_exists:
                # Map role
                new_role = ROLE_MAPPING.get(user.role, "teacher")

                # Create UserProfile instance with role-specific attributes
                profile_data = {
                    "user_id": user_id,
                    "role": new_role,
                    "attrs": {
                        "full_name": user.full_name or "",
                        "original_role": user.role,  # Keep original role for reference
                        "is_superuser": is_superuser,  # Flag for cross-tenant access
                        "migrated_from_user_id": user.id,
                        "preferences": user.preferences or "{}"
                    },
                    "accommodations": None,
                    "grades": [],
                    "subjects": []
                }

                profile_instance = ContentInstanceModel(
                    id=str(uuid.uuid4()),
                    content_type_id=user_profile_type.id,
                    data=profile_data,
                    status="published",
                    created_by=user.id
                )

                db.add(profile_instance)
                migrated_profiles += 1

                print(f"  ✓ Created UserProfile:")
                print(f"    - User ID: {user_id}")
                print(f"    - Role: {new_role} (was: {user.role})")
                print(f"    - Full Name: {user.full_name}")
                if is_superuser:
                    print(f"    - SuperUser: YES (cross-tenant access)")

            if account_exists and profile_exists:
                skipped += 1

        # Commit all changes
        db.commit()

        # Verification
        print("\n" + "=" * 80)
        print("MIGRATION COMPLETE")
        print("=" * 80)

        print(f"\nResults:")
        print(f"  Users processed: {len(users)}")
        print(f"  UserAccounts created: {migrated_accounts}")
        print(f"  UserProfiles created: {migrated_profiles}")
        print(f"  SuperUsers: {superusers}")
        print(f"  Already existed: {skipped}")

        # Show final counts
        total_accounts = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == user_account_type.id
        ).count()

        total_profiles = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == user_profile_type.id
        ).count()

        print(f"\nFinal Counts:")
        print(f"  Total UserAccounts: {total_accounts}")
        print(f"  Total UserProfiles: {total_profiles}")

        print("\n" + "=" * 80)
        print("✓ USER MIGRATION SUCCESSFUL")
        print("=" * 80)

        print("""
Next Steps:

1. All existing users now have UserAccount and UserProfile instances
2. SuperUsers are flagged in attrs.is_superuser for cross-tenant access
3. Original User table records are preserved (not deleted)
4. Next: Create RoleDefinition instances for RBAC system

Important Notes:
- SuperUsers will need special handling in the RBAC system
- The 'is_superuser' flag in UserProfile.attrs should grant cross-tenant access
- Original User.hashed_password is still in users table for authentication
""")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = migrate_users()
    sys.exit(0 if success else 1)
