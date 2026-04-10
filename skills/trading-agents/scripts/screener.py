#!/usr/bin/env python3
"""
Weekly Trader Stock Screener - Skaneerib aktsiate univerumit ja leiab parimad võimalused.
Kasutab yfinance andmeid. Ei vaja API võtmeid.

Väljastab JSON nimekirja parimatest kandidaatidest koos skooriga.
"""
import json
import sys
import warnings
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

warnings.filterwarnings("ignore")

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("ERROR: yfinance ja pandas peavad olema installeeritud.")
    sys.exit(1)

# Populaarsed aktsiad ja ETF-id mis on Lightyearis saadaval
UNIVERSE = {
    "mega_cap": [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B",
        "JPM", "V", "UNH", "XOM", "MA", "JNJ", "PG", "HD", "COST", "ABBV",
        "CRM", "MRK", "AMD", "NFLX", "AVGO", "PEP", "KO", "LLY", "TMO",
        "ADBE", "ORCL", "WMT"
    ],
    "growth": [
        "PLTR", "SNOW", "CRWD", "PANW", "DDOG", "NET", "ZS", "MDB",
        "COIN", "SQ", "SHOP", "MELI", "SE", "RBLX", "UBER", "ABNB",
        "DASH", "ARM", "SMCI", "MSTR", "SOFI", "HOOD", "AFRM", "IONQ"
    ],
    "etf": [
        "SPY", "QQQ", "IWM", "DIA", "ARKK", "XLK", "XLF", "XLE",
        "XLV", "SOXX", "SMH", "VGT", "IBIT", "GLD", "SLV", "TLT",
        "VTI", "VOO", "SCHD", "VUG"
    ],
    "eu_popular": [
        "ASML", "SAP", "NVO", "LVMUY", "TM", "SONY", "BABA", "TSM"
    ]
}


def get_all_tickers():
    """Tagastab kõik tickerid."""
    all_tickers = []
    for category in UNIVERSE.values():
        all_tickers.extend(category)
    return list(set(all_tickers))


def quick_score(symbol: str, lookback_days: int = 60) -> dict:
    """
    Kiire skaneerimine ühe aktsia kohta.
    Tagastab skoori 0-100 ja põhjenduse.

    Skoorimise kriteeriumid (Weekly Trader - keskmise riskiga, 10%+ sihtmärk):
    - Momentum (20p): Lühiajaline hinnamuutus ja trend
    - Tehniline seisund (25p): RSI, MACD, Bollingeri positsioon
    - Fundamentaalid (20p): PE, kasvu kiirus, kasumlikkus
    - Volatiilsus (15p): Piisav volatiilsus 10% liikumiseks, aga mitte liiga kõrge
    - Analüütikute konsensus (10p): Sihtmärk vs praegune hind
    - Insaiderid (10p): Ostu/müügi signaalid
    """
    try:
        ticker = yf.Ticker(symbol)

        # Hinnaandmed
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=lookback_days)
        hist = ticker.history(start=start_dt.strftime("%Y-%m-%d"), end=end_dt.strftime("%Y-%m-%d"))

        if hist.empty or len(hist) < 20:
            return {"symbol": symbol, "score": 0, "error": "Insufficient data"}

        close = hist["Close"]
        volume = hist["Volume"]
        current_price = float(close.iloc[-1])

        score = 0
        reasons = []

        # === MOMENTUM (max 20p) ===
        pct_5d = float((close.iloc[-1] / close.iloc[-5] - 1) * 100) if len(close) >= 5 else 0
        pct_20d = float((close.iloc[-1] / close.iloc[-20] - 1) * 100) if len(close) >= 20 else 0

        # Eelistame "pullback after uptrend" mustrit
        if pct_20d > 5 and pct_5d < -2:
            score += 18
            reasons.append(f"Pullback uptrend'is (20d: +{pct_20d:.1f}%, 5d: {pct_5d:.1f}%)")
        elif pct_5d > 3 and pct_5d < 10:
            score += 14
            reasons.append(f"Tugev lühiajaline momentum (+{pct_5d:.1f}%)")
        elif pct_20d > 0 and pct_5d > -5:
            score += 8
            reasons.append(f"Positiivne trend (20d: +{pct_20d:.1f}%)")
        elif pct_5d < -10:
            score += 5
            reasons.append(f"Tugev ülemüük ({pct_5d:.1f}%) - bounce potentsiaal")

        # === TEHNILINE SEISUND (max 25p) ===
        try:
            # RSI arvutamine
            delta = close.diff()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = float(100 - (100 / (1 + rs.iloc[-1])))

            if 30 <= rsi <= 45:
                score += 20
                reasons.append(f"RSI oversold bounce zone ({rsi:.0f})")
            elif 55 <= rsi <= 70:
                score += 15
                reasons.append(f"RSI tugev trend ({rsi:.0f})")
            elif 45 < rsi < 55:
                score += 8
            elif rsi > 75:
                score += 2
                reasons.append(f"RSI overbought ({rsi:.0f}) - ettevaatust")
            elif rsi < 25:
                score += 12
                reasons.append(f"RSI ülimüüdud ({rsi:.0f})")

            # MACD crossover kontroll
            ema12 = close.ewm(span=12).mean()
            ema26 = close.ewm(span=26).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9).mean()
            hist_macd = macd - signal

            if float(hist_macd.iloc[-1]) > 0 and float(hist_macd.iloc[-2]) <= 0:
                score += 5
                reasons.append("MACD bullish crossover!")
            elif float(hist_macd.iloc[-1]) > 0:
                score += 2

        except Exception:
            pass

        # === FUNDAMENTAALID (max 20p) ===
        try:
            info = ticker.info
            forward_pe = info.get("forwardPE")
            revenue_growth = info.get("revenueGrowth")
            profit_margins = info.get("profitMargins")

            if forward_pe and 5 < forward_pe < 30:
                score += 8
                reasons.append(f"Forward PE mõistlik ({forward_pe:.1f})")
            elif forward_pe and forward_pe <= 5:
                score += 4

            if revenue_growth and revenue_growth > 0.2:
                score += 7
                reasons.append(f"Tugev tulu kasv ({revenue_growth*100:.0f}%)")
            elif revenue_growth and revenue_growth > 0.05:
                score += 4

            if profit_margins and profit_margins > 0.15:
                score += 5
                reasons.append(f"Hea kasumlikkus ({profit_margins*100:.0f}%)")

            # Analüütikute sihtmärk
            target = info.get("targetMeanPrice")
            if target and current_price > 0:
                upside = (target / current_price - 1) * 100
                if upside > 30:
                    score += 10
                    reasons.append(f"Analüütikute sihtmärk +{upside:.0f}% kõrgemal")
                elif upside > 15:
                    score += 7
                    reasons.append(f"Analüütikute sihtmärk +{upside:.0f}%")
                elif upside > 5:
                    score += 3

            # Beta - volatiilsus 10% liikumiseks
            beta = info.get("beta")
            if beta:
                if 1.2 <= beta <= 2.0:
                    score += 10
                    reasons.append(f"Hea volatiilsus (beta {beta:.1f})")
                elif 0.8 <= beta < 1.2:
                    score += 5
                elif 2.0 < beta <= 3.0:
                    score += 7
                    reasons.append(f"Kõrge volatiilsus (beta {beta:.1f})")
                elif beta > 3.0:
                    score += 3

        except Exception:
            pass

        # === KÄIVE (likviidsus kontroll) ===
        avg_volume = float(volume.tail(10).mean())
        if avg_volume < 500000:
            score = max(0, score - 15)
            reasons.append("Madal käive - likviidsusrisk!")

        return {
            "symbol": symbol,
            "score": min(score, 100),
            "price": round(current_price, 2),
            "pct_5d": round(pct_5d, 2),
            "pct_20d": round(pct_20d, 2) if len(close) >= 20 else None,
            "avg_volume": int(avg_volume),
            "reasons": reasons
        }

    except Exception as e:
        return {"symbol": symbol, "score": 0, "error": str(e)}


def scan_universe(top_n: int = 10, categories: list = None) -> list:
    """Skaneerib kogu aktsiate univerumi ja tagastab top N kandidaati."""

    if categories:
        tickers = []
        for cat in categories:
            tickers.extend(UNIVERSE.get(cat, []))
        tickers = list(set(tickers))
    else:
        tickers = get_all_tickers()

    print(f"Skaneerin {len(tickers)} aktsiat...", file=sys.stderr)

    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(quick_score, t): t for t in tickers}
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            if result.get("score", 0) > 0:
                results.append(result)
            if (i + 1) % 20 == 0:
                print(f"  ...{i+1}/{len(tickers)} valmis", file=sys.stderr)

    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return results[:top_n]


if __name__ == "__main__":
    top_n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    categories = sys.argv[2].split(",") if len(sys.argv) > 2 else None

    results = scan_universe(top_n=top_n, categories=categories)
    print(json.dumps(results, indent=2))
