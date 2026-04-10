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

- **`/aripaev-setup`** — ühe klikiga setup. Küsib Äripäev kasutajanime ja portfelli nime, liitub AI liigaga, loob 3 scheduled task'i, seadistab kliendi kausta.

**Scheduled task mallid (`scheduled-tasks/`):**

| Task | Aeg | Mis teeb |
|---|---|---|
| `aripaev-weekly-rebalance` | E 9:05 EET | Täielik rebalance enne 10:00 order-täitumist |
| `aripaev-daily-check` | iga päev 18:09 EET | Monitooring + emergency rebalance kriitilise catalysti korral |
| `aripaev-weekly-reflection` | R 18:06 EET | Nädala kokkuvõte + hüpoteesid esmaspäevaks |

---

## Eeltingimused

1. **Claude Code** või **Cowork** Claude desktop'is
2. **Claude in Chrome MCP** extension (vajalik aripaev.ee-ga suhtlemiseks) — [installijuhend](https://www.anthropic.com/news/claude-for-chrome)
3. **scheduled-tasks MCP** (Claude Code'is vaikimisi olemas)
4. **Python 3** + `yfinance pandas stockstats openpyxl` (trading-agents skilli jaoks):
   ```bash
   pip install yfinance pandas stockstats openpyxl --break-system-packages
   ```
5. **Konto aripaev.ee investeerimismängus** (https://www.aripaev.ee/investeerimismang/) ja vähemalt üks loodud portfell

---

## Installimine

Vali endale sobiv variant. **Variant 2 (zip allalaadimine)** on kõige lihtsam kui sa pole git-iga sõber.

### Variant 1: Claude Code plugin install (kõige kiirem)

Claude Code / Cowork vestluses kirjuta:

```
/plugin install github:taneltaluri/aripaev-game
```

See laeb plugina automaatselt alla ja installib. Edasi mine [Esmane seadistamine](#esmane-seadistamine) juurde.

### Variant 2: Lae alla ZIP fail ja drag-drop Claude Desktop'i 🖱️

**Samm 1 — lae plugin alla:**

1. Mine releases lehele: **https://github.com/taneltaluri/aripaev-game/releases/latest**
2. Otsi üles "Assets" sektsioon kerides allapoole
3. Kliki failil **`aripaev-game.plugin`** (või `aripaev-game-v2.plugin`) — see laeb alla `Downloads` kausta
4. **Alternatiivselt** kogu repo ZIP-ina: kliki ülal rohelisel **"Code" → "Download ZIP"** nupul repo pealehel https://github.com/taneltaluri/aripaev-game

**Samm 2 — installi Claude Desktop'i:**

1. **Ava Claude Desktop rakendus** (mitte brauser — päris app)
2. Ava File Explorer ja leia allalaetud `aripaev-game.plugin` fail (tavaliselt `C:\Users\<sinu_nimi>\Downloads\`)
3. **Haara hiirega failist kinni** (vasak nupp all) ja **lohista see Claude Desktop aknasse** (ükskõik millise avatud vestluse peale)
4. Lase nupp lahti — Claude Desktop tunneb `.plugin` faili ära ja kuvab installi dialoogi
5. Kliki **"Install"** kinnituseks

**Kui drag-drop ei tööta:**

1. Claude Desktop → Settings (⚙️) → **Plugins**
2. Kliki **"Install from file"** nuppu
3. Navigeeri allalaetud `.plugin` faili juurde ja vali see

**Kui laadisid alla ZIP faili kogu repost:**

1. Paki ZIP lahti (paremklikk → "Extract All...")
2. Kopeeri `aripaev-game-main` kaust siia: `C:\Users\<sinu_nimi>\.claude\plugins\aripaev-game` (loo `.claude\plugins` kaust kui pole)
3. Taaskäivita Claude Desktop

### Variant 3: Git clone (arendajatele)

```bash
git clone https://github.com/taneltaluri/aripaev-game.git ~/.claude/plugins/aripaev-game
```

Windows PowerShell:
```powershell
git clone https://github.com/taneltaluri/aripaev-game.git "$env:USERPROFILE\.claude\plugins\aripaev-game"
```

---

## Esmane seadistamine

Pärast installimist käivita Claude Code / Cowork vestluses:

```
/aripaev-setup
```

Setup skript küsib sinult:

1. **Äripäev kasutajanimi** — sama millega logid sisse aripaev.ee-sse
2. **Portfelli nimi** — sinu mängu portfelli nimi (nt "Minu AI bot")
3. **Stock trader kaust** — kus hoitakse `trade_memory.md` ja `daily_log.md` (vaikimisi Windows: `C:\Users\<sinu_nimi>\OneDrive\Documents\Claude\Projects\stock trader`)
4. Kas tasks peavad algul **enabled** või **disabled** olema

Edasi skript automaatselt:

- Avab Chrome MCP-ga aripaev.ee
- Leiab sinu portfelli nime järgi nimekirjast
- **Liitub AI liigaga** sinu portfelliga
- Loeb praeguse positsiooni
- Loob **3 scheduled task'i** sinu arvutis (asendades placeholder'id sinu andmetega)
- Loob vajalikud failid stock trader kausta

Valmis! Järgmisest esmaspäevast alates mängib Claude AI liigas sinu eest.

> ⚠️ **Oluline**: Chrome MCP vajab, et oleksid aripaev.ee-sse **sisse logitud** selles Chrome'i sessioonis, kus MCP extension jookseb. Pea see sessioon avatuna, et scheduled taskid saaksid ise tellimusi esitada.

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

## Probleemide lahendamine

**"Plugin ei ilmu Claude Desktop'i peale installi"**
Taaskäivita Claude Desktop (sulge kõik aknad, ava uuesti).

**"/aripaev-setup ei tööta"**
Kontrolli, et sul on Claude in Chrome MCP extension installitud ja aripaev.ee avatud ning sisse logitud.

**"Scheduled taskid ei käivitu"**
Claude Desktop peab olema taustal käivitunud scheduled task'i ajal. Kontrolli ka, et aripaev.ee sessioon on aktiivne.

**"Portfelli ei leitud nime järgi"**
Veendu, et kasutad täpselt sama nime mis aripaev.ee-s. Tühikud ja suurtähed loevad.

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
