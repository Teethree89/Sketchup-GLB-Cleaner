# SketchUp GLB Cleaner

## Fixes Washed-Out GLB Models from SketchUp Pro Exports

SketchUp Pro can export **GLB files** with the `KHR_materials_pbrSpecularGlossiness` extension, which can cause models to look **washed out or incorrect** when imported into various 3D applications (e.g., Three.js, Babylon.js, Blender, Unreal Engine, etc.).

This script **automatically cleans** the exported GLB file by **removing the SpecularGlossiness extension**, ensuring correct PBR shading. It works by:

1. **Converting the GLB to GLTF**  
2. **Removing the KHR_materials_pbrSpecularGlossiness extension**  
3. **Repacking the cleaned GLTF back into a GLB file**  
4. **Keeping the original GLB file untouched for backup**  

---

## ✨ Features
✅ **Automatically detects & removes SpecularGlossiness**  
✅ **Preserves all other materials, textures, and settings**  
✅ **No manual file editing needed**  

---

## 📦 Installation

Ensure you have **Python 3.8+** installed.

### **1️⃣ Install Python (If Needed)**
- **Download Python for Windows & macOS** from [python.org](https://www.python.org/downloads/)

### **2️⃣ Install Required Dependencies**
The script will automatically check and install `pygltflib` if missing, but you can install it manually:

```bash
pip install pygltflib
```

---

## 🚀 Usage
<details>
  <summary><strong>Click to Expand</strong></summary>

1. Run the script:
   ```bash
   python clean_sketchup_glb.py
   ```
2. A file picker will appear. Select your **SketchUp-exported** `.glb` file.
3. The script will:
   - Convert **GLB → GLTF**
   - Remove **KHR_materials_pbrSpecularGlossiness**
   - Repack **GLTF → Cleaned GLB**
4. The cleaned GLB file will be saved with `_cleaned` at the end, e.g.:
   ```
   my_model.glb → my_model_cleaned.glb
   ```
</details>

---

## 🛠️ Troubleshooting
<details>
  <summary><strong>Common Issues & Fixes</strong></summary>

### **1️⃣ I get a "Missing BIN file" error**
- Make sure the **GLB contains embedded textures**.
- Some SketchUp GLB exports might not include textures properly.

### **2️⃣ The script won’t run on Mac!**
- If you see a security error on Mac, run:
  ```bash
  xattr -d com.apple.quarantine clean_sketchup_glb.py
  ```
</details>

---

## 📝 Notes & Contributions
- This script is designed **specifically for SketchUp Pro** exports.
- Contributions are welcome! If you improve the script, submit a PR.

---

## 🐜 License
MIT License - Free to use, modify, and distribute.

