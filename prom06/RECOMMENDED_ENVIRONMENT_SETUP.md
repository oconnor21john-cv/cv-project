# Recommended Environment Setup

## 🎯 Best Environment: Visual Studio Code

### Why VS Code is Perfect for This Project:

1. **View Mermaid Diagrams** - Renders network diagrams in real-time
2. **Edit Documentation** - Full markdown support with preview
3. **Work with CSV Files** - Built-in CSV viewer/editor
4. **Run Python Scripts** - Integrated terminal and Python support
5. **Version Control** - Built-in Git integration
6. **Free & Lightweight** - No cost, fast performance

---

## 🚀 Complete Setup Guide

### Step 1: Install VS Code (if not already installed)

**Download:** https://code.visualstudio.com/

**Windows Installation:**
```powershell
# Using Chocolatey (if available)
choco install vscode

# Or download installer from website
```

**Mac Installation:**
```bash
# Using Homebrew
brew install --cask visual-studio-code

# Or download from website
```

---

### Step 2: Install Required VS Code Extensions

Open VS Code and install these extensions:

#### **Essential Extensions:**

1. **Markdown Preview Mermaid Support** ⭐ CRITICAL
   - ID: `bierner.markdown-mermaid`
   - Purpose: Renders Mermaid diagrams in markdown files
   - How: Press `Ctrl+P`, type: `ext install bierner.markdown-mermaid`

2. **Rainbow CSV** ⭐ RECOMMENDED
   - ID: `mechatroner.rainbow-csv`
   - Purpose: Color-codes CSV files, makes them readable
   - How: Press `Ctrl+P`, type: `ext install mechatroner.rainbow-csv`

3. **Python** (if using diagram generator)
   - ID: `ms-python.python`
   - Purpose: Python language support
   - How: Press `Ctrl+P`, type: `ext install ms-python.python`

#### **Nice-to-Have Extensions:**

4. **Markdown All in One**
   - ID: `yzhang.markdown-all-in-one`
   - Purpose: Enhanced markdown editing

5. **Excel Viewer**
   - ID: `grapecity.gc-excelviewer`
   - Purpose: View CSV/Excel files in table format

6. **GitLens** (if using Git)
   - ID: `eamodio.gitlens`
   - Purpose: Enhanced Git integration

---

### Step 3: Open the Project

```powershell
# In VS Code: File > Open Folder
# Select: C:\Users\John\Documents\Comp Sci Msc\web\it3\prom06
```

Or from command line:
```powershell
cd "C:\Users\John\Documents\Comp Sci Msc\web\it3\prom06"
code .
```

---

### Step 4: View Mermaid Diagrams

1. Open `Mermaid_Diagrams.md`
2. Press `Ctrl+Shift+V` (Windows) or `Cmd+Shift+V` (Mac)
3. Diagrams render automatically! 🎉

**Shortcut Tips:**
- `Ctrl+Shift+V` - Markdown preview
- `Ctrl+K V` - Preview side-by-side
- `Ctrl+B` - Toggle sidebar

---

### Step 5: View CSV Files

**Option A: Built-in viewer**
1. Click on `IPv4_Address_Plan.csv`
2. Data displays in columns

**Option B: Table view (with Excel Viewer extension)**
1. Right-click CSV file
2. Select "Open Preview"
3. View as formatted table

---

### Step 6: Python Environment (for diagram generation)

#### **Install Python:**

**Windows:**
```powershell
# Check if Python installed
python --version

# If not installed:
# Download from: https://www.python.org/downloads/
# Or use Chocolatey:
choco install python
```

**Mac:**
```bash
# Using Homebrew
brew install python
```

#### **Install Graphviz:**

**Windows:**
```powershell
# Option 1: Chocolatey
choco install graphviz

# Option 2: Download installer
# Visit: https://graphviz.org/download/
```

**Mac:**
```bash
brew install graphviz
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install graphviz
```

#### **Install Python Packages:**

```powershell
# In VS Code terminal (Ctrl+`)
pip install graphviz

# Verify installation
python -c "import graphviz; print('Graphviz OK')"
```

---

## 🎨 VS Code Workspace Configuration

Create a workspace settings file for optimal experience:

### `.vscode/settings.json` (optional):

```json
{
  "markdown.preview.breaks": true,
  "markdown.preview.fontSize": 14,
  "files.associations": {
    "*.md": "markdown"
  },
  "csv-preview.separator": ",",
  "csv-preview.hasHeaders": true,
  "python.formatting.provider": "black",
  "[markdown]": {
    "editor.wordWrap": "on"
  }
}
```

---

## 🖥️ Alternative Environments

### Option 2: Web Browser (No Installation)

**For Viewing Only:**

1. **Mermaid Diagrams:**
   - Visit: https://mermaid.live/
   - Copy/paste diagram code
   - View and export

2. **CSV Files:**
   - Upload to Google Sheets
   - Or use: https://www.convertcsv.com/csv-viewer-editor.htm

3. **Markdown Files:**
   - View on GitHub (if you push to repo)
   - Or use: https://dillinger.io/

**Pros:**
- ✅ No installation needed
- ✅ Works anywhere

**Cons:**
- ❌ Need to copy/paste
- ❌ No integrated workflow

---

### Option 3: Jupyter Notebook (For Python-Heavy Work)

**If you prefer notebooks:**

```bash
# Install Jupyter
pip install jupyter

# Launch
jupyter notebook
```

**Create a notebook to:**
- Run Python diagram generator
- Document your work inline
- Export as PDF/HTML

**Pros:**
- ✅ Good for Python experiments
- ✅ Inline documentation
- ✅ Easy to share

**Cons:**
- ❌ Not ideal for markdown files
- ❌ More complex setup

---

### Option 4: PyCharm (Professional Python IDE)

**Good if you're doing heavy Python work:**

**Download:** https://www.jetbrains.com/pycharm/

**Features:**
- Professional Python IDE
- Better debugging
- Built-in terminal
- Git integration

**Pros:**
- ✅ Best Python support
- ✅ Professional debugging

**Cons:**
- ❌ Heavier than VS Code
- ❌ Paid (Professional version)
- ❌ Less good for markdown

---

### Option 5: Command Line + Text Editor

**Minimal Setup:**

```powershell
# View markdown
code Mermaid_Diagrams.md

# Run Python script
python generate_network_diagrams.py

# View CSV
start Excel IPv4_Address_Plan.csv

# Or use Notepad++, Sublime Text, etc.
```

**Pros:**
- ✅ Lightweight
- ✅ Fast

**Cons:**
- ❌ No integrated preview
- ❌ Manual workflow

---

## 📊 Environment Comparison

| Environment | Best For | Ease | Features | Cost |
|-------------|----------|------|----------|------|
| **VS Code** | Everything | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Free |
| **Browser** | Quick viewing | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Free |
| **Jupyter** | Python work | ⭐⭐⭐ | ⭐⭐⭐⭐ | Free |
| **PyCharm** | Python only | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $$ |
| **CLI** | Minimalists | ⭐⭐ | ⭐⭐ | Free |

---

## 🎯 My Specific Recommendation for You

Based on your Windows environment and this project:

### **Primary Setup: VS Code**

```powershell
# 1. Install VS Code (if needed)
# Download from: https://code.visualstudio.com/

# 2. Install extensions
# Open VS Code: Ctrl+Shift+X
# Search and install:
#   - Markdown Preview Mermaid Support
#   - Rainbow CSV
#   - Python (if generating diagrams)

# 3. Open your folder
cd "C:\Users\John\Documents\Comp Sci Msc\web\it3\prom06"
code .

# 4. View Mermaid diagrams
# Open Mermaid_Diagrams.md
# Press Ctrl+Shift+V

# Done! 🎉
```

### **Secondary Setup: Python for Diagram Generation**

```powershell
# 1. Check Python installed
python --version

# 2. Install packages
pip install graphviz

# 3. Install Graphviz software
choco install graphviz
# Or download from: https://graphviz.org/download/

# 4. Generate diagrams
python generate_network_diagrams.py

# 5. View output in network_diagrams/ folder
```

---

## 🔧 Troubleshooting Common Issues

### Issue: Mermaid diagrams not rendering in VS Code

**Solution:**
```
1. Verify extension installed: 
   - Ctrl+Shift+X
   - Search "Mermaid"
   - Should show "Markdown Preview Mermaid Support" as installed

2. Restart VS Code

3. Open Mermaid_Diagrams.md

4. Press Ctrl+Shift+V (not just Ctrl+V)

5. If still not working:
   - Try Ctrl+K V for side-by-side preview
```

### Issue: Python not found

**Solution:**
```powershell
# Add Python to PATH
# Or reinstall Python with "Add to PATH" checked

# Verify:
python --version
pip --version
```

### Issue: Graphviz not found error

**Solution:**
```powershell
# Check if graphviz executable in PATH
where dot

# If not found:
# 1. Reinstall Graphviz
# 2. Add to PATH manually:
#    C:\Program Files\Graphviz\bin

# Or use full path in script
```

### Issue: CSV looks weird in VS Code

**Solution:**
```
1. Install "Rainbow CSV" extension
2. Reopen CSV file
3. Right-click > "Open Preview" (if Excel Viewer installed)
```

---

## 💡 Productivity Tips

### **Quick Keyboard Shortcuts (VS Code):**

```
Ctrl+P          Quick file open
Ctrl+Shift+V    Markdown preview
Ctrl+K V        Split preview
Ctrl+`          Toggle terminal
Ctrl+B          Toggle sidebar
Ctrl+Shift+E    Explorer view
Ctrl+Shift+F    Search across files
Ctrl+,          Settings
```

### **Workflow Tips:**

1. **Keep preview open:**
   - Use `Ctrl+K V` for side-by-side
   - Edit markdown on left, see preview on right

2. **Use integrated terminal:**
   - Press `Ctrl+`\` to open terminal
   - Run Python scripts without leaving VS Code

3. **Multi-cursor editing:**
   - Alt+Click for multiple cursors
   - Ctrl+D to select next occurrence

4. **Quick navigation:**
   - Ctrl+P then type filename
   - Ctrl+G to go to line number

---

## 🎓 Learning Resources

### **VS Code:**
- Official docs: https://code.visualstudio.com/docs
- Keyboard shortcuts: https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf

### **Mermaid:**
- Live editor: https://mermaid.live/
- Documentation: https://mermaid.js.org/

### **Python/Graphviz:**
- Graphviz docs: https://graphviz.org/documentation/
- Python graphviz: https://graphviz.readthedocs.io/

---

## ✅ Quick Start Checklist

- [ ] Install VS Code
- [ ] Install "Markdown Preview Mermaid Support" extension
- [ ] Install "Rainbow CSV" extension
- [ ] Open prom06 folder in VS Code
- [ ] Open Mermaid_Diagrams.md
- [ ] Press Ctrl+Shift+V to view diagrams
- [ ] Open CSV files to view addressing data
- [ ] (Optional) Install Python + Graphviz for diagram generation

---

## 🎬 Video Guide Equivalent

If this were a video tutorial, here's what you'd do:

**Part 1: Basic Setup (5 minutes)**
```
00:00 - Download VS Code
00:30 - Install VS Code
01:00 - Open VS Code
01:15 - Install Markdown Preview Mermaid extension
02:00 - Open prom06 folder
02:30 - Open Mermaid_Diagrams.md
03:00 - Press Ctrl+Shift+V
03:05 - See beautiful network diagrams! 🎉
```

**Part 2: Advanced Setup (15 minutes)**
```
00:00 - Install Python
02:00 - Install pip packages
04:00 - Install Graphviz software
06:00 - Verify installation
08:00 - Run generate_network_diagrams.py
10:00 - View generated PNG files
```

---

## 📝 Summary

### **BEST CHOICE: VS Code**

**Installation time:** 10 minutes  
**Learning curve:** Low  
**Best for:** All documentation and diagram work  

### **Minimum to Get Started:**

1. Install VS Code
2. Install Mermaid extension
3. Open Mermaid_Diagrams.md
4. Press Ctrl+Shift+V

**That's it! You can view all diagrams in 10 minutes!**

---

## 🎯 What to Do Right Now

```powershell
# If you have VS Code already:
cd "C:\Users\John\Documents\Comp Sci Msc\web\it3\prom06"
code .

# Then in VS Code:
# 1. Install Mermaid extension (Ctrl+Shift+X)
# 2. Open Mermaid_Diagrams.md
# 3. Press Ctrl+Shift+V
# 4. Enjoy your network diagrams! 🎉
```

---

*Environment Setup Guide v1.0 | October 26, 2025*

