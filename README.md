# Flask Autentiserings Eksempel

Hvordan kjøre:

```python
pip install -r requirements.txt
python run.py
```

## Hosting

Du kan hoste nettsiden med docker:

```bash
docker compose up -d
```

Besøk http://localhost:5000

Denne applikasjonen er laget i Flask og bruker SQLite som database.

Funksjonalitet:
- Brukeren kan registrere seg
- Brukeren kan logge inn og logge ut
- Passord blir hash'et før lagring i databasen
- "Min profil" er en beskyttet side som krever innlogging
- Innloggede brukere kan skrive egne notater
- Notatene lagres i databasen og vises igjen etter ny innlogging

Teknologier:
- Flask
- Sessions
- SQLite
- Egendefinert autentisering
- Jinja templates