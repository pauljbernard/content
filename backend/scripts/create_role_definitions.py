"""
Create RoleDefinition and Permission instances for RBAC system.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from models.content_type import ContentTypeModel, ContentInstanceModel
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Permission definitions
PERMISSIONS = [
    # Content permissions
    {"action": "read", "resource": "content:*", "effect": "allow"},
    {"action": "create", "resource": "content:*", "effect": "allow"},
    {"action": "update", "resource": "content:*", "effect": "allow"},
    {"action": "delete", "resource": "content:*", "effect": "allow"},
    {"action": "publish", "resource": "content:*", "effect": "allow"},

    # User management permissions
    {"action": "read", "resource": "users:*", "effect": "allow"},
    {"action": "create", "resource": "users:*", "effect": "allow"},
    {"action": "update", "resource": "users:*", "effect": "allow"},
    {"action": "delete", "resource": "users:*", "effect": "allow"},

    # Assessment permissions
    {"action": "read", "resource": "assessments:*", "effect": "allow"},
    {"action": "create", "resource": "assessments:*", "effect": "allow"},
    {"action": "grade", "resource": "assessments:*", "effect": "allow"},

    # Settings permissions
    {"action": "read", "resource": "settings:*", "effect": "allow"},
    {"action": "update", "resource": "settings:*", "effect": "allow"},

    # Tenant permissions (for superuser)
    {"action": "*", "resource": "tenant:*", "effect": "allow"},

    # Organization permissions
    {"action": "read", "resource": "organizations:*", "effect": "allow"},
    {"action": "update", "resource": "organizations:*", "effect": "allow"},
]


# Role definitions with their permissions
ROLES = [
    {
        "role_id": "student",
        "name": "Student",
        "inherits": [],
        "permissions": ["read:content:*", "read:assessments:*"]
    },
    {
        "role_id": "parent",
        "name": "Parent",
        "inherits": [],
        "permissions": ["read:content:*"]  # Limited read access
    },
    {
        "role_id": "teacher",
        "name": "Teacher",
        "inherits": [],
        "permissions": [
            "read:content:*",
            "create:content:*",
            "update:content:*",
            "read:assessments:*",
            "create:assessments:*",
            "grade:assessments:*",
        ]
    },
    {
        "role_id": "content_author",
        "name": "Content Author",
        "inherits": ["teacher"],  # Inherits all teacher permissions
        "permissions": [
            "read:content:*",
            "create:content:*",
            "update:content:*",
            "delete:content:*",
            "publish:content:*",
        ]
    },
    {
        "role_id": "admin",
        "name": "Administrator",
        "inherits": ["content_author"],  # Inherits all content_author permissions
        "permissions": [
            "read:content:*",
            "create:content:*",
            "update:content:*",
            "delete:content:*",
            "publish:content:*",
            "read:users:*",
            "create:users:*",
            "update:users:*",
            "delete:users:*",
            "read:settings:*",
            "update:settings:*",
            "read:organizations:*",
            "update:organizations:*",
        ]
    },
    {
        "role_id": "superuser",
        "name": "Super User",
        "inherits": ["admin"],  # Inherits all admin permissions
        "permissions": [
            "*:tenant:*",  # Full access to all tenants
            "*:*:*",  # Full access to everything
        ],
        "is_cross_tenant": True
    },
]


def create_role_definitions():
    """Create RoleDefinition and Permission instances."""
    print("=" * 80)
    print("CREATING ROLE DEFINITIONS AND PERMISSIONS")
    print("=" * 80)

    db = SessionLocal()

    try:
        # Get content type definitions
        role_def_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "RoleDefinition"
        ).first()
        permission_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "Permission"
        ).first()

        if not role_def_type or not permission_type:
            print("❌ ERROR: RoleDefinition or Permission content types not found!")
            return False

        print(f"\n✓ Found RoleDefinition content type: {role_def_type.id}")
        print(f"✓ Found Permission content type: {permission_type.id}")

        # Create Permission instances
        print("\n" + "=" * 60)
        print("CREATING PERMISSIONS")
        print("=" * 60)

        permission_map = {}  # Map "action:resource" to instance ID
        created_permissions = 0

        # Check existing permissions
        existing_permissions = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == permission_type.id
        ).all()

        existing_perm_keys = set()
        for perm in existing_permissions:
            key = f"{perm.data.get('action')}:{perm.data.get('resource')}"
            existing_perm_keys.add(key)
            permission_map[key] = perm.id

        for perm_def in PERMISSIONS:
            key = f"{perm_def['action']}:{perm_def['resource']}"

            if key in existing_perm_keys:
                print(f"  ⚠️  Permission already exists: {key}")
                continue

            perm_data = {
                "action": perm_def["action"],
                "resource": perm_def["resource"],
                "effect": perm_def["effect"],
                "conditions": {}
            }

            perm_instance = ContentInstanceModel(
                id=str(uuid.uuid4()),
                content_type_id=permission_type.id,
                data=perm_data,
                status="published",
                created_by=1  # System admin
            )

            db.add(perm_instance)
            permission_map[key] = perm_instance.id
            created_permissions += 1

            print(f"  ✓ Created permission: {key} ({perm_def['effect']})")

        db.commit()
        print(f"\n  Total permissions created: {created_permissions}")

        # Create RoleDefinition instances
        print("\n" + "=" * 60)
        print("CREATING ROLE DEFINITIONS")
        print("=" * 60)

        created_roles = 0

        # Check existing roles
        existing_roles = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == role_def_type.id
        ).all()

        existing_role_ids = set(r.data.get("role_id") for r in existing_roles)

        for role_def in ROLES:
            if role_def["role_id"] in existing_role_ids:
                print(f"\n  ⚠️  Role already exists: {role_def['role_id']}")
                continue

            # Map permission strings to IDs
            permission_ids = []
            for perm_str in role_def["permissions"]:
                if perm_str in permission_map:
                    permission_ids.append(permission_map[perm_str])

            role_data = {
                "role_id": role_def["role_id"],
                "name": role_def["name"],
                "inherits": role_def.get("inherits", []),
                "default_permissions": role_def["permissions"]  # Store as strings for now
            }

            role_instance = ContentInstanceModel(
                id=str(uuid.uuid4()),
                content_type_id=role_def_type.id,
                data=role_data,
                status="published",
                created_by=1  # System admin
            )

            db.add(role_instance)
            created_roles += 1

            print(f"\n  ✓ Created role: {role_def['role_id']}")
            print(f"    Name: {role_def['name']}")
            print(f"    Inherits from: {', '.join(role_def['inherits']) if role_def['inherits'] else 'none'}")
            print(f"    Permissions: {len(role_def['permissions'])}")
            if role_def.get("is_cross_tenant"):
                print(f"    ⚠️  Cross-tenant access: YES")

        db.commit()
        print(f"\n  Total roles created: {created_roles}")

        # Verification
        print("\n" + "=" * 80)
        print("VERIFICATION")
        print("=" * 80)

        total_permissions = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == permission_type.id
        ).count()

        total_roles = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == role_def_type.id
        ).count()

        print(f"\nFinal Counts:")
        print(f"  Total Permissions: {total_permissions}")
        print(f"  Total Roles: {total_roles}")

        # Show role hierarchy
        print("\nRole Hierarchy:")
        all_roles = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == role_def_type.id
        ).all()

        for role in sorted(all_roles, key=lambda r: r.data.get("role_id")):
            role_id = role.data.get("role_id")
            name = role.data.get("name")
            inherits = role.data.get("inherits", [])
            perms = role.data.get("default_permissions", [])

            print(f"\n  {role_id} ({name}):")
            if inherits:
                print(f"    ↳ Inherits: {', '.join(inherits)}")
            print(f"    Permissions: {len(perms)}")

        print("\n" + "=" * 80)
        print("✓ ROLE DEFINITIONS AND PERMISSIONS CREATED")
        print("=" * 80)

        print("""
Next Steps:

1. Role-based access control (RBAC) structure is now in place
2. Each role has defined permissions and inheritance
3. SuperUser role grants cross-tenant access
4. Next: Refactor authentication and authorization to use this system

Role Hierarchy:
  student → (base level)
  parent → (base level)
  teacher → (base level)
  content_author → inherits from teacher
  admin → inherits from content_author
  superuser → inherits from admin + cross-tenant access
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
    success = create_role_definitions()
    sys.exit(0 if success else 1)
