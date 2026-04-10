# aripaev-game

Äripäev investeerimismängu (aripaev.ee/investeerimismang) **autonoomne AI kauplemissüsteem**, mis on ehitatud **AI liiga** jaoks — uus liiga, kus inimeste asemel võistlevad AI agendid.

Plugin sisaldab kogu loogikat — strateegiat, scheduled task mallid, multi-agent aktsiaanalüüsi ja automaatset setup'i — et sa saaksid paari minutiga panna oma Claude Code / Cowork instants'i iseseisvalt mängu mängima.

> 🔑 **Enne alustamist**: See plugin **eeldab, et sul on juba olemas konto ja vähemalt üks portfell** aadressil **https://www.aripaev.ee/investeerimismang/**. Kui sul veel kontot ei ole, registreeru seal kõigepealt, loo mängu portfell ja alles siis installi see plugin.

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

### Variant 2: Lae alla ZIP fail ja lisa Claude Desktop Plugins alla 📦

**Samm 1 — lae plugin ZIP-ina alla GitHubist:**

1. Mine repo pealehele: **https://github.com/taneltaluri/aripaev-game**
2. Kliki ülevalt roheline **"Code"** nupp
3. Rippmenüüst vali **"Download ZIP"**
4. Fail `aripaev-game-main.zip` salvestub `Downloads` kausta

**Alternatiiv:** kui eelistad valmis-pakitud `.plugin` faili, mine https://github.com/taneltaluri/aripaev-game/releases/latest ja lae "Assets" sektsiooni alt alla `aripaev-game.plugin` fail.

**Samm 2 — paki ZIP lahti** (ainult kui laadisid ZIP-i, mitte `.plugin` faili):

1. Ava File Explorer ja leia `aripaev-game-main.zip` `Downloads` kaustas
2. Tee paremklikk failil → **"Extract All..."** → "Extract"
3. Sa saad kausta nimega `aripaev-game-main` — sees peaks olema `.claude-plugin`, `skills`, `commands`, `scheduled-tasks` alamkaustad

**Samm 3 — lisa plugin Claude Desktop'i:**

1. **Ava Claude Desktop rakendus** (mitte brauserit — päris app)
2. Mine **Settings** (hammasratas ikoon ⚙️ all vasakus nurgas või File menüüst)
3. Vali vasakust menüüst **"Plugins"** (või "Extensions" olenevalt versioonist)
4. Kliki **"Install from file"** või **"Add plugin"** nupule
5. Navigeeri lahti pakitud `aripaev-game-main` kausta juurde (või otse `.plugin` faili juurde kui laadisid Release'ist)
6. Vali see ja kliki **"Open"** / **"Install"**
7. Claude Desktop kuvab kinnituse — kliki **"Install"** / **"Enable"**

**Samm 4 — taaskäivita Claude Desktop:**

Sulge Claude Desktop täielikult (kontrolli ka system tray'd, et app pole taustal) ja ava uuesti. Plugin peaks nüüd olema aktiivne.

**Samm 5 — kontrolli, et plugin töötab:**

Ava suvaline vestlus ja kirjuta `/aripaev-setup` — kui slash-käsk ilmub autocomplete'i, siis installimine õnnestus. Käivita see ja järgi juhiseid.

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

### 🚀 Soovituslik: jooksuta tasks kohe "Run Now" abil

**Ära oota esmaspäevani** — käivita kõik 3 scheduled task'i kohe peale setup'i, et süsteem bootstrap'iks õigesti:

1. Ava **Claude Desktop** → **Settings** → **Scheduled Tasks**
2. Leia `aripaev-weekly-rebalance` → kliki **"Run Now"** — esimene täielik analüüs + rebalance, täidab `trade_memory.md` algpositsiooniga
3. Seejärel `aripaev-daily-check` → **"Run Now"** — kontrollib, et monitooringu loogika töötab
4. Lõpuks `aripaev-weekly-reflection` → **"Run Now"** — esimene reflektsioon

**Miks kohe jooksutada:**

- **Bootstrap** — `trade_memory.md` saab päriselt esimese positsiooni ja strateegia, mitte tühjalt
- **Valideerimine** — kontrollid kohe, et Chrome MCP sessioon on OK, portfelli nimi vastab, AI liigaga liitumine õnnestus
- **Varajane veatuvastus** — kui midagi on valesti (nt vale portfelli nimi), avastad selle kohe, mitte esmaspäeva hommikul kell 9:05 kui order'eid hakatakse täitma
- **Ajavõit** — esimene nädal ei lähe kaduma, saad rebalance'i kohe käima

Pärast seda jätkavad tasks automaatselt oma cron'i järgi (E 9:05, iga päev 18:09, R 18:06 EET).

> ⚠️ **Oluline**: Chrome MCP vajab, et oleksid aripaev.ee-sse **sisse logitud** selles Chrome'i sessioonis, kus MCP extension jookseb. Pea see sessioon avatuna, et scheduled taskid saaksid ise tellimusi esitada.

---

## Strateegia põhimõtted

Plugin jagab portfelli kolme allokatsiooni: **70% agent-analüüs**, **20% winner-kopeerimine**, **10% Trump alpha**. Need ei ole juhuslikud numbrid — iga tükk põhineb erineval info-eelisel mis teistel mängijatel tõenäoliselt puudub.

### 70% — meie agentide iseseisev analüüs

See on portfelli selgroog ja tuleb otse `trading-agents` skillist. Iga nädal esmaspäeva hommikul (enne 10:00 order-täitumist) jooksutab weekly rebalance task terve multi-agent pipeline'i:

1. **4 analüütikut paralleelselt** `yfinance` andmetel:
   - **Market Analyst** — tehniline analüüs (RSI, MACD, MA crossovers, volume profile, support/resistance)
   - **Fundamentals Analyst** — P/E, P/S, earnings growth, margins, insider activity, short interest
   - **News Analyst** — viimase nädala uudiste sentiment, analyst upgrades/downgrades, guidance muudatused
   - **Social Media Analyst** — Reddit/Twitter sentiment, WSB trending, unusual options activity
2. **Bull vs Bear debate** — kaks agenti argumenteerivad iga kandidaadi kohta, teineteise väiteid ümber lükates
3. **Risk manager debate** — konservatiivne vs agressiivne riskijuht vaidlevad position sizing'u üle
4. **Portfolio manager** sünteesib kõik eelneva → lõplik kaalutud soovitus (ticker, % kaal, stop-loss, thesis)

**Miks see töötab mängus:** enamik mängijaid kopeerib edetabelit või reageerib eilsetele uudistele. Meie agendid jooksevad enne turu avanemist ja võtavad positsiooni *enne* kui hilised kopeerijad reageerida jõuavad. See on 1-2 päeva edumaa iga nädal.

### 20% — edukate mängijate kopeerimine (winner-copying)

Weekly rebalance task käib läbi **Äripäev mängu edetabeli top-10 portfellid** Chrome MCP kaudu (mäng näitab iga portfelli positsioone avalikult). Plugin otsib:

- **Mis aktsiaid hoiavad top-5 mängijad, keda meie agendid veel ei soovitanud?** — need on kandidaadid 20% kopia-ämbrisse
- **Milline mängija on kõige järjepidevalt tipus viimased 4+ nädalat?** — temalt kopeerime eelistatult (mitte ühekordsed edu-mängijad kes lihtsalt hot streak'il on)
- **Millised positsioonid on top-mängijate vahel ühised?** — consensus picks saavad suurema kaalu (nt kui 4/5 top-mängijat hoiavad NVDA-d, siis NVDA on tugev signaal)

**Oluline reegel:** me ei kopeeri pimesi. Kui meie agendid ütlesid konkreetse aktsia kohta Bear-case on tugev, siis me EI võta seda isegi kui top-mängijad hoiavad. Winner-copying täiendab agente, mitte ei asenda neid.

**Miks mitte 50% või 100% kopeerimine?** Kopeerimine on alati lagging indicator — kui sa näed edetabelis, et keegi on 3. kohal tänu NVDA-le, siis NVDA ralli on juba toimunud. 20% annab kontakti "turu tarkusega" ilma et kaotaksid meie agentide edumaa.

### 10% — Trump alpha (katalüsaator-reaktiivne ämber)

See on kõige väiksem aga kõige kõrgema oodatava tootlusega tükk. Mõte: Trumpi sõnavõtud liigutavad konkreetseid aktsiaid **minutitega**, mitte päevadega. Daily check task (iga päev 18:09 EET) ja weekly rebalance skanneerivad:

- **Truth Social ja X (Twitter) Trumpi postitused** — tariifid, tehingud, ettevõtte-spetsiifilised rünnakud/kiitused
- **Executive orders ja presidendi avaldused** — Valge Maja pressiteated
- **Sektori-level signaalid** — kui Trump ründab Hiinat → puuduta half-chip (Applied Materials, LRCX), kui kiidab Muski → TSLA long, kui ähvardab tariifidega autosid → GM/Ford short-kandidaadid

**Kuidas signaal muundub positsiooniks:**
- Selge single-stock signaal (nt "X company is a disaster") → kuni 10% short-positsioon (või cash)
- Selge positive signaal (nt kohtumine CEO'ga, positive tweet) → kuni 10% long
- Sektor-level signaal → 5% ETF positsioon (XLE, XLF, SOXX jne)
- Ebamäärane signaal → jätame vahele, cash 10%

**Miks see ämber eksisteerib:** enamik kauplejaid filtreerib Trumpi signaalid välja ("noise", "political"). Kuid Äripäev mängus on see puhas alpha — keegi teine ei reageeri kiiresti ja mäng on zero-sum. 10% kaaluga on ka halvimal juhul kaotus piiratud, aga heal juhul (2-3 korda nädalas) toob see üksi terve nädala tootluse.

### Miks autonoomne (ilma kinnituseta)?

Äripäev mäng on zero-sum — iga võidetud euro tuleb kelleltki teiselt ära. Kaks põhjust miks plugin käivitab tehingud ise, kinnitust küsimata:

1. **Ajaline edumaa** — kui catalyst tuleb öösel või tööpäeval keskel ja sa ootad, kuni inimene kinnitab, siis signaali väärtus on juba kaotatud. Scheduled task jookseb kohe kui cron tingimus täidetud.
2. **Psühholoogiline eelis** — inimesed kardavad väikese portfelliga agressiivseid liigutusi (25% ühte aktsiasse), aga mängus on just see julgus edu võti. Autonoomne süsteem järgib strateegiat distsiplineeritult, ilma et "äkki mitte" kahtlused sekkuks.

**Riskitaju:** kuna mäng EI ole päris raha, on see turvaline kontekst autonoomiaks. Sama süsteem päris rahaga vajaks human-in-the-loop kinnitust.

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
