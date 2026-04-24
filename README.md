# projinda
frances och josephines projinda-spel

## Plattformsspel
- 2D (bakgrund och mark) 
- Python (pygame)

### Spellogik
Det finns en bana. Spelaren börjar på en plats i banan och ska ta sig till målet. Det finns hinder som gör det svårare. 
#### Object
Allt på eller över marken
- Block
- X klossar (farliga)
- Hål (mark saknas, farligt)
#### Vinner
Spelaren hittar målet
#### Förlorar
Går in i x kloss eller faller ned. Spelaren börjar om igen på samma ställe

### Randomisering
#### Startposition
Spelaren startar på en random plats i spelet inom ett visst intervall (så att man inte kan råka starta för nära målet eller i ett block). Ifall man förlorar så är det denna plats man startar på igen. 
#### Målposition
Randomize när spelet först startas (inte varje gång). Förlorar man och vill spela igen är målet på samma plats men går man ut ur spelet och in igen är det random. (random höger och vänster, eller oxå inom ett intervall)
### Kamera
Hela spelplannen syns inte utan spelar är i mitten och rör sig med den.