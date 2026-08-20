# R3 — Dekomisja PHWR/CANDU, OPEX AP1000 vs CANDU, design lifetime

Badanie źródłowe (WebSearch/WebFetch) do rejestru `config/assumptions_registry.json`.
Zakres: `decommissioning_pct_capex_CANDU`, nowe wymiary OPEX dla `src/tornado_analysis.py`
(obecnie `opex_usd_per_year=100_000_000.0` identyczne dla AP1000/CANDU), oraz
`lifetime_years=60` identyczne dla obu technologii.

**Ograniczenie środowiskowe**: w tej sesji `WebFetch` był zablokowany przez proxy
egress dla praktycznie wszystkich domen źródłowych (osti.gov, researchgate.net,
cnsc-ccsn.gc.ca, nuclearfaq.ca, world-nuclear.org, wikipedia.org, cbc.ca, iaea.org,
eia.gov, nei.org — wszystkie zwróciły `EGRESS_BLOCKED`). Całe badanie opiera się
więc na streszczeniach zwracanych przez `WebSearch` (który ma własny dostęp
server-side), nie na bezpośrednim odczycie pełnych dokumentów źródłowych. Liczby
poniżej są więc pośrednie (przefiltrowane przez search-summary), nie zweryfikowane
przez odczyt oryginalnej strony/PDF-u — stąd żaden z tierów proponowanych niżej nie
schodzi poniżej 3 tam, gdzie liczba nie pochodzi z rejestru już istniejącego lub
z wielokrotnie potwierdzonego konsensusu.

## (a) Dekomisja PHWR/CANDU jako % CAPEX

**Pytanie badawcze**: czy istnieją dedykowane studia kosztów dekomisji PHWR/CANDU,
czy trzeba nadal polegać na ekstrapolacji z LWR (obecny stan rejestru)?

**Odpowiedź**: dedykowane studia PHWR/CANDU **istnieją**, ale żadne z nich nie
dostarcza czystej, gotowej do użycia liczby `% CAPEX` porównywalnej z metodą NEA
2016 dla LWR. Rekomendacja: zostać przy ekstrapolacji z premią, ale z lepszym
uzasadnieniem premii niż obecnie, i **rozszerzyć**, nie zawężyć, przedział.

| Źródło | Liczba / ustalenie | Ocena wiarygodności |
| --- | --- | --- |
| [Point Lepreau — CBC/NB Media Co-op relacje](https://nbmediacoop.org/2022/06/08/indigenous-groups-challenge-new-brunswicks-costly-radioactive-waste-legacy/) (tylko streszczenie WebSearch, WebFetch zablokowany) | Gwarancja finansowa NB Power na dekomisję: ~755 mln CAD; niezależny szacunek realnego kosztu: ~1,8 mld CAD w horyzoncie 50 lat (rozbieżność ~2.4×). Koszt budowy oryginalnej jednostki (635 MWe, 1983): ~1,4 mld CAD nominalnie. | Średnia — dane finansowe z prasy/NGO, nie z pierwotnego dokumentu OPG/NB Power (WebFetch zablokowany na cbc.ca, nbmediacoop.org). Pokazuje **fakt**: utility-owned funding estimates dla CANDU historycznie się myliły w dół, nie w górę. |
| [Cost estimate for decommissioning a CANDU 6MKI nuclear generating station](https://www.osti.gov/etdeweb/biblio/190261) (OSTI/ETDEWEB, WebFetch zablokowany) | Dedykowany, reaktoro-specyficzny szacunek kosztu dekomisji CANDU 6 (AECL-owe zlecenie dla Point Lepreau / Gentilly-2) — istnienie potwierdzone, treść niedostępna w tej sesji. | Niska w tej sesji (brak dostępu do treści) — ale **potwierdza fakt istnienia** dedykowanego, nie-LWR-owego studium AECL/CNSC. |
| [Cost evaluation of proposed decommissioning plan of CANDU reactor (JESTEC, Taylor's Univ., 2018)](https://www.researchgate.net/publication/329573242_Cost_evaluation_of_proposed_decommissioning_plan_of_CANDU_reactor) | Wariant SAFSTOR: ok. 200 mln USD (baza mocy/rok nieznana z dostępnego streszczenia — WebFetch zablokowany na researchgate.net i na PDF taylors.edu.my). | Niska–średnia: liczba istnieje, ale bez znajomości mocy jednostki i CAPEX bazowego nie da się z niej wyprowadzić wiarygodnego `%`. Nie użyto do liczb poniżej. |
| [Development of NPP decommissioning cost estimation algorithm based on the CANDU structure (ScienceDirect, 2021/2022, Annals of Nuclear Energy)](https://www.sciencedirect.com/science/article/abs/pii/S0306454921006046) | Koreański zespół (KHNP-adjacent, po zamknięciu Wolsong-1) opracował dedykowany WBS (Work Breakdown Structure) dla dekomisji CANDU, z koreańskimi stawkami roboczymi i metodą "standard quantity-per-unit" — **nie** przeróbka metody LWR. Liczby wynikowe niedostępne (paywall + WebFetch zablokowany). | Średnia — potwierdza **fakt**: metodyka PHWR-specific (nie ekstrapolacja z LWR) istnieje w recenzowanej literaturze od 2021/2022, napędzana realnym case study (Wolsong-1, pierwszy zamknięty CANDU w Korei). To bezpośrednio podważa formułę "NEA 2016 (baza jak dla LWR) z premią" jako *jedynej dostępnej* opcji. |
| IAEA TRS-407 "Heavy Water Reactors: Status and Projected Development" | Ogólny przegląd HWR; obecność w wynikach wyszukiwania potwierdzona, treść nt. dekomisji nieodczytana (WebFetch zablokowany na iaea.org). | Niska w tej sesji — nieodczytana. |
| NEA 2016 (istniejące źródło rejestru dla `decommissioning_pct_capex_large_LWR`: 0.46–0.73 mln USD/MWe dla >1100 MWe) | Baza LWR, przeliczona na 8/12/16 % — sama NEA odradza metodę procentową. | Tier 3, jak dziś w rejestrze. |

**Wniosek (a)**: dedykowane badania PHWR/CANDU istnieją (AECL/Point-Lepreau-owe
szacunki z lat 90./2000., koreański algorytm WBS z 2021/2022 po Wolsong-1), ale
żadne nie dało się w tej sesji zredukować do porównywalnej liczby `% overnight
capex` bez dostępu do pełnej treści (WebFetch zablokowany). Twarde dane, które
**udało się** potwierdzić (Point Lepreau: rozbieżność 2.4× między funduszem
utility a niezależnym szacunkiem) sugerują, że obecny górny bound rejestru (18%)
może być **zbyt niski**, nie zbyt wysoki — historia Point Lepreau pokazuje
systematyczne niedoszacowanie po stronie operatora.

**Propozycja min/mid/max**: rozszerzyć górną granicę zamiast zawężać przedział:
`min 10, mid 15, max 22` (obecnie: 10/14/18). Uzasadnienie przesunięcia mid
14→15 i max 18→22: (i) Point Lepreau — niezależny szacunek 2.4× wyższy niż
fundusz operatora sugeruje grubszy prawy ogon rozkładu niż czysta ekstrapolacja
LWR+premia zakładała; (ii) istnienie dedykowanej metodyki koreańskiej (2021/2022)
pokazuje, że branża sama uznaje LWR-owe WBS za niewystarczające dla PHWR, co jest
argumentem za *większą*, nie mniejszą niepewnością dopóki nie mamy dostępu do
wyniku tej metodyki.

**Tier / requires_confirmation**: pozostaje **Tier 3**, `requires_confirmation: true`
— bez zmian względem obecnego stanu; jeśli cokolwiek, przypadek jest teraz *silniej*
udokumentowany jako ekstrapolacja z dodatkowym ryzykiem w prawym ogonie, nie mniej.
Rekomendacja follow-up: dociec treści ScienceDirect S0306454921006046 (dostęp
instytucjonalny/Sci-Hub poza zakresem tej sesji) i/lub pierwotnego OSTI ETDEWEB
190261 — to jedyne dwa realne kandydaty na Tier 2 PHWR-specific source.

**Fakt vs ekstrapolacja**: fakt — Point Lepreau utility-guarantee/independent-estimate
gap (2.4×); fakt — istnienie koreańskiego WBS-CANDU-specific algorytmu (2021/2022);
ekstrapolacja — konkretne min/mid/max 10/15/22 (nadal odziedziczone po metodzie
NEA-LWR-plus-premia, tylko z poszerzonym ogonem).

## (b) OPEX O&M dla dużego LWR i CANDU

**Pytanie badawcze**: typowe koszty O&M (fixed+variable) dla AP1000-klasy PWR i
dla floty CANDU/PHWR, osobno, w USD/MWh i USD/MW-rok; czy identyczne
100 mln USD/rok dla obu technologii jest uzasadnione.

### Źródła

| Źródło | Liczba | Ocena wiarygodności |
| --- | --- | --- |
| [NEI "Nuclear Costs in Context" (marzec 2026 / dane 2024, i wydanie sierpień 2026 / dane 2025)](https://www.nei.org/getContentAsset/47fa8caa-9b0d-4029-932c-07f902e82f4f/8d8ff8d6-b2ae-401b-a63c-f6b108e809d2/2024-Costs-in-Context-final.pdf) | Flota USA (głównie duże PWR/BWR): "operating cost" (historycznie: O&M+paliwo, tzw. production cost, bez capex) = 20,48 USD/MWh w 2024 (z trendu: 23,43 USD/MWh w 2002 → szczyt 29,63 USD/MWh w 2012 → 20,48 USD/MWh w 2024). Osobno: "total generating cost" (capex+paliwo+O&M) = 33,74 USD/MWh w 2024, 36,46 USD/MWh w 2025 (+3,7%/+7,9% r/r). | Wysoka co do rzędu wielkości i trendu (uznane, cytowane co roku źródło branżowe), ale **średnia** co do dokładnej definicji granicy O&M/paliwo/capex w tej sesji — WebFetch zablokowany na nei.org, więc rozdzielenie na czyste O&M (bez paliwa) zrobione tu przez odjęcie rejestrowego `ap1000_fuel_usd_per_mwh` (Tier 1, mid=9,0 USD/MWh), nie odczytane wprost z PDF-u NEI. |
| Rejestr: `ap1000_fuel_usd_per_mwh` (mid 9,0 USD/MWh, Tier 1) | Użyte do odjęcia paliwa od NEI "operating cost", żeby uzyskać czyste O&M ≈ 20,48 − 9,0 ≈ 11,5 USD/MWh (2024). | Już w rejestrze, Tier 1. |
| Weryfikacja krzyżowa z obecnym hardcode | 100 mln USD/rok ÷ (1150 MW × 8760 h × 91% CF ≈ 9,167 mln MWh) = 10,91 USD/MWh dla AP1000. | Wewnętrzne obliczenie, nie zewnętrzne źródło — ale pokazuje, że obecna stała **przypadkowo** trafia blisko NEI-implikowanego O&M-only dla AP1000 (~11,5 USD/MWh), mimo że nie była tak wyprowadzona (`common = {"opex_usd_per_year": 100_000_000.0, ...}` w `src/tornado_analysis.py:91`, deklarowana w kodzie jako "nie tier-sourced"). |
| [PowerMag "How Nuclear O&M Is Evolving for the Emerging Power Paradigm"](https://www.powermag.com/how-nuclear-om-is-evolving-for-the-emerging-power-paradigm/) | Variable O&M: 9,25–17 USD/MWh; fixed O&M: 4–223 USD/kWe-rok (skrajnie szeroki, wieloczłonowy, zależny od kraju). | Niska–średnia: figura fixed O&M jest zbyt szeroka, by być użyteczna (223 USD/kWe-rok to prawdopodobnie outlier/skrajny kraj); variable O&M range spójny z NEI. |
| NREL ATB 2024 (nuclear, fixed/variable O&M $/kW-rok, $/MWh) | Istnienie strony/datasetu potwierdzone, dokładne liczby **nieodczytane** (WebFetch zablokowany na atb.nrel.gov, wynik zwrócił tylko odnośniki). | Nieużyte — follow-up. |
| ["Candu and PWR costs compared in Canada" (INIS, AECL, historyczne)](https://inis.iaea.org/records/9zvxx-5jq96) | Jakościowo: CANDU ma **dwa razy więcej systemów wodnych** niż PWR (podwójna pętla D2O: moderator+chłodziwo), co implikuje wyższe wymogi personelu O&M; koszt utrzymania D2O i tryt jest w tym starym studium AECL "more than offset" przez wyższe koszty paliwa PWR (enrichment) — czyli to studium mówi o koszcie **całkowitym** (O&M+paliwo), nie izoluje czystego O&M premium liczbowo. | Średnia — jakościowy kierunek (CANDU O&M wyższy per-system-complexity) potwierdzony z wiarygodnego źródła branżowego (AECL), ale **brak liczby**. Nie da się z tego wyprowadzić konkretnego %. |
| Szukane bezpośrednio i **nieznalezione** w tej sesji: OPG (Darlington/Pickering) koszt O&M USD/MWh, KHNP Wolsong O&M, Nuclearelectrica/SNN Cernavodă O&M | — | Brak — WebFetch zablokowany na oeb.ca / nuclearelectrica.ro bezpośrednio, WebSearch nie zwrócił konkretnych liczb kosztowych (tylko ceny sprzedaży energii, np. Cernavodă 452,96 RON/MWh — to cena rynkowa, nie koszt O&M). |

### Wniosek (b)

Dla **AP1000**: mamy stosunkowo solidną podstawę (NEI fleet-average, zgodną co do
rzędu wielkości z obecną stałą). Dla **CANDU**: **brak** jakiegokolwiek
bezpośredniego, liczbowego źródła O&M-per-MWh floty CANDU/PHWR znalezionego w
tej sesji (Wolsong/Cernavodă/OPG finansowe dane niedostępne przez zablokowany
WebFetch; WebSearch nie zwrócił kosztów operacyjnych, tylko ceny sprzedaży
energii). Różnicowanie CANDU vs AP1000 OPEX poniżej jest więc **ekstrapolacją
jakościową** (system complexity: 2× tyle systemów wodnych, D2O/tryt upkeep,
mniejsza skala jednostki: 1000 MW vs 1150 MW = -13%, brak lokalnej floty
referencyjnej dla EC6 jako nowej konstrukcji zachodniej) — nie liczbą z
konkretnego studium.

**Ważna obserwacja mechaniczna** (niezależna od technologii-specyficznej premii):
obecne identyczne 100 mln USD/rok dla obu technologii **nie jest neutralne** w
przeliczeniu na USD/MWh, ponieważ CANDU EC6 ma mniejszą moc (1000 MW) i niższy
capacity factor mid (87% vs 91%) niż AP1000:

- AP1000: 100 mln USD / (1150 MW × 8760 h × 0,91) = 100 mln / 9 167 340 MWh = **10,91 USD/MWh**
- CANDU EC6: 100 mln USD / (1000 MW × 8760 h × 0,87) = 100 mln / 7 621 200 MWh = **13,12 USD/MWh**

Czyli sam fakt identycznej stałej rocznej **już dziś** implikuje ~20% premię O&M
per-MWh dla CANDU — nie zero, jak sugerowałaby "identyczność" liczby. To działa
we właściwym kierunku jakościowo (CANDU rzeczywiście powinien mieć wyższy O&M/MWh
wg. AECL/branżowej wiedzy), ale wielkość premii (20%, czysto z CF/skali, bez
żadnego technologia-specyficznego dodatku za D2O/tryt) jest przypadkowa, nie
zamierzona — obecny kod (`src/tornado_analysis.py:37-39,63-64`) sam dokumentuje
`opex_usd_per_year` jako "fixed placeholder... not tier-sourced", więc ta 20%
premia nie była świadomą decyzją modelową.

### Propozycja min/mid/max

Wszystkie liczby w USD/MWh (2024 USD, O&M bez paliwa — paliwo pozostaje osobnym
parametrem rejestru) i przeliczone na USD/MW-rok przy capacity factor **mid**
odpowiedniej technologii (do faktycznego użycia w `opex_usd_per_year` w kodzie
trzeba pomnożyć przez `capacity_mw` × `capacity_factor` × 8760 zgodnie z tym, jak
Sobol/tornado będzie próbkować CF niezależnie — poniższe USD/MW-rok to punkt
odniesienia przy CF mid, nie sztywna stała).

**AP1000 (1150 MW):**

| | USD/MWh | USD/MW-rok (przy CF=91%) | USD/rok (×1150 MW) |
| --- | --- | --- | --- |
| min | 8 | 63 773 | 73,3 mln |
| mid | 12 | 95 659 | 110,0 mln |
| max | 17 | 135 601 | 155,9 mln |

Uzasadnienie: mid=12 wybrane lekko powyżej implikowanego NEI 2024-minus-fuel
(~11,5), żeby uwzględnić że fleet-average USA zawiera stare, zamortyzowane
jednostki (niższy O&M niż nowobudowany AP1000 w pierwszych latach — warranty,
mniejsza skala floty). min=8 blisko historycznie najniższych lat po
konsolidacji floty (post-2015 uprocess efficiency); max=17 odpowiada górnej
granicy variable O&M z PowerMag plus margines na fixed O&M dla nowej, małej
(na razie) floty AP1000 bez pełnych korzyści skali floty.

**CANDU EC6 (1000 MW):**

| | USD/MWh | USD/MW-rok (przy CF=87%) | USD/rok (×1000 MW) |
| --- | --- | --- | --- |
| min | 10 | 76 212 | 76,2 mln |
| mid | 15 | 114 318 | 114,3 mln |
| max | 24 | 182 909 | 182,9 mln |

Uzasadnienie: mid=15 to ok. +25% względem AP1000 mid (12), łącząca (i)
mechaniczny efekt mniejszej skali/CF opisany wyżej (~+20% już z samego
przeliczenia jednostek), (ii) jakościowo potwierdzoną (AECL) dodatkową
złożoność systemów D2O/tryt, (iii) brak floty referencyjnej dla EC6 jako nowej
konstrukcji w nowej jurysdykcji (first-of-a-kind Western deployment overhead).
min=10 zakłada, że premia CANDU okaże się głównie mechaniczna (skala/CF), a nie
technologiczna. max=24 (+41% vs AP1000 max) odzwierciedla ryzyko, że
tryt/D2O-specyficzny narzut jest realny i większy niż jakościowe źródła
sugerują — brak twardych danych CANDU-specific to uzasadnia jako szeroki
przedział, nie wąski.

**Tier / requires_confirmation**:
- `opex_usd_per_year_AP1000_usd_per_mwh` (nowy parametr, proponowana nazwa):
  **Tier 2**, `requires_confirmation: true` — oparte na uznanym źródle
  branżowym (NEI) z rzeczywistą, choć fleet-average (nie AP1000-specific),
  bazą danych; wymaga potwierdzenia bo (i) NEI to US fleet-wide, nie
  AP1000-specific (AP1000 ma dopiero ~6 jednostek w eksploatacji na świecie,
  Vogtle 3&4 + Sanmen 1&2 + Haiyang 1&2), (ii) rozdzielenie O&M/paliwo zrobione
  przez odjęcie, nie odczytane wprost z PDF-u NEI w tej sesji.
- `opex_usd_per_year_CANDU_usd_per_mwh` (nowy parametr): **Tier 3**,
  `requires_confirmation: true` — brak jakiegokolwiek bezpośredniego źródła
  liczbowego CANDU O&M znalezionego w tej sesji; premia względem AP1000 jest
  ekstrapolacją jakościową.

**Fakt vs ekstrapolacja**: fakt — NEI fleet-average trend 2002-2025 (kierunek i
rząd wielkości, mimo niepewności definicji granicy O&M/paliwo w tej sesji);
fakt — AECL/INIS jakościowe stwierdzenie "CANDU ma dwa razy więcej systemów
wodnych"; fakt — mechaniczny +20% wynikający z różnicy mocy/CF przy identycznej
stałej rocznej (to jest arytmetyka, nie źródło zewnętrzne, ale jest
weryfikowalne w kodzie); ekstrapolacja — wszystkie konkretne min/mid/max
powyżej, zwłaszcza CANDU-specific premia ponad efekt mechaniczny.

## (c) Design lifetime

**Pytanie badawcze**: czy `lifetime_years=60` identyczne dla AP1000 i CANDU EC6
jest uczciwym uproszczeniem, czy CANDU wymaga osobnego traktowania z
uwzględnieniem przestoju na refurbishment mid-life.

### Źródła

| Źródło | Ustalenie | Ocena wiarygodności |
| --- | --- | --- |
| [NRC — Combined License (COL) term](https://www.nrc.gov/reactors/new-reactors/large-lwr/col) | COL ważny 40 lat od daty potwierdzenia przez komisję spełnienia kryteriów akceptacji; odnawialny o kolejne 20 lat → 60 lat łącznie **po** odnowieniu licencji. Nie ma fizycznego przestoju wymaganego do osiągnięcia 60 lat — to kwestia regulacyjnego odnowienia, nie remontu kapitałowego. | Wysoka — NRC, źródło pierwotne regulatora (treść z WebSearch summary, nie z bezpośredniego odczytu nrc.gov, który nie był testowany wprost, ale format jest standardowy i wielokrotnie potwierdzony w branży). |
| [Westinghouse AP1000 Design Certification Renewal do 2046](https://info.westinghousenuclear.com/news/westinghouse-ap1000-design-receives-us-licensing-extension-to-2046) | NRC wydłużył czas trwania certyfikacji projektu (generic design certification, odrębne od licencji konkretnej elektrowni) z 15 do 40 lat; AP1000 certyfikowany od 2006, ważny do 2046. To dotyczy certyfikacji *projektu*, nie licencji *konkretnego bloku* — nie należy mylić z operating license term powyżej. | Wysoka — wielokrotnie potwierdzone (World Nuclear News, PowerMag, biznesowe wire, NRC.gov dokument w wynikach). |
| [IAEA — "The Enhanced CANDU 6 Reactor" (IAEA proceedings P1500_CD)](https://www-pub.iaea.org/MTCD/Publications/PDF/P1500_CD_Web/htm/pdf/topic3/3S02_S.%20Azeez.pdf) oraz [AtkinsRéalis EC6 Technical Summary](https://www.atkinsrealis.com/~/media/Files/A/atkinsrealis/download-centre/en/brochure/enhanced-candu-6-technical-summary-en.pdf) | EC6: **"target life up to 60 years, WITH one mid-life refurbishment of critical equipment"** (kanałów paliwowych/rur ciśnieniowych — fuel channels/pressure tubes). 60 lat dla EC6 to **nie** ciągła praca jak dla AP1000 — to z założenia dwa cykle ~30-letnie rozdzielone dużym projektem kapitałowym i wieloletnim postojem. | Wysoka — dokument techniczny producenta (AtkinsRéalis) + niezależna publikacja IAEA, spójne ze sobą. |
| [AtkinsRéalis — Qinshan Life Extension Mandate (sierpień 2024)](https://www.atkinsrealis.com/en/media/press-releases/2024/08-08-2024) | AtkinsRéalis opisuje bieżący mandat jako wsparcie "ongoing 30-year life extension" istniejących bloków CANDU zbliżających się do "scheduled date for component replacement to facilitate a further 30 years of operation" — czyli firma sama, we własnym języku marketingowym, ramuje flotę CANDU jako 30+30, nie jako ciągłe 60. | Wysoka — komunikat prasowy producenta, bezpośrednio potwierdza wzorzec 30+30 dla całej rodziny CANDU, nie tylko starszych CANDU-6. |
| Darlington (OPG, 4× CANDU, refurbishment 2016-2026) | Całkowity budżet: 12,8 mld CAD za 4 bloki (~3,2 mld CAD/blok); pojedynczy blok (unit 2): rozpoczęcie remontu 14.10.2016, czas trwania ~40 miesięcy (~3,3 roku) przestoju. Zakończone wcześniej i w budżecie wg doniesień z 2023/2024. | Wysoka — wielokrotnie potwierdzone (World Nuclear News, Globe and Mail, Power Technology, ENR), spójne liczby w kilku niezależnych źródłach. |
| Bruce Power (8× CANDU, refurbishment 2016-2033) | Całkowity koszt kapitałowy szacowany na ~25 mld CAD (w dolarach z 2017), harmonogram 2016-2033 dla całej floty 8 bloków. | Średnia-wysoka — źródło branżowe (Bruce Power own report "Nuclear Refurbishment Fall 2017"), ale to koszt całego programu, nie czysta cena per-blok. |
| Cernavodă-1 (Rumunia, CANDU 6, refurbishment ogłoszony 2022+) | Szacowana wartość nominalna projektu: ~3,2 mld EUR (grant państwowy 600 mln EUR + pożyczka EIB 800 mln EUR jako część finansowania); zakres: wymiana wszystkich rur kalandrii, generatorów pary, I&C; wydłużenie życia o **min. 25 lat**. | Wysoka — World Nuclear Association + NucNet, potwierdzone wielokrotnie, konkretne kwoty z instytucji finansujących (EIB). |
| Wolsong-1 (Korea, CANDU 6, retubing) | Przestój na retubing: 839 dni (~28 miesięcy). | Średnia — jedno źródło (search summary), ale liczba precyzyjna i wiarygodna w kontekście (znana, udokumentowana operacja). |
| Embalse (Argentyna, CANDU 6, life extension) | Przestój "breaker open to criticality": 3 lata i 5 dni. | Średnia-wysoka — NEI Magazine, źródło branżowe specjalistyczne. |

### Wniosek (c)

To jest **najbardziej jednoznaczny** z trzech wyników badania. `lifetime_years=60`
identyczne dla obu technologii jest **uczciwym uproszczeniem tylko dla AP1000**
(gdzie 60 lat = ciągła praca + regulacyjne odnowienie licencji, bez fizycznego
przestoju modelowanego gdziekolwiek indziej w LCOE — a `calculate_lcoe` i tak nie
modeluje przestojów). Dla **CANDU EC6 nie jest to uczciwe uproszczenie**:
producent (AtkinsRéalis) i niezależna literatura IAEA jednoznacznie i spójnie
opisują 60-letni target EC6 jako **dwa cykle ~30-letnie rozdzielone jednym
dużym remontem kapitałowym i wieloletnim (2,3–4-letnim, wg. Wolsong/Darlington/
Embalse) postojem bez przychodu**, a cała obecnie budowana/refurbishowana flota
CANDU-6 (Darlington, Bruce, Cernavodă) potwierdza ten wzorzec w praktyce, nie
tylko w teorii projektowej.

Obecny model (`src/lcoe_core.calculate_lcoe`, DCF na `lifetime_years` lat
ciągłej produkcji) **nie ma mechanizmu** na: (i) drugi wstrzyk kapitału w
połowie życia, (ii) kilkuletnią przerwę w generacji (zerowy przychód, ale
prawdopodobnie nadal część OPEX — utrzymanie w stanie gotowości) w środku
okresu. Dla AP1000 brak tego mechanizmu jest nieszkodliwy (nic takiego się nie
dzieje w modelu producenta). Dla CANDU EC6 jego brak **systematycznie zaniża**
LCOE CANDU względem AP1000, bo koszt refurbishmentu i utracona generacja są
realne (Darlington: ~3,2 mld CAD/blok, ~40 miesięcy przestoju — rzędu wielkości
porównywalnego z częścią overnight capex nowego bloku) i obecnie **nigdzie** nie
wchodzą do DCF.

### Rekomendacja — nie jest to prosta zmiana jednej liczby w rejestrze

To nie jest przypadek "zmień min/mid/max jednego parametru" — to luka
modelowa. Dwie opcje do rozważenia w osobnym zadaniu (poza zakresem tego R3):

1. **Krótki-horyzontowy hack**: potraktować CANDU EC6 jako dwa niezależne,
   30-letnie cykle DCF z osobnym `capex_effective` na starcie każdego cyklu
   (drugi capex = koszt refurbishmentu, nie overnight capex nowego bloku), i
   zdyskontować oba do t=0. To wymaga zmiany `calculate_lcoe` lub nowej funkcji
   w `src/lcoe_core.py` — nie mieści się w samym rejestrze.
2. **Prostszy, przybliżony fix w rejestrze**: dodać do `lifetime_years` dla
   CANDU efektywny "downtime discount" — np. `lifetime_years_effective_CANDU`
   pozostaje 60, ale dodać nowy parametr `CANDU_refurbishment_capex_usd` (do
   dodania do CAPEX zdyskontowanego na moment remontu) i
   `CANDU_refurbishment_outage_years` (do odjęcia produkcji w tym okresie z
   licznika `capacity_factor`-effective lub wprost z lat generujących
   przychód). To nadal wymaga zmiany `calculate_lcoe`, ale mniejszej.

**Proponowane nowe parametry rejestru (do przyszłego zadania, nie do tego R3)**:

| Parametr | min | mid | max | Tier | Uzasadnienie |
| --- | --- | --- | --- | --- | --- |
| `CANDU_refurbishment_capex_usd_per_1000MWe` | 1,5 mld USD | 2,4 mld USD | 3,6 mld USD | 3 | Darlington ~3,2 mld CAD/blok (~2,3 mld USD przy FX ~0,73, orientacyjnie) jako mid; Cernavodă-1 ~3,2 mld EUR (~3,5 mld USD, ale szerszy zakres) jako górna granica; dolna granica konserwatywnie niżej z uwagi na możliwe korzyści floty EC6 jako nowszej konstrukcji. Wymaga potwierdzenia — konwersje walutowe i różnice zakresu prac między projektami nie zostały ujednolicone. |
| `CANDU_refurbishment_outage_years` | 2,3 | 3,0 | 4,0 | 3 | Wolsong-1 retubing: 28 mies. (2,3 lat) jako min; Darlington unit: ~40 mies. (3,3 lat) i Embalse: 3 lata jako mid; max konserwatywnie wyżej dla ryzyka poślizgu harmonogramu (typowe dla pierwszych bloków w danej flocie/kraju). |
| `CANDU_refurbishment_timing_years` | 25 | 28 | 30 | 3 | AtkinsRéalis komunikat: "30-year life extension" jako punkt odniesienia; Darlington/Bruce bloki wchodziły w remont po ~28-32 latach eksploatacji. |

**Dla samego `lifetime_years` w obecnym, niezmienionym modelu** (bez dodania
powyższych nowych parametrów): rekomendacja to **zostawić 60 lat dla obu**, ale
dodać do `rationale` rejestru dla CANDU jawną adnotację, że ta wartość
**zakłada kontrfaktycznie brak przestoju na refurbishment** i że jest to znana,
udokumentowana luka modelowa (nie cicha, nieopisana uproszczenie). To jest
najmniejsza bezpieczna zmiana możliwa do zrobienia bez ingerencji w
`src/lcoe_core.py`.

**Tier / requires_confirmation**: istniejący `lifetime_years=60` w kodzie
(nie w rejestrze — to hardcoded literal w `src/tornado_analysis.py:91`, co już
łamie konwencję CLAUDE.md "no parameter enters src/ code as a bare literal";
osobny problem, poza zakresem tego zadania, ale wart odnotowania) powinien
**wejść do rejestru** jako `lifetime_years_AP1000` (Tier 2,
`requires_confirmation: false` — NRC 40+20 to fakt regulacyjny) i osobno
`lifetime_years_CANDU_EC6` (Tier 3, `requires_confirmation: true` — bo
"60 lat" dla CANDU jest de facto dwoma 30-letnimi cyklami z remontem między
nimi, obecnie niemodelowanym).

### Fakt vs ekstrapolacja

**Fakt** (wielokrotnie potwierdzone, niezależne źródła): AP1000 COL = 40 lat +
20 lat odnowienia = 60 lat, bez fizycznego przestoju w modelu producenta;
EC6 = target 60 lat **z jednym mid-life refurbishment** kanałów
paliwowych/rur ciśnieniowych (AtkinsRéalis + IAEA, spójne); cała obecnie
budowana flota CANDU-6 (Darlington, Bruce, Cernavodă) faktycznie przechodzi
przez wieloletnie (2,3–4-letnie), wielomiliardowe remonty w połowie życia.

**Ekstrapolacja**: konkretne min/mid/max dla nowych proponowanych parametrów
`CANDU_refurbishment_*` (konwersja walut, uśrednienie między projektami o
różnym zakresie i różnej dojrzałości technologicznej, założenie że EC6 jako
nowsza konstrukcja będzie podobna kosztowo do starszych CANDU-6 w trakcie
refurbishmentu).

## Podsumowanie rekomendacji dla `config/assumptions_registry.json`

| Parametr (istniejący/nowy) | Zmiana | Tier | requires_confirmation |
| --- | --- | --- | --- |
| `decommissioning_pct_capex_CANDU` | min/mid/max: 10/14/18 → **10/15/22** | 3 (bez zmian) | true (bez zmian) |
| `opex_usd_per_year` (AP1000) → nowy `AP1000_OM_usd_per_mwh` | nowy parametr, zastępuje hardcoded stałą w `src/tornado_analysis.py:91` | **2** (nowy) | true |
| `opex_usd_per_year` (CANDU) → nowy `CANDU_EC6_OM_usd_per_mwh` | nowy parametr, zastępuje tę samą hardcoded stałą | **3** (nowy) | true |
| `lifetime_years` (AP1000) → nowy `lifetime_years_AP1000` | nowy parametr, zastępuje hardcoded `60` | **2** (nowy) | **false** |
| `lifetime_years` (CANDU) → nowy `lifetime_years_CANDU_EC6` | nowy parametr, zastępuje tę samą hardcoded `60`; **wymaga też** nowego modelowania (refurbishment capex + outage), nie tylko nowej liczby w rejestrze | **3** (nowy) | true |
| `CANDU_refurbishment_capex_usd_per_1000MWe` (nowy, dla przyszłego zadania modelowego) | 1,5 / 2,4 / 3,6 mld USD | 3 | true |
| `CANDU_refurbishment_outage_years` (nowy) | 2,3 / 3,0 / 4,0 lat | 3 | true |
| `CANDU_refurbishment_timing_years` (nowy) | 25 / 28 / 30 lat | 3 | true |

Najistotniejsze pojedyncze ustalenie: **(c) jest realną luką modelową, nie
tylko kwestią kalibracji liczby** — `lifetime_years=60` identyczne dla obu
technologii ukrywa fakt, że CANDU EC6 z definicji producenta wymaga
wielomiliardowego remontu kapitałowego i kilkuletniego przestoju w połowie
życia, którego DCF obecnie w ogóle nie widzi. To prawdopodobnie zaniża LCOE
CANDU bardziej niż jakakolwiek pojedyncza zmiana OPEX czy decomm % opisana w
(a)/(b) powyżej.
