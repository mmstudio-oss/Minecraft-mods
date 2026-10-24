"""Fix first-person launcher occlusion and set the directed impact depth to 4 blocks.
Applied after the v1.2 patch in GitHub Actions; leaves third-person art and controls intact.
"""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1] / "JavelinForge1201"
model_path = root / "src/main/resources/assets/javelin/models/item/javelin_launcher.json"
model = json.loads(model_path.read_text(encoding="utf-8"))
display = model["display"]

# Move the held launcher low and to the side. The optic itself is still visible
# outside scope mode, but no longer fills the whole first-person screen.
display["firstperson_righthand"] = {
    "rotation": [3, -95, 37],
    "translation": [6.5, -5.2, -2.0],
    "scale": [0.70, 0.70, 0.70],
}
display["firstperson_lefthand"] = {
    "rotation": [3, 95, -37],
    "translation": [-6.5, -5.2, -2.0],
    "scale": [0.70, 0.70, 0.70],
}
model_path.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Aiming is through a separate CLU HUD. Hide the held item and off-hand ONLY
# during scoped view; don't change third person/inventory/world models.
client_path = root / "src/main/java/com/example/javelin/client/JavelinClient.java"
client = client_path.read_text(encoding="utf-8")
old_import = "import net.minecraftforge.client.event.InputEvent;"
assert old_import in client
client = client.replace(old_import,
    old_import + "\nimport net.minecraftforge.client.event.RenderHandEvent;", 1)
anchor = "        @SubscribeEvent\n        public static void preventVanillaAttack("
assert anchor in client
render_handler = """        // Forge 1.20.1: this cancellable event removes ONLY the first-person
        // hand geometry. Without it, the big tube hides the CLU crosshair.
        @SubscribeEvent
        public static void hideHandsWhileScoped(RenderHandEvent event) {
            if (isAiming()) event.setCanceled(true);
        }

"""
client = client.replace(anchor, render_handler + anchor, 1)
client_path.write_text(client, encoding="utf-8")

# Four blocks of penetration, with approximately a 2x2 block entrance.
# Retain the v1.2 bounded, directional carve, not a spherical TNT crater.
breach_path = root / "src/main/java/com/example/javelin/gameplay/DirectionalBreach.java"
breach = breach_path.read_text(encoding="utf-8")
assert "DEPTH_BLOCKS = 5;" in breach
breach = breach.replace("DEPTH_BLOCKS = 5;", "DEPTH_BLOCKS = 4;")
breach = breach.replace("five blocks into", "four blocks into")
breach_path.write_text(breach, encoding="utf-8")

# New config key defaults to true even if a legacy v1.1 player config had
# 'breakBlocks=false'. The blast still respects unbreakable/container checks.
config_path = root / "src/main/java/com/example/javelin/config/JavelinConfig.java"
config = config_path.read_text(encoding="utf-8")
assert '.define("breakBlocks", true)' in config
config = config.replace('.define("breakBlocks", true)',
                        '.define("directionalBlockDamage", true)')
config = config.replace("2x2 by 5 block", "2x2 by 4 block")
config_path.write_text(config, encoding="utf-8")

for file in [root / "gradle.properties", root / "src/main/resources/META-INF/mods.toml"]:
    t = file.read_text(encoding="utf-8")
    assert "1.2.0" in t, str(file)
    file.write_text(t.replace("1.2.0", "1.3.0"), encoding="utf-8")
print("Applied Javelin v1.3: reduced handheld model, unobstructed aiming and 2x2x4 impact")
