# MAUSMP - Minecraft Java 1.21.11

| Item | Material | Custom Model Data |
|---|---|---:|
| MAU Blitztruhe | `minecraft:chest` | `2000002` |
| MAU Weihnachtskiste | `minecraft:chest` | `2000003` |

Give the Christmas chest with:

```mcfunction
/give @p minecraft:chest[minecraft:custom_model_data={floats:[2000003.0]}]
```

The normal chest fallback remains unchanged. Place `MAUSMP_1.21.11.zip` in `.minecraft/resourcepacks`.
