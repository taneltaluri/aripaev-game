---
taskId: aripaev-weekly-reflection
description: Reede õhtune Äripäev mängu nädala refleksioon ja FinMem mälu uuendus
cronExpression: 0 18 * * 5
---

Käivita aripaev-trader nädala refleksiooni protokoll (FinMem-style memory update).

Samm-sammult:
1. Claude in Chrome MCP kaudu ava https://www.aripaev.ee/investeerimismang/ ja loe:
   - Meie portfelli jooksev seis (portfell <PORTFOLIO_ID>): positsioon edetabelis, portfelli väärtus, nädala tootlus
   - Kontrolli AI liiga staatust — veendu, et portfell on AI liigas
   - Top 10 edetabel nii SEB liigas kui AI liigas
2. Arvuta nädala tulemus:
   - Meie nädala %
   - Benchmark: S&P 500 nädala %
   - AI liiga top 10 keskmine nädala %
   - Meie alpha vs AI liiga top 10
3. Analüüs — mis töötas, mis ei töötanud?
4. Kirjuta refleksioon: <STOCK_TRADER_DIR>/trade_memory.md
   Lisa sektsioon: "## Nädal [kuupäev]"
5. Valmista ette esmaspäeva rebalansi hüpoteesid (2-3 varianti)
6. Saada kasutajale lühike kokkuvõte (3-5 lauset)
