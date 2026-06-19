# Objasnienia zapytan LogQL i PromQL

Ten plik zbiera zapytania LogQL i PromQL znalezione w laboratoriach monitoringu. Przy kazdym wpisie podano plik oraz miejsce w pliku, w ktorym znajduje sie zapytanie.

## 1.3-loki.md

**Linie 282-284**
```logql
{container="telemetry-api"} |= "ERROR"
```
Wybiera strumienie logow z etykieta `container="telemetry-api"`, a potem zostawia tylko linie zawierajace tekst `ERROR`. Operator `|=` oznacza proste wyszukiwanie tekstu w linii logu.

**Linie 298-300**
```logql
{container="telemetry-api"} |= "WARNING"
```
Dziala tak samo jak poprzednie zapytanie, ale szuka tekstu `WARNING`. To dobry wzorzec, gdy znasz dokladne slowo, ktore ma wystapic w logu.

**Linie 313-315**
```logql
{container="telemetry-api"} |~ "(?i)error"
```
Najpierw wybiera logi kontenera `telemetry-api`, a potem filtruje je wyrazeniem regularnym. Operator `|~` oznacza dopasowanie regex, a `(?i)` sprawia, ze wielkosc liter nie ma znaczenia.

**Linie 329-331**
```logql
{container="telemetry-api"} != "DEBUG"
```
Wybiera logi kontenera `telemetry-api`, ale usuwa linie zawierajace `DEBUG`. Przydaje sie, gdy chcesz ukryc zbyt szczegolowe logi techniczne.

**Linie 344-346**
```logql
{container="telemetry-api"} |= "INFO" |= "item"
```
Filtry sa wykonywane po kolei. Wynik musi zawierac jednoczesnie `INFO` i `item`, wiec to odpowiednik dwoch filtrow polaczonych logicznym AND.

**Linie 361-373**
```logql
{container="telemetry-api"} |= "Fetching"
{container="telemetry-api"} |~ "WARNING|ERROR"
{container="telemetry-api"} |= "id=1"
{container="telemetry-api"} != "DEBUG" |= "slow"
```
To zestaw rozwiazan cwiczenia. Pierwsze i trzecie zapytanie robia proste wyszukiwanie tekstu, drugie uzywa regex do znalezienia `WARNING` albo `ERROR`, a czwarte najpierw wyklucza `DEBUG`, potem szuka slowa `slow`.

## 1.4-k8s-lab-env.md

**Linie 195-197**
```promql
sum(kube_pod_status_ready)
```
Dodaje wartosci metryki `kube_pod_status_ready` ze wszystkich pasujacych serii. Dla poczatkujacego: `sum(...)` zwija wiele wynikow w jedna liczbe.

**Linie 207-209**
```logql
{namespace="monitoring"}
```
Wybiera wszystkie strumienie logow z etykieta `namespace="monitoring"`. Nie ma tu filtra tekstowego, wiec Loki pokazuje wszystkie zebrane linie logow z tej przestrzeni nazw.

## 2.1-promql.md

**Linie 215-217**
```promql
http_requests_total
```
Pokazuje wszystkie serie licznika `http_requests_total`. Licznik rosnie od startu aplikacji i zwykle jest podzielony etykietami, np. endpointem, metoda i statusem.

**Linie 221-223**
```promql
http_requests_total{handler="/items/{item_id}"}
```
Filtr w nawiasach klamrowych wybiera tylko serie, ktore maja etykiete `handler` rowna `/items/{item_id}`. To ogranicza wynik do jednego endpointu.

**Linie 227-229**
```promql
http_requests_total{status="2xx"}
```
Wybiera tylko serie z etykieta `status="2xx"`, czyli zadania zakonczone sukcesem HTTP.

**Linie 236-238**
```promql
rate(http_requests_total[5m])
```
`rate(...)` przelicza rosnacy licznik na tempo zmian, czyli zadania na sekunde. `[5m]` oznacza, ze Prometheus patrzy na ostatnie 5 minut probek.

**Linie 247-249**
```promql
sum(rate(http_requests_total[5m]))
```
Najpierw liczy tempo zadan dla kazdej serii, a potem `sum(...)` sumuje je w jeden laczny ruch na sekunde.

**Linie 253-255**
```promql
sum by (handler) (rate(http_requests_total[5m]))
```
Liczy zadania na sekunde osobno dla kazdego `handler`. `sum by (handler)` zostawia podzial po endpointach, ale laczy pozostale etykiety.

**Linie 259-261**
```promql
sum by (status) (rate(http_requests_total[5m]))
```
Liczy tempo zadan z podzialem po statusie, np. `2xx`, `4xx`, `5xx`. Pomaga zobaczyc, ile ruchu konczy sie sukcesem lub bledem.

**Linie 276-280**
```promql
sum by (handler) (rate(http_requests_total{status="5xx"}[5m]))
/
sum by (handler) (rate(http_requests_total[5m]))
```
Gorna czesc to tempo bledow serwera `5xx` dla kazdego endpointu, dolna czesc to tempo wszystkich zadan dla tego samego endpointu. Iloraz daje udzial bledow, np. `0.05` oznacza 5%.

**Linie 292-298**
```promql
1 - (
  sum by (handler) (rate(http_requests_total{status="5xx"}[5m]))
  /
  sum by (handler) (rate(http_requests_total[5m]))
)
```
To odwrotnosc error rate. Jesli 5% zadan to bledy, dostepnosc wynosi `1 - 0.05 = 0.95`, czyli 95%.

**Linie 306-310**
```promql
histogram_quantile(0.95,
  sum by (handler, le) (rate(http_request_duration_seconds_bucket[5m]))
)
```
Oblicza przyblizony percentyl p95 czasu odpowiedzi dla kazdego endpointu. `le` to granice koszykow histogramu, ktore musza zostac zachowane, aby `histogram_quantile` moglo policzyc percentyl.

**Linie 314-318**
```promql
histogram_quantile(0.99,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```
Liczy ogolny percentyl p99 dla calej aplikacji. Brak `handler` w `sum by` oznacza, ze wynik nie jest podzielony na endpointy.

**Linie 343-345 oraz 361-363**
```logql
{container="telemetry-api"} |= `$searchText`
```
Wybiera logi kontenera `telemetry-api` i filtruje je tekstem z dashboardowej zmiennej `$searchText`. W Grafanie uzytkownik wpisuje wartosc w polu, a Loki dostaje juz podstawiony tekst.

**Linie 376-378 oraz 520-522**
```promql
sum by (handler) (rate(http_requests_total[5m]))
```
Wersja dashboardowa ruchu na sekunde per endpoint. Pokazuje, ktore endpointy sa najczesciej wywolywane.

**Linie 393-399**
```promql
(1 - (
  sum by (handler) (rate(http_requests_total{status="5xx"}[5m]))
  /
  sum by (handler) (rate(http_requests_total[5m]))
)) * 100
```
Liczy dostepnosc procentowa per endpoint. `* 100` zamienia wartosc `0.99` na `99`, co pasuje do panelu procentowego.

**Linie 418-423**
```promql
sum by (handler) (rate(http_requests_total{status=~"4xx|5xx"}[5m]))
/
sum by (handler) (rate(http_requests_total[5m]))
* 100
```
Liczy procent zadan zakonczonych bledem klienta lub serwera. `status=~"4xx|5xx"` to dopasowanie regex, ktore pasuje do obu klas statusow.

**Linie 439-443**
```promql
histogram_quantile(0.95,
  sum by (handler, le) (rate(http_request_duration_seconds_bucket[5m]))
)
```
To p95 latency per endpoint dla panelu. Trzeba grupowac po `handler` i `le`, aby wynik byl osobny dla endpointow i nadal zawieral koszyki histogramu.

**Linie 507-509**
```promql
rate(http_requests_total[5m])
```
Surowe tempo zadan bez agregacji. Zwraca wiele serii, po jednej dla kazdej kombinacji etykiet.

**Linie 533-537**
```promql
sum by (handler) (rate(http_requests_total{status="5xx"}[5m]))
/
sum by (handler) (rate(http_requests_total[5m]))
```
Ten sam wzorzec ratio co wyzej: bledy `5xx` podzielone przez wszystkie zadania. Obie strony musza miec ten sam `by (handler)`, zeby Prometheus umial sparowac serie.

## 2.2-k8s-lab-info.md

**Linie 200-202**
```promql
kube_
```
To nie jest pelne zapytanie do wykresu, tylko prefiks do odkrywania metryk. W Grafanie uruchamia podpowiedzi metryk Kubernetes zaczynajacych sie od `kube_`.

**Linie 211-227**
```promql
kube_pod_status_phase
kube_pod_container_status_restarts_total
kubelet_active_pods
kube_deployment_status_replicas
kube_deployment_status_replicas_available
kube_node_status_condition
```
To bezposrednie zapytania o metryki Kubernetes. Pokazuja kolejno fazy podow, restarty kontenerow, liczbe aktywnych podow, repliki deploymentow, dostepne repliki oraz warunki zdrowia wezlow.

**Linia 234**
```promql
kube_pod_status_phase{phase!="Running", phase!="Succeeded"} == 1
```
Filtruje fazy podow, zostawiajac te inne niz `Running` i `Succeeded`, a `== 1` wybiera tylko aktywna faze. Pomaga znalezc pody w stanach problematycznych, np. `Pending` lub `Failed`.

**Linia 239**
```promql
increase(kube_pod_container_status_restarts_total[1h]) > 0
```
`increase(...[1h])` liczy, o ile wzrosl licznik restartow w ostatniej godzinie. `> 0` zostawia kontenery, ktore zrestartowaly sie przynajmniej raz.

## 2.3-custom-metrics.md

**Linie 287-289**
```promql
items_processed_total
```
Pokazuje surowy licznik przetworzonych elementow. Jako counter rosnie w czasie i zwykle ma etykiety opisujace status.

**Linie 293-295**
```promql
sum by (status) (items_processed_total)
```
Sumuje licznik osobno dla kazdego statusu. Wynik odpowiada na pytanie: ile elementow zakonczono kazdym statusem.

**Linie 299-303**
```promql
sum(items_processed_total{status="success"})
/
sum(items_processed_total)
```
Liczba sukcesow podzielona przez liczbe wszystkich przetworzonych elementow. Wynik jest ulamek od 0 do 1.

**Linie 307-309**
```promql
sum by (status) (rate(items_processed_total[5m]))
```
Pokazuje tempo przetwarzania elementow na sekunde z podzialem po statusie.

**Linie 313-315**
```promql
sum by (category) (rate(endpoint_hits_total[5m]))
```
Pokazuje tempo wywolan endpointow z podzialem po biznesowej kategorii, a nie po samym URL-u.

**Linie 321-323**
```promql
processing_queue_depth
```
To gauge, czyli aktualna wartosc. Pokazuje obecna dlugosc kolejki przetwarzania.

**Linie 327-329**
```promql
system_health_score
```
Pokazuje aktualny wynik zdrowia systemu. Gauge moze rosnac i malec.

**Linie 333-335**
```promql
avg_over_time(system_health_score[10m])
```
Liczy srednia wartosc `system_health_score` z ostatnich 10 minut. Wygladza krotkie skoki.

**Linie 341-345, 501-505**
```promql
histogram_quantile(0.95,
  sum by (le) (rate(item_processing_duration_seconds_bucket[5m]))
)
```
Liczy p95 czasu przetwarzania elementu. Odpowiada na pytanie: ponizej jakiego czasu miesci sie 95% operacji.

**Linie 349-353**
```promql
histogram_quantile(0.50,
  sum by (le) (rate(item_processing_duration_seconds_bucket[5m]))
)
```
Liczy mediane czasu przetwarzania. Polowa operacji jest szybsza od tej wartosci, a polowa wolniejsza.

**Linie 357-362**
```promql
sum(rate(item_processing_duration_seconds_bucket{le="1"}[5m]))
/
sum(rate(item_processing_duration_seconds_bucket{le="+Inf"}[5m]))
* 100
```
Porownuje tempo operacji mieszczacych sie w 1 sekundzie z tempem wszystkich operacji. `+Inf` oznacza koszyk zawierajacy wszystkie obserwacje.

**Linie 373-378 oraz 460-465**
```promql
sum(rate(items_processed_total{status="success"}[5m]))
/
sum(rate(items_processed_total{status!="not_found"}[5m]))
* 100
```
Liczy procent udanych przetworzen, wykluczajac `not_found` z mianownika. To pasuje do SLO, w ktorym brak elementu jest bledem klienta, a nie awaria uslugi.

**Linie 384-389**
```promql
sum(rate(item_processing_duration_seconds_bucket{le="2"}[5m]))
/
sum(rate(item_processing_duration_seconds_bucket{le="+Inf"}[5m]))
* 100
```
Liczy procent operacji zakonczonych w czasie do 2 sekund. To typowy sposob sprawdzania SLO latency opartego o histogram.

**Linie 394-396**
```promql
system_health_score >= 80
```
Porownuje aktualny health score z progiem. Wynik jest prawdziwy, gdy metryka ma wartosc co najmniej 80.

**Linie 402-404**
```promql
processing_queue_depth < 20
```
Sprawdza, czy aktualna kolejka ma mniej niz 20 elementow. Nadaje sie do alertu lub panelu statusowego.

**Linie 418-420**
```promql
sum(rate(http_requests_total{status="5xx"}[5m]))
```
Pokazuje laczne tempo bledow HTTP 500 na sekunde. To metryka techniczna aplikacji.

**Linie 424-426**
```promql
sum(rate(items_processed_total{status="failed"}[5m]))
```
Pokazuje tempo biznesowych niepowodzen przetwarzania. Porownanie z HTTP 500 pomaga znalezc korelacje miedzy awariami API a logika biznesowa.

**Linie 434-438**
```promql
histogram_quantile(0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket{handler="/items/{item_id}/process"}[5m]))
)
```
Liczy p95 czasu odpowiedzi HTTP dla endpointu przetwarzania. Filtr `handler="..."` ogranicza histogram do jednej trasy.

**Linie 442-446**
```promql
histogram_quantile(0.95,
  sum by (le) (rate(item_processing_duration_seconds_bucket[5m]))
)
```
Liczy p95 samego czasu logiki biznesowej. Roznica wzgledem p95 HTTP pokazuje narzut warstwy HTTP i infrastruktury.

**Linie 476-478**
```promql
processing_queue_depth
```
Panel z aktualna dlugoscia kolejki. Najlepiej sprawdza sie jako Stat, bo istotna jest biezaca wartosc.

**Linie 488-490**
```promql
system_health_score
```
Panel z aktualnym wynikiem zdrowia systemu w skali 0-100.

**Linie 535-537**
```promql
sum(rate(counter{status="success"}[5m])) / sum(rate(counter[5m]))
```
Ogólny wzorzec na success rate z licznika. Licznik sukcesow dzielony jest przez licznik wszystkich zdarzen.

**Linie 541-543**
```promql
histogram_quantile(0.95, sum by (le) (rate(histogram_bucket[5m])))
```
Ogólny wzorzec liczenia percentyla z histogramu. `sum by (le)` zachowuje granice koszykow.

**Linie 547-549**
```promql
sum(rate(histogram_bucket{le="THRESHOLD"}[5m])) / sum(rate(histogram_bucket{le="+Inf"}[5m]))
```
Ogólny wzorzec na procent obserwacji pod progiem. Koszyk progu jest dzielony przez koszyk `+Inf`, czyli wszystkie obserwacje.

## 3.1-advanced-dashboard.md

**Linia 50**
```logql
{app="your-api"} |~ "$search"
```
Wybiera logi aplikacji po etykiecie `app` i filtruje je regexem z dashboardowej zmiennej `$search`. Uzytkownik moze zmieniac wyszukiwanie bez edycji zapytania.

**Linia 54**
```promql
kube_deployment_status_replicas_available{deployment="your-api"}
```
Pokazuje aktualna liczbe dostepnych replik deploymentu `your-api`. To bezposredni odczyt metryki typu gauge.

**Linia 58**
```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job="your-api"}[5m])) by (le))
```
Liczy p95 latency dla zadania `your-api`. `rate` oblicza tempo zmian koszykow, `sum by (le)` laczy serie, a `histogram_quantile` wylicza percentyl.

**Linia 62**
```promql
sum(rate(http_requests_total{job="your-api",status!~"5.."}[5m])) / sum(rate(http_requests_total{job="your-api"}[5m]))
```
Liczy udzial zadan, ktore nie skonczyly sie bledem serwera `5xx`. Licznik nie-5xx jest dzielony przez licznik wszystkich zadan.

## 3.2-alerts.md

**Linie 36-38**
```promql
mysql_up
```
Pokazuje sygnal dostepnosci MySQL. Wartosc `1` oznacza, ze MySQL dziala, a `0` oznacza problem, dlatego ta metryka dobrze nadaje sie do alertu.
