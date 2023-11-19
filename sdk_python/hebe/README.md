# Wulkanowy SDK Python - Moduł HEBE
## Jak używać?
### Tworzenie i rejestrowanie cerytfikatu
```py
from sdk_python.hebe.certificate import Certificate

async def main():
    certificate = Certificate.create() # Tworzenie certyfikatu
    await certificate.register("token", "symbol", "pin") # Rejestrowanie utworzonego certyfikatu token, symbol i pin uzyskuje się z zakładki Dostęp Mobilny w module Uczeń/Uczeń+ na stronie dziennika 
```
### Pobieranie uczniów
```py
from sdk_python.hebe.certificate import Certificate
from sdk_python.hebe.api import API
from sdk_python.hebe.client import Client

async def main():
    api = API(certificate) # certificate - utworzony i zarejestrowany certyfikat
    client = Client(api) 
    pupils = await client.get_pupils_infos() # Pobieranie listy uczniów
```

### Pobieranie innych danych
```py
from sdk_python.hebe.certificate import Certificate
from sdk_python.hebe.api import API
from sdk_python.hebe.client import Client

async def main():
    api = API(certificate, rest_url) # certificate - utworzony i zarejestrowany certyfikat, rest_url - url api z Pupil.unit.rest_url
    client = Client(api)
    grades = await client.get_grades_by_pupil_and_period(pupil_id, period_id) # Pobieranie ocen ucznia pupil_id - id ucznia, period_id - id semestru
```
