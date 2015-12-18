# puzzleOfDoom

## Etude du problème:
- Un puzzle est composé de 256 pièces.
- Chaque pièce est composée de 4 faces
- Chaque pièce peut être disposée sur le plateau suivant un axe x ou y
- Chaque pièce peut être tournée

- Différentes méthodes de résolution du puzzle ont déjà été exploités :
	- Equerre => Triangle => Carré
	- Bordure => intérieur

- Différents algorithmes :
	- tabu search
	- backtrack
## Etude des possibilités
- Différentes îles:
	- Une par mutation:
		- rotation mutation => un gène tourné
		- swap mutation => échange deux gènes
		- swap & rotate => échange deux gènes et les tournes
		- rotate region mutation => prend une région >= 4 gènes et la tourne
		- swap region mutation => échange deux régions
		- region inversion mutation => inverse la position des gènes dans une région
		- row and column inversion mutation => swap deux gènes cote à cote
		- scramble mutation => garde un coin du plateau et mélange le reste
	- Une par croisement:
		- region exchange crossover => clone les deux parents et échange deux régions
		- uniform crossover => même chose que region exchange, sauf qu'on crée un template de régions 1 et 2 et on attribut les gènes correspondants au parent 1 ou 2 en fonction du template
	- Une par choix de départ (0, 1 ou 5 indices)

## Notation du projet
- La cotation du projet se fait sur le nombre de bords de pièces qui matchent.
- Le score maximal à atteindre pour la soutenance est 480
- Le score maximal trouvé est de 467