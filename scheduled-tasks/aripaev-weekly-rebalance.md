---
taskId: aripaev-weekly-rebalance
description: Esmaspäeva hommikune Äripäev mängu rebalanss — täielikult autonoomne, teostab tehingud ise
cronExpression: 0 9 * * 1
---

Käivita aripaev-trader weekly rebalance protokoll — TÄIELIKULT AUTONOOMSELT. Eesmärk: VÕITA see mäng (AI liigas). Ära küsi kasutajalt kinnitust, tee kõik otsused ja tehingud ise.

Kontekst:
- Mäng: https://www.aripaev.ee/investeerimismang/ (Äripäev/Swedbank)
- Portfell ID: <PORTFOLIO_ID>, rebalanss URL: https://www.aripaev.ee/investeerimismang/rebalansseeri?portfell=<PORTFOLIO_ID>
- Liiga: AI liiga (peamine), SEB liiga (sekundaarne)
- Praegune positsioon (viimati salvestatud): <POSITION_PLACEHOLDER — setup täidab esimese jooksu ajal>
- Orderid täituvad 10:00 EET — sul on ~1h aega analüüsiks ja tehingute teostamiseks enne seda
- Reeglid: min 5 aktsiat, max 25% aktsia kohta, no shorts, no leverage

STRATEEGIA — 70/20/10 raamistik:
- **70% meie agentide analüüs**: sõltumatu bull/bear debate, momentum, technicals, katalüsaatorid
- **20% winner-kopeerimine**: top edetabeli portfellide mustrid (ainult kinnituseks)
- **10% Trump alpha**: Trumpi viimase nädala sõnavõtud → konkreetsed kiired trade'id

Näited Trump catalyst-idest:
- "Tariffs on semiconductors" → US chipmakers reaction
- "Deal with Saudi/Gulf states" → Raytheon/LMT/GD
- "Big Beautiful Bill" / deficit spending → banks (JPM, BAC, GS)
- "AI investment package" → NVDA/MSFT
- "Made in America" → US manufacturers
- Kriitika konkreetse firma suhtes → väldi seda aktsiat

Samm-sammult:
1. Loe trade_memory.md kliendi kaustast (<STOCK_TRADER_DIR>/trade_memory.md)
2. Claude in Chrome MCP kaudu ava aripaev.ee/investeerimismang, loe:
   - Meie portfelli jooksev seis + positsioon edetabelis
   - **Kontrolli AI liiga**: Liigad → AI liiga. Kui portfell pole liigas, vajuta "Liitu liigaga".
   - Top 10 edetabel nii SEB liigas kui AI liigas + nende portfellid
3. Käivita paralleelselt 3 subagenti (general-purpose):
   a) Subagent A — **70%**: Iseseisev aktsiaanalüüs. Kasuta yfinance andmeid. Analüüsi 6-8 kandidaati: momentum (1W, 1M %), RSI, volumeen, earnings catalyst, sektor-rotatsioon. Bull/Bear debate. TOP 3-5 aktsiat koos kaaludega (kokku 70%).
   b) Subagent B — **20%**: Top 5 edetabeli portfellid. Mis aktsiad korduvad? Kas kattuvad A-ga? 1-2 aktsiat (kokku 20%).
   c) Subagent C — **10%**: Trump alpha skaneer. WebSearch viimase 7 päeva Trump sõnavõtud. 0-1 aktsia (0% kui pole signaali, 25% kui tugev).
4. Sünteesi otsus ise. Min 5 aktsiat, max 25% igaüks. Eelista kontsentratsiooni.
5. Teosta tehingud Chrome MCP-ga rebalanss URL-il:
   - Eemalda/Lisa aktsiaid
   - Sea kaalud ARIA slider keyboard pattern'iga (ArrowRight/ArrowLeft = 1%)
   - Verify JS: [...document.querySelectorAll('[role="slider"]')].map((s,i)=>({i,value:s.getAttribute('aria-valuenow')}))
   - Summa = 100%
   - Salvesta muudatused, oota kinnitust
6. Logi trade_memory.md-sse:
   - Agentide analüüs (70%): [...]
   - Winner-kopeerimine (20%): [...]
   - Trump alpha (10%): [...]
7. Uuenda "Praegune positsioon" rida selles promptis update_scheduled_task-iga.
8. Notifikatsioon kasutajale: "✅ Weekly rebalance tehtud. AI liiga positsioon: X/Y."

TEHNILISED MÄRKUSED:
- Slider keyboard: javascript_tool action:"keyboard" text:"ArrowRight"
- TSM pole stock pool'is
- Trump alpha search: "Trump [sektor/firma] site:truthsocial.com OR reuters.com OR bloomberg.com"

OLULINE:
- ÄRA küsi kinnitust
- AI liigas on konkurents AI-d omavahel — ole julge, mitte konservatiivne
- Trump alpha: ainult kui signaal selge ja aktsia pole reageerinud
