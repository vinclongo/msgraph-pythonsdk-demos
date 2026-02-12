# 01 - Application Authentication (Client Credentials)

This demo shows how to call Microsoft Graph using **app‑only (application) permissions** with the **client credentials flow** in Python using the Microsoft Graph SDK.

---

## 🎯 Scenario

- Authenticate as an **application** (no user sign‑in required).
- Use `ClientSecretCredential` from **azure‑identity**.
- Use `GraphServiceClient` from **msgraph‑sdk**.
- Perform operations requiring **application permissions** such as listing users or reading directory data.

---

## 📂 Files

- **`config.py`**  
  Loads configuration from `.env`: `CLIENT_ID`, `TENANT_ID`, `CLIENT_SECRET`, `GRAPH_SCOPES`.

- **`auth_application.py`**  
  Creates an app‑only `GraphServiceClient` using `ClientSecretCredential`.

- **`demo.py`**  
  Demonstrates example Graph operations (e.g., list users).

---

## 🔧 Azure AD App Registration

1. Go to **Azure Portal** → **Entra ID** → **App registrations**.
2. Select **New registration**:
   - Name: `graph-python-application-auth-demo`
   - Supported account types: choose based on your tenant needs
   - Redirect URI: **leave empty** (not needed for client credentials)
3. Click **Register**.

---

### Configure Client Credentials

1. Open **Certificates & secrets**.
2. Add **New client secret** and copy the **Value** immediately.
3. From **Overview**, copy:
   - **Application (client) ID**
   - **Directory (tenant) ID**

---

### Configure API Permissions (Application)

1. Go to **API permissions** → **Add a permission**.
2. Select **Microsoft Graph** → **Application permissions**.
3. Add at least:
   - `User.Read.All` (required for listing users)
4. Click **Add permissions**.
5. Click **Grant admin consent** (requires an administrator).

---

## 🔐 Environment Configuration

Create a `.env` file (based on `.env.example`):

```env
CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
TENANT_ID=yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy
CLIENT_SECRET=your-client-secret-value
GRAPH_SCOPES=https://graph.microsoft.com/.default
````

Notes:

*   `GRAPH_SCOPES` must be set to `.default`  
    → This instructs Microsoft Graph to use **all application permissions** granted to the app.

***

## 🚀 Run the Demo

From the repo root (with venv activated):

```bash
cd 01-application-auth
pip install -r requirements.txt  # if not already installed
python demo.py
```

Expected output:

*   Lists users in the tenant
*   Shows details such as:
    *   Display name
    *   User principal name (UPN)
    *   Object ID

***

## 🧠 Key Concepts

*   **Application permissions**  
    The app runs as itself (daemon service) — *not* as a user.

*   **Client credentials flow**  
    Uses `client_id` + `client_secret` to obtain an app‑only token.

*   **`/me` is not allowed**  
    App‑only authentication cannot call `/me`.  
    Instead use:
    *   `/users`
    *   `/users/{id | userPrincipalName}`

***

## 🐛 Common Errors

### ❌ `Authorization_RequestDenied` / Insufficient privileges

Cause: Missing or not admin‑consented application permissions.  
Fix: Ensure required permissions (e.g., `User.Read.All`) are added and admin‑consented.

***

### ❌ `invalid_client`

Cause: Incorrect `CLIENT_ID`, `TENANT_ID`, or `CLIENT_SECRET`.  
Fix: Reconfigure values in `.env`.

***

### ❌ Using `/me` with app‑only authentication

Cause: `/me` requires delegated permissions.  
Fix: Use:

*   `.users.by_user_id('user@domain.com')`
*   `.users.get()`

***

## 📚 References

*   Build Python apps with Microsoft Graph and app‑only authentication
*   Microsoft Graph permissions reference
*   Choose an authentication provider for Microsoft Graph

