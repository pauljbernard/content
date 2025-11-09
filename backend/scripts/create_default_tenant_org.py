"""
Create default tenant and organization structure for multi-tenant system.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from models.content_type import ContentTypeModel, ContentInstanceModel
from datetime import datetime
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_default_tenant_org():
    """Create default tenant and organization instances."""
    print("=" * 80)
    print("CREATING DEFAULT TENANT AND ORGANIZATION STRUCTURE")
    print("=" * 80)

    db = SessionLocal()

    try:
        # Get content type definitions
        tenant_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "Tenant"
        ).first()
        org_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "Organization"
        ).first()

        if not tenant_type or not org_type:
            print("❌ ERROR: Tenant or Organization content types not found!")
            return False

        print(f"\n✓ Found Tenant content type: {tenant_type.id}")
        print(f"✓ Found Organization content type: {org_type.id}")

        # Check if default tenant already exists
        all_tenants = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == tenant_type.id
        ).all()

        existing_tenant = None
        for t in all_tenants:
            if t.data.get("tenant_id") == "default-tenant":
                existing_tenant = t
                break

        if existing_tenant:
            print(f"\n⚠️  Default tenant already exists (ID: {existing_tenant.id})")
            tenant_instance = existing_tenant
        else:
            # Create default tenant instance
            print("\n1. Creating default tenant...")
            tenant_data = {
                "tenant_id": "default-tenant",
                "name": "Default Tenant",
                "plan_tier": "enterprise",
                "active_from": datetime.utcnow().date().isoformat(),
                "active_to": None,
                "settings": {
                    "features": {
                        "multi_org": True,
                        "rbac": True,
                        "audit_logging": True,
                        "api_access": True
                    },
                    "limits": {
                        "max_users": -1,  # Unlimited
                        "max_orgs": -1,
                        "max_content_instances": -1
                    }
                }
            }

            tenant_instance = ContentInstanceModel(
                id=str(uuid.uuid4()),
                content_type_id=tenant_type.id,
                data=tenant_data,
                status="published",
                created_by=1  # System admin user
            )

            db.add(tenant_instance)
            db.commit()
            db.refresh(tenant_instance)

            print(f"   ✓ Created tenant: {tenant_instance.id}")
            print(f"   ✓ Tenant ID: {tenant_data['tenant_id']}")
            print(f"   ✓ Name: {tenant_data['name']}")
            print(f"   ✓ Plan: {tenant_data['plan_tier']}")

        # Check if default organization already exists
        all_orgs = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == org_type.id
        ).all()

        existing_org = None
        for o in all_orgs:
            if o.data.get("org_id") == "default-org":
                existing_org = o
                break

        if existing_org:
            print(f"\n⚠️  Default organization already exists (ID: {existing_org.id})")
            org_instance = existing_org
        else:
            # Create default organization instance
            print("\n2. Creating default organization...")
            org_data = {
                "org_id": "default-org",
                "tenant_id": "default-tenant",
                "type": "district",
                "name": "Default Organization",
                "parent_org_id": None
            }

            org_instance = ContentInstanceModel(
                id=str(uuid.uuid4()),
                content_type_id=org_type.id,
                data=org_data,
                status="published",
                created_by=1  # System admin user
            )

            db.add(org_instance)
            db.commit()
            db.refresh(org_instance)

            print(f"   ✓ Created organization: {org_instance.id}")
            print(f"   ✓ Org ID: {org_data['org_id']}")
            print(f"   ✓ Name: {org_data['name']}")
            print(f"   ✓ Type: {org_data['type']}")
            print(f"   ✓ Tenant: {org_data['tenant_id']}")

        # Verify creation
        print("\n" + "=" * 80)
        print("VERIFICATION")
        print("=" * 80)

        tenant_count = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == tenant_type.id
        ).count()

        org_count = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == org_type.id
        ).count()

        print(f"\nTotal Tenants: {tenant_count}")
        print(f"Total Organizations: {org_count}")

        # Show details
        print("\nDefault Tenant Details:")
        print(f"  Instance ID: {tenant_instance.id}")
        print(f"  Name: {tenant_instance.data.get('name')}")
        print(f"  Tenant ID: {tenant_instance.data.get('tenant_id')}")
        print(f"  Plan Tier: {tenant_instance.data.get('plan_tier')}")
        print(f"  Status: {tenant_instance.status}")

        print("\nDefault Organization Details:")
        print(f"  Instance ID: {org_instance.id}")
        print(f"  Name: {org_instance.data.get('name')}")
        print(f"  Org ID: {org_instance.data.get('org_id')}")
        print(f"  Tenant ID: {org_instance.data.get('tenant_id')}")
        print(f"  Type: {org_instance.data.get('type')}")
        print(f"  Status: {org_instance.status}")

        print("\n" + "=" * 80)
        print("✓ DEFAULT TENANT AND ORGANIZATION CREATED SUCCESSFULLY")
        print("=" * 80)

        print("""
Next Steps:

1. These are the base tenant and organization for the system
2. All existing users will be migrated to UserAccount instances under this tenant/org
3. Additional organizations can be created under this tenant
4. Additional tenants can be created for true multi-tenancy

Ready to proceed with user migration!
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
    success = create_default_tenant_org()
    sys.exit(0 if success else 1)
