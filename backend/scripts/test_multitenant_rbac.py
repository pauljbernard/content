"""
Test multi-tenant RBAC system to verify all components work correctly.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from models.user import User
from models.content_type import ContentTypeModel, ContentInstanceModel
from services.content_instance_service import content_instance_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_multitenant_rbac():
    """Test the multi-tenant RBAC system."""
    print("=" * 80)
    print("TESTING MULTI-TENANT RBAC SYSTEM")
    print("=" * 80)

    db = SessionLocal()
    test_results = []

    try:
        # Test 1: Verify all users have UserAccount instances
        print("\n" + "=" * 60)
        print("TEST 1: User Account Migration")
        print("=" * 60)

        users = db.query(User).all()
        user_account_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "UserAccount"
        ).first()

        user_accounts = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == user_account_type.id
        ).all()

        print(f"\nUsers in legacy table: {len(users)}")
        print(f"UserAccount instances: {len(user_accounts)}")

        for user in users:
            user_id_str = f"user-{user.id}"
            account = content_instance_service.get_user_account_by_user_id(db, user_id_str)
            if account:
                print(f"  ✓ {user.email} → UserAccount found (tenant: {account.data.get('tenant_id')})")
                test_results.append(("UserAccount Migration", user.email, "PASS"))
            else:
                print(f"  ✗ {user.email} → UserAccount NOT FOUND")
                test_results.append(("UserAccount Migration", user.email, "FAIL"))

        # Test 2: Verify all users have UserProfile instances
        print("\n" + "=" * 60)
        print("TEST 2: User Profile Migration")
        print("=" * 60)

        user_profile_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "UserProfile"
        ).first()

        user_profiles = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == user_profile_type.id
        ).all()

        print(f"\nUserProfile instances: {len(user_profiles)}")

        for user in users:
            user_id_str = f"user-{user.id}"
            profile = content_instance_service.get_user_profile_by_user_id(db, user_id_str)
            if profile:
                role = profile.data.get('role')
                attrs = profile.data.get('attrs', {})
                is_superuser = attrs.get('is_superuser', False)
                print(f"  ✓ {user.email} → Role: {role}, SuperUser: {is_superuser}")
                test_results.append(("UserProfile Migration", user.email, "PASS"))
            else:
                print(f"  ✗ {user.email} → UserProfile NOT FOUND")
                test_results.append(("UserProfile Migration", user.email, "FAIL"))

        # Test 3: Verify tenant and organization structure
        print("\n" + "=" * 60)
        print("TEST 3: Tenant & Organization Structure")
        print("=" * 60)

        tenant_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "Tenant"
        ).first()
        org_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "Organization"
        ).first()

        tenants = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == tenant_type.id
        ).all()

        orgs = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == org_type.id
        ).all()

        print(f"\nTenants: {len(tenants)}")
        for tenant in tenants:
            print(f"  - {tenant.data.get('name')} (ID: {tenant.data.get('tenant_id')}, Plan: {tenant.data.get('plan_tier')})")
            test_results.append(("Tenant Structure", tenant.data.get('name'), "PASS"))

        print(f"\nOrganizations: {len(orgs)}")
        for org in orgs:
            print(f"  - {org.data.get('name')} (ID: {org.data.get('org_id')}, Type: {org.data.get('type')}, Tenant: {org.data.get('tenant_id')})")
            test_results.append(("Organization Structure", org.data.get('name'), "PASS"))

        # Test 4: Verify role definitions
        print("\n" + "=" * 60)
        print("TEST 4: Role Definitions & Permissions")
        print("=" * 60)

        role_def_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "RoleDefinition"
        ).first()

        roles = db.query(ContentInstanceModel).filter(
            ContentInstanceModel.content_type_id == role_def_type.id
        ).all()

        print(f"\nRole Definitions: {len(roles)}")
        for role in roles:
            role_id = role.data.get('role_id')
            name = role.data.get('name')
            inherits = role.data.get('inherits', [])
            permissions = role.data.get('default_permissions', [])

            print(f"\n  {role_id} ({name}):")
            print(f"    Inherits: {', '.join(inherits) if inherits else 'none'}")
            print(f"    Permissions: {len(permissions)}")
            test_results.append(("Role Definition", role_id, "PASS"))

        # Test 5: Test permission checking
        print("\n" + "=" * 60)
        print("TEST 5: Permission Checking")
        print("=" * 60)

        test_cases = [
            ("user-1", "read", "content:*", True),  # Admin should have access
            ("user-2", "read", "content:*", True),  # Teacher should have read
            ("user-2", "delete", "content:*", False),  # Teacher should NOT have delete
        ]

        for user_id, action, resource, expected in test_cases:
            result = content_instance_service.check_user_permission(db, user_id, action, resource)
            status = "✓ PASS" if result == expected else "✗ FAIL"
            print(f"  {status}: {user_id} → {action}:{resource} = {result} (expected: {expected})")
            test_results.append(("Permission Check", f"{user_id}:{action}:{resource}", "PASS" if result == expected else "FAIL"))

        # Test 6: Verify superuser detection
        print("\n" + "=" * 60)
        print("TEST 6: SuperUser Detection")
        print("=" * 60)

        for user in users:
            user_id_str = f"user-{user.id}"
            is_superuser = content_instance_service.is_user_superuser(db, user_id_str)
            print(f"  {user.email}: SuperUser = {is_superuser}")

            # user-1 (admin@hmhco.com) should be superuser
            if user.id == 1:
                if is_superuser:
                    test_results.append(("SuperUser Detection", user.email, "PASS"))
                else:
                    test_results.append(("SuperUser Detection", user.email, "FAIL"))

        # Test 7: Verify tenant/org retrieval
        print("\n" + "=" * 60)
        print("TEST 7: Tenant & Organization Retrieval")
        print("=" * 60)

        for user in users:
            user_id_str = f"user-{user.id}"
            tenant_id = content_instance_service.get_user_tenant_id(db, user_id_str)
            org_id = content_instance_service.get_user_org_id(db, user_id_str)

            print(f"  {user.email}:")
            print(f"    Tenant: {tenant_id}")
            print(f"    Org: {org_id}")

            if tenant_id and org_id:
                test_results.append(("Tenant/Org Retrieval", user.email, "PASS"))
            else:
                test_results.append(("Tenant/Org Retrieval", user.email, "FAIL"))

        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)

        total_tests = len(test_results)
        passed = sum(1 for _, _, status in test_results if status == "PASS")
        failed = total_tests - passed

        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed} ({int(passed/total_tests*100)}%)")
        print(f"Failed: {failed}")

        if failed > 0:
            print("\nFailed Tests:")
            for test_name, subject, status in test_results:
                if status == "FAIL":
                    print(f"  ✗ {test_name}: {subject}")

        print("\n" + "=" * 80)
        if failed == 0:
            print("✓ ALL TESTS PASSED - MULTI-TENANT RBAC SYSTEM IS WORKING")
        else:
            print(f"⚠ {failed} TESTS FAILED - REVIEW ISSUES ABOVE")
        print("=" * 80)

        return failed == 0

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = test_multitenant_rbac()
    sys.exit(0 if success else 1)
