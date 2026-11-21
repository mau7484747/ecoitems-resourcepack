# MAUSMP - Minecraft Java 1.21.11

| Item | Material | Custom Model Data |
|---|---|---:|
| MAU Blitztruhe | `minecraft:chest` | `2000002` |
| MAU Weihnachtskiste | `minecraft:chest` | `2000003` |
| MAU Winter-Spitzhacke | `minecraft:netherite_pickaxe` | `2000004` |
| MAU Eiskristall-Stab | `minecraft:netherite_sword` | `2000005` |

Give the Christmas chest with:

```mcfunction
/give @p minecraft:chest[minecraft:custom_model_data={floats:[2000003.0]}]
```

Give the winter pickaxe with:

```mcfunction
/give @p minecraft:netherite_pickaxe[minecraft:custom_model_data={floats:[2000004.0]}]
```

Give the animated ice staff with:

```mcfunction
/give @p minecraft:netherite_sword[minecraft:custom_model_data={floats:[2000005.0]}] 1
```

The ice staff uses a custom 3D model and an eight-frame animated ice texture. Its server-side right-click behaviour is intentionally separate and can be implemented in Skript by checking the netherite sword's Custom Model Data value `2000005`.

The normal item models remain as fallbacks. Place the resource pack in `.minecraft/resourcepacks` and reload it in Minecraft with `F3` + `T`.
