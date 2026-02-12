# 02 - Delegated Authentication (Device Code / Browser)

This demo shows how to call Microsoft Graph using **delegated permissions** (on behalf of a signed‑in user) with **Device Code Flow** and **Interactive Browser Flow** using the Microsoft Graph Python SDK.

---

## 🎯 Scenario

- Authenticate a **user** interactively.
- Use `DeviceCodeCredential` (CLI/headless) and/or `InteractiveBrowserCredential` (desktop) from `azure-identity`.
- Use `GraphServiceClient` from `msgraph-sdk`.
- Call endpoints such as:
  - `/me`
  - `/users/{id}` (as the signed-in user)

---

## 📂 Files

- **`config.py`**  
  Shared configuration: `CLIENT_ID`, `TENANT_ID`, `GRAPH_SCOPES`.

- **`auth_delegated.py`**  
  Implements `DelegatedAuthProvider`:
  - `auth_type='device_code'` (default) or `'browser'`
  - Builds delegated `GraphServiceClient` using:
    - `DeviceCodeCredential`
    - `InteractiveBrowserCredential`

- **`demo.py`**  
  Example Graph calls (e.g., get `/me`, list messages).

---

## 🔧 Azure AD App Registration (Delegated)

1. Go to **Azure Portal** → **Entra ID** → **App registrations**.
2. Select **New registration**:
   - Name: `graph-python-delegated-auth-demo`
   - Supported account types: choose per scenario
   - Redirect URI:  
     - Optional for Device Code  
     - Required for interactive browser flows
3. Click **Register**.

---

### Enable Public Client Flows (Required)

1. Open the **Authentication** blade.
2. Under **Advanced settings**, enable:
   - **Allow public client flows** → **Yes**
3. Save changes.

---

### Configure API Permissions (Delegated)

1. Go to **API permissions** → **Add a permission**.
2. Choose **Microsoft Graph** → **Delegated permissions**.
3. Add at minimum:
   - `User.Read`
4. Additional common permissions:
   - `Mail.Read`
   - `Calendars.Read` or `Calendars.ReadWrite`
5. Click **Add permissions**.
6. Optional (depending on tenant policy):
   - **Grant admin consent** or allow user consent.

---

## 🔐 Environment Configuration

Create a `.env` file in this folder:

```env
CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
TENANT_ID=yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy
GRAPH_SCOPES=User.Read
````

Notes:

*   No `CLIENT_SECRET` is required for **public client** delegated flows like Device Code.
*   `GRAPH_SCOPES` is **space-separated**, e.g.:  
    `User.Read Mail.Read`

***

## 🚀 Run the Demo

From the **repo root** (venv activated):

```bash
cd 02-delegated-auth
pip install -r requirements.txt  # if needed
python demo.py
```

Depending on your selected `auth_type`, you will see:

***

### 🔑 Device Code Flow

Terminal output example:

    To sign in, use a web browser to open the page https://microsoft.com/devicelogin
    and enter the code ABCD-EFGH to authenticate.

Steps:

1.  Go to <https://microsoft.com/devicelogin>
2.  Enter the displayed code
3.  Sign in with your Microsoft 365 account
4.  Consent to requested permissions
5.  Return to the terminal — script continues and calls Microsoft Graph

***

### 🌐 Interactive Browser Flow

*   A browser window opens automatically
*   You sign in and consent
*   The app receives tokens and calls Microsoft Graph

***

## 🧠 Key Concepts

*   **Delegated permissions**  
    App acts as the **signed-in user**; effective permissions = intersection of:
    *   permissions granted to the app
    *   permissions the user actually has

*   **Device Code Flow**  
    Ideal for CLI/headless environments; user authenticates on another device.

*   **Interactive Browser Flow**  
    Best for rich desktop environments.

*   **`/me` endpoint**  
    Only works in **delegated** (not app‑only) scenarios.

***

## 🐛 Common Errors

### ❌ `invalid_client` / `AADSTS7000218` (client\_secret required)

Cause: App is configured as **confidential client** only.  
Fix: Enable **public client flows** and **do not** use a client secret with `DeviceCodeCredential`.

***

### ❌ `insufficient privileges` / `Authorization_RequestDenied`

Cause:  
App has permissions, but user lacks rights (e.g., accessing another user’s mailbox).

***

### ❌ Consent blocked ("Need admin approval")

Cause:  
User cannot consent to the requested scopes.  
Fix:  
Administrator must grant consent or allow user consent.

***

## 📚 References

*   Add user authentication to Python apps for Microsoft Graph
*   Device Code Flow documentation
*   Authentication providers for Microsoft Graph Python SDK
*   Official `msgraph-sdk-python` samples




