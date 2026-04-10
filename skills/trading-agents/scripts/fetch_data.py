#!/usr/bin/env python3
"""
TradingAgents Data Fetcher - Kogub aktsia andmed yfinance'ist.
Ei vaja API võtmeid. Väljastab JSON formaadis andmepaketi.
"""
import json
import sys
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("ERROR: yfinance ja pandas peavad olema installeeritud.")
    print("Käivita: pip install yfinance pandas stockstats --break-system-packages")
    sys.exit(1)


def fetch_stock_data(symbol: str, end_date: str, lookback_days: int = 90) -> dict:
    """Kogu kõik aktsia andmed ühte paketti."""
    result = {"symbol": symbol, "date": end_date, "errors": []}

    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    start_dt = end_dt - timedelta(days=lookback_days)
    start_date = start_dt.strftime("%Y-%m-%d")

    ticker = yf.Ticker(symbol)

    # 1. OHLCV hinnaandmed
    try:
        hist = ticker.history(start=start_date, end=end_date, auto_adjust=False)
        if hist.empty:
            # Try with one extra day
            hist = ticker.history(start=start_date, end=(end_dt + timedelta(days=1)).strftime("%Y-%m-%d"), auto_adjust=False)
        if not hist.empty:
            hist.index = hist.index.strftime("%Y-%m-%d")
            # Last 30 days for summary, full for indicators
            recent = hist.tail(30)
            result["price_data"] = {
                "latest_close": round(float(recent["Close"].iloc[-1]), 2),
                "latest_date": recent.index[-1],
                "period_high": round(float(recent["High"].max()), 2),
                "period_low": round(float(recent["Low"].min()), 2),
                "avg_volume": int(recent["Volume"].mean()),
                "price_change_30d_pct": round(
                    float((recent["Close"].iloc[-1] / recent["Close"].iloc[0] - 1) * 100), 2
                ),
                "last_5_days": [
                    {
                        "date": d,
                        "open": round(float(row["Open"]), 2),
                        "high": round(float(row["High"]), 2),
                        "low": round(float(row["Low"]), 2),
                        "close": round(float(row["Close"]), 2),
                        "volume": int(row["Volume"]),
                    }
                    for d, row in recent.tail(5).iterrows()
                ],
            }

            # 2. TECHNICAL INDICATORS
            try:
                from stockstats import StockDataFrame
                sdf = StockDataFrame.retype(hist.copy())
                indicators = {}

                # RSI
                try:
                    rsi = sdf["rsi_14"]
                    indicators["rsi_14"] = round(float(rsi.iloc[-1]), 2)
                except:
                    pass

                # MACD
                try:
                    indicators["macd"] = round(float(sdf["macd"].iloc[-1]), 4)
                    indicators["macd_signal"] = round(float(sdf["macds"].iloc[-1]), 4)
                    indicators["macd_histogram"] = round(float(sdf["macdh"].iloc[-1]), 4)
                except:
                    pass

                # Bollinger Bands
                try:
                    indicators["boll_upper"] = round(float(sdf["boll_ub"].iloc[-1]), 2)
                    indicators["boll_middle"] = round(float(sdf["boll"].iloc[-1]), 2)
                    indicators["boll_lower"] = round(float(sdf["boll_lb"].iloc[-1]), 2)
                except:
                    pass

                # ATR
                try:
                    indicators["atr_14"] = round(float(sdf["atr_14"].iloc[-1]), 2)
                except:
                    pass

                # SMA
                try:
                    close = hist["Close"]
                    if len(close) >= 50:
                        indicators["sma_50"] = round(float(close.rolling(50).mean().iloc[-1]), 2)
                    if len(close) >= 200:
                        indicators["sma_200"] = round(float(close.rolling(200).mean().iloc[-1]), 2)
                    indicators["ema_10"] = round(float(close.ewm(span=10).mean().iloc[-1]), 2)
                except:
                    pass

                result["technical_indicators"] = indicators
            except ImportError:
                result["errors"].append("stockstats not installed, skipping technical indicators")
            except Exception as e:
                result["errors"].append(f"Technical indicators error: {str(e)}")
        else:
            result["errors"].append("No price data available")
    except Exception as e:
        result["errors"].append(f"Price data error: {str(e)}")

    # 3. FUNDAMENTAALSED ANDMED
    try:
        info = ticker.info
        fundamentals = {}
        fields = [
            "shortName", "sector", "industry", "marketCap", "trailingPE",
            "forwardPE", "pegRatio", "priceToBook", "trailingEps", "forwardEps",
            "dividendYield", "beta", "fiftyTwoWeekHigh", "fiftyTwoWeekLow",
            "fiftyDayAverage", "twoHundredDayAverage", "totalRevenue",
            "grossProfits", "ebitda", "netIncomeToCommon", "profitMargins",
            "operatingMargins", "returnOnEquity", "returnOnAssets",
            "debtToEquity", "currentRatio", "bookValue", "freeCashflow",
            "revenueGrowth", "earningsGrowth", "targetMeanPrice",
            "recommendationKey", "numberOfAnalystOpinions",
        ]
        for f in fields:
            if f in info and info[f] is not None:
                fundamentals[f] = info[f]
        result["fundamentals"] = fundamentals
    except Exception as e:
        result["errors"].append(f"Fundamentals error: {str(e)}")

    # 4. FINANTSARUANDED (viimane kvartal)
    try:
        bs = ticker.quarterly_balance_sheet
        if bs is not None and not bs.empty:
            latest_bs = bs.iloc[:, 0]
            result["balance_sheet"] = {
                str(k): round(float(v), 0) if pd.notna(v) else None
                for k, v in latest_bs.items()
            }
            result["balance_sheet"]["_period"] = str(bs.columns[0].strftime("%Y-%m-%d") if hasattr(bs.columns[0], 'strftime') else bs.columns[0])
    except Exception as e:
        result["errors"].append(f"Balance sheet error: {str(e)}")

    try:
        cf = ticker.quarterly_cashflow
        if cf is not None and not cf.empty:
            latest_cf = cf.iloc[:, 0]
            result["cashflow"] = {
                str(k): round(float(v), 0) if pd.notna(v) else None
                for k, v in latest_cf.items()
            }
    except Exception as e:
        result["errors"].append(f"Cashflow error: {str(e)}")

    try:
        inc = ticker.quarterly_income_stmt
        if inc is not None and not inc.empty:
            latest_inc = inc.iloc[:, 0]
            result["income_statement"] = {
                str(k): round(float(v), 0) if pd.notna(v) else None
                for k, v in latest_inc.items()
            }
    except Exception as e:
        result["errors"].append(f"Income statement error: {str(e)}")

    # 5. UUDISED
    try:
        news = ticker.news
        if news:
            result["news"] = [
                {
                    "title": n.get("title", ""),
                    "publisher": n.get("publisher", ""),
                    "link": n.get("link", ""),
                    "published": n.get("providerPublishTime", ""),
                    "type": n.get("type", ""),
                }
                for n in news[:15]
            ]
        else:
            result["news"] = []
    except Exception as e:
        result["errors"].append(f"News error: {str(e)}")

    # 6. INSIDER TRANSACTIONS
    try:
        insiders = ticker.insider_transactions
        if insiders is not None and not insiders.empty:
            recent_ins = insiders.head(10)
            result["insider_transactions"] = recent_ins.to_dict("records")
    except Exception as e:
        result["errors"].append(f"Insider transactions error: {str(e)}")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kasutamine: python fetch_data.py TICKER [YYYY-MM-DD]")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    if len(sys.argv) >= 3:
        date = sys.argv[2]
    else:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    data = fetch_stock_data(symbol, date)
    print(json.dumps(data, indent=2, default=str))
