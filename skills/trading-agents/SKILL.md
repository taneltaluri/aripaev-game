---
name: trading-agents
description: "Multi-agent aktsiaanalüüs ja Weekly Trader mis teostab automaatseid tehinguid Lightyearis. Kasuta ALATI kui kasutaja mainib aktsiaid, kauplemist, investeerimist, aktsiaanalüüsi, tickerit (NVDA, AAPL, TSLA jne) koos analüüsi sooviga. Samuti: 'analüüsi aktsiat', 'kas peaks ostma', 'stock analysis', 'trading decision', 'aktsia soovitus', 'investeerimisotsus', 'bull vs bear', 'riskianalüüs', 'ostu/müügi soovitus', 'weekly trader', 'nädala tehing', 'lightyear', 'portfell', 'tehingute ajalugu', 'sandbox trade', 'sandbox tehing', 'paper trade', 'tee trade sandboxis', 'igapäevane monitooring', 'reede kokkuvõte'. Ei vaja API võtmeid - kasutab yfinance andmeid, Claude agente ja Claude in Chrome'i Lightyeari jaoks."
---

# TradingAgents - Multi-Agent Aktsiaanalüüs + Weekly Trader

Põhineb [TradingAgents](https://github.com/TauricResearch/TradingAgents) raamistikul. Claude mängib kõiki agentide rolle, yfinance annab reaalsed turuandmed. API võtmeid ei vaja.

## KOLM REŽIIMI

### Režiim A: Analüüs (algne)
Kasutaja küsib konkreetse aktsia analüüsi → täielik multi-agent analüüs.
Trigger: "analüüsi NVDA", "kas peaks ostma TSLA", "aktsia analüüs" + ticker

### Režiim B: Weekly Trader (päris tehingud)
Automaatne iganädalane kauplemissüsteem mis skaneerib turgu, valib parima võimaluse ja teostab tehingu Lightyearis.
Trigger: "weekly trader", "nädala tehing", "käivita trader", "mis aktsia osta", "lightyear tehing", "müü positsioon"

### Režiim C: Sandbox Trader (simuleeritud, Excelisse)
Simuleeritud kauplemisrežiim — tehinguid logitakse AINULT Excelisse, Lightyearis reaalseid tehinguid EI tehta. Sisaldab igapäevast monitooringut ja reede kokkuvõtet emailile.
Trigger: "tee trade sandboxis", "sandbox trade", "sandbox tehing", "paper trade", "simuleeritud tehing", "monitooring", "reede kokkuvõte"

---

## REŽIIM A: ANALÜÜS (Algne süsteem)

Analüüs järgib 5-etapilist protsessi:
1. **4 Analüütikut** (paralleelselt subagentidega) → andmepõhised raportid
2. **Bull vs Bear debatt** → vastanduvad argumendid
3. **Kaupleja otsus** → BUY/HOLD/SELL ettepanek
4. **Riskijuhtide debatt** (agressiivne vs konservatiivne vs neutraalne)
5. **Portfellijuht** → lõplik otsus (Buy/Overweight/Hold/Underweight/Sell)

### Samm 1: Sisend ja andmete kogumine

Küsi kasutajalt ticker (nt NVDA) ja valikuliselt kuupäev. Vaikimisi kasuta eilset kuupäeva.

Käivita andmete kogumine:

```bash
python3 <SKILL_DIR>/scripts/fetch_data.py TICKER YYYY-MM-DD
```

Asenda `<SKILL_DIR>` selle skilli tegeliku asukohaga (kasuta Glob tööriista et leida `trading-agents/scripts/fetch_data.py`). Timeout vähemalt 60000ms.

Kui `yfinance` pole installeeritud:
```bash
pip install yfinance pandas stockstats openpyxl --break-system-packages
```

### Samm 2: Käivita 4 analüütikut paralleelselt

Käivita **4 subagenti kõik korraga ühes sõnumis** (Agent tool), igal oma roll. Anna igale agendile kaasa kogutud andmed.

#### Agent 1: Turuanalüütik (Market Analyst)
```
Sa oled turuanalüütik. Analüüsi järgmisi tehnilisi andmeid aktsia {TICKER} kohta kuupäeval {DATE}.

ANDMED:
{price_data + technical_indicators sektsioon JSON-ist}

Ülesanne:
1. Vali kuni 8 kõige relevantsemad tehnilised indikaatorid ja selgita nende tähendust
2. Tuvasta trend (tõusev, langev, külgsuunas)
3. Tuvasta support/resistance tasemed
4. Hinda volatiilsust (ATR, Bollinger ribad)
5. Anna tehniline hinnang: BULLISH / BEARISH / NEUTRAL koos põhjendusega

Väljasta Markdown raport tabeliga peamiste leidude kohta.
```

#### Agent 2: Fundamentaalanalüütik (Fundamentals Analyst)
```
Sa oled fundamentaalanalüütik. Analüüsi ettevõtte {TICKER} finantse kuupäeval {DATE}.

ANDMED:
{fundamentals + balance_sheet + cashflow + income_statement sektsioonid JSON-ist}

Ülesanne:
1. Hinda ettevõtte finantsseisundit (kasumlikkus, võlatase, likviidsus)
2. Võrdle PE, PEG, P/B suhtarve sektori keskmistega
3. Analüüsi tulu kasvu ja kasumimarginaale
4. Hinda vaba rahavoogu ja dividendipoliitikat
5. Anna fundamentaalne hinnang: BULLISH / BEARISH / NEUTRAL

Väljasta Markdown raport tabeliga peamiste finantsmeetrikute kohta.
```

#### Agent 3: Uudisteamalüütik (News Analyst)
```
Sa oled uudisteamalüütik. Analüüsi värskeid uudiseid aktsia {TICKER} kohta kuupäeval {DATE}.

ANDMED:
{news sektsioon JSON-ist}

Ülesanne:
1. Kategoriseeri uudised: positiivsed, negatiivsed, neutraalsed
2. Tuvasta makromajanduslikud mõjud
3. Hinda sektori-spetsiifilisi arenguid
4. Märka ärirske või võimalusi uudistest
5. Anna uudistepõhine hinnang: BULLISH / BEARISH / NEUTRAL

Väljasta Markdown raport.
```

#### Agent 4: Sentimendiamalüütik (Sentiment Analyst)
```
Sa oled sentimendiamalüütik. Analüüsi avalikku sentimenti ja insaidertehinguid aktsia {TICKER} kohta kuupäeval {DATE}.

ANDMED:
{news + insider_transactions sektsioonid JSON-ist}

Ülesanne:
1. Hinda üldist turusentimenti uudiste põhjal
2. Analüüsi insaidertehinguid - kas juhtkond ostab või müüb
3. Tuvasta sentimendi muutuse suund (paranev/halvenev)
4. Hinda, kas aktsia on üle-/alahinnatud turusentimendi alusel
5. Anna sentimendihinnang: BULLISH / BEARISH / NEUTRAL

Väljasta Markdown raport.
```

### Samm 3: Bull vs Bear debatt

Kui kõik 4 analüütiku raportit on käes, käivita **2 subagenti korraga**:

#### Bull uurija
```
Sa oled Bull uurija - sinu ülesanne on ehitada tugevaim võimalik argument INVESTEERIMISE POOLT aktsiasse {TICKER}.

ANALÜÜTIKUTE RAPORTID:
{kõik 4 raportit}

Ehita oma argument nendel telgedel:
1. **Kasvupotentsiaal** - turuvõimalused, tulu prognoosid, skaleeritavus
2. **Konkurentsieelised** - unikaalsed tooted, bränd, turudomineerimine
3. **Positiivsed indikaatorid** - finantsnäitajad, sektoritrendid, head uudised
4. **Bear-argumentide ümberlükkamine** - miks pessimistlikud hirmud on üle paisutatud

Ole konkreetne, kasuta numbreid ja fakte raportidest. Väljasta tugev argument 300-500 sõna.
```

#### Bear uurija
```
Sa oled Bear uurija - sinu ülesanne on ehitada tugevaim võimalik argument INVESTEERIMISE VASTU aktsiasse {TICKER}.

ANALÜÜTIKUTE RAPORTID:
{kõik 4 raportit}

Ehita oma argument nendel telgedel:
1. **Riskid ja ohud** - turu küllastumine, finantssebastabiilsus, makromajanduslikud ohud
2. **Konkurentsinõrkused** - nõrk positsioneerimine, innovatsiooni langus, konkurentide ohud
3. **Negatiivsed indikaatorid** - halvad finantsnäitajad, negatiivsed trendid, halvad uudised
4. **Bull-argumentide ümberlükkamine** - miks optimism on liialdatud

Ole konkreetne, kasuta numbreid ja fakte raportidest. Väljasta tugev argument 300-500 sõna.
```

### Samm 4: Kaupleja otsus

Käivita **1 subagent**:

```
Sa oled kogenud kaupleja. Analüüsi kõiki andmeid ja tee investeerimisotsus aktsia {TICKER} kohta kuupäeval {DATE}.

ANALÜÜTIKUTE RAPORTID:
{kõik 4 raportit}

BULL ARGUMENT:
{bull uurija argument}

BEAR ARGUMENT:
{bear uurija argument}

Sinu ülesanne:
1. Kaalu mõlemaid pooli objektiivselt
2. Tuvasta tugevaimad argumendid mõlemalt poolt
3. Tee selge otsus: BUY, HOLD või SELL
4. Põhjenda oma otsust konkreetselt
5. Määra soovituslik positsioon ja ajahorisont

Lõpeta ALATI reaga: "LÕPLIK TEHINGUETTEPANEK: **BUY/HOLD/SELL**"
```

### Samm 5: Riskijuhtide debatt

Käivita **3 subagenti korraga**:

#### Agressiivne riskijuht
```
Sa oled agressiivne riskijuht. Hinda kaupleja ettepanekut aktsia {TICKER} kohta.
KAUPLEJA ETTEPANEK: {kaupleja otsus}
RAPORTID: {kõik 4 raportit}

Sinu vaatenurk: kõrge tootlus nõuab riski. Rõhuta võimalusi, mida ettevaatlikkus jätab kasutamata. Ole julge aga andmepõhine. 200-300 sõna.
```

#### Konservatiivne riskijuht
```
Sa oled konservatiivne riskijuht. Hinda kaupleja ettepanekut aktsia {TICKER} kohta.
KAUPLEJA ETTEPANEK: {kaupleja otsus}
RAPORTID: {kõik 4 raportit}

Sinu vaatenurk: kapitali kaitse on esmane. Tuvasta kõik riskid, halvimaima stsenaariumi analüüs. Soovita riskimaandamismeetmeid. 200-300 sõna.
```

#### Neutraalne riskijuht
```
Sa oled neutraalne riskijuht. Hinda kaupleja ettepanekut aktsia {TICKER} kohta.
KAUPLEJA ETTEPANEK: {kaupleja otsus}
RAPORTID: {kõik 4 raportit}

Sinu vaatenurk: tasakaalustatud. Kaalu nii riski kui tootlust, hinda risk/reward suhet. Paku kompromisslahendusi. 200-300 sõna.
```

### Samm 6: Portfellijuhi lõppotsus

Käivita **1 subagent**:

```
Sa oled portfellijuht. Tee lõplik investeerimisotsus aktsia {TICKER} kohta kuupäeval {DATE}.

KAUPLEJA ETTEPANEK:
{kaupleja otsus}

RISKIJUHTIDE DEBATT:
- Agressiivne: {agressiivne hinnang}
- Konservatiivne: {konservatiivne hinnang}
- Neutraalne: {neutraalne hinnang}

Tee oma otsus kasutades täpset skaalat:
- **Buy**: Tugev veendumus positsioonile sisenemiseks
- **Overweight**: Soosiv, järk-järguline positsiooni suurendamine
- **Hold**: Säilita positsioon, ei tegutse
- **Underweight**: Vähenda positsiooni, võta kasumit
- **Sell**: Välju positsioonist

Väljasta:
1. **REITING**: Buy/Overweight/Hold/Underweight/Sell
2. **KOKKUVÕTE**: Tegevuskava - sisenemissstrateegia, positsiooni suurus, riskitase, ajahorisont
3. **INVESTEERIMISTEES**: Detailne põhjendus, mis toetub debatile ja andmetele
```

### Samm 7: Tulemuste esitamine

Koosta kasutajale selge kokkuvõte:

1. Lõplik reiting ja otsus (portfellijuhilt)
2. Peamised argumendid poolt ja vastu
3. Riskihinnang
4. Soovituslik tegevuskava

Lisa ALATI hoiatus:
> ⚠️ **Hoiatus**: See analüüs on ainult hariduslikul ja uurimislikul eesmärgil. See ei ole finantsnõustamine. Ära tee reaalse rahaga kauplemisotsuseid ainult selle tööriista põhjal.

Valikuliselt salvesta raport Markdown-failina kasutaja workspace'i.

---

## REŽIIM B: WEEKLY TRADER (Päris tehingud Lightyearis)

### Ülevaade
Weekly Trader on automaatne kauplemissüsteem mis skaneerib turgu, valib parima võimaluse ja teostab tehingu Lightyearis.

Trigger: "weekly trader", "nädala tehing", "käivita trader", "mis aktsia osta", "lightyear tehing", "müü positsioon"

### Protsess
1. Kontrolli avatud positsioone (trade_journal.py exits)
2. Kui on müügisignaale → töötle need esmalt (müü Lightyearis läbi Claude in Chrome)
3. Skaneeri turgu uute võimaluste jaoks (screener.py)
4. Top 3 kandidaadile käivita Režiim A analüüs
5. Parima analüüsiskooriga aktsia kohta tee Lightyearis ostu tehing (Claude in Chrome)
6. Logi tehing trade_journal.py-sse
7. Genereeri Excel raport (generate_excel.py)

---

## REŽIIM C: SANDBOX TRADER (Simuleeritud, ainult Excelisse)

### Ülevaade
Sandbox Trader on **simuleeritud kauplemisrežiim** — kõik tehingud logitakse AINULT Excelisse, Lightyearis reaalseid tehinguid **EI tehta**. Eesmärk on jälgida strateegia tulemuslikkust ilma reaalse rahaga riskimata.

**OLULINE**: Kui kasutaja ütleb "tee trade sandboxis", siis:
- ÄRA ava Lightyeari
- ÄRA kasuta Claude in Chrome'i tehingute tegemiseks
- Logi kõik AINULT sandbox_tracker.py kaudu Excelisse

Trigger: "tee trade sandboxis", "sandbox trade", "sandbox tehing", "paper trade", "simuleeritud tehing"

### Sandbox Trade protsess

**Samm 1: Analüüs**
Käivita Režiim A täisanalüüs valitud aktsia(te)le (või screener.py kui ticker pole määratud).

**Samm 2: Otsus ja logimine**
Portfellijuhi lõppotsuse põhjal fikseeri sandbox-tehing:

```bash
# Installi vajalikud paketid kui puudu
pip install yfinance pandas openpyxl --break-system-packages

# Lisa sandbox ost
python3 <SKILL_DIR>/scripts/sandbox_tracker.py add_trade TICKER BUY SHARES PRICE AMOUNT_EUR "põhjus" SCORE

# Lisa sandbox müük
python3 <SKILL_DIR>/scripts/sandbox_tracker.py add_trade TICKER SELL SHARES PRICE AMOUNT_EUR "põhjus"
```

Asenda `<SKILL_DIR>` selle skilli tegeliku asukohaga. Hind võta yfinance'ist (reaalajas hind).

**Samm 3: Genereeri Excel**
```bash
python3 <SKILL_DIR>/scripts/sandbox_tracker.py generate_excel "/path/to/workspace/sandbox_portfell.xlsx"
```

Excel fail salvestatakse kasutaja workspace kausta. Fail sisaldab kõiki sheete (Dashboard, Tehingud, Price Tracking, Daily Snapshots, Weekly Summary, Analüüs, Seaded).

**Samm 4: Kinnita kasutajale**
Näita kokkuvõtet: mis tehti, mis hinnaga, miks. Anna link Excel failile.

### Igapäevane monitooring (scheduled task, E-R)

Scheduled task käivitab iga tööpäev (E-R) üks kord monitooringu. Protsess:

1. **Kontrolli avatud sandbox-positsioone ja hetkehindu**:
   ```bash
   python3 <SKILL_DIR>/scripts/sandbox_tracker.py check_prices
   ```
   See tagastab JSON-i avatud positsioonide ja nende hetkeseisuga.

2. **Fikseeri hetkehinnad** Excelisse (Price Tracking sheet):
   ```bash
   python3 <SKILL_DIR>/scripts/sandbox_tracker.py log_daily_prices
   ```

3. **Hinda kas on vaja sekkuda**:
   - Kas mõni positsioon on saavutanud kasumi sihtmärgi (+10%)? → Sandbox SELL
   - Kas mõni positsioon on stop-loss tasemel (-7%)? → Sandbox SELL
   - Kas turul on uus hea võimalus? → Käivita screener + analüüs → Sandbox BUY
   - Kui tehakse sandbox-tehing, logi see kohe (add_trade)

4. **Salvesta päeva snapshot**:
   ```bash
   python3 <SKILL_DIR>/scripts/sandbox_tracker.py save_daily_snapshot
   ```

5. **Uuenda Excel**:
   ```bash
   python3 <SKILL_DIR>/scripts/sandbox_tracker.py generate_excel "/path/to/workspace/sandbox_portfell.xlsx"
   ```

### Reede kokkuvõte (email)

Igal reedel õhtul (scheduled task) genereeri nädala kokkuvõte ja saada emailile:

1. **Kogu nädala andmed**:
   ```bash
   python3 <SKILL_DIR>/scripts/sandbox_tracker.py weekly_summary
   ```

2. **Koosta email kokkuvõte** (saada <YOUR_EMAIL>):
   - Nädala tehingud (ostud, müügid) tabelina
   - Avatud positsioonide seis (ticker, ostuhind, praegune hind, muutus %)
   - Nädala kasum/kahjum kokku (€ ja %)
   - Portfelli koguväärtus
   - Top performer ja worst performer
   - Järgmise nädala vaade (kas midagi müüa/osta)

3. **Saatmine**: Kasuta Gmail MCP-d:
   - gmail_create_draft → saada emailile
   - Teema: "Sandbox Trader nädala kokkuvõte DD.MM - DD.MM.YYYY"

4. **Salvesta Excelisse**: Lisa nädala kokkuvõte Weekly Summary sheeti

### Sandbox konfiguratsioon

Vaikimisi seaded (muudetavad):
- **max_trade_eur**: 500 (max summa ühe tehingu kohta)
- **target_profit_pct**: 10 (kasumi sihtmärk %)
- **stop_loss_pct**: -7 (stop-loss %)
- **max_open_positions**: 5 (max avatud positsioonid)
- **risk_level**: medium

Seadeid saab muuta:
```bash
python3 <SKILL_DIR>/scripts/sandbox_tracker.py set_config max_trade_eur 750
```

### Sandbox Excel struktuur

Fail: `sandbox_portfell.xlsx` kasutaja workspace kaustas

**Sheet 1: Dashboard** — koondvaade
- Avatud positsioonid koos hetkehindu ja P&L-iga
- Kogustatistika (tehingud, win rate, kogukasum)
- Portfelli koguväärtus

**Sheet 2: Tehingud** — kõik sandbox-tehingud (BUY/SELL) detailselt
- ID, kuupäev, ticker, tehing, aktsiad, hind, summa, skoor, põhjus, staatus, P&L

**Sheet 3: Price Tracking** — igapäevased hinnad
- Kuupäev, ticker, hind, muutus päevaga, muutus ostuhinnast

**Sheet 4: Daily Snapshots** — portfelli väärtus iga päev
- Kuupäev, avatud positsioonide arv, portfelli väärtus, päeva P&L, kumulatiivne P&L

**Sheet 5: Weekly Summary** — nädala kokkuvõtted
- Nädal, tehingute arv, ostud, müügid, nädala P&L, kogu P&L, win rate

**Sheet 6: Analüüs** — graafikud
- Kumulatiivne kasumi graafik
- Per-aktsia performance
- Win rate trend

**Sheet 7: Seaded** — sandbox konfiguratsioon
