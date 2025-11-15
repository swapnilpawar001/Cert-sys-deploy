# 📄 Certificate Template Upload Instructions

## From Google Slides to Codespaces

### Method 1: Download & Upload (Recommended)
1. **Open your certificate in Google Slides**
2. **File → Download → PNG Image** (better quality) or JPEG
3. **Save as**: `certificate-template.png` or `certificate-template.jpg`
4. **In Codespaces**: Drag & drop file to `data/certificate-templates/raw/`

### Method 2: Via GitHub Web
1. **Go to your repository on GitHub**
2. **Navigate to**: `data/certificate-templates/raw/`
3. **Click "Add file" → "Upload files"**
4. **Upload your template file**
5. **In Codespaces**: Run `git pull origin main`

### Method 3: Share Link (Temporary)
1. **In Google Slides**: File → Share → Get link
2. **Make link "Anyone with link can view"**
3. **Copy the sharing link**
4. **In Codespaces**: We'll help you download it

## After Upload
Run: `python scripts/check-template.py` to verify upload
