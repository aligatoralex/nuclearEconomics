# Lekcja 2: Fizyka reaktora prędkiego

## Cele
Zrozumieć widmo neutronów, powielanie paliwa i różnice względem reaktora
lekkowodnego (LWR). Dane liczbowe poniżej to wiedza ogólna **[do weryfikacji]**,
chyba że zaznaczono inaczej.

## 1. Widmo neutronów
- LWR: woda moderuje neutrony do energii termicznych (~0,025 eV).
- SFR: sód jest słabym moderatorem, więc neutrony pozostają „prędkie"
  (rzędu 100 keV–1 MeV).
- Skutek: w widmie prędkim rośnie liczba neutronów na jedną absorpcję
  w Pu-239, co umożliwia **powielanie**.

## 2. Współczynnik powielania
Breeding ratio: BR = (produkcja nowego materiału rozszczepialnego) / (zużycie).
BR > 1 oznacza, że reaktor produkuje więcej paliwa niż spala.
Typowo BR ≈ 1,0–1,3 dla projektów SFR **[do weryfikacji]**; wartość dla SNR-300
trzeba wziąć z dokumentacji projektowej (nie znaleziono w źródłach z tej sesji).

Bilans: η − 2 − (straty) > 0 (powielanie wymaga η > 2: jeden neutron podtrzymuje reakcję, jeden zamienia U-238 w Pu-239), gdzie η to liczba neutronów na absorpcję
w materiale rozszczepialnym.

## 3. Paliwo MOX w SNR-300
Rdzeń MOX (mieszanina tlenków uranu i plutonu). Według IAEA rdzeń zmieniono
w trakcie projektu: pełny rdzeń z plutonu z reaktorów MAGNOX nie był możliwy,
więc użyto też plutonu z reaktorów lekkowodnych (licencjonowany rdzeń Mark-Ia).
Wniosek: skład izotopowy plutonu bezpośrednio zmienia neutronikę.

## 4. Obliczenia w praktyce
Do modelowania takiego rdzenia pasują kody z notatki
[`docs/serpent_alternatives.md`](../../serpent_alternatives.md): OpenMC
(z danymi dla widma prędkiego i łańcuchem wypalania dla SFR) lub Serpent
(licencja wymagana).

## Zadania
1. Oblicz η dla Pu-239 w widmie termicznym i prędkim, korzystając z biblioteki
   przekrojów (ENDF/B). Porównaj.
2. Opisz, jak zmieni się BR, gdyby użyto plutonu z paliwa o wyższym wypaleniu
   (więcej Pu-240, Pu-242).
3. (Zaawansowane) Zbuduj w OpenMC model komórki paliwowej MOX w sodzie i policz k∞.
   Zapisz wynik do `data/output/` i opisz założenia w rejestrze, zgodnie z CLAUDE.md.

## Wskazówki
- Zad. 2: Pu-240 jest materiałem żyznym, a Pu-242 pochłania neutrony — skutek zależy od bilansu.

## Demo kodu SCONE
Uruchamialny przykład w [`examples/scone_demo`](../../../examples/scone_demo/README.md)
(`./run_demo.sh`) pokazuje przebieg obliczenia własnego (eigenvalue) Monte Carlo:
cykle nieaktywne i aktywne, k-eff z niepewnością. To **zabawkowa**
biblioteka wielogrupowa U-235, a nie model SNR-300 – służy do poznania
przepływu pracy, nie do wniosków o reaktorze.
