import os
import json
import sys
import subprocess

# 🔹 Ensure `pygltflib` is installed
try:
    from pygltflib.utils import glb2gltf, gltf2glb
except ImportError:
    print("⚠️ 'pygltflib' not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygltflib"])
    print("✅ Installation complete. Restarting script...\n")
    os.execv(sys.executable, [sys.executable] + sys.argv)  # Restart script

from AppKit import NSOpenPanel

def open_file_dialog():
    """Opens a file picker to select a GLB file for conversion and cleaning."""
    
    panel = NSOpenPanel.openPanel()
    panel.setCanChooseFiles_(True)
    panel.setCanChooseDirectories_(False)
    panel.setAllowsMultipleSelection_(False)
    panel.setAllowedFileTypes_(["glb"])

    if panel.runModal():
        file_path = panel.URLs()[0].path()
        print(f"📂 Selected file: {file_path}")
        
        gltf_path = convert_glb_to_gltf(file_path)
        cleaned_gltf_path = remove_gltf_extensions(gltf_path)

        # ✅ Delete original GLTF file and rename _cleaned.gltf to original name
        if os.path.exists(gltf_path):
            os.remove(gltf_path)
            print(f"🗑️ Deleted original GLTF: {gltf_path}")

        final_gltf_path = cleaned_gltf_path.replace("_cleaned.gltf", ".gltf")
        os.rename(cleaned_gltf_path, final_gltf_path)
        print(f"📛 Renamed cleaned GLTF: {cleaned_gltf_path} → {final_gltf_path}")

        # ✅ Convert back to GLB with _cleaned suffix
        cleaned_glb_path = convert_gltf_to_glb(final_gltf_path)

        if cleaned_glb_path:
            # ✅ Delete the temporary GLTF and BIN files
            bin_path = final_gltf_path.replace(".gltf", ".bin")
            os.remove(final_gltf_path)
            print(f"🗑️ Deleted temporary GLTF: {final_gltf_path}")
            if os.path.exists(bin_path):
                os.remove(bin_path)
                print(f"🗑️ Deleted temporary BIN: {bin_path}")

            print(f"🎉 Final cleaned GLB: {cleaned_glb_path}")
        
        print(f"✅ Process complete! Original GLB preserved.")

def convert_glb_to_gltf(input_path):
    """Converts GLB to GLTF and overwrites if file exists."""
    gltf_path = input_path.replace(".glb", ".gltf")  # New GLTF filename

    # ✅ Delete existing GLTF file if it already exists
    if os.path.exists(gltf_path):
        os.remove(gltf_path)
        print(f"⚠️ Overwriting existing file: {gltf_path}")

    # Convert GLB → GLTF
    glb2gltf(input_path, gltf_path)

    print(f"✅ Converted: {input_path} → {gltf_path}")
    return gltf_path

def remove_gltf_extensions(gltf_path):
    """Removes ONLY 'KHR_materials_pbrSpecularGlossiness' safely."""
    
    with open(gltf_path, "r", encoding="utf-8") as f:
        gltf_data = json.load(f)  # ✅ Load as JSON dictionary

    # ✅ Remove "KHR_materials_pbrSpecularGlossiness" from extensionsUsed
    if "extensionsUsed" in gltf_data:
        gltf_data["extensionsUsed"] = [
            ext for ext in gltf_data["extensionsUsed"]
            if ext != "KHR_materials_pbrSpecularGlossiness"
        ]
        if not gltf_data["extensionsUsed"]:  # If empty, remove key
            del gltf_data["extensionsUsed"]

    # ✅ Remove "KHR_materials_pbrSpecularGlossiness" from materials
    if "materials" in gltf_data:
        for material in gltf_data["materials"]:
            if "extensions" in material and "KHR_materials_pbrSpecularGlossiness" in material["extensions"]:
                del material["extensions"]["KHR_materials_pbrSpecularGlossiness"]
                if not material["extensions"]:  # Remove empty dict
                    del material["extensions"]

    # ✅ Save cleaned GLTF as a separate _cleaned file
    cleaned_gltf_path = gltf_path.replace(".gltf", "_cleaned.gltf")
    with open(cleaned_gltf_path, "w", encoding="utf-8") as f:
        json.dump(gltf_data, f, indent=2)  # ✅ Ensures valid JSON format

    print(f"✅ Cleaned GLTF saved as: {cleaned_gltf_path}")
    return cleaned_gltf_path

def convert_gltf_to_glb(gltf_path):
    """Converts cleaned GLTF + BIN back to GLB with _cleaned suffix."""
    glb_output_path = gltf_path.replace(".gltf", "_cleaned.glb")

    # ✅ Ensure .bin file exists
    bin_path = gltf_path.replace(".gltf", ".bin")
    if not os.path.exists(bin_path):
        print(f"❌ Error: Missing BIN file: {bin_path}")
        return None

    # ✅ Delete existing cleaned GLB file if it already exists
    if os.path.exists(glb_output_path):
        os.remove(glb_output_path)
        print(f"⚠️ Overwriting existing cleaned GLB file: {glb_output_path}")

    # ✅ Convert GLTF → GLB
    gltf2glb(gltf_path, glb_output_path)
    
    print(f"✅ Converted to cleaned GLB: {glb_output_path}")
    return glb_output_path

# Run the script
open_file_dialog()
