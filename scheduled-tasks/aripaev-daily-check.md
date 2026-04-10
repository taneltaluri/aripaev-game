---
taskId: aripaev-daily-check
description: Igapäevane Äripäev portfelli monitooring — autonoomne, teeb emergency rebalance'i kui kriitiline catalyst
cronExpression: 0 18 * * *
---

Igapäevane Äripäev mängu portfelli monitooring — AUTONOOMNE INTERVENTSIOON kui vaja. Ära küsi kasutajalt kinnitust.

Kontekst:
- Mäng: https://www.aripaev.ee/investeerimismang/, portfell "<PORTFOLIO_NAME>"
- Rebalanss URL: https://www.aripaev.ee/investeerimismang/ (leia "Minu portfellid" alt portfell nimega "<PORTFOLIO_NAME>" ja ava see)
- Liiga: AI liiga (peamine)
- Praegune positsioon (viimati salvestatud): <POSITION_PLACEHOLDER — setup täidab esimese jooksu ajal>
- Orderid täituvad 10:00 EET
- Reeglid: min 5 aktsiat, max 25% aktsia kohta

Samm-sammult:
1. Loe aripaev-trader skilli (plugin: aripaev-game → skills/aripaev-trader/SKILL.md)
2. Loe trade_memory.md kliendi kaustast
3. Claude in Chrome MCP kaudu ava aripaev.ee/investeerimismang (portfell "<PORTFOLIO_NAME>"):
   - Kontrolli AI liiga staatust (Liigad → AI liiga). Kui portfell pole liigas, liitu kohe.
   - Portfelli jooksev väärtus ja päeva %
   - Positsioon AI liiga edetabelis (võrdle eilsega daily_log.md-st)
4. Kontrolli iga holdingut:
   - WebSearch: "[ticker] news today" + "[ticker] stock"
   - yfinance: päeva %, volume, 52w high/low
   - Catalyste: earnings, guidance, downgrade/upgrade, M&A, regulatory, product launch, CEO changes
5. Kontrolli AI liiga top 5 — kas nende portfellid muutusid
6. Red flag hindamine:
   - 🔴 KRIITILINE (kohene tegutsemine):
     * Holding langeb >7% päevas + negatiivne fundamentaalne uudis
     * Major downgrade (2+ analüütikut päevas)
     * Sektor-laiune shock >2 holdingut
     * AI liiga positsioon langeb >500 koha
   - 🟡 HOIATUS (logi ainult):
     * Holding -3 kuni -7% ilma põhjuseta
     * Üksik downgrade
     * Positsioon -200...-500
7. Otsustamine:
   - 🔴 → TEOSTA REBALANSS KOHE Chrome MCP-ga. Säilita min 5 aktsiat, summa 100%. Salvesta. Logi. Notifikatsioon: "🚨 EMERGENCY REBALANCE: [...]"
   - 🟡 → logi ainult
   - OK → 2-rida staatus + logi
8. Logi ALATI daily_log.md-sse (<STOCK_TRADER_DIR>/daily_log.md):
   "[kuupäev] Portfell: €X (±Y%). AI liiga koht: Z. Holdings: [iga ticker ±%]. Catalysts: [...]. Tegevus: [None/Rebalanss]."

OLULINE:
- ÄRA küsi kinnitust kriitilise otsuse puhul — iga tund maksab
- Eelista julget sekkumist passiivsusele
- Ära rebalansseeri iga päev — ainult tõelise kriisi korral
