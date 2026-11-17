# Black Cat Control (Android APK + Termux Bridge)

Kompletny system do sterowania botami (`autobot_v13.py` oraz `blackcat_hunter_v12.py`) z poziomu natywnej aplikacji na Androida.

## Jak wygenerować plik `.apk` automatycznie na GitHubie?
1. Utwórz nowe repozytorium na swoim koncie GitHub.
2. Wrzuć wszystkie pliki z tego folderu (wraz z ukrytym folderem `.github/workflows/build_apk.yml`) do repozytorium.
3. Wejdź na GitHubie w zakładkę **Actions** -> wybierz workflow **Build Android APK**.
4. Po zakończeniu kompilacji (ok. 5–8 minut) pobierz gotowy plik instalacyjny z sekcji **Artifacts** (`BlackCatControl-APK`) i zainstaluj na telefonie.

## Jak podłączyć aplikację pod Termuxa?
1. Skopiuj plik `blackcat_bridge.py` do swojego katalogu domowego w Termuxie (`~/`).
2. Uruchom mostek w tle:
   ```bash
   nohup python blackcat_bridge.py > bridge.log 2>&1 &
   ```
3. Otwórz zainstalowaną aplikację **Black Cat Control** na telefonie i przełączaj funkcje jednym kliknięciem!
