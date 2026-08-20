# R2 — CANDU capacity factor: weryfikacja `capacity_factor_CANDU_EC6_pct`

Zadanie badawcze (read-only). Weryfikacja obecnego wpisu w
`config/assumptions_registry.json`:

```
capacity_factor_CANDU_EC6_pct: min 80, mid 87, max 91 (tier 2, requires_confirmation: true)
source: "IAEA PRIS lifetime load factors floty CANDU-6 (Qinshan III, Cernavodă, Wolsong ~85-90%); NuclearFAQ.ca"
```

Metoda: WebSearch (WebFetch był zablokowany przez proxy sieciowy dla
wszystkich sprawdzonych domen — pris.iaea.org, world-nuclear.org,
en.wikipedia.org, cbc.ca, nbmediacoop.org, theenergymix.com,
thedonjonesarticles.wordpress.com — więc dane pochodzą z fragmentów/
podsumowań zwracanych przez WebSearch, nie z bezpośredniego odczytu stron).
Nie udało się dotrzeć bezpośrednio do interfejsu PRIS; dane PRIS cytowane
tu pochodzą z wtórnych źródeł, które explicite powołują się na PRIS jako
źródło pierwotne (głównie coroczne artykuły Donalda Jonesa, emerytowanego
inżyniera branży jądrowej, publikowane od lat i cytowane w prasie
branżowej).

## 1. Tabela źródeł

| Jednostka | Kraj | Okres uśrednienia | Lifetime/long-run CF | Źródło | Wiarygodność |
|---|---|---|---|---|---|
| Qinshan III, blok 1 i 2 | Chiny | rok po krytyczności → koniec 2019 (~16-17 lat) | **~90%** (cytowane jako "0.9") dla obu bloków | Don Jones, "CANDU 6 Performance in 2019" (thedonjonesarticles.wordpress.com), dane wywodzone z IAEA PRIS | Wysoka — wtórne, ale wprost odwołuje się do PRIS; spójne z niezależną wzmianką o Qinshan III jako jednym z najlepiej osiągających bloków CANDU-6 |
| Flota CANDU-6, 9 działających bloków (agregat) | globalnie | do końca 2019 | lifetime **86.8%**; roczny CF 2019 = 83.9% | Don Jones, "CANDU 6 Performance in 2019" | Wysoka — agregat wg PRIS, powtarzalna metodologia z roku na rok |
| Flota CANDU-6, 9 działających bloków (agregat) | globalnie | do końca 2022 | lifetime **86.5%**; roczny CF 2022 = 81.3% (EAF 81.0%) | Don Jones, "CANDU 6 Performance in 2022" | Wysoka — jak wyżej, nowszy punkt danych; potwierdza stabilność ~86-87% na przestrzeni lat |
| Cernavodă 1 | Rumunia | ~9 lat wczesnej eksploatacji (od komercyjnego uruchomienia 1996) | gross CF **87.13%** | "Aspects of power production at Cernavoda NPP" (INIS-IAEA); cytowane też jako "jeden z 10 najbardziej efektywnych bloków CANDU na świecie" | Średnio-wysoka — konferencyjny referat INIS, ale konkretna liczba i okres; to NIE jest pełny lifetime CF do dziś (~28 lat pracy), tylko wczesny 9-letni odcinek |
| Wolsong 1 | Korea Płd. | cały cykl życia, 1983 → ok. 2015 (obejmuje przestój na retubing 2009-2011) | lifetime **86.2%** | Prasa branżowa (NEI Magazine i pochodne o retubingu Wolsong 1) | Średnia — brak jawnego przypisania do PRIS w źródle, ale liczba spójna z resztą floty |
| Wolsong 1 (= Point Lepreau?, patrz uwaga) | — | od uruchomienia komercyjnego 1983 → koniec 2022, WŁĄCZAJĄC przestój refurbishmentu | lifetime **71.5%** (roczny CF 2022 = 61.5%) | Don Jones, "CANDU 6 Performance in 2022" | Wysoka jakość danych, ale **uwaga interpretacyjna**: ten niski wynik to efekt uśrednienia CF po całym okresie życia WŁĄCZNIE z wieloletnim przestojem na refurbishment (nie jest to "zdolność operacyjna po refurbishmencie") — patrz sekcja 4 |
| Embalse | Argentyna | do końca 2004 (~22 lata pracy, przed refurbishmentem 2015-2018) | lifetime **83.2%** | Wtórne źródło cytujące dane branżowe/PRIS-pochodne za 2004 | Średnia — starszy punkt danych (sprzed refurbishmentu), ale dobrze udokumentowany |
| Flota CANDU-6, 10 bloków (agregat, wcześniejszy punkt czasowy) | globalnie | do końca 2004 | lifetime **87%** | j.w. (ten sam zestaw źródeł co Embalse) | Średnia — starszy agregat, ale zgodny z późniejszymi (86.5-86.8%) |
| Point Lepreau, przed refurbishmentem | Kanada | 1983 → marzec 2008 (zamknięcie na refurbishment) | lifetime **82%** | Materiały konferencyjne o "Powering the future — Life extension of Point Lepreau" (OSTI/ETDEWEB) + wtórne | Średnio-wysoka |
| **Point Lepreau, PO refurbishmencie** | Kanada | 2013-01-01 → 2024-12-31 (12 lat, operacyjny long-run) | CF **78%**, poniżej średniej globalnej; NB Power celował w 89% | CBC News (2024), "N.B.'s Point Lepreau nuclear plant ranked as poor performer among international peers"; potwierdzone przez Globe and Mail, NB Media Co-op, ScottMadden benchmarking (2024-2025) | Wysoka — świeże (2024-2025), spójna narracja w wielu niezależnych mediach kanadyjskich, konkretny 12-letni okres uśrednienia, jawnie kontrastowane z celem projektowym 89% |
| Design/target CF (NIE dane operacyjne) | — | — | Cel projektowy CANDU-6 = 89% design / 85% operacyjny (z buforem 4%); cel EC6 ≥ 90% | NuclearFAQ.ca / dokumentacja techniczna AECL / CANDU Energy "Enhanced CANDU 6 Technical Summary" | Niska dla celów tego wpisu — to deklaracje projektowe/marketingowe producenta, nie dane eksploatacyjne |

## 2. Ocena obecnego wpisu (min 80 / mid 87 / max 91)

- **mid=87**: dobrze potwierdzone. Świeże agregaty floty CANDU-6 z PRIS
  (via Don Jones) dają 86.5-86.8% na końcu 2019 i 2022 — to najbardziej
  wiarygodny, powtarzalny i aktualny punkt odniesienia. **Nie wymaga
  korekty.**
- **max=91**: rozsądny górny kraniec. Najlepsze bloki (Qinshan III,
  ~90% lifetime) leżą tuż poniżej. Cernavodă 1 (~87% we wczesnym okresie)
  mieści się w środku zakresu. **Bez zmian, ewentualnie można obniżyć do
  90, ale 91 nie jest nieuzasadnione jako górny "optimistic tail".**
- **min=80**: to jest **słabo uzasadnione i prawdopodobnie zbyt
  optymistyczne**. Najlepiej udokumentowany, najświeższy long-run
  przypadek gorszej wydajności — Point Lepreau po refurbishmencie,
  2013-2024 (12 lat, nie krótki epizod) — daje CF = **78%**, czyli
  *poniżej* obecnego minimum 80. To nie jest dane odstające z młodej
  jednostki w rozruchu — to udokumentowana, wieloletnia realna wydajność
  odnowionego bloku CANDU-6, opisywana w 2024-2025 jako "poor performer"
  na tle międzynarodowych rówieśników. Obecny wpis w rejestrze cytuje
  "Wolsong ~85-90%" jako część uzasadnienia dolnego krańca, ale
  rzeczywiste dane dla Wolsong 1 (86.2% lifetime) i floty ogółem
  (86.5-86.8%) nie schodzą w okolice 80% — a jedyny udokumentowany punkt
  bliski/poniżej 80% (Point Lepreau) nie był uwzględniony w oryginalnym
  źródle wpisu.

## 3. Rekomendacja min/mid/max

Proponowane: **min = 78, mid = 87, max = 91** (tier i distribution bez zmian).

Uzasadnienie:
- **min 78** zamiast 80: podnosi wiarygodność dolnego krańca przez
  zakotwiczenie go w realnej, 12-letniej obserwacji (Point Lepreau
  post-refurbishment), zamiast w niesprecyzowanym szacunku. To też
  spójne z ryzykiem, które model LCOE powinien uchwycić — refurbished/
  FOAK-adjacent CANDU nie zawsze osiąga wydajność projektową.
- **mid 87** bez zmian: bezpośrednio wsparte agregatem floty z PRIS
  (86.5-86.8%, dwa niezależne roczne punkty czasowe 2019 i 2022).
- **max 91** bez zmian: górny kraniec bliski najlepszym rzeczywistym
  blokom (Qinshan III ~90%) plus mały margines na to, że EC6 to
  nowsza generacja z potencjalnie lepszą dostępnością.

Alternatywa ostrożniejsza (jeśli wolisz węższy rozkład wokół dobrze
potwierdzonego agregatu floty): min=82, mid=86, max=90 — ale to
świadomie ignoruje udokumentowany przypadek Point Lepreau jako
"outlier" zamiast realnego ogona ryzyka. Rekomendacja główna (78/87/91)
jest preferowana, bo szerszy dolny ogon lepiej odzwierciedla
niepewność projektu, który jeszcze nie ma zbudowanych jednostek EC6.

## 4. Co jest bezpośrednim odczytem z PRIS, a co ekstrapolacją

**Bezpośrednie / blisko-pierwotne dane operacyjne CANDU-6 (nie EC6):**
- Agregat floty 86.5-86.8% (Don Jones, jawnie odwołuje się do PRIS jako
  źródła).
- Qinshan III ~90%, Wolsong 1 86.2%, Cernavodă 1 ~87% (wczesny okres),
  Embalse 83.2% (do 2004), Point Lepreau 82% (przed refurbishmentem) i
  78% (po refurbishmencie, 2013-2024).
- Wszystko to dotyczy **CANDU-6**, nie EC6 (Enhanced CANDU 6) — EC6 nie
  ma jeszcze zbudowanej ani eksploatowanej jednostki referencyjnej
  (oferta AtkinsRéalis dla Polski to wciąż etap ofertowy, patrz
  `CANDU_EC6_CAPEX_usd_per_kW` w rejestrze).

**Ekstrapolacja — założenia, nie dane:**
- Że EC6 osiągnie CF w tym samym zakresie co historyczna flota CANDU-6.
  To rozsądny proxy (ta sama architektura reaktora, on-power refuelling,
  ten sam producent), ale EC6 wprowadza zmiany projektowe (m.in. dłuższy
  projektowany czas życia, ulepszone systemy) i deklarowany cel
  projektowy ≥90% — sam producent sugeruje, że EC6 *powinien* bić
  historyczne CANDU-6, głównie dzięki wyeliminowaniu wczesnych problemów
  z retubingiem/feederami, które ciążyły starszym blokom (Point Lepreau,
  Wolsong 1 przed retubingiem).
- Kontrargument: nowe projekty jądrowe (FOAK) historycznie *nie*
  osiągają od razu deklarowanych parametrów projektowych (patrz też
  `construction_years_AP1000` w rejestrze, gdzie FOAK systematycznie
  przekracza deklaracje NOAK). Nie ma powodu zakładać, że CF będzie
  wyjątkiem — stąd rekomendacja, by NIE podnosić mid/max ponad
  zaobserwowany zakres historyczny CANDU-6, mimo deklaracji projektowej
  EC6 ≥90%.
- Krótkoterminowe dane projektowe/marketingowe (design target 89-90%+)
  są celowo **wykluczone** z proponowanego zakresu jako zbyt
  optymistyczne / niezweryfikowane operacyjnie — użyte tylko jako
  potwierdzenie, że górny kraniec (91%) nie jest nierealistyczny.

## 5. Proponowany tier i `requires_confirmation`

- **Tier: pozostaje 2.** Dane źródłowe są solidne dla CANDU-6 (bliskie
  Tier 1 — PRIS jest źródłem pierwotnym, ale docieramy do niego przez
  wtórne kompilacje, nie bezpośredni odczyt bazy), ale sam wpis dotyczy
  EC6, więc pozostaje ekstrapolacja generacyjna → Tier 2 jest właściwe
  (nie Tier 1, bo brak bezpośrednich danych operacyjnych EC6; nie Tier
  3, bo istnieje bogaty, spójny, wieloźródłowy zbiór danych CANDU-6
  jako proxy).
- **`requires_confirmation`: pozostaje `true`.** Do czasu uzyskania
  bezpośredniego dostępu do interfejsu PRIS (obecnie zablokowany w tym
  środowisku) i/lub pierwszych danych operacyjnych rzeczywistej
  jednostki EC6, wpis powinien pozostać oznaczony jako wymagający
  potwierdzenia. Dodatkowo warto rozważyć rozszerzenie `source` o
  wyraźne odwołanie do przypadku Point Lepreau post-refurbishment jako
  uzasadnienia dolnego krańca (patrz sekcja 3), oraz zaznaczenie, że
  "Wolsong ~85-90%" w obecnym opisie źródła jest nieco mylące — realny
  Wolsong 1 lifetime CF to 86.2%, blisko dolnego, nie górnego krańca
  tego przedziału.

## 6. Otwarte pytania / ograniczenia badania

- Nie udało się bezpośrednio zweryfikować liczb na `pris.iaea.org`
  (proxy sieciowy blokuje dostęp) — wszystkie liczby "z PRIS" są tu
  cytowane za wtórnymi źródłami, które same powołują się na PRIS.
  Rekomendacja: przy najbliższej okazji z odblokowanym dostępem do
  PRIS, zweryfikować bezpośrednio strony `LifeTimeUnitCapabilityFactor.aspx`
  i `ReactorDetails.aspx` dla Qinshan III-1/2, Cernavodă-1/2, Wolsong-1/2/3/4,
  Point Lepreau i Embalse.
- Nie znaleziono świeższych danych (2023-2025) dla agregatu floty
  CANDU-6 poza punktem 2022 (86.5%) — możliwe, że Don Jones publikuje
  coroczne aktualizacje ("CANDU 6 Performance in 2023/2024"), których
  nie udało się odnaleźć/dotrzeć w tej sesji.
- Liczba "9 działających bloków" w agregatach floty nie jest w pełni
  wyjaśniona (Qinshan III×2 + Cernavodă×2 + Wolsong×4 + Point Lepreau +
  Embalse = 10 potencjalnych bloków CANDU-6/pochodnych) — możliwe, że
  Embalse lub inny blok był czasowo wyłączony z agregatu z powodu
  przestoju/refurbishmentu w danym roku sprawozdawczym.
