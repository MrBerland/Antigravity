import json
import base64
import os

LOGOS_DIR = "/Users/timstevens/Antigravity/logos"
REGISTRY_FILE = os.path.join(LOGOS_DIR, "brand_registry.json")

brands_to_add = [
    {"id": "jumeirah", "name": "Jumeirah", "sector": "Hospitality", "file": "jumeirah.png", "type": "image/png"},
    {"id": "radisson", "name": "Radisson Hotels", "sector": "Hospitality", "file": "radisson.png", "type": "image/png"},
    {"id": "protea", "name": "Protea Hotels", "sector": "Hospitality", "file": "protea.svg", "type": "image/svg+xml", "text_only": True},
    {"id": "sandals", "name": "Sandals Resorts", "sector": "Hospitality", "file": "sandals.svg", "type": "image/svg+xml", "text_only": True},
    {"id": "belmond", "name": "Belmond Hotels", "sector": "Hospitality", "file": "belmond.png", "type": "image/png"},
    {"id": "taj", "name": "Taj Hotels", "sector": "Hospitality", "file": "taj.png", "type": "image/png"},
    {"id": "sun_international", "name": "Sun International", "sector": "Hospitality", "file": "sun_international.svg", "type": "image/svg+xml", "text_only": True},
    {"id": "westin", "name": "Westin Hotels", "sector": "Hospitality", "file": "westin.png", "type": "image/png"},
    {"id": "oneandonly", "name": "One&Only Resorts", "sector": "Hospitality", "file": "oneandonly.svg", "type": "image/svg+xml", "text_only": True},
    {"id": "afrihost", "name": "Afrihost", "sector": "Telecommunications", "file": "afrihost.png", "type": "image/png"},
    {"id": "dimension_data", "name": "Dimension Data", "sector": "Telecommunications", "file": "dimension_data.svg", "type": "image/svg+xml", "text_only": True}
]

with open(REGISTRY_FILE, "r") as f:
    reg = json.load(f)

for brand in brands_to_add:
    file_path = os.path.join(LOGOS_DIR, brand["file"])
    with open(file_path, "rb") as f:
        file_content = f.read()
    
    if brand["type"] == "image/svg+xml":
        b64_data = base64.b64encode(file_content).decode('ascii')
    else:
        b64_data = base64.b64encode(file_content).decode('ascii')
        
    data_uri = f"data:{brand['type']};base64,{b64_data}"
    
    new_brand = {
        "id": brand["id"],
        "name": brand["name"],
        "sector": brand["sector"],
        "logo_data_uri": data_uri
    }
    if brand.get("text_only"):
        new_brand["text_fallback"] = True
        
    reg["brands"].append(new_brand)

reg["_meta"]["last_updated"] = "2026-02-21"

with open(REGISTRY_FILE, "w") as f:
    json.dump(reg, f, indent=2)

print(f"Successfully added {len(brands_to_add)} brands to registry.")
