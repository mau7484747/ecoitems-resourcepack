# MAUSMP - Minecraft Java 1.21.11

| Item | Material | Custom Model Data |
|---|---|---:|
| MAU Blitztruhe | `minecraft:chest` | `2000002` |
| MAU Weihnachtskiste | `minecraft:chest` | `2000003` |
| MAU Winter-Spitzhacke | `minecraft:netherite_pickaxe` | `2000004` |
| MAU Eiskristall-Stab (Spezialpapier) | `minecraft:paper` | `1001` |
| MAU Eiskristall-Stab (Schwert-Variante) | `minecraft:netherite_sword` | `2000005` |

Give the Spezialpapier ice staff with:

```mcfunction
/give @p minecraft:paper[minecraft:custom_model_data={floats:[1001.0]}] 1
```

Give the sword-mapped version with:

```mcfunction
/give @p minecraft:netherite_sword[minecraft:custom_model_data={floats:[2000005.0]}] 1
```

Both variants use the same custom Eistab model. The art is based on the new icy fantasy staff concept, with a curved crystal crown, wrapped grip, and a separate eight-frame animated frost spiral.

The server-side right-click behaviour is separate and can be implemented in Skript by checking the relevant item's Custom Model Data value. The normal item models remain as fallbacks.

Place the resource pack in `.minecraft/resourcepacks` and reload it in Minecraft with `F3` + `T`.
