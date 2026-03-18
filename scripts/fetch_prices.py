import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone

LEAGUES = ["Mercenaries", "Standard", "Hardcore Mercenaries"]
TYPES = ["UniqueWeapon", "UniqueArmour", "UniqueAccessory", "UniqueFlask", "UniqueJewel"]

def fetch(league, type_):
    url = "https://poe.ninja/api/data/itemoverview?league=" + urllib.parse.quote(league) + "&type=" + type_
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read()).get("lines", [])

def trim(item):
    return {
        "name": item.get("name", ""),
        "chaosValue": item.get("chaosValue", 0),
        "baseType": item.get("baseType", ""),
        "icon": item.get("icon", ""),
    }

data = {}
for league in LEAGUES:
    lines = []
    for type_ in TYPES:
        print(f"Fetching {league} / {type_}...")
        lines.extend(trim(i) for i in fetch(league, type_))
    data[league] = lines
    print(f"  {len(lines)} items")

output = {
    "updatedAt": datetime.now(timezone.utc).isoformat(),
    "leagues": data,
}

with open("data.json", "w") as f:
    json.dump(output, f, separators=(",", ":"))

print("Done.")
