"""
Advanced validation utilities for content type attributes.
"""
import re
from typing import Any, Dict, List, Optional
from datetime import datetime
from core.security import encrypt_secret, decrypt_secret, mask_secret


class ValidationRule:
    """Base class for validation rules."""

    def __init__(self, error_message: Optional[str] = None):
        self.error_message = error_message

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        """
        Validate the value.
        Returns None if valid, error message string if invalid.
        """
        raise NotImplementedError


class RequiredRule(ValidationRule):
    """Validates that a value is present."""

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        if value is None or value == "" or (isinstance(value, list) and len(value) == 0):
            return self.error_message or f"{attribute_name} is required"
        return None


class MinLengthRule(ValidationRule):
    """Validates minimum string/array length."""

    def __init__(self, min_length: int, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.min_length = min_length

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        if value is None:
            return None  # Use RequiredRule for required checks

        length = len(str(value)) if not isinstance(value, (list, dict)) else len(value)

        if length < self.min_length:
            return self.error_message or f"{attribute_name} must be at least {self.min_length} characters"
        return None


class MaxLengthRule(ValidationRule):
    """Validates maximum string/array length."""

    def __init__(self, max_length: int, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.max_length = max_length

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        if value is None:
            return None

        length = len(str(value)) if not isinstance(value, (list, dict)) else len(value)

        if length > self.max_length:
            return self.error_message or f"{attribute_name} must be at most {self.max_length} characters"
        return None


class PatternRule(ValidationRule):
    """Validates string against regex pattern."""

    def __init__(self, pattern: str, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.pattern = re.compile(pattern)

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        if value is None:
            return None

        if not self.pattern.match(str(value)):
            return self.error_message or f"{attribute_name} format is invalid"
        return None


class MinValueRule(ValidationRule):
    """Validates minimum numeric value."""

    def __init__(self, min_value: float, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.min_value = min_value

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        if value is None:
            return None

        try:
            if float(value) < self.min_value:
                return self.error_message or f"{attribute_name} must be at least {self.min_value}"
        except (ValueError, TypeError):
            return f"{attribute_name} must be a number"

        return None


class MaxValueRule(ValidationRule):
    """Validates maximum numeric value."""

    def __init__(self, max_value: float, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.max_value = max_value

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        if value is None:
            return None

        try:
            if float(value) > self.max_value:
                return self.error_message or f"{attribute_name} must be at most {self.max_value}"
        except (ValueError, TypeError):
            return f"{attribute_name} must be a number"

        return None


class EmailRule(ValidationRule):
    """Validates email format."""

    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        if value is None:
            return None

        if not self.EMAIL_PATTERN.match(str(value)):
            return self.error_message or f"{attribute_name} must be a valid email address"
        return None


class URLRule(ValidationRule):
    """Validates URL format."""

    URL_PATTERN = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        if value is None:
            return None

        if not self.URL_PATTERN.match(str(value)):
            return self.error_message or f"{attribute_name} must be a valid URL"
        return None


class ChoiceRule(ValidationRule):
    """Validates value is in allowed choices."""

    def __init__(self, choices: List[Any], error_message: Optional[str] = None):
        super().__init__(error_message)
        self.choices = choices

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        if value is None:
            return None

        # Handle multiple choice
        if isinstance(value, list):
            invalid = [v for v in value if v not in self.choices]
            if invalid:
                return self.error_message or f"{attribute_name} contains invalid choices: {', '.join(map(str, invalid))}"
        else:
            if value not in self.choices:
                return self.error_message or f"{attribute_name} must be one of: {', '.join(map(str, self.choices))}"

        return None


class DateRangeRule(ValidationRule):
    """Validates date is within range."""

    def __init__(self, min_date: Optional[str] = None, max_date: Optional[str] = None, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.min_date = datetime.fromisoformat(min_date) if min_date else None
        self.max_date = datetime.fromisoformat(max_date) if max_date else None

    def validate(self, value: Any, attribute_name: str) -> Optional[str]:
        if value is None:
            return None

        try:
            if isinstance(value, str):
                date_value = datetime.fromisoformat(value)
            else:
                date_value = value

            if self.min_date and date_value < self.min_date:
                return self.error_message or f"{attribute_name} must be after {self.min_date.isoformat()}"

            if self.max_date and date_value > self.max_date:
                return self.error_message or f"{attribute_name} must be before {self.max_date.isoformat()}"

        except (ValueError, TypeError):
            return f"{attribute_name} must be a valid date"

        return None


def validate_attribute(attribute_name: str, attribute_def: Dict, value: Any) -> List[str]:
    """
    Validate a single attribute value against its definition.

    Returns a list of error messages (empty if valid).
    """
    errors = []
    attribute_type = attribute_def.get("type")
    config = attribute_def.get("config", {})
    required = attribute_def.get("required", False)

    # Required validation
    if required:
        error = RequiredRule().validate(value, attribute_def.get("label", attribute_name))
        if error:
            errors.append(error)
            return errors  # If required and missing, skip other validations

    # Skip further validation if value is None/empty and not required
    if value is None or value == "":
        return errors

    # Type-specific validations
    if attribute_type == "text":
        if config.get("minLength"):
            error = MinLengthRule(config["minLength"]).validate(value, attribute_def.get("label", attribute_name))
            if error:
                errors.append(error)

        if config.get("maxLength"):
            error = MaxLengthRule(config["maxLength"]).validate(value, attribute_def.get("label", attribute_name))
            if error:
                errors.append(error)

        if config.get("pattern"):
            error = PatternRule(config["pattern"], config.get("patternMessage")).validate(
                value, attribute_def.get("label", attribute_name)
            )
            if error:
                errors.append(error)

    elif attribute_type == "long_text" or attribute_type == "rich_text":
        if config.get("minLength"):
            error = MinLengthRule(config["minLength"]).validate(value, attribute_def.get("label", attribute_name))
            if error:
                errors.append(error)

        if config.get("maxLength"):
            error = MaxLengthRule(config["maxLength"]).validate(value, attribute_def.get("label", attribute_name))
            if error:
                errors.append(error)

    elif attribute_type == "number":
        if config.get("min") is not None:
            error = MinValueRule(config["min"]).validate(value, attribute_def.get("label", attribute_name))
            if error:
                errors.append(error)

        if config.get("max") is not None:
            error = MaxValueRule(config["max"]).validate(value, attribute_def.get("label", attribute_name))
            if error:
                errors.append(error)

    elif attribute_type == "email":
        error = EmailRule().validate(value, attribute_def.get("label", attribute_name))
        if error:
            errors.append(error)

    elif attribute_type == "url":
        error = URLRule().validate(value, attribute_def.get("label", attribute_name))
        if error:
            errors.append(error)

    elif attribute_type == "choice":
        if config.get("choices"):
            error = ChoiceRule(config["choices"]).validate(value, attribute_def.get("label", attribute_name))
            if error:
                errors.append(error)

    elif attribute_type == "date":
        error = DateRangeRule(
            config.get("min"),
            config.get("max")
        ).validate(value, attribute_def.get("label", attribute_name))
        if error:
            errors.append(error)

    elif attribute_type == "password_secret":
        # Password/secret fields have same validations as text
        if config.get("minLength"):
            error = MinLengthRule(config["minLength"]).validate(value, attribute_def.get("label", attribute_name))
            if error:
                errors.append(error)

        if config.get("maxLength"):
            error = MaxLengthRule(config["maxLength"]).validate(value, attribute_def.get("label", attribute_name))
            if error:
                errors.append(error)

    # Custom validation rules
    if config.get("customValidation"):
        custom_rules = config.get("customValidation", [])
        for rule in custom_rules:
            rule_type = rule.get("type")
            if rule_type == "regex":
                error = PatternRule(rule["pattern"], rule.get("message")).validate(
                    value, attribute_def.get("label", attribute_name)
                )
                if error:
                    errors.append(error)

    return errors


def validate_instance_data(content_type_attributes: List[Dict], instance_data: Dict) -> List[str]:
    """
    Validate all attributes in an instance against content type definition.

    Returns a list of all error messages.
    """
    all_errors = []

    # Create attribute lookup
    attributes_by_name = {attr["name"]: attr for attr in content_type_attributes}

    # Validate each attribute
    for attr_name, attr_def in attributes_by_name.items():
        value = instance_data.get(attr_name)
        errors = validate_attribute(attr_name, attr_def, value)
        all_errors.extend(errors)

    return all_errors


def encrypt_password_secret_fields(content_type_attributes: List[Dict], instance_data: Dict) -> Dict:
    """
    Encrypt all password_secret fields in instance data before saving to database.

    Args:
        content_type_attributes: List of attribute definitions from content type
        instance_data: Instance data dictionary to encrypt

    Returns:
        New dictionary with password_secret fields encrypted
    """
    encrypted_data = instance_data.copy()

    for attr in content_type_attributes:
        if attr.get("type") == "password_secret":
            attr_name = attr["name"]
            value = encrypted_data.get(attr_name)

            if value and isinstance(value, str) and value.strip():
                # Only encrypt non-empty strings
                # Check if already encrypted (starts with specific pattern)
                if not value.startswith("gAAAAA"):  # Fernet tokens start with this
                    encrypted_data[attr_name] = encrypt_secret(value)

    return encrypted_data


def decrypt_password_secret_fields(content_type_attributes: List[Dict], instance_data: Dict) -> Dict:
    """
    Decrypt all password_secret fields in instance data after reading from database.

    Args:
        content_type_attributes: List of attribute definitions from content type
        instance_data: Instance data dictionary to decrypt

    Returns:
        New dictionary with password_secret fields decrypted
    """
    decrypted_data = instance_data.copy()

    for attr in content_type_attributes:
        if attr.get("type") == "password_secret":
            attr_name = attr["name"]
            value = decrypted_data.get(attr_name)

            if value and isinstance(value, str):
                try:
                    decrypted_data[attr_name] = decrypt_secret(value)
                except Exception:
                    # If decryption fails, leave as is (might already be decrypted)
                    pass

    return decrypted_data


def mask_password_secret_fields(content_type_attributes: List[Dict], instance_data: Dict) -> Dict:
    """
    Mask all password_secret fields in instance data for API responses.

    Args:
        content_type_attributes: List of attribute definitions from content type
        instance_data: Instance data dictionary to mask

    Returns:
        New dictionary with password_secret fields masked
    """
    masked_data = instance_data.copy()

    for attr in content_type_attributes:
        if attr.get("type") == "password_secret":
            attr_name = attr["name"]
            value = masked_data.get(attr_name)

            if value and isinstance(value, str):
                try:
                    # Decrypt first, then mask
                    decrypted = decrypt_secret(value)
                    masked_data[attr_name] = mask_secret(decrypted)
                except Exception:
                    # If decryption fails, just mask what we have
                    masked_data[attr_name] = mask_secret(value)

    return masked_data
