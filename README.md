# projinda

Ett 2D-plattformsspel byggt i Python med pygame.

## Features
- Kamera som följer spelaren
- Slumpmässigt genererade plattformar
- Hål och farliga block
- Sprite-animationer
- Kollisionssystem
- Win/lose states

## Spellogik

Spelaren spawnar på en slumpmässig säker plats inom ett fördefinierat område av världen och ska ta sig till målet utan att dö.

### Vinna
Spelaren vinner när den nuddar målet.

### Förlora
Spelaren förlorar om den träffar ett farligt block eller faller ner i ett hål. Efter förlust kan spelaren trycka R för att försöka igen på samma bana, eller Q för att avsluta spelet.

## Objekt i världen
- Plattformar/block
- Farliga block
- Hål där mark saknas

## Bana
Banan genereras slumpmässigt när spelet startar. Plattformar placeras ut med varierande höjd och hål kan uppstå mellan dem. Farliga block spawnar på vissa plattformar.

## Startposition
Spawn-systemet säkerställer att spelaren inte spawnar inne i block, inte spawnar på fiender och alltid har mark under sig

## Kamera
Kameran följer spelarens position och håller spelaren centrerad på skärmen istället för att visa hela världen samtidigt.

## Kontroller

| Tangent | Funktion |
|---|---|
| A | Gå vänster |
| D | Gå höger |
| SPACE | Hoppa |
| R | Starta om |
| Q | Lämna spelet |

## Hur man spelar

Installera pygame:

```bash
pip install pygame