"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Milan Angelis
email: milanangelis@seznam.cz
"""


import click
import pathvalidate
import requests
import csv
from bs4 import BeautifulSoup as bs


def over_adresu(url_adresa: str) -> str:
    """
    Funkce, která ověří, zdali je vybraná URL adresa validní.

    :param url_adresa: adresa, jež je porovnána s adresami,
        které může kód využít
    :type url_adresa: str
    :return: URL adresa v případě úspěšné validace
    :rtype: str
    :raises click.BadParameter: upozornění v případě neúspěšné validace

    :Example:
    >>> overeni = over_adresu(
    ...     "https://www.volby.cz/pls/ps2017nss/ps32?\
    ...     xjazyk=CZ&xkraj=11&xnumnuts=6207"
    ... )
    >>> overeni
    "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6207"
    """

    odkaz_kraje = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    html_kraje = requests.get(odkaz_kraje)
    html_kraje_rozdelene = bs(html_kraje.text, features="html.parser")
    tagy_a = html_kraje_rozdelene.find_all("a")

    zacatek_adresy = "https://www.volby.cz/pls/ps2017nss/"
    existujici_adresy = list()

    for tag in tagy_a:
        if "ps32" in str(tag) and not "ps36" in str(tag):
            konec_adresy = str(tag).split("\"")[1]
            kompletni_adresa = zacatek_adresy + konec_adresy
            kompletni_adresa = kompletni_adresa.replace("amp;", "")
            existujici_adresy.append(kompletni_adresa)

    if url_adresa in existujici_adresy:
        return url_adresa
    
    elif url_adresa == "https://www.volby.cz/pls/ps2017nss/ps36?xjazyk=CZ":
        raise click.BadParameter(
            "Zahraničí není podporováno, vyberte, prosím, platný okres."
        )
    else:
        raise click.BadParameter(
            "Tato URL adresa má nesprávný formát.", param_hint="adresa_url"
        )


def over_nazev_souboru(nazev_souboru: str) -> str:
    """
    Funkce, která ověřuje, zda je možné použít zadaný 
    string jako platný název souboru.
    
    :param nazev_souboru: název souboru určený k validaci
    :type nazev_souboru: str
    :return: název souboru v případě úspěšné validace
    :rtype: str
    :raises click.BadParameter: upozornění v případě neúspěšné validace

    :Example:
    >>> validace = over_nazev_souboru("me_treti_csv")
    >>> validace
    "me_treti_csv"
    """

    try:
        pathvalidate.validate_filename(nazev_souboru)
        return nazev_souboru
    except pathvalidate.ValidationError:
        raise click.BadParameter(
            "Neplatny nazev souboru.", 
            param_hint="nazev_csv"
        )


def ziskej_kod_kraje(adresa_okres: str) -> str:
    """
    Funkce, která se zadané URL adresy okresu (str) získá číslo kraje (str).

    :Example:
    >>> kod = ziskej_kod_kraje(
    ...     "https://www.volby.cz/pls/ps2017nss/ps32\
    ...     ?xjazyk=CZ&xkraj=11&xnumnuts=6207"
    ... )
    >>> kod
    "11"
    """

    cislo = adresa_okres.split("=")[2].split("&")[0]
    return cislo


def ziskej_kody_obci(adresa_okres: str) -> list[str]:
    """
    Funkce, která z dané URL adresy získá kódy obcí daného okresu.

    :param adresa_okres: URL adresa okresu, ze které budou extrahována čísla
        jednotlivých obcí
    :type adresa: str
    :return: list obsahující kódy všech obcí v daném okrese
    :rtype: list[str]

    :Example:
    >>> kody = ziskej_kody_obci(
    ...     "https://www.volby.cz/pls/ps2017nss/ps32\
    ...     ?xjazyk=CZ&xkraj=11&xnumnuts=6207"
    ... )
    >>> kody
    ["593729", "593737", "593745", ...]
    """

    html_doc = requests.get(adresa_okres)
    html_rozdelene = bs(html_doc.text, features="html.parser")
    vsechna_a = html_rozdelene.find_all("a")
    kody_obci = [
        polozka.text for polozka in vsechna_a if polozka.text.isdigit()
        ]
    
    return kody_obci


def vytvor_adresy_obci(
        cislo_kraje: str, 
        cislo_okresu: str, 
        cisla_obci: list
        ) -> list[str]:
    """
    Funkce, která z kódu kraje, okresu a kódů příslušných obcí
    vytvoří URL adresy obcí daného okresu.

    :param cislo_kraje: kód odpovídající kraji ("1" až "14"), 
        jehož územní součástí je daný okres
    :type cislo_kraje: str
    :param cislo_okresu: kód okresu
    :type cislo_okresu: str
    :param cisla_obci: kódy obcí v rámci daného okresu
    :type cisla_obci: list
    :return: naformátované URL adresy jednotlivých obcí
    :rtype: list[str]

    :Example:
    >>> adresy = vytvor_adresy_obci("11", "6207", ["593711", "595179"])
    >>> adresy
    [
        "https://www.volby.cz/pls/ps2017nss/ps311\
        ?xjazyk=CZ&xkraj=11&xobec=593711&xvyber=6207",
        "https://www.volby.cz/pls/ps2017nss/ps311\
        ?xjazyk=CZ&xkraj=11&xobec=595179&xvyber=6207"
    ]
    """

    adresy = list()

    for cislo in cisla_obci:
        adresa = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=\
        {cislo_kraje}&xobec={cislo}&xvyber={cislo_okresu}"
        adresy.append(adresa)

    return adresy


def vytvor_slovnik_o_obci(obec_adresa: str, obec_kod: str) -> dict:
    """
    Funkce vytvářející ze zadané URL adresy obce a kódu obce
    slovník se základními údaji o obci a počtech hlasů
    pro jednotlivé politické strany.

    :param obec_adresa: URL adresa dané obce s volebními výsledky
    :type obec_adresa: str
    :param obec_kod: kód specifický pro danou obec
    :type obec_kod: str
    :return: slovník s údaji z voleb pro danou obec
    :rtype: dict

    :Example:
    >>> udaje_obec = vytvor_slovnik_o_obci(
    ...     "https://www.volby.cz/pls/ps2017nss/ps311\
    ...     ?xjazyk=CZ&xkraj=11&xobec=593711&xvyber=6207",
    ...     "593711"
    ... )
    >>> udaje_obec
    {
        'Kód obce': '593711', 
        'Název obce': 'Znojmo', 
        'Voliči v seznamu': '27 255',
        'Vydané obálky': '16 292', 
        'Platné hlasy': '16 179', 
        'Občanská demokratická strana': '1 644',
        'Řád národa - Vlastenecká unie': '21', 
        'CESTA ODPOVĚDNÉ SPOLEČNOSTI': '7', 
        'Česká str.sociálně demokrat.': '1 725', 
        'Radostné Česko': '8',
        'STAROSTOVÉ A NEZÁVISLÍ': '506', 
        'Komunistická str.Čech a Moravy': '1 431',
        'Strana zelených': '175', 
        'ROZUMNÍ-stop migraci,diktát.EU': '115',
        'Strana svobodných občanů': '257', 
        'Blok proti islam.-Obran.domova': '18',
        'Občanská demokratická aliance': '38',
        'Česká pirátská strana': '1 255',
        'Referendum o Evropské unii': '6', 
        'TOP 09': '507', 'ANO 2011': '5 023',
        'Dobrá volba 2016': '16', 
        'SPR-Republ.str.Čsl. M.Sládka': '23', 
        'Křesť.demokr.unie-Čs.str.lid.': '896', 
        'Česká strana národně sociální': '3',
        'REALISTÉ': '68', 'SPORTOVCI': '11', 
        'Dělnic.str.sociální spravedl.': '16',
        'Svob.a př.dem.-T.Okamura (SPD)': '2 316' , 
        'Strana Práv Občanů': '88', 
        'Národ Sobě': '6'
    }
    """

    html_obec = requests.get(obec_adresa)
    rozdelene_html_ob = bs(html_obec.text, features="html.parser")

    # Získání názvu obce
    hlavicka_obce = rozdelene_html_ob.find_all("h3")
    # Praha -> název je v 2. <h3> tagu
    if "vyber=1100" in obec_adresa:
        nazev_obce = hlavicka_obce[1].text.strip()
    
    else: 
    # Ostatní oblasti -> název je ve 3. <h3> tagu:
        nazev_obce = hlavicka_obce[2].text.strip()
    nazev_obce = nazev_obce.replace("Obec: ", "") # Získej pouze název obce

    # Získání údajů o obci (počet voličů, vydané obálky a platné hlasy)
    tabulka_1 = rozdelene_html_ob.find("table",{"id": "ps311_t1"})
    vsechna_tr = tabulka_1.find_all("tr")
    radek_3 = vsechna_tr[2].text.splitlines()
    radek_3 = [udaj.replace("\xa0", " ") for udaj in radek_3]
    volici, obalky, hlasy = radek_3[4], radek_3[5], radek_3[8]

    # Získání listu názvů stran a přísluných počtů hlasů:
    nazvy_stran = rozdelene_html_ob.find_all("td", {"class": "overflow_name"})
    list_nazvu_stran = [strana.text for strana in nazvy_stran]

    list_poctu_hlasu = list()
    for strana in nazvy_stran:
        pocet_hlasu = strana.find_next_sibling("td")
        pocet_hlasu = pocet_hlasu.text.strip().replace("\xa0", " ")
        list_poctu_hlasu.append(pocet_hlasu)

    # Vytvoř slovník pro danou obec:
    udaje_o_obci = {
                "Kód obce": obec_kod,
                "Název obce": nazev_obce,
                "Voliči v seznamu": volici,
                "Vydané obálky": obalky,
                "Platné hlasy": hlasy,
            }
        
    # Rozšiř slovník o jednotlivé strany a příslušné počty hlasů:
    strany_hlasy = dict(zip(list_nazvu_stran, list_poctu_hlasu))
    udaje_o_obci.update(strany_hlasy)
    return udaje_o_obci


def zapis_do_csv(nazev: str, list_slovniku: list[dict]) -> str:
    """
    Funkce, která zapíše list slovníků do CSV souboru.

    :param nazev: název vytvořeného CSV souboru (včetně přípony .csv)
    :type nazev: str
    :param list_slovniku: list obsahující slovníky s údaji, 
        které mají být zapsány
    :type list_slovniku: list[dict]
    :return: název nového souboru s příponou .csv
    :rtype: str

    :Example:
    >>> soubor_csv = zapis_do_csv("csv_s_vysledky.csv", 
    ... [{'Kód': 1456, 'Obec': 'Město X'}, 
    ... {'Kód': 1789, 'Obec': 'Město Y'}])
    >>> soubor_csv
    "csv_s_vysledky.csv"
    """

    with open(nazev, mode="w", encoding="utf-8", newline="") as f:
        zahlavi = list_slovniku[0].keys()
        zapisovac = csv.DictWriter(f, fieldnames=zahlavi)
        zapisovac.writeheader()
        zapisovac.writerows(list_slovniku)
        return nazev


# Pomocí knihovny click je program spuštěn z příkazové řádky,
# 1. argument je url adresa okresu, 2. argument je název vytvořeného
# CSV souboru s výsledky voleb v jednotlivých obcích daného okresu.

@click.command()
@click.argument("adresa_url", type=over_adresu)
@click.argument("nazev_csv", type=over_nazev_souboru)


def main(adresa_url: str, nazev_csv: str):

    # Pomocí uživ. funkcí vytvoř list URL adres jednotlivých obcí okresu:
    kod_kraje = ziskej_kod_kraje(adresa_url)
    kod_okresu = adresa_url[-4:]
    kody_obci = ziskej_kody_obci(adresa_url)
    soubor_adres = vytvor_adresy_obci(kod_kraje, kod_okresu, kody_obci)
    click.echo(f"STAHUJI DATA Z VYBRANEHO URL: {adresa_url}")

    # Vytvoř list, kam budou vkládány všechny slovníky s daty o každé obcích:
    soubor_obci = list()

    # Pro každou obec z daného okresu vytvoř slovník s údaji:
    for index_obce in range(len(soubor_adres)):
        slovnik_s_obci = vytvor_slovnik_o_obci(
            soubor_adres[index_obce], kody_obci[index_obce]
            )
        # Přidej slovník s daty o obci do výsledného listu:
        soubor_obci.append(slovnik_s_obci)
    
    # Zapiš výsledný list s jednotlivými slovníky do CSV souboru:
    vysledny_csv_soubor = (zapis_do_csv(nazev_csv + ".csv", soubor_obci))
    click.echo(f"ULOZENO DO SOUBORU: {vysledny_csv_soubor}")
    

if __name__ == "__main__":
    main()
