#!/usr/bin/env python3
"""
Trade Journal - Tehingute ajalugu ja P&L jälgimine.
Salvestab kõik tehingud JSON faili ja arvutab statistika.
"""
import json
import sys
import os
from datetime import datetime

JOURNAL_DIR = os.path.expanduser("~/.trading-agents")
JOURNAL_FILE = os.path.join(JOURNAL_DIR, "trade_journal.json")
CONFIG_FILE = os.path.join(JOURNAL_DIR, "config.json")

DEFAULT_CONFIG = {
    "max_trade_eur": 500,
    "target_profit_pct": 10,
    "stop_loss_pct": -7,
    "max_open_positions": 5,
    "weekly_trade_day": "monday",
    "risk_level": "medium",
}


def ensure_dir():
    os.makedirs(JOURNAL_DIR, exist_ok=True)


def load_journal() -> dict:
    ensure_dir()
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r") as f:
            return json.load(f)
    return {"trades": [], "stats": {}}


def save_journal(journal: dict):
    ensure_dir()
    with open(JOURNAL_FILE, "w") as f:
        json.dump(journal, f, indent=2, default=str)


def load_config() -> dict:
    ensure_dir()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG


def save_config(config: dict):
    ensure_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def add_trade(symbol: str, action: str, shares: float, price: float,
              amount_eur: float, reason: str, analysis_score: int = 0) -> dict:
    """Lisa uus tehing journalisse."""
    journal = load_journal()

    trade = {
        "id": len(journal["trades"]) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "symbol": symbol,
        "action": action.upper(),
        "shares": shares,
        "price": price,
        "amount_eur": round(amount_eur, 2),
        "reason": reason,
        "analysis_score": analysis_score,
        "status": "OPEN" if action.upper() == "BUY" else "CLOSED",
        "profit_eur": None,
        "profit_pct": None,
    }

    if action.upper() == "SELL":
        for t in reversed(journal["trades"]):
            if t["symbol"] == symbol and t["action"] == "BUY" and t["status"] == "OPEN":
                buy_price = t["price"]
                profit_pct = round((price / buy_price - 1) * 100, 2)
                profit_eur = round(amount_eur - t["amount_eur"], 2)
                trade["profit_pct"] = profit_pct
                trade["profit_eur"] = profit_eur
                trade["buy_trade_id"] = t["id"]
                t["status"] = "CLOSED"
                t["closed_date"] = trade["date"]
                t["profit_pct"] = profit_pct
                t["profit_eur"] = profit_eur
                break

    journal["trades"].append(trade)
    journal["stats"] = calculate_stats(journal["trades"])
    save_journal(journal)
    return trade


def calculate_stats(trades: list) -> dict:
    """Arvuta üldine statistika."""
    closed = [t for t in trades if t.get("profit_pct") is not None]
    open_trades = [t for t in trades if t["action"] == "BUY" and t["status"] == "OPEN"]

    if not closed:
        return {
            "total_trades": len(trades),
            "open_positions": len(open_trades),
            "closed_trades": 0,
            "win_rate": 0,
            "total_profit_eur": 0,
            "avg_profit_pct": 0,
        }

    wins = [t for t in closed if t["profit_pct"] > 0]

    return {
        "total_trades": len(trades),
        "open_positions": len(open_trades),
        "open_symbols": [t["symbol"] for t in open_trades],
        "closed_trades": len(closed),
        "wins": len(wins),
        "losses": len(closed) - len(wins),
        "win_rate": round(len(wins) / len(closed) * 100, 1) if closed else 0,
        "total_profit_eur": round(sum(t.get("profit_eur", 0) for t in closed if t.get("profit_eur")), 2),
        "avg_profit_pct": round(sum(t["profit_pct"] for t in closed) / len(closed), 2),
        "best_trade_pct": round(max(t["profit_pct"] for t in closed), 2),
        "worst_trade_pct": round(min(t["profit_pct"] for t in closed), 2),
        "best_trade": max(closed, key=lambda t: t["profit_pct"])["symbol"],
        "worst_trade": min(closed, key=lambda t: t["profit_pct"])["symbol"],
    }


def get_open_positions() -> list:
    journal = load_journal()
    return [t for t in journal["trades"] if t["action"] == "BUY" and t["status"] == "OPEN"]


def get_portfolio_summary() -> dict:
    journal = load_journal()
    config = load_config()
    open_pos = get_open_positions()

    return {
        "config": config,
        "stats": journal.get("stats", {}),
        "open_positions": open_pos,
        "total_invested_eur": round(sum(t["amount_eur"] for t in open_pos), 2),
        "available_for_trade": round(config["max_trade_eur"], 2),
        "can_trade": len(open_pos) < config["max_open_positions"],
    }


def check_exit_signals(positions: list = None) -> list:
    """Kontrolli kas mõni avatud positsioon vajab müümist."""
    import yfinance as yf

    if positions is None:
        positions = get_open_positions()

    config = load_config()
    signals = []

    for pos in positions:
        try:
            ticker = yf.Ticker(pos["symbol"])
            current = ticker.info.get("currentPrice") or ticker.info.get("regularMarketPrice", 0)

            if current and pos["price"] > 0:
                pct_change = (current / pos["price"] - 1) * 100

                signal = {
                    "symbol": pos["symbol"],
                    "buy_price": pos["price"],
                    "current_price": round(current, 2),
                    "pct_change": round(pct_change, 2),
                    "buy_date": pos["date"],
                    "trade_id": pos["id"],
                }

                if pct_change >= config["target_profit_pct"]:
                    signal["action"] = "SELL_PROFIT"
                    signal["reason"] = f"Sihtmärk saavutatud! +{pct_change:.1f}%"
                elif pct_change <= config["stop_loss_pct"]:
                    signal["action"] = "SELL_STOPLOSS"
                    signal["reason"] = f"Stop-loss! {pct_change:.1f}%"
                else:
                    signal["action"] = "HOLD"
                    signal["reason"] = f"Hoiame ({pct_change:+.1f}%)"

                signals.append(signal)
        except Exception as e:
            signals.append({"symbol": pos["symbol"], "error": str(e), "action": "CHECK_MANUALLY"})

    return signals


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"

    if cmd == "summary":
        print(json.dumps(get_portfolio_summary(), indent=2, default=str))
    elif cmd == "exits":
        print(json.dumps(check_exit_signals(), indent=2, default=str))
    elif cmd == "open":
        print(json.dumps(get_open_positions(), indent=2, default=str))
    elif cmd == "stats":
        journal = load_journal()
        print(json.dumps(journal.get("stats", {}), indent=2))
    elif cmd == "config":
        print(json.dumps(load_config(), indent=2))
    elif cmd == "set":
        if len(sys.argv) >= 4:
            config = load_config()
            key, value = sys.argv[2], sys.argv[3]
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
            config[key] = value
            save_config(config)
            print(f"Config updated: {key} = {value}")
    elif cmd == "add_buy":
        if len(sys.argv) >= 7:
            trade = add_trade(sys.argv[2], "BUY", float(sys.argv[3]), float(sys.argv[4]),
                            float(sys.argv[5]), sys.argv[6], int(sys.argv[7]) if len(sys.argv) > 7 else 0)
            print(json.dumps(trade, indent=2, default=str))
    elif cmd == "add_sell":
        if len(sys.argv) >= 7:
            trade = add_trade(sys.argv[2], "SELL", float(sys.argv[3]), float(sys.argv[4]),
                            float(sys.argv[5]), sys.argv[6])
            print(json.dumps(trade, indent=2, default=str))
    elif cmd == "history":
        journal = load_journal()
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        print(json.dumps(journal["trades"][-n:], indent=2, default=str))
    else:
        print("Commands: summary, exits, open, stats, config, set, add_buy, add_sell, history")
