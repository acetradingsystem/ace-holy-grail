import streamlit as st
import requests
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ACE Holy Grail Scanner",
    page_icon="♠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

* { font-family: 'Syne', sans-serif; }
.stApp { background-color: #0a0a0f; }
#MainMenu, footer, header { visibility: hidden; }

.ace-header {
    background: linear-gradient(135deg, #0a0a0f 0%, #0d1a2e 50%, #0a0a0f 100%);
    border-bottom: 1px solid #1a2a4a;
    padding: 2rem 0 1.5rem 0;
    text-align: center;
    margin-bottom: 2rem;
}
.ace-logo {
    font-family: 'Space Mono', monospace;
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    background: linear-gradient(135deg, #FFD700, #FFA500, #FFD700);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite;
}
@keyframes shimmer { 0% { background-position: 0% } 100% { background-position: 200% } }
.ace-subtitle { color: #a0c8e8; font-size: 0.75rem; letter-spacing: 0.4em; text-transform: uppercase; margin-top: 0.3rem; }
.ace-tagline  { color: #4a6080; font-size: 0.65rem; letter-spacing: 0.3em; text-transform: uppercase; margin-top: 0.2rem; }

.rule-box {
    background: #0d1520;
    border: 1px solid #1a3a1a;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #6a90b0;
    line-height: 2;
}
.rule-highlight { color: #FFD700; font-weight: 700; }

.bull-header { color: #00d4aa; font-family: 'Space Mono', monospace; font-size: 0.75rem; letter-spacing: 0.3em; margin-bottom: 1rem; }
.bear-header { color: #ff6b6b; font-family: 'Space Mono', monospace; font-size: 0.75rem; letter-spacing: 0.3em; margin-bottom: 1rem; margin-top: 2rem; }

.bull-card {
    background: #0a1a0a;
    border: 1px solid #00d4aa;
    border-radius: 8px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 0 20px rgba(0,212,170,0.08);
}
.bear-card {
    background: #1a0a0a;
    border: 1px solid #ff6b6b;
    border-radius: 8px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 0 20px rgba(255,107,107,0.08);
}
.holy-grail-card {
    background: #0d1a0d;
    border: 2px solid #FFD700;
    border-radius: 8px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 0 30px rgba(255,215,0,0.15);
}

.coin-name { font-size: 1.2rem; font-weight: 700; font-family: 'Space Mono', monospace; }
.bull-name { color: #00d4aa; }
.bear-name { color: #ff6b6b; }
.gold-name { color: #FFD700; }

.metric-label { font-size: 0.58rem; letter-spacing: 0.2em; text-transform: uppercase; color: #6a90b0; margin-bottom: 2px; }
.metric-value { font-size: 0.88rem; font-family: 'Space Mono', monospace; color: #b0d0f0; }
.metric-green { color: #00d4aa; }
.metric-red   { color: #ff6b6b; }
.metric-gold  { color: #FFD700; }

.ma-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 3px;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    background: #FFD700;
    color: #000;
    margin-left: 8px;
}

.stat-box {
    background: #0d1520;
    border: 1px solid #1a2a3a;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}
.stat-number { font-size: 2rem; font-weight: 700; font-family: 'Space Mono', monospace; }
.stat-label  { font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase; color: #6a90b0; margin-top: 0.2rem; }

.no-results {
    text-align: center;
    padding: 3rem;
    color: #6a90b0;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    border: 1px dashed #1a2a3a;
    border-radius: 8px;
    line-height: 2.5;
}
.timestamp { font-family: 'Space Mono', monospace; font-size: 0.65rem; color: #4a6080; text-align: center; margin-bottom: 1.2rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ace-header">
<div class="ace-logo">♠ACE</div>
    <div class="ace-subtitle">Accumulation Computation Engine</div>
     <div class="ace-subtitle">Tight Consolidation Breakout</div>
    <div class="ace-subtitle">TSX · D1 Timeframe</div>
""", unsafe_allow_html=True)

# ── The Rule ───────────────────────────────────────────────────────────────────

""", unsafe_allow_html=True)

# ── Scanner Functions ──────────────────────────────────────────────────────────
def get_tsx_symbols():
    try:
        url = "https://www.tsx.com/json/company-directory/search/tsx/^*"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        data = r.json()
        excluded = ["etf","cdr","trust","fund","index","ishares","vanguard",
                    "horizons","debenture","warrant","bond","preferred","reit"]
        symbols = []
        for c in data.get("results", []):
            sym  = c.get("symbol","").strip()
            name = c.get("name","").lower()
            if not sym or "." in sym: continue
            if any(k in name for k in excluded): continue
            symbols.append(f"{sym}.TO")
        return symbols
    except:
        return ["SHOP.TO","BB.TO","LSPD.TO","NFI.TO","MRE.TO","TLRY.TO",
                "ATZ.TO","GIL.TO","DOL.TO","MRU.TO","WSP.TO","CAE.TO"]

def fetch_holy_grail(symbol):
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        hist   = ticker.history(period="120d")
        if hist.empty or len(hist) < 205:
            return None

        today     = hist.iloc[-1]
        prev      = hist.iloc[-11:-1]  # 10 days before today

        close     = float(today["Close"])
        vol_today = float(today["Volume"])
        t_open    = float(today["Open"])
        t_high    = float(today["High"])
        t_low     = float(today["Low"])

        if close < 5 or vol_today == 0:
            return None

        # Calculate MA20 and MA200
        ma20  = float(hist["Close"].iloc[-21:-1].mean())   # 20 day MA (excluding today)
        ma200 = float(hist["Close"].iloc[-201:-1].mean())  # 200 day MA (excluding today)

        # THREE FINGERS TIGHT — MA20 within 3% of MA200
        # Check that the narrow state has been present for at least 10 days
        ma_diff_pct = abs(ma20 - ma200) / ma200 * 100
        if ma_diff_pct > 3.0:
            return None

        # Verify narrow state persisted for 10 days (not just today)
        narrow_days = 0
        for i in range(2, 12):  # check last 10 days
            try:
                ma20_i  = float(hist["Close"].iloc[-(20+i):-(i)].mean())
                ma200_i = float(hist["Close"].iloc[-(200+i):-(i)].mean())
                diff_i  = abs(ma20_i - ma200_i) / ma200_i * 100
                if diff_i <= 3.0:
                    narrow_days += 1
            except: pass
        if narrow_days < 5:  # at least 5 of last 10 days must be tight
            return None

        # Volume checks
        avg_vol   = float(prev["Volume"].mean())
        vol_ratio = vol_today / avg_vol if avg_vol > 0 else 0
        if vol_today < 100_000 or vol_ratio < 3.0:
            return None

        # Candle body size
        body_pct  = abs(close - t_open) / close * 100
        if body_pct < 3.0:
            return None

        # Day range position
        day_range = t_high - t_low
        close_pos = (close - t_low) / day_range * 100 if day_range > 0 else 0

        # 10-day high/low
        high_10d  = float(prev["High"].max())
        low_10d   = float(prev["Low"].min())
        range_10d = high_10d - low_10d
        range_pct = range_10d / high_10d * 100 if high_10d > 0 else 0

        # Sector filter
        try:
            info     = ticker.info
            sector   = (info.get("sector","") or "").lower()
            industry = (info.get("industry","") or "").lower()
            excl_s   = ["basic materials","energy","utilities","real estate"]
            excl_i   = ["gold","silver","copper","mining","oil","gas","coal","uranium","etf","trust"]
            if any(s in sector   for s in excl_s): return None
            if any(s in industry for s in excl_i): return None
        except: pass

        # BULL ELEPHANT — breaks above 10d high, closes near high
        is_bull = (close > high_10d and
                   close > t_open and
                   close_pos >= 75.0)

        # BEAR ELEPHANT — breaks below 10d low, closes near low
        is_bear = (close < low_10d and
                   close < t_open and
                   close_pos <= 25.0)

        if not is_bull and not is_bear:
            return None

        direction  = "BULL" if is_bull else "BEAR"
        breakout   = (close - high_10d) / high_10d * 100 if is_bull else (low_10d - close) / low_10d * 100

        # Scoring
        # MA tightness (0-4)
        if ma_diff_pct < 0.5:   ma_score = 4
        elif ma_diff_pct < 1.0: ma_score = 3
        elif ma_diff_pct < 2.0: ma_score = 2
        else:                   ma_score = 1

        # Volume score (0-3)
        if vol_ratio >= 7:    vol_score = 3
        elif vol_ratio >= 5:  vol_score = 2
        else:                 vol_score = 1

        # Body score (0-2)
        if body_pct >= 5:     body_score = 2
        elif body_pct >= 3:   body_score = 1
        else:                 body_score = 0

        # Breakout score (0-2)
        if breakout >= 3:     bo_score = 2
        elif breakout >= 1:   bo_score = 1
        else:                 bo_score = 0

        total = ma_score + vol_score + body_score + bo_score

        return {
            "symbol":      symbol.replace(".TO",""),
            "direction":   direction,
            "score":       total,
            "ma_score":    ma_score,
            "vol_score":   vol_score,
            "body_score":  body_score,
            "bo_score":    bo_score,
            "close":       round(close, 2),
            "volume":      int(vol_today),
            "vol_ratio":   round(vol_ratio, 1),
            "body_pct":    round(body_pct, 1),
            "close_pos":   round(close_pos, 1),
            "ma20":        round(ma20, 2),
            "ma200":       round(ma200, 2),
            "ma_diff_pct": round(ma_diff_pct, 2),
            "high_10d":    round(high_10d, 2),
            "low_10d":     round(low_10d, 2),
            "range_pct":   round(range_pct, 2),
            "breakout_pct":round(breakout, 2),
        }
    except: return None

def run_holy_grail_scan():
    progress = st.progress(0, text="Fetching TSX symbol list from TMX...")
    symbols  = get_tsx_symbols()
    total    = len(symbols)
    progress.progress(10, text=f"Scanning {total} TSX stocks for Holy Grail setups (3-5 min)...")
    results  = []
    done     = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(fetch_holy_grail, s): s for s in symbols}
        for f in as_completed(futures):
            done += 1
            if done % 60 == 0:
                pct = 10 + int(done/total*85)
                progress.progress(pct, text=f"Progress: {done}/{total} | Holy Grail setups found: {len(results)}")
            try:
                r = f.result()
                if r: results.append(r)
            except: pass
    results.sort(key=lambda x: (-x["score"], -x["vol_ratio"]))
    progress.progress(100, text="Scan complete!")
    time.sleep(0.5)
    progress.empty()
    return results

def score_badge(score):
    if score >= 10: bg, fg = "#FFD700", "#000"
    elif score >= 8: bg, fg = "#00d4aa", "#000"
    elif score >= 6: bg, fg = "#4FC3F7", "#000"
    else: bg, fg = "#1a2a3a", "#6a90b0"
    return f'<span style="background:{bg};color:{fg};padding:2px 10px;border-radius:3px;font-family:Space Mono,monospace;font-weight:700;font-size:0.9rem">{score}</span>'

def display_results(results):
    bulls = [r for r in results if r["direction"] == "BULL"]
    bears = [r for r in results if r["direction"] == "BEAR"]
    holy  = [r for r in results if r["score"] >= 9]

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-number metric-gold">{len(holy)}</div><div class="stat-label">🏆 Holy Grail (9+)</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="stat-number metric-green">{len(bulls)}</div><div class="stat-label">🐘 Bull Elephants</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-box"><div class="stat-number metric-red">{len(bears)}</div><div class="stat-label">🐻 Bear Elephants</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-box"><div class="stat-number" style="color:#fff">{len(results)}</div><div class="stat-label">Total Setups</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    def render_card(r, card_class, name_class):
        direction_emoji = "🐘" if r["direction"] == "BULL" else "🐻"
        close_color = "metric-green" if r["direction"] == "BULL" else "metric-red"
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem">
                <span class="coin-name {name_class}">{direction_emoji} {r['symbol']}</span>
                <div style="display:flex;align-items:center;gap:0.5rem">
                    <span class="ma-badge">MA∆ {r['ma_diff_pct']}%</span>
                    {score_badge(r['score'])}
                </div>
            </div>
            <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:0.8rem;margin-bottom:0.8rem">
                <div><div class="metric-label">Price CAD</div><div class="metric-value {close_color}">${r['close']:,.2f}</div></div>
                <div><div class="metric-label">Volume</div><div class="metric-value">{r['volume']:,}</div></div>
                <div><div class="metric-label">Vol Surge</div><div class="metric-value metric-gold">{r['vol_ratio']}x</div></div>
                <div><div class="metric-label">Body %</div><div class="metric-value">{r['body_pct']}%</div></div>
                <div><div class="metric-label">Close Pos</div><div class="metric-value">{r['close_pos']}%</div></div>
                <div><div class="metric-label">Breakout</div><div class="metric-value {close_color}">+{r['breakout_pct']}%</div></div>
            </div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.8rem">
                <div><div class="metric-label">MA20</div><div class="metric-value">${r['ma20']}</div></div>
                <div><div class="metric-label">MA200</div><div class="metric-value">${r['ma200']}</div></div>
                <div><div class="metric-label">10d High</div><div class="metric-value">${r['high_10d']}</div></div>
                <div><div class="metric-label">10d Low</div><div class="metric-value">${r['low_10d']}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Holy Grail setups first
    if holy:
        st.markdown('<div class="bull-header">🏆 HOLY GRAIL SETUPS — SCORE 9+ — HIGHEST CONVICTION</div>', unsafe_allow_html=True)
        for r in holy:
            card = "holy-grail-card"
            name = "gold-name"
            render_card(r, card, name)

    # Bull Elephants
    regular_bulls = [r for r in bulls if r["score"] < 9]
    if bulls:
        st.markdown('<div class="bull-header">🐘 BULL ELEPHANTS — LONG SETUPS</div>', unsafe_allow_html=True)
        for r in (holy if not regular_bulls else regular_bulls):
            if r["direction"] == "BULL":
                render_card(r, "bull-card", "bull-name")

    if not bulls:
        st.markdown('<div style="color:#1a3a1a;font-family:Space Mono,monospace;font-size:0.75rem;text-align:center;padding:1rem;border:1px dashed #1a3a1a;border-radius:8px;margin-bottom:1rem">🐘 No Bull Elephant setups today</div>', unsafe_allow_html=True)

    # Bear Elephants
    if bears:
        st.markdown('<div class="bear-header">🐻 BEAR ELEPHANTS — SHORT SETUPS (Questrade Margin)</div>', unsafe_allow_html=True)
        for r in bears:
            render_card(r, "bear-card", "bear-name")
    else:
        st.markdown('<div style="color:#3a1a1a;font-family:Space Mono,monospace;font-size:0.75rem;text-align:center;padding:1rem;border:1px dashed #3a1a1a;border-radius:8px">🐻 No Bear Elephant setups today</div>', unsafe_allow_html=True)

    if not results:
        st.markdown("""
        <div class="no-results">
            NO HOLY GRAIL SETUPS TODAY<br><br>
            The three fingers are not tight enough on any TSX stock<br>
            OR no elephant bars fired from a tight MA state<br><br>
            This is the rarest and highest quality signal<br>
            Patience is the strategy<br><br>
            Best run after 4:00pm EST on trading days
        </div>""", unsafe_allow_html=True)

# ── Main ───────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run = st.button("▶  RUN HOLY GRAIL SCAN", type="primary", use_container_width=True)

if run:
    with st.spinner(""):
        results = run_holy_grail_scan()
        st.session_state["hg_results"] = results
        st.session_state["hg_time"]    = datetime.now().strftime("%Y-%m-%d %H:%M ET")

if "hg_results" in st.session_state:
    st.markdown(f'<div class="timestamp">Last scan: {st.session_state["hg_time"]}</div>', unsafe_allow_html=True)
    display_results(st.session_state["hg_results"])
else:
    st.markdown("""
    <div class="no-results">
        CLICK RUN HOLY GRAIL SCAN TO START<br><br>
        Scans 640+ TSX stocks<br>
        Detects when MA20 ≈ MA200 (Three Fingers Tight)<br>
        🐘 Bull Elephant — breaks UP from tight MAs<br>
        🐻 Bear Elephant — breaks DOWN from tight MAs<br><br>
        Best run after 4:00pm EST on trading days
    </div>""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding-top:1rem;border-top:1px solid #1a2a3a">
    <span style="font-family:Space Mono,monospace;font-size:0.6rem;letter-spacing:0.4em;color:#2a4060">
        ♠ ACE 1 TAB · TIGHT CONSOLIDATION BREAKOUT · TSX · D1 · NOT FINANCIAL ADVICE
    </span>
</div>
""", unsafe_allow_html=True)
