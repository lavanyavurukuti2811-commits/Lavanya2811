# How to Run SentiMart Frontend in VS Code

## Option 1: Using Live Server Extension (Recommended) ⭐

### Step 1: Install Live Server Extension
1. Open **VS Code**
2. Go to **Extensions** (Click the Extensions icon on the left sidebar or press `Ctrl+Shift+X`)
3. Search for **"Live Server"** by Ritwick Dey
4. Click **Install**

### Step 2: Run the Frontend
1. Open the folder containing `sentimart-frontend.html` in VS Code
2. Right-click on `sentimart-frontend.html` in the file explorer
3. Select **"Open with Live Server"**
4. Your default browser will open automatically at `http://127.0.0.1:5500`

**Advantages:**
- ✅ Auto-refresh on file changes
- ✅ No configuration needed
- ✅ Very fast and easy

---

## Option 2: Using Python's Built-in Server

### Prerequisites:
- Python installed on your system (Python 3.x recommended)

### Step 1: Open Terminal in VS Code
1. Open the folder with `sentimart-frontend.html`
2. Press `Ctrl + ` (backtick) to open the terminal in VS Code
3. Or go to **Terminal → New Terminal**

### Step 2: Run Python Server
**For Python 3.x:**
```bash
python -m http.server 8000
```

**For Python 2.x:**
```bash
python -m SimpleHTTPServer 8000
```

### Step 3: Open in Browser
- Visit `http://localhost:8000/sentimart-frontend.html`

**Output in terminal:**
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

---

## Option 3: Using Node.js HTTP Server

### Prerequisites:
- Node.js installed

### Step 1: Install http-server globally
```bash
npm install -g http-server
```

### Step 2: Open Terminal in VS Code
Press `Ctrl + ` (backtick)

### Step 3: Run the Server
```bash
http-server
```

### Step 4: Open in Browser
- Visit `http://localhost:8080/sentimart-frontend.html`

---

## Option 4: Using VS Code Built-in Features

### Step 1: Install Web Server Extension
1. Go to Extensions (`Ctrl+Shift+X`)
2. Search for **"Simple Web Server"** or **"Web Server"**
3. Install one of the available extensions

### Step 2: Start Server
- Click the server icon in the status bar
- Or use Command Palette (`Ctrl+Shift+P`) and search for the extension commands

---

## Complete Step-by-Step Guide (For Beginners)

### 📥 Step 1: Clone/Open the Repository
```bash
# Clone if you haven't already
git clone https://github.com/lavanyavurukuti2811-commits/Lavanya2811.git

# Navigate to the folder
cd Lavanya2811

# Open in VS Code
code .
```

### 🔌 Step 2: Install Live Server (Easiest Method)
1. Click **Extensions** icon (left sidebar)
2. Search: `Live Server`
3. Click **Install** on the first result by Ritwick Dey

### ▶️ Step 3: Run the Frontend
1. Right-click on `sentimart-frontend.html`
2. Select **"Open with Live Server"**
3. Your browser opens automatically! 🎉

### 🧪 Step 4: Test the Application
- Select a language from the dropdown
- Enter a customer review in the text area
- Click **"Analyze Sentiment"**
- See the results with beautiful visualizations

---

## Connecting to Backend API

After running the frontend, you'll need to connect it to your backend:

### Edit API URL in the Frontend
1. Open `sentimart-frontend.html` in VS Code
2. Find this line (around line 650):
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

3. Replace with your backend URL:
```javascript
const API_BASE_URL = 'http://your-backend-server:port/api';
```

4. Save (`Ctrl+S`)
5. The page will auto-refresh if using Live Server

### Expected Backend Response Format:
```json
{
    "sentiment": "positive",
    "confidence": 0.92,
    "scores": {
        "positive": 0.92,
        "neutral": 0.06,
        "negative": 0.02
    },
    "key_phrases": ["amazing product", "great quality"]
}
```

---

## Troubleshooting

### ❌ "Live Server not working"
- Make sure you installed the correct extension (by Ritwick Dey)
- Restart VS Code after installation
- Check if port 5500 is not already in use

### ❌ "Port 8000 already in use"
```bash
# Use a different port
python -m http.server 9000
# Then visit: http://localhost:9000
```

### ❌ "Cannot connect to backend API"
- Ensure your backend server is running
- Check the backend URL is correct
- Look at browser console for CORS errors (`F12`)

### ❌ "Blank page or no styles showing"
- Clear browser cache (`Ctrl+Shift+Delete`)
- Hard refresh (`Ctrl+Shift+R`)
- Check browser console for errors (`F12`)

---

## Debug Mode (Developer Tools)

### Open Browser Developer Tools:
- Press `F12` or `Ctrl+Shift+I`

### Check Console for Errors:
1. Go to **Console** tab
2. Look for red error messages
3. Check **Network** tab to see API calls

### Example Console Error:
```
Failed to fetch http://localhost:5000/api/analyze
CORS error: Access to XMLHttpRequest blocked
```

**Solution:** Enable CORS in your backend:
```python
# Flask backend example
from flask_cors import CORS
CORS(app)
```

---

## Quick Command Reference

| Task | Command |
|------|---------|
| Open folder in VS Code | `code .` |
| Open terminal | `Ctrl + `` |
| Open dev tools | `F12` |
| Hard refresh page | `Ctrl+Shift+R` |
| Save file | `Ctrl+S` |
| Search in project | `Ctrl+Shift+F` |
| Command palette | `Ctrl+Shift+P` |

---

## Summary

**Quickest Way (Recommended):**
1. Install Live Server extension
2. Right-click `sentimart-frontend.html`
3. Click "Open with Live Server"
4. Done! 🎉

**All methods work great!** Choose based on what's already installed on your system.

---

## Additional Resources

- [VS Code Documentation](https://code.visualstudio.com/docs)
- [Live Server GitHub](https://github.com/ritwickdey/vscode-live-server)
- [Python HTTP Server Guide](https://docs.python.org/3/library/http.server.html)
- [Node.js http-server](https://www.npmjs.com/package/http-server)

**Need help?** Check the browser console (`F12`) for detailed error messages! 🔍
