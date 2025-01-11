# iTeam-Steam-Project

## Inleiding

Dit project is een dashboard dat gegevens van de Steam API verzamelt en visualiseert. Het biedt gamers inzicht in hun speelgedrag door statistieken over speeltijd en prestaties te analyseren en visueel weer te geven. Met deze informatie kunnen spelers bewustere keuzes maken en een betere balans vinden tussen gamen en hun dagelijkse leven.


### Doel van het Project

Het project is ontwikkeld voor het tweede blok van het eerste jaar van de opleiding HBO-ICT aan de Hogeschool Utrecht. Door bij te dragen aan een gezondere leefstijl ondersteunt het systeem **Sustainable Development Goal (SDG) 3: Goede gezondheid en welzijn**.


### Functionaliteiten

- Analyse en visualisatie van speeltijd en prestaties via de Steam API.
- Mogelijkheid om speeltijd te vergelijken met het gemiddelde van andere spelers.
- Een gebruiksvriendelijk dashboard dat interactieve grafieken en statistieken toont.


## Installatie

Volg de onderstaande stappen om het project te installeren en uit te voeren:


### 1. Clone de Repository

Clone deze repository naar je lokale machine met het volgende commando:

```
git clone https://github.com/KoenvdBrink/iTeam-Steam-Project.git
```

Ga vervolgens naar de map van het project:

```
cd iTeam-Steam-Project\SD
```

### 2. Installeer Vereisten

Zorg ervoor dat je Python 3.10 of hoger hebt geïnstalleerd. Installeer daarna de benodigde pakketten:

```
pip install pillow
pip install matplotlib
pip install requests
pip install steamspypi
pip install tqdm
pip install psycopg2
pip install pyserial
pip install serial
```

### 3. Start de Applicatie

Run het programma door het volgende commando uit te voeren in de terminal:

```
py dashboard_main.py
```


## Navigatie-instructies

### Interface Overview

Bij het opstarten van het programma zie je een dashboard bestaande uit drie vakken waarin informatie wordt weergegeven:

1. Linkervak (Accountinformatie): Hier vind je gegevens zoals je naam, online/offline status, laatst uitgelogd tijdstip, mediaan speeltijd, gemiddelde speeltijd, en hoe jouw speeltijd zich verhoudt tot de gemiddelde Steam-gebruiker (hoeveel jij meer of minder gamet).

2. Middenvak (Top 20 meest gespeelde games): Dit toont een lijst van je top 20 meest gespeelde games.

3. Rechtervak (Playtime vs Achievements, Grafiek): Een visuele weergave van speeltijd versus behaalde achievements.


### Stappen om het programma te gebruiken

1. Steam ID invoeren: Vul je Steam ID in het invoerveld naast de tekst "Voer Steam ID in:".

2. Klik op 'Ophalen': Door op de knop te klikken, haalt het programma je gegevens op van de Steam API.

3. Bekijk je gegevens: De gegevens worden gevisualiseerd in de drie vakken.

- Accountinformatie: Toont gegevens zoals gemiddelde speeltijd en vergelijkingen met andere spelers.

- Top 20 meest gespeelde games: Een lijst van je meest gespeelde games wordt weergegeven.

- Playtime vs Achievements (Grafiek): De relatie tussen speeltijd en behaalde achievements wordt getoond.

4. Nieuw Steam ID invoeren: Wil je informatie over een ander Steam ID? Voer het nieuwe ID in hetzelfde invoerveld in en klik opnieuw op 'Ophalen'.


### Timerfunctionaliteit

Je gemiddelde speeltijd in de afgelopen twee weken wordt via de Raspberry Pi Pico ingesteld als een timer. Dit helpt je om je speeltijd bij te houden en te beperken, indien nodig. Hiermee kun je bijvoorbeeld proberen onder je gemiddelde te blijven om je speeltijd te verminderen.


#### Navigeren met de Pico

De Raspberry Pi Pico heeft zes knoppen met de volgende functies (van links naar rechts):

1. Start/Pauzeer: Start of pauzeert de timer.

2. Uren: Stelt het aantal uren in.

3. Minuten: Stelt het aantal minuten in.

4. Seconden: Stelt het aantal seconden in.

5. Reset Timer: Reset de huidige timer.

6. Reset Pico: Reset de volledige Pico.


#### Afstandssensor functionaliteit 

Als de gebruiker verder dan 50 cm van de Pico is, pauzeert de timer automatisch. Bovendien:

- Als je gemiddelde speeltijd in de afgelopen twee weken minder dan 60 minuten is, wordt de timer ingesteld op 60 minuten.

- Als je gemiddelde speeltijd meer dan 6 uur is, wordt de timer ingesteld op 6 uur.


### Foutmeldingen

Ongeldig Steam ID of fout bij ophalen van gegevens:

- Zorg ervoor dat je accountinstellingen op public staan.

- Als het probleem aanhoudt, kan het liggen aan tijdelijke problemen met de Steam API.


## Benodigde Afhankelijkheden

### Lijst van vereiste Python-modules

Om het programma te draaien, installeer je de volgende modules:

```
pip install pillow
pip install matplotlib
pip install requests
pip install steamspypi
pip install tqdm
pip install psycopg2
pip install pyserial
```

Zorg ervoor dat je deze modules installeert in een Python-omgeving die geschikt is voor jouw systeem.


### PostgreSQL-database

Voor volledig gebruik moet de PostgreSQL-database draaien met de juiste configuraties. Neem contact op met de ontwikkelaars als deze niet draait.


### Raspberry Pi Pico

- Hoewel het programma zonder de Raspberry Pi Pico draait, is de Pico essentieel voor het project voor de timerfunctionaliteit.

- De seriële poort wordt automatisch ingesteld in de code. Neem contact op met de ontwikkelaars als er problemen zijn met de verbinding.


### Steam-accountinstellingen

- Zorg ervoor dat je Steam-accountinstellingen zijn ingesteld op public om gegevens succesvol van de Steam API op te halen.


### Python-versie

- Het programma vereist Python 3.10 of hoger.


## Contributors

Dit project werd gemaakt door:

- Nizar

- Bryan

- Tess

- Tuana

- Koen

Klas V1B.


