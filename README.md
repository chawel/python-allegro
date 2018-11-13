# python-allegro
Simple wrapper (client) for Allegro.pl REST API written in Python (using requests)

## Wstęp
README napisane w języku polskim, ze względu na oczywisty "userbase".

Prosty klient dla REST API platformy Allegro.pl napisany w Python z użyciem biblioteki requests.
Nie korzysta z magii, każdy endpoint jest zdefiniowany.
Obsługuje autentykację OAuth2, automatycznie odświeża token oraz obługuje metody CRUD dla zasobów.

## Instalacja
Będąc w katalogu w którym jest plik `setup.py`, wystaczy polecenie: 
```bash
    pip install -e .
```

## Użycie
Potrzebujemy danych dostępowych dla procesu uwierzytelnienia naszej aplikacji. Jak je zdobyć opisałem na blogu:
[Allegro.pl REST API w Pythonie - wprowadzenie (OAuth)](https://cwsi.pl/ecommerce/allegro/allegro-pl-rest-api-w-pythonie-wprowadzenie/#wst%C4%99p)

### Autentykacja
Aby korzystać z zasobów REST API Allegro.pl potrzebujemy uzyskać `access_token` służący do uwierzytelnienia naszych żądań.
W tym celu musimy zatańczyć (przejść flow) z OAuth2. Token możemy przekazać podczas instancjonowania klienta

```python
from allegroapi import Allegro

allegro = Allegro(client_id=<CLIENT_ID>, 
                  client_secret=<CLIENT_SECRET>, 
                  redirect_uri=<REDIRECT_URI>,  # np. "http://localhost:80"
                  access_token=<ACCESS_TOKEN>,
                  refresh_token=<REFRESH_TOKEN>,
                  sandbox=True)
```

Jeżeli chcemy by klient przeprowadził nas przez cały OAuth2 flow, należy skorzystać z metody `sign_in()` klasy `Allegro`

```python
from allegroapi import Allegro

allegro = Allegro(client_id=<CLIENT_ID>, 
                  client_secret=<CLIENT_SECRET>, 
                  redirect_uri=<REDIRECT_URI>,  # np. "http://localhost:80"
                  sandbox=True)
              
allegro.sign_in()
```

### Korzystanie z zasobów REST API
Uwierzytelniony klient ma dostęp do zasobów REST API platformy Allegro.pl

#### Przykład użycia: Kategorie
```python
# --- CATEGORIES ---
# Get main categories
print(allegro.sale.categories.all())
# Get child categories with provided parent_id
print(allegro.sale.categories.all(parent_id='122233'))
# Get specific category tree
print(allegro.sale.categories.get('122233'))
# Get specific category
print(allegro.sale.categories.get('122285'))
# Get category parameters
print(allegro.sale.categories.parameters.get('122285'))
```

#### OUTPUT:
```
{'categories': [{'id': 'bfad3525-dd91-491a-a66f-036c77ca3269', 'name': 'Dom i zdrowie', 'parent': None, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '11763', 'name': 'Dziecko', 'parent': None, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '42540aec-367a-4e5e-b411-17c09b08e41f', 'name': 'Elektronika', 'parent': None, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '4bd97d96-f0ff-46cb-a52c-2992bd972bb1', 'name': 'Firma i usługi', 'parent': None, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': 'a408e75a-cede-4587-8526-54e9be600d9f', 'name': 'Kolekcje i sztuka', 'parent': None, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '38d588fd-7e9c-4c42-a4ae-6831775eca45', 'name': 'Kultura i rozrywka', 'parent': None, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': 'ea5b98dd-4b6f-4bd0-8c80-22c2629132d0', 'name': 'Moda i uroda', 'parent': None, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '3', 'name': 'Motoryzacja', 'parent': None, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '889eca47-1df3-40f4-a655-150d6938488e', 'name': 'Sport i wypoczynek', 'parent': None, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}]}
{'categories': [{'id': '122237', 'name': 'Game Boy', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122234', 'name': 'Game Boy Advance', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122240', 'name': 'Microsoft Xbox', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122243', 'name': 'Microsoft Xbox 360', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '147134', 'name': 'Microsoft Xbox One', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122255', 'name': 'Nintendo 3DS', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122256', 'name': 'Nintendo 64', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122257', 'name': 'Nintendo DS', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122261', 'name': 'Nintendo GameCube', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '256862', 'name': 'Nintendo Switch', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '125422', 'name': 'Nintendo Wii U', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122264', 'name': 'Nintendo (SNES i NES)', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122267', 'name': 'Nintendo Wii', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122273', 'name': 'Sega Dreamcast', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122274', 'name': 'Sega (inne)', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122292', 'name': 'Sony PlayStation (PSX)', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122275', 'name': 'Sony PlayStation 2 (PS2)', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122284', 'name': 'Sony PlayStation 3 (PS3)', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '146562', 'name': 'Sony PlayStation 4 (PS4)', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122300', 'name': 'Sony PS Vita', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122301', 'name': 'Sony PSP', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122317', 'name': "'Gierki' elektroniczne", 'parent': {'id': '122233'}, 'leaf': True, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122318', 'name': 'Pegasus', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122319', 'name': 'Automaty do gier', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '253040', 'name': 'Usługi', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}, {'id': '122329', 'name': 'Pozostałe', 'parent': {'id': '122233'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}]}
{'id': '122233', 'name': 'Konsole i automaty', 'parent': {'id': '42540aec-367a-4e5e-b411-17c09b08e41f'}, 'leaf': False, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}
{'id': '122285', 'name': 'Konsole', 'parent': {'id': '122284'}, 'leaf': True, 'options': {'advertisement': False, 'advertisementPriceOptional': False}}
{'parameters': [{'id': '11323', 'name': 'Stan', 'type': 'dictionary', 'required': True, 'unit': None, 'dictionary': [{'id': '11323_1', 'value': 'Nowy'}, {'id': '11323_2', 'value': 'Używany'}], 'restrictions': {'multipleChoices': False}}, {'id': '17448', 'name': 'Waga (z opakowaniem)', 'type': 'float', 'required': False, 'unit': 'kg', 'restrictions': {'min': 0, 'max': 2147483647, 'range': False, 'precision': 2}}, {'id': '3306', 'name': 'Wersja Playstation 3', 'type': 'dictionary', 'required': False, 'unit': None, 'dictionary': [{'id': '3306_10', 'value': 'Classic'}, {'id': '3306_20', 'value': 'Slim'}, {'id': '3306_21', 'value': 'Super Slim'}], 'restrictions': {'multipleChoices': False}}, {'id': '5178', 'name': 'Dodatkowe informacje', 'type': 'dictionary', 'required': False, 'unit': None, 'dictionary': [{'id': '5178_8', 'value': 'Dwa pady w zestawie'}, {'id': '5178_32', 'value': 'Gry w zestawie'}], 'restrictions': {'multipleChoices': True}}, {'id': '5179', 'name': 'Pojemność dysku', 'type': 'dictionary', 'required': False, 'unit': None, 'dictionary': [{'id': '5179_51', 'value': '500 GB'}, {'id': '5179_53', 'value': '320 GB'}, {'id': '5179_10', 'value': '250 GB'}, {'id': '5179_20', 'value': '120 GB'}, {'id': '5179_30', 'value': '80 GB'}, {'id': '5179_40', 'value': '60 GB'}, {'id': '5179_52', 'value': '12 GB'}, {'id': '5179_50', 'value': 'Inna'}], 'restrictions': {'multipleChoices': False}}]}
```
