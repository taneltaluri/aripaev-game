---
description: Seadista aripaev-game plugin uuel arvutil — liitu AI liigaga, loo 3 scheduled task'i automaatselt
---

Sa oled aripaev-game plugina setup skript. Ülesanne: seadistada kasutaja arvutis Äripäev investeerimismängu autonoomne kauplemissüsteem.

Samm-sammult:

1. **Küsi kasutajalt** `AskUserQuestion` abil:
   - Äripäev mängu portfelli ID (leitav aripaev.ee/investeerimismang URL-ist pärast sisselogimist)
   - Stock trader kaust kus hoitakse `trade_memory.md` ja `daily_log.md` (vaikimisi Windows: `C:\Users\<USER>\OneDrive\Documents\Claude\Projects\stock trader`)
   - Kas tasks peavad algul enabled olema või kõigepealt disabled (et kasutaja saaks üle vaadata)

2. **Kontrolli, et Claude in Chrome MCP on saadaval**. Kui ei ole, lõpeta setup ja ütle kasutajale, et see on eeltingimus.

3. **Ava aripaev.ee Chrome MCP kaudu**:
   - Navigeeri `https://www.aripaev.ee/investeerimismang/`
   - Veendu, et kasutaja on sisse logitud (kui ei, küsi kasutajalt käsitsi sisse logida ja oota)
   - **Liitu AI liigaga**: Mine Liigad → AI liiga → kui nähtav "Liitu liigaga" / "Registreeri portfell" nupp, kliki seda ja vali antud portfelli ID. Kinnita liitumine.
   - Verifitseeri, et portfell on nüüd AI liiga edetabelis nähtav.

4. **Loe kõik 3 scheduled task malli** selle plugina kaustast `scheduled-tasks/`:
   - `aripaev-weekly-rebalance.md`
   - `aripaev-daily-check.md`
   - `aripaev-weekly-reflection.md`

   Iga fail sisaldab YAML frontmatter'it (taskId, description, cronExpression) ja prompt'i sisu pärast frontmatter'it.

5. **Asenda placeholder'id** prompti sisus:
   - `<PORTFOLIO_ID>` → kasutaja antud portfelli ID
   - `<STOCK_TRADER_DIR>` → kasutaja antud stock trader kaust
   - `<POSITION_PLACEHOLDER ...>` → praegune portfelli positsioon aripaev.ee-st (loe Chrome MCP-ga), formaadis "TICKER 25%, TICKER 20%, ..."

6. **Loo tasks** `mcp__scheduled-tasks__create_scheduled_task` tool'iga:
   - taskId, description, cronExpression frontmatter'ist
   - prompt = asendatud sisu pärast frontmatter'it

7. **Kontrolli**, et kõik 3 task'i on loodud: `mcp__scheduled-tasks__list_scheduled_tasks`. Kui kasutaja valis disabled algul, kasuta `update_scheduled_task` et disable'da.

8. **Loo kliendi kaust**, kui pole: `<STOCK_TRADER_DIR>` ning sinna tühjad `trade_memory.md` ja `daily_log.md` failid.

9. **Meenuta kasutajale**:
   - Weekly rebalance käib esmaspäeviti 9:05 EET (enne 10:00 order-täitumist)
   - Daily check käib igal päeval 18:09 EET
   - Weekly reflection käib reedeti 18:06 EET
   - Scheduled task jookseb Chrome'i sessiooni all — pea aripaev.ee sessioon sisse loginuks
   - Täida `trade_memory.md` algne positsioon ja strateegia käsitsi või lase esimesel rebalance'il see teha

10. **Väljasta kokkuvõte** — AI liiga staatus + loodud tasks + nende järgmised käivitused + stock trader kausta asukoht.
