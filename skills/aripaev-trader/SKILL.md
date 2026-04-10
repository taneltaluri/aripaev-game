---
name: aripaev-trader
description: Äripäev investeerimismängu (aripaev.ee/investeerimismang) autonoomne kauplemissüsteem AI liiga jaoks. Kasuta kui kasutaja mainib Äripäev mängu, investeerimismängu, rebalanssi, AI liigat, SEB liigat või palub teha Äripäev mängu tehinguid. Sisaldab weekly rebalance strateegiat (70/20/10 raamistik), daily emergency check protokoll ja weekly reflection FinMem-style mälu uuenduse. Eeldab Claude in Chrome MCP-d aripaev.ee lehega suhtlemiseks.
---

# Äripäev Trader — Autonoomne investeerimismängu agent

Äripäev/Swedbank investeerimismängu (https://www.aripaev.ee/investeerimismang/) autonoomne kauplemissüsteem **AI liiga** jaoks — liiga, kus AI agendid võistlevad omavahel. See skill ei küsi kinnitust — teostab tehinguid ise, eesmärgiga **VÕITA** mäng.

## Kontekst

- **Mäng**: https://www.aripaev.ee/investeerimismang/
- **Portfelli ID**: `<PORTFOLIO_ID>` (asenda setup käigus oma ID-ga)
- **Rebalanss URL**: `https://www.aripaev.ee/investeerimismang/rebalansseeri?portfell=<PORTFOLIO_ID>`
- **Edetabelid**:
  - **AI liiga** (peamine): Liigad → AI liiga — seal võistleme teiste AI agentidega
  - SEB liiga (sekundaarne): Liigad → SEB liiga → `/liigas/13`
- **Liigaga liitumine**: Setupi ajal ja ka esimesel rebalansil kontrolli, kas portfell on **AI liigas** registreeritud. Kui ei ole, liitu: Liigad → AI liiga → "Liitu liigaga" nupp.
- **Reeglid**: min 5 aktsiat, max 25% aktsia kohta, no shorts, no leverage
- **Orderid täituvad**: 10:00 EET

## Failid (kliendi kausta)

- `trade_memory.md` — hüpoteesid, nädala refleksioonid, praegune positsioon
- `daily_log.md` — igapäevane portfelli logi

Vaikimisi asukoht: `C:\Users\<USER>\OneDrive\Documents\Claude\Projects\stock trader\` (Windows) või `~/Documents/Claude/Projects/stock-trader/` (macOS/Linux).

---

## STRATEEGIA — 70/20/10 raamistik

- **70% meie agentide analüüs** — sõltumatu bull/bear debate, momentum, technicals, katalüsaatorid. Peamine eelis.
- **20% winner-kopeerimine** — top edetabeli portfellide mustrid (ainult kinnituseks).
- **10% Trump alpha** — Trumpi viimase nädala sõnavõtud → konkreetsed kiired trade'id.

**Miks nii?** Winner-kopeerimine paneb meid 1 sammu maha. Agentide iseseisev analüüs annab EDUMAA — reageerime enne kui teised edetabelit kopeerima hakkavad.

### Trump alpha loogika (10%)

Trump teeb regulaarselt järske pöördeid (tariifid, tehingud, ähvardused, positiivsed tveedid), mis liigutavad aktsiaid. Kui signaal on selge, anna 25% positsioon (üks aktsia = kogu 10% slot).

Näited:
- "Tariffs on semiconductors" → US chipmakers
- "Deal with Saudi/Gulf states" → Raytheon/LMT/GD
- "Big Beautiful Bill" / deficit → banks (JPM, BAC, GS)
- "AI investment package" → NVDA/MSFT
- "Made in America" → US manufacturers
- Kriitika konkreetse firma suhtes → väldi seda aktsiat

---

## REŽIIM A — Weekly Rebalance (esmaspäeva hommik)

Trigger: "äripäev rebalance", "esmaspäeva rebalanss", scheduled task `aripaev-weekly-rebalance`.

Samm-sammult:

1. Loe `trade_memory.md`
2. Claude in Chrome MCP kaudu ava aripaev.ee/investeerimismang:
   - Meie portfelli jooksev seis + positsioon edetabelis
   - **Kontrolli AI liiga staatust** — kui portfell ei ole AI liigas, liitu kohe (Liigad → AI liiga → Liitu liigaga)
   - Top 10 edetabel **nii SEB liigas kui AI liigas** + nende portfellid
3. Käivita **paralleelselt 3 subagenti** (general-purpose):
   - **Subagent A — 70% osa**: Iseseisev aktsiaanalüüs. yfinance andmed. 6–8 kandidaati: momentum, RSI, volumeen, earnings catalyst, sektor-rotatsioon. Bull/Bear debate. TOP 3–5 aktsiat koos kaaludega (kokku 70%).
   - **Subagent B — 20% osa**: Top 5 edetabeli portfellid (AI liiga prioriteet). Mis aktsiad korduvad? 1–2 aktsiat (kokku 20%).
   - **Subagent C — 10% osa**: Trump alpha skaneer. WebSearch viimase 7 päeva. 0–1 aktsia (0% kui signaali pole, 25% kui tugev).
4. **Sünteesi otsus ise**:
   - 70/20/10 raamistik
   - Min 5 aktsiat, max 25% igaüks
   - Eelista kontsentratsiooni
5. **Teosta tehingud Chrome MCP kaudu** rebalanss URL-il:
   - Eemalda/lisa aktsiaid
   - Sea kaalud ARIA slider keyboard pattern'iga (ArrowRight/ArrowLeft = 1%)
   - Verify JS: `[...document.querySelectorAll('[role="slider"]')].map((s,i)=>({i,value:s.getAttribute('aria-valuenow')}))`
   - Summa = 100%
   - Salvesta muudatused, oota "Muudatused salvestatud"
6. **Logi** `trade_memory.md`-sse:
   - Agentide analüüs (70%)
   - Winner-kopeerimine (20%)
   - Trump alpha (10%)
7. Uuenda scheduled task `aripaev-weekly-rebalance` promptis "Praegune positsioon" rida (`update_scheduled_task`).
8. Notifikatsioon: "✅ Weekly rebalance tehtud. AI liiga positsioon: X/Y."

### Tehnilised märkused

- Edetabelid: Liigad → AI liiga või SEB liiga
- Slider keyboard: `javascript_tool action:"keyboard" text:"ArrowRight"`
- TSM ei ole stock pool'is
- Trump alpha search: `Trump [sektor/firma] site:truthsocial.com OR reuters.com OR bloomberg.com`

---

## REŽIIM B — Daily Check (igapäevane monitooring)

Trigger: "äripäev daily check", scheduled task `aripaev-daily-check`.

Eesmärk: kaitsta alpha'it AI liigas. **Ära küsi kinnitust**.

Samm-sammult:

1. Loe `trade_memory.md`
2. Claude in Chrome kaudu ava portfell `<PORTFOLIO_ID>`:
   - Kontrolli AI liiga staatust — liitu, kui pole
   - Jooksev väärtus, päeva %
   - Positsioon AI liiga edetabelis (võrdle eilse päevaga)
3. Iga holdingu kohta:
   - WebSearch: `[ticker] news today` + `[ticker] stock`
   - yfinance: päeva %, volume, 52w high/low
   - Catalyste: earnings, guidance, downgrade/upgrade, M&A, regulatory, product launch, CEO changes
4. AI liiga top 5 — kas nende portfellid muutusid
5. **Red flag hindamine**:
   - 🔴 **KRIITILINE**:
     - Holding langeb >7% päevas + negatiivne uudis
     - Major downgrade (2+ analüütikut)
     - Sektor-laiune shock >2 holdingut
     - AI liiga positsioon langeb >500 koha
   - 🟡 **HOIATUS**:
     - Holding −3 kuni −7% ilma põhjuseta
     - Üksik downgrade
     - Positsioon −200…−500
6. **Otsustamine**:
   - 🔴 → TEOSTA REBALANSS KOHE. Min 5 aktsiat, summa 100%. Logi. Notifikatsioon: "🚨 EMERGENCY REBALANCE"
   - 🟡 → logi ainult
   - OK → 2-rida staatus
7. **Logi ALATI** `daily_log.md`:
   ```
   [kuupäev] Portfell: €X (±Y%). AI liiga koht: Z. Holdings: [...]. Catalysts: [...]. Tegevus: [None/Rebalanss].
   ```

---

## REŽIIM C — Weekly Reflection (reede õhtu)

Trigger: "äripäev refleksioon", scheduled task `aripaev-weekly-reflection`.

FinMem-style mälu uuendus.

Samm-sammult:

1. Claude in Chrome kaudu ava portfell `<PORTFOLIO_ID>`:
   - Jooksev seis, AI liiga positsioon, portfelli väärtus, nädala tootlus
   - AI liiga ja SEB liiga top 10
2. **Arvuta nädala tulemus**:
   - Meie nädala %
   - S&P 500 nädala %
   - AI liiga top 10 keskmine
   - Alpha vs AI liiga top 10
3. **Analüüs** — mis töötas, mis ei töötanud?
4. **Kirjuta refleksioon** `trade_memory.md`-sse:
   ```
   ## Nädal [kuupäev]
   - Tulemus: ...
   - Tähelepanekud: ...
   - Plaan esmaspäevaks: ...
   ```
5. Valmista ette **esmaspäeva rebalansi hüpoteesid** (2–3 varianti)
6. Saada kasutajale lühike kokkuvõte (3–5 lauset)

---

## Installatsioon uuel arvutil

1. Installi plugin `aripaev-game`
2. Käivita `/aripaev-setup` — liitub AI liigaga, loob 3 scheduled task'i
3. Veendu, et Claude in Chrome MCP on seadistatud
4. Loo kliendi kaust ja `trade_memory.md` + `daily_log.md`
