# Wardrobe
 
## Instrukcja uruchomienia lokalnego

Poniższa instrukcja dotyczy uruchomienia serwera w najprostszej postaci. Oznacza to, że ***pliki statyczne nie są obsługiwane przez AWS S3, tylko zapisywane lokalnie***. W przypadku uruchomienia aplikacji na produkcji, należy zadeklarować zmienne środowiskowe systemu:
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_STORAGE_BUCKET_NAME
* AWS_QUERYSTRING_AUTH  
i odkomentować deklaracje zmiennych w pliku `wardrobe/wardrobe/settings.py` od linii 144 do 156.

### Wstępne wymagania:
* Python (rekomendowana wersja: >3.10)
* Pip
* Python Venv
* System: Linux (podane zostały komendy dla systemu Linux, w przypadku innych systemów należy dostosować komendy do odpowiedniego systemu)

### 1. Pobierz repozytorium
```gh repo clone kacpermisiek/Wardrobe```

### 2. Wejdź do pobranego folderu i wybierz poprawny branch
```cd /path/to/Wardrobe```  
```git switch local```

### 3. Stwórz środowisko wirtualne
```python3 -m venv venv```  

### 4. Aktywuj środowisko wirtualne
```source venv/bin/activate```

### 5. Zainstaluj Postgresql
```sudo apt install postgresql ```

### 6. Zainstaluj wymagane moduły
```sudo apt install libpq-dev python3-dev gcc```  
```pip install -r requirements.txt```

### 7. Wykonaj migrację bazy danych
```python wardrobe/manage.py makemigrations```  
```python wardrobe/manage.py migrate```

### 8. Stwórz potrzebne zmienne środowiskowe
```export SECRET_KEY=SuperSecretKey```  
```export EMAIL_HOST_PASSWORD=PASSWORD```  
`SECRET_KEY` może być dowolny, natomiast `EMAIL_HOST_PASSWORD` jest poufny. Jeżeli nie masz dostępu do hasła, możesz stworzyć swoje własne hasło do aplikacji [LINK](https://support.google.com/accounts/answer/185833?hl=pl)

### 9. Stwórz superusera
```python wardrobe/manage.py createsuperuser```  
Podaj nazwę użytkownika oraz hasło

### 10. Ustawianie adresatów wiadomości e-mail  
W pliku `Wardrobe/wardrobe/stuff/views.py` zmień zawartość listy SUPER_USER_EMAILS (linijka 28). Usuń obecny email i dodaj do listy adresy e-mail. 

```SUPER_USER_EMAILS = ["YOUR@MAIL.COM"] ```  

Na podane adresy wysyłane będą wiadomości z prośbą o udostępnienie zestawów.


### 11. Uruchom serwer
```python3 warrdrobe/manage.py runserver```

Możesz teraz wejść na adres 127.0.0.1:8000.  
Jeżeli wyskoczył komunikat `A server error occurred. Please contact the administrator` należy wyłączyć serwer i ponownie wykonać krok 7.


## Ważne informacje
### 1. Po stworzeniu szablonu, widoczny jest on tylko dla użytkownika, który go stworzył oraz dla superuserów. W tym momencie można zmieniać potrzebne przedmioty dla zestawu. Gdy szablon jest już gotowy, należy zaznaczyć pole "Gotowy do udostępnienia" w edycji zestawu.

### 2. Superuserzy mają dostęp do panelu administracyjnego aplikacji. Można go znaleźć pod adresem `/admin`, na przykład `127.0.0.1:8000/admin`

### 3. Aplikacja domyślnie jest uruchomiona w trybie debugowania. Oznacza to, że w przypadku rzucenia jakiegokolwiek błędu, wyświetlony zostanie trace błędu. Aby wyłączyć wyświetlanie trace'u, należy zmienić w pliku `wardrobe/settings.py` wartość zmiennej DEBUG na False

### 4. W celu przechowywania plików w usłudze Amazon S3, należy skonfigurować swój własny bucket na stronie [AWS](https://aws.amazon.com/pm/serv-s3/?trk=518a7bef-5b4f-4462-ad55-80e5c177f12b&sc_channel=ps&ef_id=Cj0KCQjwz6ShBhCMARIsAH9A0qXEBriQ2zlsmv5QCdetZ9IL1GmrjWmXst6Ph0NWIwbTt-qKPQNbNngaAjSPEALw_wcB:G:s&s_kwcid=AL!4422!3!645186213484!e!!g!!amazon%20s3!19579892800!143689755565). Ze względów bezpieczeństwa, twórca aplikacji nie udostępnia danych swojego bucketa.

### 5. `EMAIL_HOST_PASSWORD` jest poufny. Jeżeli nie masz dostępu do hasła, możesz stworzyć swoje własne hasło do aplikacji [LINK](https://support.google.com/accounts/answer/185833?hl=pl)
