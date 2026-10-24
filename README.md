# Minecraft Mods — FGM-148 Javelin (Minecraft 1.20.1 / Forge)

Minecraft-styled guided launcher with right-click scope, hold-left-click to fire, entity or terrain targeting, rocket flight and staged explosion effects.

**Build status:** the real Forge JAR is compiled by GitHub Actions. Open the **Actions** tab, select `Build Javelin mod JAR` and download the build artifact after a successful run.

The source bundle is stored at `javelin-source.tar.gz`. The workflow extracts it, regenerates original textures and builds with ForgeGradle.

Controls: hold **RMB** to aim, hold **LMB** for 0.6 s to launch. Creative mode has infinite ammunition.

Commands:
```
/give @s javelin:javelin_launcher 1
/give @s javelin:javelin_round 16
```

Requires Minecraft 1.20.1, Forge 47.4.x and Java 17. Explosions don't destroy blocks by default (`config/javelin-common.toml`).
