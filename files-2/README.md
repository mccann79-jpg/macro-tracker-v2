# Macro Tracker PWA

A progressive web app for tracking macros, meals, and weight — designed to be added to your iPhone Home Screen.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Main app (all HTML/CSS/JS in one file) |
| `manifest.json` | PWA manifest for Home Screen install |
| `sw.js` | Service worker for offline support |
| `generate-icons.html` | Open in browser to download all required icons |
| `icon-192.png` | Android/Chrome icon (generate with above) |
| `icon-512.png` | Large icon (generate with above) |
| `icon-180.png` | Apple Touch Icon (generate with above) |
| `favicon-16.png` | Browser tab icon (generate with above) |
| `favicon-32.png` | Browser tab icon (generate with above) |
| `favicon-64.png` | Browser tab icon (generate with above) |

## Setup Instructions

### 1. Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click **Add project** → name it (e.g., "macro-tracker") → Create
3. Go to **Build → Realtime Database → Create Database**
4. Choose your region → **Start in test mode** → Enable
5. Go to **Project Settings** (gear icon) → **General** → scroll to **Your apps**
6. Click the web icon (`</>`) → name it → Register app
7. Copy the `firebaseConfig` object values

### 2. Add Firebase Config to the App

Open `index.html` and find this section near the top of the `<script>`:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY_HERE",
    authDomain: "YOUR_PROJECT.firebaseapp.com",
    databaseURL: "https://YOUR_PROJECT-default-rtdb.firebaseio.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT.firebasestorage.app",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

Replace each `YOUR_...` value with your actual Firebase config values.

### 3. Set Firebase Database Rules

In Firebase Console → Realtime Database → Rules, set:

```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

> **Note:** This is open access. For better security, use:
> ```json
> {
>   "rules": {
>     "$pin": {
>       ".read": true,
>       ".write": true
>     }
>   }
> }
> ```

### 4. Generate Icons

1. Open `generate-icons.html` in your browser
2. Click each button to download the icon files
3. Place all downloaded `.png` files in the same folder as `index.html`

### 5. Deploy to GitHub Pages

1. Create a new GitHub repository
2. Push all files to the `main` branch:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```
3. Go to **Settings → Pages**
4. Source: **Deploy from a branch** → Branch: `main` → Folder: `/ (root)` → Save
5. Your site will be live at `https://YOUR_USERNAME.github.io/YOUR_REPO/`

### 6. Add to iPhone Home Screen

1. Open your GitHub Pages URL in Safari on your iPhone
2. Tap the **Share** button (square with arrow)
3. Scroll down and tap **Add to Home Screen**
4. Name it "Macros" → tap **Add**

The app will now launch fullscreen like a native app with the dark theme and bottom tab navigation.

## Features

- **Food Database** — Add, edit, search, import/export foods with full macro data
- **Meal Builder** — Combine foods into reusable meals with per-serving calculations
- **My Day** — Track daily intake with goals, progress bars, and close-out history
- **Weight Tracking** — Log weight, see 7-day averages, trend lines, and goal projections
- **Charts** — Protein, calorie, carbs, fats history charts with toggleable elements
- **Firebase Sync** — PIN-based cloud sync across all your devices
- **Offline Support** — Service worker caches the app for offline use
- **PWA** — Installable on iPhone Home Screen with native-app feel
- **Import/Export** — CSV import/export for all data types
