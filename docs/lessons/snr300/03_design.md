# Lekcja 3: Konstrukcja i układy bezpieczeństwa

## Cele
Opisać architekturę SFR typu pętlowego i zagrożenia związane z sodem.
Liczby inne niż w README to wiedza ogólna **[do weryfikacji]**; liczbę pętli,
ciśnienia i rozmieszczenie elementów SNR-300 trzeba wziąć z dokumentacji.

## 1. Trzy obiegi
1. **Obieg pierwotny (sód radioaktywny)** — odbiera ciepło z rdzenia.
2. **Obieg pośredni (sód nieradioaktywny)** — izoluje obieg pierwotny od wody.
3. **Obieg wodno-parowy** — wytwarza parę dla turbiny.

Obieg pośredni istnieje dlatego, że sód reaguje gwałtownie z wodą.

## 2. Zalety sodu jako chłodziwa
- Wysoka przewodność cieplna, niskie ciśnienie robocze (temperatura wrzenia sodu
  ≈ 883 °C przy 1 atm), duży margines do wrzenia przy ≈ 546 °C na wylocie rdzenia.
- Słaba moderacja — zachowuje widmo prędkie.

## 3. Wady i zagrożenia
- Reaguje z wodą i palnie w powietrzu.
- Jest nieprzezroczysty, co utrudnia inspekcję i obsługę paliwa.
- Dodatni współczynnik reaktywności pustek w dużych rdzeniach (wrzenie sodu
  może zwiększyć moc) **[do weryfikacji]**.
- Aktywacja Na-24 (obieg pierwotny jest silnie radioaktywny).

## 4. Zasady bezpieczeństwa
- Ujemne sprzężenia temperaturowe (efekt Dopplera, rozszerzalność).
- Pasywne odprowadzanie ciepła powyłączeniowego.
- Dwa niezależne systemy wyłączania **[do weryfikacji dla SNR-300]**.

## Zadania
1. Narysuj schemat trzech obiegów i oznacz, gdzie zachodzą wymiany ciepła.
2. Oszacuj sprawność z danych podstawowych: 327 MWe / 762 MWt ≈ **42,9%** (brutto).
   Porównaj z typowym LWR (~33%) i wyjaśnij, skąd różnica (wyższa temperatura pary).
3. Opisz scenariusz „wyciek sodu do pomieszczenia z wodą" i dwa środki ograniczające skutki.
