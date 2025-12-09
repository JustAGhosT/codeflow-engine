# GitHub App Registration - Quick Fill Guide

Fill out the form step by step. Use your deployed app URL or localhost for testing.

## âœ… What You've Already Done

- **App name:** `CodeFlow` âœ“
- **Expire user authorization tokens:** âœ… Checked âœ“
- **Enable Device Flow:** âŒ Unchecked âœ“

## ðŸ“ What to Fill In Now

### 1. Description

Replace the current description with:

```
Automated setup and configuration for Twines and Straps SA platform.
One-click installation that automatically configures Azure secrets and GitHub Actions workflows.
```

### 2. Homepage URL

**If your app is deployed:**
```
https://dev-app-san-tassa.azurewebsites.net
```

**If testing locally (use GitHub repo URL):**
```
https://github.com/JustAGhosT/twinesandstraps
```

### 3. Callback URL

**If your app is deployed:**
```
https://dev-app-san-tassa.azurewebsites.net/api/github-app/callback
```

**If testing locally:**
```
http://localhost:3000/api/github-app/callback
```

### 4. Request user authorization (OAuth) during installation

âœ… **CHECK THIS BOX** - You need this to identify the installing user

### 5. Setup URL (optional)

**If your app is deployed:**
```
https://dev-app-san-tassa.azurewebsites.net/setup
```

**If testing locally:**
```
http://localhost:3000/setup
```

### 6. Redirect on update

âœ… **CHECK THIS BOX** - Redirects users when repos are added/removed

### 7. Webhook URL

**If your app is deployed:**
```
https://dev-app-san-tassa.azurewebsites.net/api/github-app/webhook
```

**If testing locally (use ngrok):**
```
https://your-ngrok-url.ngrok.io/api/github-app/webhook
```

### 8. Webhook Secret

Generate a secret (run this in PowerShell or terminal):

```powershell
# PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

Or use OpenSSL:
```bash
openssl rand -hex 32
```

**âš ï¸ SAVE THIS SECRET!** You'll need it for `GITHUB_WEBHOOK_SECRET` environment variable.

### 9. Permissions

Click to expand **Repository permissions** and set:

- **Secrets:** `Read and write` âœ…
- **Metadata:** `Read-only` âœ…
- **Contents:** `Read-only` âœ…
- **Actions:** `Read-only` (optional)
- Everything else: `No access`

**Organization permissions:** Leave all as `No access`

**Account permissions:** Leave all as `No access`

### 10. Subscribe to Events

Check these boxes:

- âœ… **Installation** - When app is installed/uninstalled
- âœ… **Installation repositories** - When repos are added/removed

Leave everything else unchecked.

### 11. Where can this GitHub App be installed?

Select: **âœ… Any account** (recommended)

Or if you only want it on your account: **Only on this account**

---

## ðŸŽ¯ Quick Summary

**Required Fields:**
- âœ… App name: `CodeFlow`
- âœ… Description: (see above)
- âœ… Homepage URL: Your app URL or GitHub repo
- âœ… Callback URL: Your app URL + `/api/github-app/callback`
- âœ… Setup URL: Your app URL + `/setup`
- âœ… Webhook URL: Your app URL + `/api/github-app/webhook`
- âœ… Webhook Secret: Generate one (save it!)
- âœ… Permissions: Secrets (write), Metadata (read), Contents (read)
- âœ… Events: Installation, Installation repositories

**Checkboxes:**
- âœ… Expire user authorization tokens
- âœ… Request user authorization (OAuth) during installation
- âœ… Redirect on update
- âœ… Active (webhook)

**Unchecked:**
- âŒ Enable Device Flow

---

## ðŸš€ After Creating the App

You'll get:
1. **App ID** â†’ Save as `GITHUB_APP_ID`
2. **Client ID** â†’ Save as `GITHUB_APP_CLIENT_ID`
3. **Client Secret** â†’ Save as `GITHUB_APP_CLIENT_SECRET`
4. **Private Key** â†’ Download .pem file â†’ Save as `GITHUB_APP_PRIVATE_KEY`
5. **Webhook Secret** â†’ The one you generated â†’ Save as `GITHUB_WEBHOOK_SECRET`

Add all of these to your Azure App Service environment variables or `.env.local` file.

