"""
Test audit logging system to verify AuditEvent creation and retrieval.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from models.user import User
from models.content_type import ContentTypeModel, ContentInstanceModel
from services.audit_service import audit_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_audit_logging():
    """Test the audit logging system."""
    print("=" * 80)
    print("TESTING AUDIT LOGGING SYSTEM")
    print("=" * 80)

    db = SessionLocal()
    test_results = []

    try:
        # Test 1: Verify AuditEvent content type exists
        print("\n" + "=" * 60)
        print("TEST 1: AuditEvent Content Type")
        print("=" * 60)

        audit_event_type = db.query(ContentTypeModel).filter(
            ContentTypeModel.name == "AuditEvent"
        ).first()

        if audit_event_type:
            print(f"✓ AuditEvent content type found (ID: {audit_event_type.id})")
            test_results.append(("AuditEvent Type", "exists", "PASS"))
        else:
            print("✗ AuditEvent content type NOT FOUND")
            test_results.append(("AuditEvent Type", "exists", "FAIL"))
            return False

        # Test 2: Log a test event
        print("\n" + "=" * 60)
        print("TEST 2: Create Audit Event")
        print("=" * 60)

        test_user = db.query(User).first()
        if not test_user:
            print("✗ No users found for testing")
            test_results.append(("Create Event", "no users", "FAIL"))
            return False

        event = audit_service.log_event(
            db=db,
            who=f"user-{test_user.id}",
            action="test_action",
            resource="test_resource",
            decision="allow",
            reason="Test audit logging",
            created_by_id=test_user.id
        )

        if event:
            print(f"✓ Audit event created successfully")
            print(f"  Event ID: {event.id}")
            print(f"  Who: {event.data.get('who')}")
            print(f"  Action: {event.data.get('action')}")
            print(f"  Resource: {event.data.get('resource')}")
            print(f"  Decision: {event.data.get('decision')}")
            print(f"  Timestamp: {event.data.get('timestamp')}")
            test_results.append(("Create Event", "basic", "PASS"))
        else:
            print("✗ Failed to create audit event")
            test_results.append(("Create Event", "basic", "FAIL"))

        # Test 3: Test specialized logging methods
        print("\n" + "=" * 60)
        print("TEST 3: Specialized Logging Methods")
        print("=" * 60)

        # Test login logging
        login_event = audit_service.log_login(db, test_user, success=True)
        if login_event:
            print(f"✓ Login event logged")
            test_results.append(("Log Method", "login", "PASS"))
        else:
            print("✗ Failed to log login event")
            test_results.append(("Log Method", "login", "FAIL"))

        # Test logout logging
        logout_event = audit_service.log_logout(db, test_user)
        if logout_event:
            print(f"✓ Logout event logged")
            test_results.append(("Log Method", "logout", "PASS"))
        else:
            print("✗ Failed to log logout event")
            test_results.append(("Log Method", "logout", "FAIL"))

        # Test create logging
        create_event = audit_service.log_create(db, test_user, "test_content", "123")
        if create_event:
            print(f"✓ Create event logged")
            test_results.append(("Log Method", "create", "PASS"))
        else:
            print("✗ Failed to log create event")
            test_results.append(("Log Method", "create", "FAIL"))

        # Test update logging
        update_event = audit_service.log_update(db, test_user, "test_content", "123")
        if update_event:
            print(f"✓ Update event logged")
            test_results.append(("Log Method", "update", "PASS"))
        else:
            print("✗ Failed to log update event")
            test_results.append(("Log Method", "update", "FAIL"))

        # Test delete logging
        delete_event = audit_service.log_delete(db, test_user, "test_content", "123")
        if delete_event:
            print(f"✓ Delete event logged")
            test_results.append(("Log Method", "delete", "PASS"))
        else:
            print("✗ Failed to log delete event")
            test_results.append(("Log Method", "delete", "FAIL"))

        # Test view logging
        view_event = audit_service.log_view(db, test_user, "test_content", "123")
        if view_event:
            print(f"✓ View event logged")
            test_results.append(("Log Method", "view", "PASS"))
        else:
            print("✗ Failed to log view event")
            test_results.append(("Log Method", "view", "FAIL"))

        # Test access denied logging
        denied_event = audit_service.log_access_denied(
            db, test_user, "delete", "test_content:456", "Insufficient permissions"
        )
        if denied_event:
            print(f"✓ Access denied event logged")
            test_results.append(("Log Method", "access_denied", "PASS"))
        else:
            print("✗ Failed to log access denied event")
            test_results.append(("Log Method", "access_denied", "FAIL"))

        # Test 4: Retrieve audit trail
        print("\n" + "=" * 60)
        print("TEST 4: Retrieve Audit Trail")
        print("=" * 60)

        user_id_str = f"user-{test_user.id}"
        audit_trail = audit_service.get_user_audit_trail(db, user_id_str, limit=10)

        print(f"\nAudit trail for {test_user.email} ({user_id_str}):")
        print(f"Total events: {len(audit_trail)}")

        if len(audit_trail) >= 8:  # We created at least 8 events above
            print("✓ Audit trail retrieval working")
            test_results.append(("Audit Trail", "retrieval", "PASS"))

            print("\nRecent events:")
            for i, event in enumerate(audit_trail[:5], 1):
                data = event.data
                print(f"  {i}. {data.get('action')} on {data.get('resource')} - {data.get('decision')}")
        else:
            print(f"✗ Expected at least 8 events, found {len(audit_trail)}")
            test_results.append(("Audit Trail", "retrieval", "FAIL"))

        # Test 5: Retrieve recent events
        print("\n" + "=" * 60)
        print("TEST 5: Retrieve Recent Events (All Users)")
        print("=" * 60)

        recent_events = audit_service.get_recent_events(db, limit=10)
        print(f"\nTotal recent events: {len(recent_events)}")

        if len(recent_events) > 0:
            print("✓ Recent events retrieval working")
            test_results.append(("Recent Events", "retrieval", "PASS"))

            print("\nMost recent events:")
            for i, event in enumerate(recent_events[:5], 1):
                data = event.data
                print(f"  {i}. {data.get('who')} → {data.get('action')} on {data.get('resource')} ({data.get('decision')})")
        else:
            print("✗ No recent events found")
            test_results.append(("Recent Events", "retrieval", "FAIL"))

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
            print("✓ ALL TESTS PASSED - AUDIT LOGGING SYSTEM IS WORKING")
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
    success = test_audit_logging()
    sys.exit(0 if success else 1)
