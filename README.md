# aripaev-game

Äripäev investeerimismängu (aripaev.ee/investeerimismang) **autonoomne AI kauplemissüsteem**, mis on ehitatud **AI liiga** jaoks — uus liiga, kus inimeste asemel võistlevad AI agendid.

Plugin sisaldab kogu loogikat — strateegiat, scheduled task mallid, multi-agent aktsiaanalüüsi ja automaatset setup'i — et sa saaksid paari minutiga panna oma Claude Code / Cowork instants'i iseseisvalt mängu mängima.

> ⚠️ **Disclaimer**: See on investeerimismäng, mitte päris kauplemine. Plugin EI tee päris raha tehinguid. Tulemused ei ole garanteeritud.

---

## Mis on sees?

**Skillid (`skills/`):**

- **`aripaev-trader`** — Äripäev mängu süda. 70/20/10 raamistik:
  - **70%** meie agentide iseseisev analüüs (Bull/Bear debate, technicals, catalysts)
  - **20%** winner-kopeerimine top edetabeli portfellidest
  - **10%** Trump alpha (kiired reaktsioonid Trumpi sõnavõttudele)

  Kolm režiimi: weekly rebalance, daily emergency check, weekly reflection (FinMem mälu uuendus).

- **`trading-agents`** — üldine multi-agent aktsiaanalüüs. 4 analüütikut paralleelselt (turg, fundamentaal, uudised, sotsiaalmeedia) → Bull/Bear debate → riskijuhtide debatt → portfellijuht. Põhineb [TradingAgents](https://github.com/TauricResearch/TradingAgents) raamistikul. Kasutab `yfinance`, API võtmeid ei vaja.

**Commands (`commands/`):**

- **`/aripaev-setup`** — ühe klikiga setup. Liitub AI liigaga, loob 3 scheduled task'i, küsib portfelli ID, seadistab kliendi kausta.

**Scheduled task mallid (`scheduled-tasks/`):**

| Task | Aeg | Mis teeb |
|---|---|---|
| `aripaev-weekly-rebalance` | E 9:05 EET | Täielik rebalance enne 10:00 order-täitumist |
| `aripaev-daily-check` | iga päev 18:09 EET | Monitooring + emergency rebalance kriitilise catalysti korral |
| `aripaev-weekly-reflection` | R 18:06 EET | Nädala kokkuvõte + hüpoteesid esmaspäevaks |

---

## Eeltingimused

1. **Claude Code** või **Cowork** Claude desktop'is
2. **Claude in Chrome MCP** extension (vajalik aripaev.ee-ga suhtlemiseks)
3. **scheduled-tasks MCP** (Claude Code'is vaikimisi olemas)
4. **Python 3** + `yfinance pandas stockstats openpyxl` (trading-agents skilli jaoks):
   ```bash
   pip install yfinance pandas stockstats openpyxl --break-system-packages
   ```
5. **Konto aripaev.ee investeerimismängus** (https://www.aripaev.ee/investeerimismang/)

---

## Installimine

### Variant 1: GitHub (soovitatud)

```bash
git clone https://github.com/<YOUR_GITHUB_USER>/aripaev-game.git ~/.claude/plugins/aripaev-game
```

Või kui kasutad Claude Code plugin manager'it:

```
/plugin install github:<YOUR_GITHUB_USER>/aripaev-game
```

### Variant 2: `.plugin` fail

1. Lae alla `aripaev-game.plugin` release'ist
2. Ava Claude Code / Cowork → Settings → Plugins → Install from file
3. Vali allalaetud `.plugin` fail

### Variant 3: Käsitsi

Kopeeri kogu `aripaev-game/` kaust oma Claude skillide / pluginate kausta.

---

## Esmane seadistamine

Pärast installimist käivita vestluses:

```
/aripaev-setup
```

Setup skript:

1. Küsib sinu **portfelli ID** (vaata aripaev.ee URL-ist pärast sisselogimist: `?portfell=XXXX`)
2. Küsib **stock trader kausta** asukohta (kus hoitakse `trade_memory.md` ja `daily_log.md`)
3. Avab Chrome MCP-ga aripaev.ee, **liitub AI liigaga** automaatselt
4. Loeb praeguse portfelli positsiooni
5. Loob **3 scheduled task'i** sinu arvutis (asendades placeholder'id sinu andmetega)
6. Loob vajalikud failid kliendi kausta

Valmis! Järgmisest esmaspäevast alates mängib Claude AI liigas sinu eest.

---

## Strateegia põhimõtted

**Miks 70/20/10, mitte lihtsalt top-kopeerimine?**

Winner-kopeerimine paneb sind alati 1 sammu maha — sa ostad siis, kui nemad on juba ostnud. Agentide iseseisev analüüs annab edumaa: reageerid turule enne, kui teised mängijad edetabelit kopeerima hakkavad.

**Miks Trump alpha?**

Trumpi sõnavõtud liigutavad konkreetseid aktsiaid momentaanselt (tariifid, tehingud, ähvardused, positiivsed tveedid). Enamik mängijaid ei reageeri kiiresti. Kui signaal on selge, anna sellele 25% positsioon.

**Miks autonoomne (ilma kinnituseta)?**

Äripäev mäng on zero-sum. Iga tund kriitilise catalysti ajal loeb. Keskmine ei võida — julge sekkumine võidab.

---

## Kaust-struktuur

```
aripaev-game/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── aripaev-trader/
│   │   └── SKILL.md
│   └── trading-agents/
│       ├── SKILL.md
│       └── scripts/
├── commands/
│   └── aripaev-setup.md
├── scheduled-tasks/
│   ├── aripaev-weekly-rebalance.md
│   ├── aripaev-daily-check.md
│   └── aripaev-weekly-reflection.md
├── README.md
├── LICENSE
└── .gitignore
```

---

## Kaastööline (contributing)

Pull requestid on tere tulnud. Mõned ideed:

- Täiendada Trump alpha detektorit (täiendavad uudiseallikad)
- Lisada teisi AI-fookusega katalüsaatoreid (FOMC, CPI, earnings calendars)
- Lisada backtesting tulemusi
- Portida teistele investeerimismängudele

---

## Litsents

MIT — vaata [LICENSE](LICENSE).

---

## Autor

Tanel Taluri
