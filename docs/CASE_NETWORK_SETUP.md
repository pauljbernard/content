# CASE Network Integration Setup Guide

## Overview

The system now supports importing educational standards from the **CASE Network** (1EdTech's Competencies and Academic Standards Exchange Network) using OAuth2 authentication.

This integration allows you to securely access standards from the CASE Network API at https://casenetwork.1edtech.org/

## Architecture

The integration consists of:

1. **Secrets Management System** - Securely stores OAuth2 credentials
2. **Secrets Helper Service** - Retrieves credentials for system use
3. **OAuth2 CASE Parser** - Authenticates with CASE Network and parses standards
4. **Frontend UI** - User-friendly interface for importing from CASE Network

## Setup Instructions

### Step 1: Obtain CASE Network Credentials

1. Register for a CASE Network account at https://casenetwork.1edtech.org/
2. Create an OAuth2 client application
3. Note your **Client ID** and **Client Secret**

### Step 2: Store Credentials in Secrets

1. Log in to the system as a **knowledge_engineer**
2. Navigate to **Secrets** in the System menu
3. Click **New Secret**
4. Fill in the form:
   - **Secret Name**: `case_network_key` (exactly this name - required!)
   - **API Key / Username**: Your OAuth2 Client ID
   - **Secret Value / Password**: Your OAuth2 Client Secret
   - **Description**: "CASE Network OAuth2 credentials for standards import"
   - **Category**: API_KEY
   - **Environment**: PRODUCTION (or appropriate environment)
   - **Active**: ✓ Checked
5. Click **Create**

### Step 3: Import Standards from CASE Network

1. Navigate to **Import** → **CASE Standards Importer**
2. Fill in the import form:
   - **Source Type**: Select "CASE Network (OAuth2 authenticated)"
   - **Framework Selection** (if available):
     - The system will attempt to fetch available frameworks automatically
     - If the framework list loads, select your desired framework
     - The source location and metadata will auto-populate
   - **Manual Entry** (if framework list doesn't load):
     - Enter the CASE Network API endpoint URL manually in Source Location
     - Example: `https://casenetwork.1edtech.org/api/v1/CFPackages/abc123`
     - Fill in metadata (name, code, subject, etc.) manually
   - **Format**: CASE (IMS Global Standard)
3. Click **Start Import**

The system will:
1. Retrieve your OAuth2 credentials from Secrets
2. Request an access token from the CASE Network
3. Authenticate your request with the access token
4. Download and parse the standards
5. Create the standard in your database

**Note**: The framework list feature requires the CASE Network API to support the `/api/v1/CFDocuments` endpoint. If this endpoint is not available or returns an error, you can still import standards by manually entering the CFPackage URL.

## How It Works

### OAuth2 Flow

```
┌─────────────┐                                    ┌────────────────────┐
│  Standards  │                                    │   CASE Network     │
│  Importer   │                                    │   OAuth2 Server    │
└─────┬───────┘                                    └──────────┬─────────┘
      │                                                       │
      │ 1. Retrieve credentials                              │
      │    (client_id, client_secret)                        │
      ├──────────────────┐                                   │
      │                  │                                   │
      │    ┌─────────────▼────────┐                         │
      │    │   Secrets Helper     │                         │
      │    │  (case_network_key)  │                         │
      │    └─────────────┬────────┘                         │
      │◄─────────────────┘                                   │
      │                                                      │
      │ 2. POST /case-oauth2/clienttoken                    │
      │    (client credentials grant)                        │
      ├─────────────────────────────────────────────────────►│
      │                                                      │
      │ 3. Access Token                                      │
      │◄─────────────────────────────────────────────────────┤
      │                                                      │
      │                                    ┌─────────────────▼──────┐
      │                                    │  CASE Network API      │
      │                                    │  (Standards Data)      │
      │ 4. GET /api/v1/CFPackages/{id}    └─────────────────┬──────┘
      │    Authorization: Bearer {token}                     │
      ├──────────────────────────────────────────────────────►
      │                                                      │
      │ 5. CASE JSON (standards data)                       │
      │◄─────────────────────────────────────────────────────┤
      │                                                      │
      │ 6. Parse and save to database                        │
      │                                                      │
```

### Token Caching

The OAuth2 access token is cached to avoid unnecessary token requests:
- Tokens are cached with their expiration time
- Tokens are refreshed 1 minute before expiration
- Cache is shared across import jobs in the same session

### Security

- **Credentials stored encrypted**: The Secrets system uses Fernet encryption (AES-128) to encrypt credentials in the database
- **Role-based access**: Only knowledge_engineers can view/manage secrets
- **OAuth2 client credentials grant**: Industry-standard authentication method
- **HTTPS only**: All communication with CASE Network uses encrypted HTTPS

## Troubleshooting

### Error: "CASE Network credentials not found"

**Solution**: Ensure you have created a secret with the exact name `case_network_key` (case-sensitive).

### Error: "Failed to get OAuth2 token: HTTP 401"

**Possible causes**:
1. Invalid Client ID or Client Secret
2. Credentials expired or revoked

**Solution**:
1. Verify your credentials are correct in the CASE Network dashboard
2. Update the `case_network_key` secret with new credentials

### Error: "Failed to fetch CASE data: HTTP 403"

**Possible causes**:
1. Access token expired
2. Insufficient permissions for the requested resource

**Solution**:
1. Token should auto-refresh - try again
2. Verify your CASE Network account has access to the requested standards

### Error: "Database session required for CASE Network authentication"

**Cause**: System error - the database session was not passed to the importer

**Solution**: Contact system administrator - this is a code-level issue

## API Endpoints

### CASE Network API

- **Base URL**: https://casenetwork.1edtech.org/
- **OAuth2 Token Endpoint**: https://casenetwork.1edtech.org/case-oauth2/clienttoken
- **CASE API**: https://casenetwork.1edtech.org/api/v1/

### Internal Secrets API

Knowledge engineers can programmatically access secrets via:

- **List secrets**: `GET /api/v1/secrets`
- **Get secret value**: `GET /api/v1/secrets/{id}/value`
- **Get by name**: `GET /api/v1/secrets/by-name/case_network_key`

All endpoints require authentication and knowledge_engineer role.

## Multi-Environment Support

The Secrets system supports multiple environments. You can create separate credentials for:

- **PRODUCTION**: Production CASE Network credentials
- **STAGING**: Staging/testing credentials
- **DEVELOPMENT**: Development credentials
- **TEST**: Test environment credentials

To use different environments:
1. Create multiple secrets with the same `case_network_key` name but different environments
2. The system will use the first active secret found (currently no environment filtering)
3. Future enhancement: Allow specifying environment in import form

## Files Modified

### Backend

- `backend/services/secrets_helper.py` - New helper service for retrieving secrets
- `backend/services/standards_importer.py` - Updated CASE parser with OAuth2 support
- `backend/api/v1/standards.py` - Pass database session to import service

### Frontend

- `frontend/src/pages/CASEStandardsImporter.jsx` - Added CASE Network option to UI

### Documentation

- `docs/CASE_NETWORK_SETUP.md` - This file

## Related Documentation

- [Secrets Management System](../backend/api/v1/secrets.py)
- [CASE Specification](https://www.imsglobal.org/spec/case/v1p1)
- [1EdTech Security Framework](https://www.imsglobal.org/spec/security/v1p1)
- [CASE Network](https://casenetwork.1edtech.org/)

## Support

For issues or questions:
1. Check this documentation
2. Review the error messages and troubleshooting section
3. Contact your system administrator
4. Submit an issue to the development team

---

**Last Updated**: 2025-11-08
**Version**: 1.0.0
