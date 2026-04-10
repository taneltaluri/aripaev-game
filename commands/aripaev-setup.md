---
description: Seadista aripaev-game plugin uuel arvutil — liitu AI liigaga, loo 3 scheduled task'i automaatselt
---

Sa oled aripaev-game plugina setup skript. Ülesanne: seadistada kasutaja arvutis Äripäev investeerimismängu autonoomne kauplemissüsteem.

Samm-sammult:

1. **Küsi kasutajalt** `AskUserQuestion` abil:
   - **Äripäev kasutajanimi** (sama millega logid sisse aripaev.ee-sse)
   - **Portfelli nimi** — sinu mängu portfelli **täpne nimi** nii nagu see on kirjas aripaev.ee "Minu portfellid" lehel (nt "Minu AI bot"). Tühikud ja suurtähed loevad.
   - **Stock trader kaust** kus hoitakse `trade_memory.md` ja `daily_log.md` (vaikimisi Windows: `C:\Users\<USER>\OneDrive\Documents\Claude\Projects\stock trader`)
   - Kas tasks peavad algul **enabled** olema või kõigepealt **disabled** (et kasutaja saaks üle vaadata)

   > ℹ️ **Miks mitte portfelli ID?** Äripäev mäng ei kuva portfelli ID-d kasutajale avalikult — ainult nimi on nähtav. Kogu automaatika töötab edaspidi nime põhjal (Chrome MCP navigeerib "Minu portfellid" lehele ja klikib õigel nimel).

2. **Kontrolli, et Claude in Chrome MCP on saadaval**. Kui ei ole, lõpeta setup ja ütle kasutajale, et see on eeltingimus.

3. **Ava aripaev.ee Chrome MCP kaudu ja kontrolli sisselogimist**:
   - Navigeeri `https://www.aripaev.ee/investeerimismang/`
   - Veendu, et kasutaja on sisse logitud antud **kasutajanimega**. Kui ei, küsi kasutajalt käsitsi sisse logida ja oota.
   - Mine **"Minu portfellid"** lehele ja kinnita, et kasutaja antud portfelli nimi `<PORTFOLIO_NAME>` on nimekirjas nähtav. Kui ei ole, lõpeta setup ja ütle kasutajale, et nimi peab täpselt vastama.
   - **Liitu AI liigaga**: Mine Liigad → AI liiga → kui nähtav "Liitu liigaga" / "Registreeri portfell" nupp, kliki seda ja vali antud portfell **nime järgi** (mitte ID järgi). Kinnita liitumine.
   - Verifitseeri, et portfell (nime järgi) on nüüd AI liiga edetabelis nähtav.

4. **Loe kõik 3 scheduled task malli** selle plugina kaustast `scheduled-tasks/`:
   - `aripaev-weekly-rebalance.md`
   - `aripaev-daily-check.md`
   - `aripaev-weekly-reflection.md`

   Iga fail sisaldab YAML frontmatter'it (taskId, description, cronExpression) ja prompt'i sisu pärast frontmatter'it.

5. **Asenda placeholder'id** prompti sisus:
   - `<PORTFOLIO_NAME>` → kasutaja antud portfelli nimi (täpselt nii nagu sisestatud)
   - `<ARIPAEV_USERNAME>` → kasutaja antud Äripäev kasutajanimi
   - `<STOCK_TRADER_DIR>` → kasutaja antud stock trader kaust
   - `<POSITION_PLACEHOLDER ...>` → praegune portfelli positsioon aripaev.ee-st (loe Chrome MCP-ga, navigeerides "Minu portfellid" → klikkides portfelli nimel), formaadis "TICKER 25%, TICKER 20%, ..."

6. **Loo tasks** `mcp__scheduled-tasks__create_scheduled_task` tool'iga:
   - taskId, description, cronExpression frontmatter'ist
   - prompt = asendatud sisu pärast frontmatter'it

7. **Kontrolli**, et kõik 3 task'i on loodud: `mcp__scheduled-tasks__list_scheduled_tasks`. Kui kasutaja valis disabled algul, kasuta `update_scheduled_task` et disable'da.

8. **Loo kliendi kaust**, kui pole: `<STOCK_TRADER_DIR>` ning sinna tühjad `trade_memory.md` ja `daily_log.md` failid.

9. **Meenuta kasutajale**:
   - Weekly rebalance käib esmaspäeviti 9:05 EET (enne 10:00 order-täitumist)
   - Daily check käib igal päeval 18:09 EET
   - Weekly reflection käib reedeti 18:06 EET
   - Scheduled task jookseb Chrome'i sessiooni all — pea aripaev.ee sessioon kasutajanimega `<ARIPAEV_USERNAME>` sisse loginuks
   - Kogu navigeerimine käib portfelli **nime** järgi, seega kui sa nimetad portfelli aripaev.ee-s ümber, peab ka scheduled taskides olevad `<PORTFOLIO_NAME>` väärtused uuendama
   - Täida `trade_memory.md` algne positsioon ja strateegia käsitsi või lase esimesel rebalance'il see teha

9.5. **SOOVITUS — jooksuta kõik tasks kohe "Run Now" abil**, et süsteem kohe bootstrap'iks ega peaks ootama esimese esmaspäevani:

   - Mine Claude Desktop → Settings → Scheduled Tasks
   - Leia `aripaev-weekly-rebalance` → kliki **"Run Now"** — see teeb esimese täieliku portfelli analüüsi ja rebalance'i, täidab `trade_memory.md` algse positsiooni ja strateegia
   - Seejärel kliki `aripaev-daily-check` → **"Run Now"** — see kinnitab, et daily monitoring loogika töötab
   - Lõpuks `aripaev-weekly-reflection` → **"Run Now"** — genereerib esimese reflektsiooni (kuigi see on parim pärast nädalat andmeid)

   **Miks kohe jooksutada:**
   - Bootstrap `trade_memory.md` päriselt esimese positsiooniga, mitte tühjalt
   - Kontrollid, et Chrome MCP on sisse logitud ja navigatsioon nime järgi töötab
   - Tuvastad vead kohe (nt vale portfelli nimi, Chrome sessioon aegunud), mitte esmaspäeva hommikul kui pole aega parandada
   - Saad esimese rebalance'i kohe käima ja ei kaota nädalat

10. **Väljasta kokkuvõte** — Äripäev kasutajanimi + portfelli nimi + AI liiga staatus + loodud tasks + nende järgmised käivitused + stock trader kausta asukoht.
