# Lekcja 4: Ekonomia — koszt i opóźnienia

## Cele
Policzyć wpływ nakładów, czasu budowy i stopy dyskontowej na LCOE
na przykładzie SNR-300. To lekcja najbliższa temu repo.

## 1. Dane
| Wielkość | Wartość | Status |
|---|---|---|
| Szacunek 1972 | 1535 mln DM | zweryfikowane (JAEA) |
| Koszt na 1991 | ok. 7000 mln DM | najczęściej podawane; źródła się różnią |
| Wzrost | ×4,56 | obliczone z powyższych |
| Czas budowy | ok. 18 lat (1973–1991) | zweryfikowane |
| Moc | 327 MWe brutto | zweryfikowane |

Uwaga: wartości DM z różnych lat nie są porównywalne bez deflatora; dodatkowo
część wzrostu to inflacja, a część zmiany wymagań licencyjnych i przestoje.
Inne źródła podają ≈ 4 mld USD lub 500 mln marek w cenach z 1969 r., więc
**przed wykorzystaniem w modelu ustal bazę cenową**.

## 2. Koszt jednostkowy
Overnight cost na kW(e): 7000 mln DM / 327 MWe ≈ **21 400 DM/kW** (nominalnie, bez dyskonta
i bez deflatora). To tylko ilustracja rzędu wielkości.

## 3. Wpływ opóźnień
Odsetki w czasie budowy (IDC) rosną wykładniczo z czasem budowy. Dla stopy r
i równomiernych wydatków przez T lat:
IDC/Overnight ≈ (e^{rT} − 1)/(rT) − 1.
Przykład: r = 5%, T = 8 lat → ok. 23%; T = 18 lat → ok. 62%.

## 4. LCOE
LCOE = (Σ kosztów zdyskontowanych) / (Σ energii zdyskontowanej).
Dla projektu, który nigdy nie wyprodukował energii, mianownik = 0, więc
LCOE jest nieokreślone — cały koszt jest „utopiony". Ćwiczenie pokazuje,
dlaczego ryzyko licencyjne trzeba modelować jawnie (np. jako prawdopodobieństwo
nieuzyskania pozwolenia).

## Zadania
1. Policz IDC dla r = 3%, 5%, 8% i T = 6, 10, 18 lat. Zrób tabelę.
2. Załóż, że reaktor pracuje 40 lat z współczynnikiem obciążenia 80%.
   Policz LCOE dla kosztu 7000 mln DM i r = 5% (pomiń O&M i paliwo).
3. Zmodeluj ryzyko: z prawdopodobieństwem p projekt zostaje anulowany po 18 latach.
   Jaki jest oczekiwany koszt na kWh jako funkcja p?
4. (Repo) Dodaj parametry (koszt, czas budowy, prawdopodobieństwo anulowania)
   do `config/assumptions_registry.json` z poziomem wiarygodności, zgodnie z CLAUDE.md;
   żadnych literałów w kodzie `src/`.

## Wskazówki
- Zad. 2: LCOE = overnight·CRF / (P·8760·CF), CRF = r/(1−(1+r)^−N).
- Wynik zad. 2 zależy od przyjętej bazy cenowej — opisz ją.
