# Lekcje: reaktor SNR-300 (Kalkar)

> **Korekta założenia:** SNR-300 to reaktor prędki chłodzony **sodem (SFR)**,
> nie ołowiem (LFR). Lekcje 1–4 dotyczą SFR; Lekcja 5 porównuje go z LFR, żeby
> pokazać, czym te dwie rodziny się różnią.

Cel kursu: zrozumieć fizykę, konstrukcję i ekonomię reaktora prędkiego
na przykładzie projektu, który został w pełni zbudowany, ale nigdy nie
pracował. Kurs jest powiązany z modelem LCOE w tym repo.

| # | Lekcja | Czas | Wynik |
|---|---|---|---|
| 1 | [Kontekst i historia projektu](01_context.md) | 45 min | oś czasu, rozumienie przyczyn niepowodzenia |
| 2 | [Fizyka reaktora prędkiego](02_physics.md) | 60 min | współczynnik powielania, widmo, bilans neutronów |
| 3 | [Konstrukcja i układy bezpieczeństwa](03_design.md) | 60 min | schemat pętli, zagrożenia sodowe |
| 4 | [Ekonomia: koszt i opóźnienia](04_economics.md) | 60 min | obliczenia LCOE z narzutem czasu i kosztu |
| 5 | [SFR vs LFR](05_sfr_vs_lfr.md) | 45 min | tabela porównawcza, wybór chłodziwa |

Wymagania wstępne: podstawy fizyki jądrowej (rozszczepienie, przekrój czynny,
moderacja) i podstawy rachunku kosztów (dyskontowanie).

## Dane źródłowe

Wartości liczbowe w lekcjach pochodzą z poniższych źródeł. Każdą wartość
oznaczono jako **[zweryfikowane]** (znaleziona w źródle) lub **[do weryfikacji]**
(wiedza ogólna, trzeba potwierdzić przed użyciem w modelu).

- [IAEA INIS – opis SNR-300](https://inis.iaea.org/records/46c8x-des30)
- [Konferencja 1976 – parametry projektowe](https://inis.iaea.org/records/3x94f-9vs07)
- [KfK 5455 (Marth, 1994) – historia projektu](https://publikationen.bibliothek.kit.edu/270037170/3813531)
- [SNR-300 – Wikipedia](https://en.wikipedia.org/wiki/SNR-300)
- [JAEA ATOMICA – SNR-300](https://atomica.jaea.go.jp/data/pdf/ATOMICA_03-01-05-07.pdf.zip)

Koszt końcowy w źródłach się rozjeżdża (≈7 mld DM jest podawany najczęściej);
szczegóły w Lekcji 4.

## Parametry podstawowe

| Parametr | Wartość | Status |
|---|---|---|
| Typ | SFR, paliwo MOX | zweryfikowane |
| Moc cieplna | ≈ 762 MWt (771 MWt na wlocie do turbiny wg publikacji z 1976) | zweryfikowane |
| Moc elektryczna brutto | 327 MWe | zweryfikowane |
| Temperatura wylotowa rdzenia | ≈ 819 K (≈ 546 °C) | zweryfikowane (zapis w źródle zawiera literówkę) |
| Początek budowy | kwiecień 1973 | zweryfikowane |
| Zakończenie konstrukcji | ok. 1985 | zweryfikowane |
| Zakończenie projektu | marzec 1991, bez załadunku paliwa | zweryfikowane |
| Koszt szacunkowy 1972 → 1991 | 1535 mln DM → ok. 7000 mln DM | zweryfikowane (JAEA); inne źródła podają inne wartości |
| Liczba pętli, ciśnienie, skład rdzenia | — | brak w znalezionych źródłach |
