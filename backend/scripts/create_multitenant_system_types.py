"""
Create multi-tenant system content types: identity, entitlements, policy/RBAC
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database.session import SessionLocal
from models.content_type import ContentTypeModel
import uuid

def create_all_system_types():
    """Create all multi-tenant system content types."""
    print("=" * 60)
    print("Creating Multi-Tenant System Content Types")
    print("=" * 60)
    
    db = SessionLocal()
    created_count = 0
    skipped_count = 0
    
    try:
        # Define all system types
        types_to_create = [
            # Core Identity & Org Graph
            ("Tenant", "Multi-tenant organization root", "BuildingOfficeIcon", [
                {"name": "tenant_id", "label": "Tenant ID", "type": "text", "required": True, "config": {"maxLength": 100, "unique": True}, "help_text": "Unique tenant identifier", "order_index": 0},
                {"name": "name", "label": "Tenant Name", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Organization name", "order_index": 1},
                {"name": "plan_tier", "label": "Plan Tier", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["free", "basic", "professional", "enterprise"]}, "help_text": "Subscription tier", "order_index": 2},
                {"name": "active_from", "label": "Active From", "type": "date", "required": True, "config": {}, "help_text": "Account activation date", "order_index": 3},
                {"name": "active_to", "label": "Active To", "type": "date", "required": False, "config": {}, "help_text": "Account expiration (if any)", "order_index": 4},
                {"name": "settings", "label": "Settings", "type": "json", "required": False, "config": {}, "help_text": "Tenant configuration JSON", "default_value": {}, "order_index": 5}
            ]),
            
            ("Organization", "District, school, or vendor", "BuildingLibraryIcon", [
                {"name": "org_id", "label": "Organization ID", "type": "text", "required": True, "config": {"maxLength": 100, "unique": True}, "help_text": "Unique org identifier", "order_index": 0},
                {"name": "tenant_id", "label": "Tenant ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Parent tenant", "order_index": 1},
                {"name": "type", "label": "Organization Type", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["district", "school", "vendor", "department"]}, "help_text": "Type of organization", "order_index": 2},
                {"name": "name", "label": "Name", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Organization name", "order_index": 3},
                {"name": "parent_org_id", "label": "Parent Org ID", "type": "text", "required": False, "config": {"maxLength": 100}, "help_text": "Parent organization (for hierarchy)", "order_index": 4}
            ]),
            
            ("UserAccount", "Platform user account", "UserIcon", [
                {"name": "user_id", "label": "User ID", "type": "text", "required": True, "config": {"maxLength": 100, "unique": True}, "help_text": "Unique user identifier", "order_index": 0},
                {"name": "tenant_id", "label": "Tenant ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Tenant membership", "order_index": 1},
                {"name": "primary_org_id", "label": "Primary Org ID", "type": "text", "required": False, "config": {"maxLength": 100}, "help_text": "Primary organization", "order_index": 2},
                {"name": "email", "label": "Email", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "User email address", "order_index": 3},
                {"name": "locale", "label": "Locale", "type": "choice", "required": False, "config": {"multiple": False, "choices": ["en-US", "es-MX", "fr-FR", "de-DE"]}, "help_text": "Preferred language", "order_index": 4},
                {"name": "status", "label": "Status", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["active", "suspended", "inactive"]}, "help_text": "Account status", "order_index": 5}
            ]),
            
            ("UserProfile", "Extended user profile by role", "IdentificationIcon", [
                {"name": "user_id", "label": "User ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Associated user", "order_index": 0},
                {"name": "role", "label": "Role", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["student", "teacher", "admin", "parent", "content_author"]}, "help_text": "User role", "order_index": 1},
                {"name": "attrs", "label": "Attributes", "type": "json", "required": False, "config": {}, "help_text": "Role-specific attributes JSONB", "default_value": {}, "order_index": 2},
                {"name": "accommodations", "label": "Accommodations", "type": "reference", "required": False, "config": {"contentType": "Accommodation", "multiple": True}, "help_text": "User accommodations", "order_index": 3},
                {"name": "grades", "label": "Grades", "type": "choice", "required": False, "config": {"multiple": True, "choices": ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]}, "help_text": "Grade levels", "order_index": 4},
                {"name": "subjects", "label": "Subjects", "type": "choice", "required": False, "config": {"multiple": True, "choices": ["Math", "ELA", "Science", "Social Studies"]}, "help_text": "Subject areas", "order_index": 5}
            ]),
            
            ("Group", "Cohort, classroom, PLC, club", "UserGroupIcon", [
                {"name": "group_id", "label": "Group ID", "type": "text", "required": True, "config": {"maxLength": 100, "unique": True}, "help_text": "Unique group identifier", "order_index": 0},
                {"name": "tenant_id", "label": "Tenant ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Tenant membership", "order_index": 1},
                {"name": "org_id", "label": "Organization ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Organization", "order_index": 2},
                {"name": "type", "label": "Group Type", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["classroom", "cohort", "plc", "club", "intervention_group"]}, "help_text": "Type of group", "order_index": 3},
                {"name": "name", "label": "Name", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Group name", "order_index": 4},
                {"name": "metadata", "label": "Metadata", "type": "json", "required": False, "config": {}, "help_text": "Additional group data", "default_value": {}, "order_index": 5}
            ]),
            
            ("RosterMembership", "Group membership record", "ClipboardDocumentListIcon", [
                {"name": "group_id", "label": "Group ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Group", "order_index": 0},
                {"name": "user_id", "label": "User ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "User", "order_index": 1},
                {"name": "role_in_group", "label": "Role in Group", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["teacher", "student", "admin", "observer"]}, "help_text": "Role within this group", "order_index": 2},
                {"name": "active_from", "label": "Active From", "type": "date", "required": True, "config": {}, "help_text": "Membership start date", "order_index": 3},
                {"name": "active_to", "label": "Active To", "type": "date", "required": False, "config": {}, "help_text": "Membership end date", "order_index": 4}
            ]),
            
            # Entitlements & Subscriptions
            ("Product", "Licensed product/capability", "ShoppingBagIcon", [
                {"name": "sku", "label": "SKU", "type": "text", "required": True, "config": {"maxLength": 100, "unique": True}, "help_text": "Product SKU", "order_index": 0},
                {"name": "name", "label": "Product Name", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Product name", "order_index": 1},
                {"name": "capabilities", "label": "Capabilities", "type": "json", "required": False, "config": {}, "help_text": "Feature capabilities array", "default_value": [], "order_index": 2},
                {"name": "content_scopes", "label": "Content Scopes", "type": "json", "required": False, "config": {}, "help_text": "Content access scopes", "default_value": [], "order_index": 3}
            ]),
            
            ("Subscription", "Product subscription", "CreditCardIcon", [
                {"name": "subscription_id", "label": "Subscription ID", "type": "text", "required": True, "config": {"maxLength": 100, "unique": True}, "help_text": "Subscription identifier", "order_index": 0},
                {"name": "subscriber_type", "label": "Subscriber Type", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["tenant", "org", "user"]}, "help_text": "Who owns subscription", "order_index": 1},
                {"name": "subscriber_id", "label": "Subscriber ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Subscriber identifier", "order_index": 2},
                {"name": "product_sku", "label": "Product SKU", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Subscribed product", "order_index": 3},
                {"name": "seats", "label": "Seats", "type": "number", "required": True, "config": {"min": 1}, "help_text": "Number of seats/licenses", "order_index": 4},
                {"name": "start_date", "label": "Start Date", "type": "date", "required": True, "config": {}, "help_text": "Subscription start", "order_index": 5},
                {"name": "end_date", "label": "End Date", "type": "date", "required": False, "config": {}, "help_text": "Subscription end", "order_index": 6},
                {"name": "status", "label": "Status", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["active", "expired", "cancelled", "trial"]}, "help_text": "Subscription status", "order_index": 7}
            ]),
            
            ("SeatAssignment", "User license assignment", "UserPlusIcon", [
                {"name": "subscription_id", "label": "Subscription ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Parent subscription", "order_index": 0},
                {"name": "user_id", "label": "User ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Assigned user", "order_index": 1},
                {"name": "assigned_at", "label": "Assigned At", "type": "date", "required": True, "config": {}, "help_text": "Assignment date", "order_index": 2},
                {"name": "revoked_at", "label": "Revoked At", "type": "date", "required": False, "config": {}, "help_text": "Revocation date", "order_index": 3}
            ]),
            
            ("Entitlement", "Normalized access fact", "KeyIcon", [
                {"name": "subject_id", "label": "Subject ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "User/group/org ID", "order_index": 0},
                {"name": "capability", "label": "Capability", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Granted capability", "order_index": 1},
                {"name": "scope", "label": "Scope", "type": "text", "required": False, "config": {"maxLength": 200}, "help_text": "Access scope", "order_index": 2},
                {"name": "constraints", "label": "Constraints", "type": "json", "required": False, "config": {}, "help_text": "Constraint rules JSONB", "default_value": {}, "order_index": 3},
                {"name": "source", "label": "Source", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["subscription", "grant", "trial"]}, "help_text": "Entitlement source", "order_index": 4},
                {"name": "active_from", "label": "Active From", "type": "date", "required": True, "config": {}, "help_text": "Start date", "order_index": 5},
                {"name": "active_to", "label": "Active To", "type": "date", "required": False, "config": {}, "help_text": "End date", "order_index": 6}
            ]),
            
            # Policy & RBAC
            ("RoleDefinition", "User role definition", "ShieldExclamationIcon", [
                {"name": "role_id", "label": "Role ID", "type": "text", "required": True, "config": {"maxLength": 100, "unique": True}, "help_text": "Role identifier", "order_index": 0},
                {"name": "name", "label": "Role Name", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Human-readable name", "order_index": 1},
                {"name": "inherits", "label": "Inherits", "type": "json", "required": False, "config": {}, "help_text": "Parent roles array", "default_value": [], "order_index": 2},
                {"name": "default_permissions", "label": "Default Permissions", "type": "json", "required": False, "config": {}, "help_text": "Default permission array", "default_value": [], "order_index": 3}
            ]),
            
            ("Permission", "Access permission rule", "LockClosedIcon", [
                {"name": "action", "label": "Action", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Action (e.g., read, write, delete)", "order_index": 0},
                {"name": "resource", "label": "Resource", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Resource pattern", "order_index": 1},
                {"name": "effect", "label": "Effect", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["allow", "deny"]}, "help_text": "Allow or deny", "order_index": 2},
                {"name": "conditions", "label": "Conditions", "type": "json", "required": False, "config": {}, "help_text": "Conditional rules JSONB", "default_value": {}, "order_index": 3}
            ]),
            
            ("PolicyRule", "OPA/Casbin policy row", "DocumentTextIcon", [
                {"name": "policy_id", "label": "Policy ID", "type": "text", "required": True, "config": {"maxLength": 100, "unique": True}, "help_text": "Policy identifier", "order_index": 0},
                {"name": "subject_kind", "label": "Subject Kind", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["user", "role", "group"]}, "help_text": "Type of subject", "order_index": 1},
                {"name": "subject_id", "label": "Subject ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Subject identifier", "order_index": 2},
                {"name": "action", "label": "Action", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Action verb", "order_index": 3},
                {"name": "resource_pattern", "label": "Resource Pattern", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Resource path/pattern", "order_index": 4},
                {"name": "effect", "label": "Effect", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["allow", "deny"]}, "help_text": "Allow or deny", "order_index": 5},
                {"name": "conditions", "label": "Conditions", "type": "json", "required": False, "config": {}, "help_text": "Conditional logic JSONB", "default_value": {}, "order_index": 6}
            ]),
            
            ("ConsentRecord", "User consent tracking", "DocumentCheckIcon", [
                {"name": "user_id", "label": "User ID", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "User providing consent", "order_index": 0},
                {"name": "purpose", "label": "Purpose", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Consent purpose", "order_index": 1},
                {"name": "granted_at", "label": "Granted At", "type": "date", "required": True, "config": {}, "help_text": "Consent date", "order_index": 2},
                {"name": "expires_at", "label": "Expires At", "type": "date", "required": False, "config": {}, "help_text": "Expiration date", "order_index": 3}
            ]),
            
            ("AuditEvent", "System audit log", "ClipboardDocumentIcon", [
                {"name": "who", "label": "Who", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Actor user ID", "order_index": 0},
                {"name": "action", "label": "Action", "type": "text", "required": True, "config": {"maxLength": 100}, "help_text": "Action performed", "order_index": 1},
                {"name": "resource", "label": "Resource", "type": "text", "required": True, "config": {"maxLength": 200}, "help_text": "Affected resource", "order_index": 2},
                {"name": "decision", "label": "Decision", "type": "choice", "required": True, "config": {"multiple": False, "choices": ["allow", "deny"]}, "help_text": "Access decision", "order_index": 3},
                {"name": "reason", "label": "Reason", "type": "text", "required": False, "config": {"maxLength": 500}, "help_text": "Decision reason", "order_index": 4},
                {"name": "timestamp", "label": "Timestamp", "type": "date", "required": True, "config": {}, "help_text": "Event time", "order_index": 5}
            ])
        ]
        
        for type_info in types_to_create:
            name, description, icon, attributes = type_info
            existing = db.query(ContentTypeModel).filter(ContentTypeModel.name == name).first()
            
            if existing:
                print(f"\n⚠ {name} already exists (skipping)")
                skipped_count += 1
            else:
                print(f"\n✓ Creating {name}...")
                new_type = ContentTypeModel(
                    id=str(uuid.uuid4()),
                    name=name,
                    description=description,
                    icon=icon,
                    is_system=True,
                    attributes=attributes,
                    created_by=1
                )
                db.add(new_type)
                db.commit()
                created_count += 1
                print(f"  ID: {new_type.id}, Attributes: {len(new_type.attributes)}")
        
        print("\n" + "=" * 60)
        print(f"Complete! Created: {created_count}, Skipped: {skipped_count}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_all_system_types()
