# Elections Scraper
Jedná se o třetí projekt v rámci Python Akademie od ENGETO.
## O projektu

Projekt je zaměřen na extrakci (scraping) výsledků parlamentních voleb v roce 2017, konkrétně výsledků hlasování v jednotlivých obcích zvoleného územního celku (okresu).
Data jsou získávána pomocí web scrapingu z oficiálních stránek Českého statistického úřadu (ČSÚ), konkrétně z portálu [volby.cz](https://www.volby.cz/), jenž poskytuje přehledy volebních výsledků až na úroveň jednotlivých obcí.

## Postup správného spuštění projektu

### Požadovaná verze Pythonu
Doporučená verze Pythonu: 3.10 nebo vyšší

Minimální podporovaná verze: 3.9

Ve starších verzích Pythonu nejsou podporovány některé typové typové anotace (např. `list[str]`).

### Instalace požadovaných knihoven
Soubor požadavků (použité knihovny) je uveden v souboru `requirements.txt`.
Doporučuje se vytvořit nové virtuální prostředí a následně spustit:
```
pip3 --version                      # Ověřuje verzi správce balíčků
pip3 install -r requirements.txt    # Nainstaluje potřebné knihovny
```
## Spuštění projektu
Projekt se spouští z příkazové řádky. Ke správnému spuštění je třeba zadat dva argumenty:
1. Odkaz na územní celek (upřesnění viz dále),
2. Název CSV souboru, kam mají být výsledky uloženy.
#### 1. Odkaz na územní celek
Jedná se o odkaz na webovou stránku s výsledky voleb v určitém územním celku (okresu). Seznam okresů je dostupný [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). Na této stránce vyberte okres kliknutím na symbol `X` ve sloupci **Výběr obce** a následně zkopírujte URL adresu.

Zadává se včetně uvozovek: `"<odkaz_na_uzemni_celek>"`

#### 2. Název CSV souboru
Jedná se o jméno výstupního CSV souboru. Je třeba, aby byly splněny požadavky pro platný název, tj. aby název neobsahoval nepovolené znaky (`?`, `/`, `:` apod.)

Zadává se bez přípony: `<nazev_csv_souboru>`

Ukázka spuštění:
```
python main.py "<odkaz_na_uzemni_celek>" <nazev_csv_souboru>
```

## Výstup projektu
Výsledky voleb v jednotlivých obcích daného okresu se stáhnou jako soubor s příponou `.csv`. 

Soubor obsahuje pro každou obec následující údaje:
- Kód obce
- Název obce
- Voliči v seznamu
- Vydané obálky
- Platné hlasy
- Počty platných hlasů pro jednotlivé politické strany

## Ukázka projektu
Výsledky voleb pro územní celek Znojmo:

1. Spuštění programu:
```
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6207" vysledky_znojmo
```
2. Průběh:
```
STAHUJI DATA Z VYBRANEHO URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6207
```
3. Dokončení procesu:
```
ULOZENO DO SOUBORU: vysledky_znojmo.csv
```
Ukázka výstupního CSV souboru:
```
Kód obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,...
593729,Bantice,228,153,151,8,0,0,13,0,4,12,4,4,4,0,0,9,0,1,34,0,0,32,0,0,0,1,23,1,1
593737,Běhařovice,318,209,208,5,0,0,20,1,3,16,1,2,0,0,1,12,0,0,101,0,0,28,0,0,0,1,17,0,0
593745,Bezkov,157,110,110,0,0,0,9,0,4,12,2,1,3,0,0,6,0,6,25,0,0,26,0,0,0,0,14,2,0
...
```