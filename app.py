import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="PropIQ Commercial — CRE Analyzer",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

:root {
    --gold:    #D4A843;
    --gold-lt: #F0C96A;
    --dark:    #080C12;
    --surface: #0F141E;
    --card:    #141C28;
    --card2:   #1A2235;
    --border:  #243045;
    --text:    #E2E8F0;
    --muted:   #5A7090;
    --green:   #22C55E;
    --red:     #EF4444;
    --blue:    #3B82F6;
    --amber:   #F59E0B;
    --teal:    #14B8A6;
    --purple:  #A855F7;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--dark) !important;
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--text);
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stHeader"] { display: none !important; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1500px !important; }

.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 44px;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-lt) 50%, #FFFBE8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin-bottom: 2px;
}
.page-sub { color: var(--muted); font-size: 13px; margin-bottom: 28px; font-family: 'IBM Plex Mono', monospace; letter-spacing: 1px; text-transform: uppercase; }

.kpi-row { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.kpi-card {
    flex: 1; min-width: 150px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
    transition: all 0.2s;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: 0.4;
}
.kpi-card:hover { border-color: var(--gold); transform: translateY(-1px); box-shadow: 0 8px 24px rgba(0,0,0,0.4); }
.kpi-label { font-size: 10px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: var(--muted); margin-bottom: 8px; font-family: 'IBM Plex Mono', monospace; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 700; color: var(--text); line-height: 1; }
.kpi-value.positive { color: var(--green); }
.kpi-value.negative { color: var(--red); }
.kpi-value.warning  { color: var(--amber); }
.kpi-sub { font-size: 10px; color: var(--muted); margin-top: 6px; font-family: 'IBM Plex Mono', monospace; }
.kpi-icon { position: absolute; top: 14px; right: 14px; font-size: 18px; opacity: 0.2; }

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    margin: 28px 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 10px;
    letter-spacing: -0.3px;
}
.section-title span { color: var(--gold); }

.badge { display:inline-block; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600; font-family:'IBM Plex Mono',monospace; letter-spacing:0.5px; }
.badge-green  { background:rgba(34,197,94,0.12);  color:var(--green);  border:1px solid rgba(34,197,94,0.25); }
.badge-red    { background:rgba(239,68,68,0.12);   color:var(--red);    border:1px solid rgba(239,68,68,0.25); }
.badge-gold   { background:rgba(212,168,67,0.12);  color:var(--gold);   border:1px solid rgba(212,168,67,0.25); }
.badge-blue   { background:rgba(59,130,246,0.12);  color:var(--blue);   border:1px solid rgba(59,130,246,0.25); }
.badge-amber  { background:rgba(245,158,11,0.12);  color:var(--amber);  border:1px solid rgba(245,158,11,0.25); }
.badge-teal   { background:rgba(20,184,166,0.12);  color:var(--teal);   border:1px solid rgba(20,184,166,0.25); }

[data-testid="stTabs"] [role="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 500;
    color: var(--muted) !important;
    border-bottom: 2px solid transparent;
    padding: 8px 18px;
    letter-spacing: 0.5px;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom-color: var(--gold) !important;
}
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid var(--border);
    gap: 2px;
}

[data-testid="stNumberInput"] input, [data-testid="stTextInput"] input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}

[data-testid="stMetricValue"] { font-family: 'Syne', sans-serif; font-size: 22px !important; }
[data-testid="stMetricLabel"] { font-family: 'IBM Plex Mono', monospace; font-size: 11px !important; }
</style>
""", unsafe_allow_html=True)

# ── PLOTLY THEME ──────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(20,28,40,0.5)',
    font=dict(family='IBM Plex Sans', color='#5A7090', size=11),
    margin=dict(l=12, r=12, t=40, b=12),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0', size=11)),
    xaxis=dict(gridcolor='#243045', linecolor='#243045', zerolinecolor='#243045'),
    yaxis=dict(gridcolor='#243045', linecolor='#243045', zerolinecolor='#243045'),
)
C = dict(gold='#D4A843', gold_lt='#F0C96A', green='#22C55E', red='#EF4444',
         blue='#3B82F6', amber='#F59E0B', teal='#14B8A6', purple='#A855F7', orange='#F97316')


def hex_to_rgba(hex_color, alpha=0.08):
    """Safely convert a hex color string like #RRGGBB to rgba(r,g,b,alpha)."""
    h = hex_color.lstrip('#')
    r_val = int(h[0:2], 16)
    g_val = int(h[2:4], 16)
    b_val = int(h[4:6], 16)
    return f"rgba({r_val},{g_val},{b_val},{alpha})"


# ══════════════════════════════════════════════════════════════
# FINANCIAL FUNCTIONS
# ══════════════════════════════════════════════════════════════
def monthly_payment(principal, annual_rate_pct, term_months):
    r = annual_rate_pct / 1200
    if r == 0:
        return principal / term_months
    return float(principal) * (r * (1 + r) ** term_months) / ((1 + r) ** term_months - 1)


def calc_noi(rent, vacancy_pct, opex_ratio, annual_tax_pct, annual_ins_pct):
    eff = rent * (1 - vacancy_pct / 100)
    opex = eff * (opex_ratio / 100)
    tax_mo = rent * (annual_tax_pct / 100) / 12
    ins_mo = rent * (annual_ins_pct / 100) / 12
    return (eff - opex - tax_mo - ins_mo) * 12


def build_amortization(principal, annual_rate_pct, term_months):
    r = annual_rate_pct / 1200
    payment = monthly_payment(principal, annual_rate_pct, term_months)
    balance, cumint = principal, 0
    records = []
    for month in range(1, int(term_months) + 1):
        interest = balance * r
        principal_pd = payment - interest
        balance -= principal_pd
        cumint += interest
        records.append({
            'Month': month, 'Payment': round(payment, 2),
            'Principal': round(principal_pd, 2), 'Interest': round(interest, 2),
            'Balance': round(max(balance, 0), 2), 'Cumul. Interest': round(cumint, 2),
            'Equity': round(principal - max(balance, 0), 2)
        })
    return pd.DataFrame(records)


def full_analysis(price, rent, closing, loan, rate, term, vacancy,
                  opex_ratio, tax_pct, ins_pct, asset_type='warehouse'):
    payment = monthly_payment(loan, rate, term)
    down = price - loan
    cash_req = down + closing
    noi = calc_noi(rent, vacancy, opex_ratio, tax_pct, ins_pct)
    annual_debt = payment * 12
    annual_cf = noi - annual_debt
    cap_rate = (noi / price) * 100 if price > 0 else 0
    coc = (annual_cf / cash_req) * 100 if cash_req > 0 else 0
    dscr = noi / annual_debt if annual_debt > 0 else 0
    gross_yield = (rent * 12 / price) * 100 if price > 0 else 0
    grm = price / (rent * 12) if rent > 0 else 0
    noi_per_sf = noi / (price / 150) if price > 0 else 0
    return dict(
        payment=round(payment, 2), total_payments=round(payment * term, 2),
        total_interest=round(payment * term - loan, 2),
        cash_required=round(cash_req, 2), down_payment=round(down, 2),
        annual_debt=round(annual_debt, 2), noi=round(noi, 2),
        annual_cf=round(annual_cf, 2), monthly_cf=round(annual_cf / 12, 2),
        cap_rate=round(cap_rate, 2), coc=round(coc, 2), dscr=round(dscr, 3),
        gross_yield=round(gross_yield, 2), grm=round(grm, 2),
        ltv=round((loan / price) * 100, 1) if price > 0 else 0,
        noi_per_sf=round(noi_per_sf, 2),
    )


# ══════════════════════════════════════════════════════════════
# TENANT STRESS ENGINE
# ══════════════════════════════════════════════════════════════
def run_tenant_stress(tenants, base_rent, loan, rate, term, opex_pct,
                      reabsorption_months, downtime_months):
    payment = monthly_payment(loan, rate, term)
    records = []
    for scenario_name, scenario_vacancies in tenants.items():
        monthly_records = []
        for month in range(1, 61):
            yr = (month - 1) // 12 + 1
            active_tenants = []
            for t in scenario_vacancies:
                is_vacant = (month >= t['vacant_start'] and
                             month < t['vacant_start'] + t['vacant_months'])
                refilling = (month >= t['vacant_start'] + t['vacant_months'] and
                             month < t['vacant_start'] + t['vacant_months'] + reabsorption_months)
                if is_vacant:
                    active_tenants.append({'name': t['name'], 'rent': 0, 'status': 'VACANT'})
                elif refilling:
                    recovery_pct = (month - (t['vacant_start'] + t['vacant_months'])) / max(reabsorption_months, 1)
                    active_tenants.append(
                        {'name': t['name'], 'rent': t['rent'] * recovery_pct * 0.85, 'status': 'REFILLING'})
                else:
                    active_tenants.append({'name': t['name'], 'rent': t['rent'], 'status': 'OCCUPIED'})

            collected_rent = sum(t['rent'] for t in active_tenants)
            opex = collected_rent * (opex_pct / 100)
            noi_mo = collected_rent - opex
            cf_mo = noi_mo - payment
            occupancy = sum(1 for t in active_tenants if t['status'] == 'OCCUPIED') / len(active_tenants) * 100

            monthly_records.append({
                'Month': month, 'Year': yr,
                'Collected Rent': round(collected_rent, 0),
                'NOI': round(noi_mo, 0),
                'Cash Flow': round(cf_mo, 0),
                'Occupancy': round(occupancy, 1),
                'Debt Service': round(payment, 0),
                'Shortfall': round(max(-cf_mo, 0), 0),
                'Scenario': scenario_name
            })
        records.extend(monthly_records)
    return pd.DataFrame(records)


def breakeven_occupancy_commercial(payment, opex_pct, gross_rent):
    if gross_rent == 0:
        return 100
    net_per_unit = 1 - (opex_pct / 100)
    return (payment / (gross_rent * net_per_unit)) * 100


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px'>
      <div style='font-family:"Syne",sans-serif;font-size:28px;font-weight:800;
                  background:linear-gradient(135deg,#D4A843,#F0C96A);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  letter-spacing:-1px'>PropIQ</div>
      <div style='font-size:10px;color:#5A7090;margin-top:2px;font-family:"IBM Plex Mono",monospace;
                  letter-spacing:1.5px;text-transform:uppercase'>Commercial · CRE Analyzer</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    project_name = st.text_input("🏷️ Project Name", value="Industrial Park A1")
    asset_type = st.selectbox("🏗️ Asset Type", ["Last Mile Warehouse", "Multi-Family Apartments",
                                                  "Mixed-Use", "Cold Storage", "Flex Industrial"])

    st.markdown("#### 📐 Property Details")
    price = st.number_input("Acquisition Price ($)", value=4_500_000, step=100_000, format="%d")
    total_sqft = st.number_input("Total Leasable Area (SF)", value=50_000, step=1_000, format="%d")
    num_units = st.number_input("Number of Tenants / Units", value=6, step=1, min_value=1, max_value=30)
    rent_per_sf = st.number_input("Base Rent ($/SF/yr)", value=14.0, step=0.50, format="%.2f")
    closing = st.number_input("Closing / Transaction Costs ($)", value=90_000, step=5_000, format="%d")
    arv = st.number_input("Stabilized Value ($)", value=5_200_000, step=100_000, format="%d")
    capex = st.number_input("CapEx / TI Allowance ($)", value=250_000, step=10_000, format="%d")

    st.markdown("#### 🏦 Financing")
    use_default = st.checkbox("Use 65% LTC (CRE default)", value=True)
    loan = price * 0.65 if use_default else st.number_input("Loan Amount ($)", value=int(price * 0.65),
                                                              step=50_000, format="%d")
    if use_default:
        st.caption(f"Loan: ${loan:,.0f}")
    rate = st.number_input("Interest Rate (%)", value=6.75, step=0.125, format="%.3f")
    term = st.selectbox("Loan Term", [300, 360, 240, 180, 120],
                        format_func=lambda x: f"{x // 12} yrs ({x} mo)")
    io_period = st.number_input("Interest-Only Period (months)", value=24, step=6, min_value=0, max_value=60)

    st.markdown("#### 📊 Operating Expenses")
    opex_type = st.selectbox("Lease Structure", ["NNN (Triple Net)", "Modified Gross", "Full Service Gross"])
    if opex_type == "NNN (Triple Net)":
        opex_ratio = st.slider("OpEx (landlord only, %)", 0.0, 15.0, 5.0, 0.5)
    elif opex_type == "Modified Gross":
        opex_ratio = st.slider("OpEx Ratio (%)", 5.0, 30.0, 15.0, 1.0)
    else:
        opex_ratio = st.slider("OpEx Ratio (%)", 15.0, 50.0, 32.0, 1.0)
    tax_pct = st.slider("Property Tax (% of price/yr)", 0.5, 3.0, 1.2, 0.1)
    ins_pct = st.slider("Insurance (% of price/yr)", 0.1, 1.0, 0.3, 0.1)
    mgmt_fee = st.slider("Mgmt/Asset Mgmt Fee (%)", 0.0, 8.0, 3.0, 0.5)

    st.markdown("#### 🔴 Tenant Stress Test")
    st.caption("Simulate tenant departures and re-leasing timelines")
    reabsorption = st.slider("Re-Leasing Period (months)", 3, 24, 9, 3)
    downtime_mo = st.slider("Free Rent / Downtime (months)", 0, 12, 3, 1)
    leasing_cost_pct = st.slider("Leasing Commission (% of annual rent)", 2.0, 8.0, 4.0, 0.5)

    st.markdown("#### 📈 Hold & Exit")
    hold_yrs = st.slider("Hold Period (years)", 3, 15, 7)
    app_rate = st.slider("Annual Appreciation (%)", 0.0, 8.0, 3.5, 0.5)
    rent_escal = st.slider("Annual Rent Escalation (%)", 0.0, 5.0, 2.5, 0.25)
    exit_cap = st.slider("Exit Cap Rate (%)", 4.0, 9.0, 6.0, 0.25)

    st.markdown("---")
    st.caption("💡 CRE calculations. Not financial advice.")

# ══════════════════════════════════════════════════════════════
# DERIVED INPUTS
# ══════════════════════════════════════════════════════════════
rent_annual = total_sqft * rent_per_sf
rent_monthly = rent_annual / 12
opex_total = opex_ratio + mgmt_fee
vacancy_pct = 5.0

r = full_analysis(price, rent_monthly, closing, loan, rate, term,
                  vacancy_pct, opex_total, tax_pct, ins_pct, asset_type)
am = build_amortization(loan, rate, term)

noi_annual = r['noi']
price_per_sf = price / total_sqft if total_sqft > 0 else 0
rent_per_sf_eff = (rent_monthly * (1 - vacancy_pct / 100) * 12) / total_sqft if total_sqft > 0 else 0
noi_per_sf = noi_annual / total_sqft if total_sqft > 0 else 0
stabilized_value = noi_annual / (exit_cap / 100) if exit_cap > 0 else 0
value_add = stabilized_value - price
yield_on_cost = (noi_annual / (price + capex)) * 100 if (price + capex) > 0 else 0
spread_to_cap = yield_on_cost - r['cap_rate']
breakeven_occ = breakeven_occupancy_commercial(r['payment'], opex_total, rent_monthly)

io_payment = loan * (rate / 1200)
io_cf_monthly = (noi_annual / 12) - io_payment

exit_noi = noi_annual * (1 + rent_escal / 100) ** hold_yrs
exit_value_cap = exit_noi / (exit_cap / 100) if exit_cap > 0 else 0
exit_balance = float(am[am['Month'] == min(hold_yrs * 12, len(am))]['Balance'].values[-1]) if len(am) > 0 else loan
sale_net = exit_value_cap * 0.97
equity_exit = sale_net - exit_balance
total_cf_hold = r['annual_cf'] * hold_yrs
total_return = equity_exit - r['cash_required'] - capex + total_cf_hold
irr_approx = ((1 + total_return / max(r['cash_required'] + capex, 1)) ** (1 / hold_yrs) - 1) * 100

rent_per_tenant = rent_monthly / num_units
tenant_list = [{'name': f'Tenant {i + 1}', 'rent': rent_per_tenant, 'vacant_start': 999, 'vacant_months': 0}
               for i in range(num_units)]

t_base = [dict(t, vacant_start=999, vacant_months=0) for t in tenant_list]

t_s1 = [dict(t) for t in tenant_list]
if len(t_s1) > 0:
    t_s1[0]['rent'] = rent_monthly * 0.25
    t_s1[0]['vacant_start'] = 6
    t_s1[0]['vacant_months'] = reabsorption
    for i in range(1, len(t_s1)):
        t_s1[i]['rent'] = rent_monthly * 0.75 / max(len(t_s1) - 1, 1)

t_s2 = [dict(t) for t in tenant_list]
cascade_count = max(1, int(num_units * 0.4))
for i in range(cascade_count):
    t_s2[i]['vacant_start'] = 3 + i * 2
    t_s2[i]['vacant_months'] = reabsorption

t_s3 = [dict(t) for t in tenant_list]
for t in t_s3:
    t['vacant_start'] = 4
    t['vacant_months'] = reabsorption

scenarios_dict = {
    '✅ Stabilized (Base)': t_base,
    '⚡ Anchor Loss (25%)': t_s1,
    '⚠️ Cascade Vacancy (40%)': t_s2,
    '🔴 Full Vacancy': t_s3,
}
stress_df = run_tenant_stress(scenarios_dict, rent_monthly, loan, rate, term,
                               opex_total, reabsorption, downtime_mo)

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    asset_icon = {"Last Mile Warehouse": "🏭", "Multi-Family Apartments": "🏢", "Mixed-Use": "🏙️",
                  "Cold Storage": "❄️", "Flex Industrial": "🔧"}.get(asset_type, "🏗️")
    st.markdown(f'<div class="page-title">PropIQ Commercial</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="page-sub">{asset_icon} {asset_type} · {project_name} · {total_sqft:,} SF · {num_units} Tenants</div>',
        unsafe_allow_html=True)
with col_h2:
    if r['annual_cf'] > 0 and r['dscr'] >= 1.25 and r['cap_rate'] >= 5 and yield_on_cost > r['cap_rate']:
        v_html = '<span class="badge badge-green">✅ STRONG DEAL</span>'
    elif r['annual_cf'] > 0 and r['dscr'] >= 1.0:
        v_html = '<span class="badge badge-amber">⚡ INVESTABLE</span>'
    else:
        v_html = '<span class="badge badge-red">⚠️ REVIEW</span>'
    st.markdown(f'<div style="text-align:right;padding-top:22px">{v_html}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="text-align:right;font-size:11px;color:#5A7090;margin-top:5px;font-family:IBM Plex Mono,monospace">'
        f'Cap: {r["cap_rate"]:.2f}% · YoC: {yield_on_cost:.2f}% · DSCR: {r["dscr"]:.2f}</div>',
        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# KPI ROW 1
# ══════════════════════════════════════════════════════════════
cf_cls = "positive" if r['monthly_cf'] >= 0 else "negative"
coc_cls = "positive" if r['coc'] >= 8 else "warning" if r['coc'] >= 4 else "negative"
dscr_cls = "positive" if r['dscr'] >= 1.25 else "negative"
spread_cls = "positive" if spread_to_cap > 1 else "warning" if spread_to_cap > 0 else "negative"

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon">💵</div>
    <div class="kpi-label">Monthly Cash Flow</div>
    <div class="kpi-value {cf_cls}">${r['monthly_cf']:,.0f}</div>
    <div class="kpi-sub">Annual: ${r['annual_cf']:,.0f}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">📊</div>
    <div class="kpi-label">Cap Rate</div>
    <div class="kpi-value">{r['cap_rate']:.2f}%</div>
    <div class="kpi-sub">NOI / Price</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">🔨</div>
    <div class="kpi-label">Yield on Cost</div>
    <div class="kpi-value {spread_cls}">{yield_on_cost:.2f}%</div>
    <div class="kpi-sub">Spread: {spread_to_cap:+.2f}%</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">💰</div>
    <div class="kpi-label">Cash-on-Cash</div>
    <div class="kpi-value {coc_cls}">{r['coc']:.2f}%</div>
    <div class="kpi-sub">Equity: ${r['cash_required'] + capex:,.0f}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">🏦</div>
    <div class="kpi-label">DSCR</div>
    <div class="kpi-value {dscr_cls}">{r['dscr']:.2f}x</div>
    <div class="kpi-sub">Min 1.25x lenders</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">🎯</div>
    <div class="kpi-label">Breakeven Occ.</div>
    <div class="kpi-value {'positive' if breakeven_occ < 70 else 'warning' if breakeven_occ < 85 else 'negative'}">{breakeven_occ:.1f}%</div>
    <div class="kpi-sub">To cover debt svc</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">📈</div>
    <div class="kpi-label">Est. IRR</div>
    <div class="kpi-value {'positive' if irr_approx > 12 else 'warning' if irr_approx > 8 else 'negative'}">{irr_approx:.1f}%</div>
    <div class="kpi-sub">{hold_yrs}yr hold · exit @ {exit_cap}%</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# KPI ROW 2
# ══════════════════════════════════════════════════════════════
io_cls = "positive" if io_cf_monthly >= 0 else "negative"
va_cls = "positive" if value_add > 0 else "negative"

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-icon">📐</div>
    <div class="kpi-label">Price / SF</div>
    <div class="kpi-value">${price_per_sf:,.0f}</div>
    <div class="kpi-sub">{total_sqft:,} SF total</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">🏠</div>
    <div class="kpi-label">Rent / SF / yr</div>
    <div class="kpi-value">${rent_per_sf:.2f}</div>
    <div class="kpi-sub">Effective: ${rent_per_sf_eff:.2f}</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">⚡</div>
    <div class="kpi-label">NOI / SF</div>
    <div class="kpi-value">${noi_per_sf:.2f}</div>
    <div class="kpi-sub">Annual per SF</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">🏗️</div>
    <div class="kpi-label">Stabilized Value</div>
    <div class="kpi-value">${stabilized_value / 1e6:.2f}M</div>
    <div class="kpi-sub">@ {exit_cap}% cap rate</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">💎</div>
    <div class="kpi-label">Value-Add Spread</div>
    <div class="kpi-value {va_cls}">${value_add / 1e3:+.0f}K</div>
    <div class="kpi-sub">Stab. Value − Acq. Price</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">📋</div>
    <div class="kpi-label">I/O Period CF</div>
    <div class="kpi-value {io_cls}">${io_cf_monthly:,.0f}/mo</div>
    <div class="kpi-sub">First {io_period} months</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-icon">🔑</div>
    <div class="kpi-label">LTV</div>
    <div class="kpi-value">{r['ltv']:.1f}%</div>
    <div class="kpi-sub">CRE max: 65–70%</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Cash Flow", "🔴 Tenant Stress", "🔄 Sensitivity",
    "📅 Amortization", "📈 Projections", "🏗️ Deal Score", "📋 Report"
])

# ════════════════════════════════════════════════════════════
# TAB 1 — CASH FLOW
# ════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">💵 <span>Pro Forma Income Statement</span></div>',
                unsafe_allow_html=True)

    eff_rent = rent_monthly * (1 - vacancy_pct / 100)
    opex_mo = eff_rent * (opex_total / 100)
    tax_mo = rent_monthly * (tax_pct / 100) / 12
    ins_mo = rent_monthly * (ins_pct / 100) / 12
    noi_mo = eff_rent - opex_mo - tax_mo - ins_mo
    cf_mo = noi_mo - r['payment']

    col1, col2 = st.columns(2)
    with col1:
        cats = ['Gross Rent', 'Vacancy', 'OpEx', 'Prop. Tax', 'Insurance', 'Debt Svc', 'Net CF']
        vals = [rent_monthly, -(rent_monthly - eff_rent), -opex_mo, -tax_mo, -ins_mo, -r['payment'], cf_mo]
        fig_wf = go.Figure(go.Waterfall(
            orientation='v', measure=['absolute'] + ['relative'] * 5 + ['total'],
            x=cats, y=vals,
            connector=dict(line=dict(color='#243045', width=1)),
            increasing=dict(marker_color=C['gold']),
            decreasing=dict(marker_color=C['red']),
            totals=dict(marker_color=C['green'] if cf_mo >= 0 else C['red']),
            text=[f'${v:,.0f}' for v in vals],
            textposition='outside', textfont=dict(color='#E2E8F0', size=10),
        ))
        fig_wf.update_layout(**PLOT_LAYOUT, title='Monthly Cash Flow Waterfall', height=380,
                             title_font=dict(color='#E2E8F0', size=14))
        st.plotly_chart(fig_wf, use_container_width=True)

    with col2:
        labels = ['Vacancy Loss', 'OpEx / Mgmt', 'Property Tax', 'Insurance', 'Debt Service', 'Net CF']
        values_d = [rent_monthly - eff_rent, opex_mo, tax_mo, ins_mo, r['payment'], max(cf_mo, 0)]
        clrs = [C['orange'], C['blue'], C['teal'], C['gold'], C['red'], C['green']]
        fig_pie = go.Figure(go.Pie(
            labels=labels, values=values_d, hole=0.58,
            marker_colors=clrs, textinfo='percent',
            textfont=dict(size=10, color='#E2E8F0'),
            hovertemplate='%{label}<br>$%{value:,.0f}/mo<extra></extra>'
        ))
        fig_pie.add_annotation(text=f'${rent_monthly:,.0f}<br><span style="font-size:9px">GROSS/MO</span>',
                               x=0.5, y=0.5, font_size=15, font_color='#E2E8F0', showarrow=False)
        fig_pie.update_layout(**PLOT_LAYOUT, title=f'Cost Structure — {opex_type}',
                              height=380, title_font=dict(color='#E2E8F0', size=14))
        st.plotly_chart(fig_pie, use_container_width=True)

    rows = [
        ('Gross Scheduled Rent (annual)', f'${rent_annual:,.0f}', f'${rent_per_sf:.2f}/SF'),
        ('Less: Vacancy ({:.0f}%)'.format(vacancy_pct), f'-${(rent_monthly - eff_rent) * 12:,.0f}',
         f'-${(rent_per_sf * vacancy_pct / 100):.2f}/SF'),
        ('Effective Gross Income', f'${eff_rent * 12:,.0f}', ''),
        ('─────────────────', '', ''),
        (f'Less: OpEx + Mgmt ({opex_total:.1f}%)', f'-${opex_mo * 12:,.0f}', ''),
        (f'Less: Property Tax ({tax_pct:.1f}%)', f'-${tax_mo * 12:,.0f}', f'${tax_pct:.1f}% of price'),
        (f'Less: Insurance ({ins_pct:.1f}%)', f'-${ins_mo * 12:,.0f}', ''),
        ('NET OPERATING INCOME', f'${noi_mo * 12:,.0f}', f'${noi_per_sf:.2f}/SF'),
        ('─────────────────', '', ''),
        ('Less: Debt Service (P&I)', f'-${r["annual_debt"]:,.0f}', f'${r["payment"]:,.0f}/mo'),
        ('NET CASH FLOW', f'${r["annual_cf"]:,.0f}', f'${r["monthly_cf"]:,.0f}/mo'),
        ('─────────────────', '', ''),
        ('Cash-on-Cash Return', f'{r["coc"]:.2f}%', f'On ${r["cash_required"] + capex:,.0f} equity'),
        ('Cap Rate', f'{r["cap_rate"]:.2f}%', 'Unlevered return'),
        ('Yield on Cost', f'{yield_on_cost:.2f}%', f'Incl. ${capex:,.0f} CapEx'),
        ('DSCR', f'{r["dscr"]:.2f}x', 'Min 1.25x for CRE loans'),
    ]
    df_stmt = pd.DataFrame(rows, columns=['Line Item', 'Annual', 'Notes'])
    st.dataframe(df_stmt, use_container_width=True, hide_index=True, height=520)

# ════════════════════════════════════════════════════════════
# TAB 2 — TENANT STRESS TEST
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">🔴 <span>Tenant Stress Test & Vacancy Simulation</span></div>',
                unsafe_allow_html=True)

    scenario_names = list(scenarios_dict.keys())
    summary_cols = st.columns(4)
    scenario_colors = [C['green'], C['amber'], C['orange'], C['red']]

    for idx, (sc_name, col_obj) in enumerate(zip(scenario_names, summary_cols)):
        sc_df = stress_df[stress_df['Scenario'] == sc_name]
        worst_cf = sc_df['Cash Flow'].min()
        avg_occ = sc_df['Occupancy'].mean()
        total_shortfall = sc_df['Shortfall'].sum()
        months_negative = (sc_df['Cash Flow'] < 0).sum()
        sc_col = scenario_colors[idx]
        with col_obj:
            st.markdown(f"""
            <div style="background:var(--card);border:1px solid var(--border);
                        border-top:3px solid {sc_col};border-radius:10px;padding:16px;">
              <div style="font-size:10px;color:#5A7090;text-transform:uppercase;letter-spacing:1px;
                          font-family:'IBM Plex Mono',monospace;margin-bottom:8px">{sc_name}</div>
              <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:700;
                          color:{'#22C55E' if worst_cf >= 0 else '#EF4444'}">
                ${worst_cf:,.0f}<span style="font-size:12px;color:#5A7090">/mo worst</span>
              </div>
              <div style="font-size:11px;color:#5A7090;margin-top:6px;font-family:'IBM Plex Mono',monospace">
                Avg Occ: {avg_occ:.0f}% · Neg months: {months_negative}<br>
                Total shortfall: ${total_shortfall:,.0f}
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    col1, col2 = st.columns([3, 2])

    with col1:
        fig_stress = go.Figure()
        colors_sc = [C['green'], C['amber'], C['orange'], C['red']]
        dash_styles = ['solid', 'dot', 'dash', 'dashdot']
        for sc_name, sc_color, sc_dash in zip(scenario_names, colors_sc, dash_styles):
            sc_data = stress_df[stress_df['Scenario'] == sc_name]
            fig_stress.add_trace(go.Scatter(
                x=sc_data['Month'], y=sc_data['Cash Flow'],
                name=sc_name, line=dict(color=sc_color, width=2, dash=sc_dash),
                hovertemplate='Month %{x}<br>CF: $%{y:,.0f}<extra>' + sc_name + '</extra>'
            ))
        fig_stress.add_hline(y=0, line=dict(color='#5A7090', dash='dot', width=1),
                             annotation_text='Break-Even', annotation_font_color='#5A7090')
        fig_stress.add_hline(y=-r['payment'], line=dict(color=C['red'], dash='dot', width=1),
                             annotation_text='Full Debt Service', annotation_font_color=C['red'],
                             annotation_position='bottom right')
        fig_stress.update_layout(**PLOT_LAYOUT, title='Monthly Cash Flow by Vacancy Scenario (60 months)',
                                 height=400, title_font=dict(color='#E2E8F0', size=14),
                                 yaxis_tickprefix='$', yaxis_tickformat=',.0f',
                                 xaxis_title='Month', yaxis_title='Cash Flow')
        st.plotly_chart(fig_stress, use_container_width=True)

    with col2:
        fig_occ = go.Figure()
        for sc_name, sc_color in zip(scenario_names, colors_sc):
            sc_data = stress_df[stress_df['Scenario'] == sc_name]
            fig_occ.add_trace(go.Scatter(
                x=sc_data['Month'], y=sc_data['Occupancy'],
                name=sc_name, line=dict(color=sc_color, width=2),
                fill='none'
            ))
        fig_occ.add_hline(y=breakeven_occ, line=dict(color=C['amber'], dash='dash', width=1.5),
                          annotation_text=f'Breakeven {breakeven_occ:.0f}%',
                          annotation_font_color=C['amber'])
        # FIX 1: split update_layout and update_yaxes to avoid duplicate yaxis key
        fig_occ.update_layout(**PLOT_LAYOUT, title='Occupancy Rate by Scenario',
                              height=400, title_font=dict(color='#E2E8F0', size=14),
                              yaxis_title='Occupancy %', xaxis_title='Month')
        fig_occ.update_yaxes(range=[0, 105])
        st.plotly_chart(fig_occ, use_container_width=True)

    st.markdown('<div class="section-title">💸 <span>Cumulative Capital Reserve Requirement</span></div>',
                unsafe_allow_html=True)
    fig_cum = go.Figure()
    for sc_name, sc_color in zip(scenario_names, colors_sc):
        sc_data = stress_df[stress_df['Scenario'] == sc_name].copy()
        sc_data['Cum Shortfall'] = sc_data['Shortfall'].cumsum()
        # FIX 2: use hex_to_rgba() instead of broken string manipulation
        fig_cum.add_trace(go.Scatter(
            x=sc_data['Month'], y=sc_data['Cum Shortfall'],
            name=sc_name, line=dict(color=sc_color, width=2),
            fill='tozeroy', fillcolor=hex_to_rgba(sc_color, 0.08)
        ))
    fig_cum.update_layout(**PLOT_LAYOUT, title='Cumulative Cash Reserve Needed (shortfall)',
                          height=320, title_font=dict(color='#E2E8F0', size=14),
                          yaxis_tickprefix='$', yaxis_tickformat=',.0f',
                          xaxis_title='Month')
    st.plotly_chart(fig_cum, use_container_width=True)

    st.markdown("#### 📋 Stress Scenario Detail (Month-by-Month, Year 1–2)")
    stress_display = stress_df[stress_df['Month'] <= 24][
        ['Scenario', 'Month', 'Collected Rent', 'NOI', 'Cash Flow', 'Occupancy', 'Shortfall']
    ].copy()
    for col_fmt in ['Collected Rent', 'NOI', 'Cash Flow', 'Shortfall']:
        stress_display[col_fmt] = stress_display[col_fmt].apply(lambda x: f"${x:,.0f}")
    stress_display['Occupancy'] = stress_display['Occupancy'].apply(lambda x: f"{x:.0f}%")
    st.dataframe(stress_display, use_container_width=True, hide_index=True, height=420)

    st.markdown('<div class="section-title">🏷️ <span>Re-Leasing Cost Analysis</span></div>',
                unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    leasing_comm = (rent_per_tenant * 12 * leasing_cost_pct / 100)
    free_rent_cost = rent_per_tenant * downtime_mo
    ti_per_tenant = capex / num_units
    total_relet_cost = (leasing_comm + free_rent_cost + ti_per_tenant) * num_units

    col1.metric("Leasing Commission / Tenant", f"${leasing_comm:,.0f}", delta=f"{leasing_cost_pct}% annual rent")
    col2.metric("Free Rent Cost / Tenant", f"${free_rent_cost:,.0f}", delta=f"{downtime_mo} months")
    col3.metric("TI Allowance / Tenant", f"${ti_per_tenant:,.0f}")
    col4.metric("Total Re-Leasing Cost (all)", f"${total_relet_cost:,.0f}")

# ════════════════════════════════════════════════════════════
# TAB 3 — SENSITIVITY
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🔄 <span>Sensitivity Analysis</span></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        vacancy_range = np.arange(0, 35, 5)
        rent_sf_range = np.arange(max(rent_per_sf * 0.6, 4), rent_per_sf * 1.4, rent_per_sf * 0.1)
        heat_cap = []
        for v in vacancy_range:
            row_data = []
            for r_sf in rent_sf_range:
                r_mo = (r_sf * total_sqft) / 12
                rr = full_analysis(price, r_mo, closing, loan, rate, term, v, opex_total, tax_pct, ins_pct)
                row_data.append(round(rr['cap_rate'], 2))
            heat_cap.append(row_data)

        fig_h1 = go.Figure(go.Heatmap(
            z=heat_cap,
            x=[f'${r:.2f}/SF' for r in rent_sf_range],
            y=[f'{v:.0f}%' for v in vacancy_range],
            colorscale=[[0, C['red']], [0.4, C['amber']], [0.7, C['gold']], [1, C['green']]],
            text=[[f'{v:.1f}%' for v in row] for row in heat_cap],
            texttemplate='%{text}', textfont=dict(size=9),
        ))
        fig_h1.update_layout(**PLOT_LAYOUT, title='Cap Rate: Rent/SF vs Vacancy',
                             height=360, title_font=dict(color='#E2E8F0', size=14),
                             xaxis_title='Rent/SF/yr', yaxis_title='Vacancy %')
        st.plotly_chart(fig_h1, use_container_width=True)

    with col2:
        rate_range2 = np.arange(5.0, 9.5, 0.5)
        occ_range = np.arange(60, 101, 5)
        heat_dscr = []
        for occ in occ_range:
            row_data = []
            for rt in rate_range2:
                vac = 100 - occ
                rr = full_analysis(price, rent_monthly, closing, loan, rt, term, vac, opex_total, tax_pct, ins_pct)
                row_data.append(round(rr['dscr'], 2))
            heat_dscr.append(row_data)

        fig_h2 = go.Figure(go.Heatmap(
            z=heat_dscr,
            x=[f'{rt:.1f}%' for rt in rate_range2],
            y=[f'{occ:.0f}%' for occ in occ_range],
            colorscale=[[0, C['red']], [0.45, C['amber']], [0.6, C['gold']], [1, C['green']]],
            text=[[f'{v:.2f}x' for v in row] for row in heat_dscr],
            texttemplate='%{text}', textfont=dict(size=9),
        ))
        fig_h2.update_layout(**PLOT_LAYOUT, title='DSCR: Interest Rate vs Occupancy',
                             height=360, title_font=dict(color='#E2E8F0', size=14),
                             xaxis_title='Interest Rate', yaxis_title='Occupancy %')
        st.plotly_chart(fig_h2, use_container_width=True)

    st.markdown("#### Three-Scenario Comparison")
    r_bear = full_analysis(price, rent_monthly * 0.8, closing, loan * 1.05 if loan < price else loan,
                           rate + 1.0, term, 20, opex_total + 5, tax_pct, ins_pct)
    r_bull = full_analysis(price * 0.95, rent_monthly * 1.1, closing, loan * 0.95,
                           rate - 0.5, term, 3, opex_total - 2, tax_pct, ins_pct)

    scenarios_cmp = ['🐻 Bear', '📊 Base', '🐂 Bull']
    metrics_cmp = {
        'Cap Rate (%)': [r_bear['cap_rate'], r['cap_rate'], r_bull['cap_rate']],
        'CoC Return (%)': [r_bear['coc'], r['coc'], r_bull['coc']],
        'DSCR (x)': [r_bear['dscr'], r['dscr'], r_bull['dscr']],
        'Annual CF ($K)': [r_bear['annual_cf'] / 1e3, r['annual_cf'] / 1e3, r_bull['annual_cf'] / 1e3],
    }
    fig_cmp = go.Figure()
    cmp_colors = [C['red'], C['gold'], C['green']]
    for i, (sc, col_obj) in enumerate(zip(scenarios_cmp, cmp_colors)):
        fig_cmp.add_trace(go.Bar(
            name=sc, x=list(metrics_cmp.keys()),
            y=[v[i] for v in metrics_cmp.values()],
            marker_color=col_obj, opacity=0.85,
            text=[f'{v[i]:.2f}' for v in metrics_cmp.values()],
            textposition='outside', textfont=dict(color='#E2E8F0', size=10)
        ))
    fig_cmp.update_layout(**PLOT_LAYOUT, barmode='group', height=340,
                          title='Bear / Base / Bull Scenario Comparison',
                          title_font=dict(color='#E2E8F0', size=14))
    st.plotly_chart(fig_cmp, use_container_width=True)

    sens_table = pd.DataFrame({
        'Metric': ['Monthly CF', 'Annual CF', 'Cap Rate', 'CoC', 'DSCR', 'Yield on Cost'],
        '🐻 Bear': [f"${r_bear['monthly_cf']:,.0f}", f"${r_bear['annual_cf']:,.0f}",
                    f"{r_bear['cap_rate']:.2f}%", f"{r_bear['coc']:.2f}%", f"{r_bear['dscr']:.2f}x", "—"],
        '📊 Base': [f"${r['monthly_cf']:,.0f}", f"${r['annual_cf']:,.0f}",
                    f"{r['cap_rate']:.2f}%", f"{r['coc']:.2f}%", f"{r['dscr']:.2f}x", f"{yield_on_cost:.2f}%"],
        '🐂 Bull': [f"${r_bull['monthly_cf']:,.0f}", f"${r_bull['annual_cf']:,.0f}",
                    f"{r_bull['cap_rate']:.2f}%", f"{r_bull['coc']:.2f}%", f"{r_bull['dscr']:.2f}x", "—"],
    })
    st.dataframe(sens_table, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════
# TAB 4 — AMORTIZATION
# ════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">📅 <span>Loan Amortization</span></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_am = go.Figure()
        fig_am.add_trace(go.Scatter(x=am['Month'], y=am['Principal'], name='Principal',
                                    line=dict(color=C['green'], width=2), fill='tozeroy',
                                    fillcolor='rgba(34,197,94,0.08)'))
        fig_am.add_trace(go.Scatter(x=am['Month'], y=am['Interest'], name='Interest',
                                    line=dict(color=C['red'], width=2)))
        if io_period > 0:
            fig_am.add_vrect(x0=0, x1=io_period, fillcolor='rgba(245,158,11,0.08)',
                             line=dict(color=C['amber'], dash='dot', width=1),
                             annotation_text="I/O Period", annotation_position="top left",
                             annotation_font_color=C['amber'])
        fig_am.update_layout(**PLOT_LAYOUT, title='Principal vs Interest Over Time',
                             height=360, title_font=dict(color='#E2E8F0', size=14),
                             yaxis_tickprefix='$', yaxis_tickformat=',.0f')
        st.plotly_chart(fig_am, use_container_width=True)

    with col2:
        fig_eq = go.Figure()
        fig_eq.add_trace(go.Scatter(x=am['Month'], y=am['Balance'],
                                    fill='tozeroy', fillcolor='rgba(239,68,68,0.08)',
                                    line=dict(color=C['red'], width=2), name='Loan Balance'))
        fig_eq.add_trace(go.Scatter(x=am['Month'], y=am['Equity'],
                                    fill='tozeroy', fillcolor='rgba(34,197,94,0.08)',
                                    line=dict(color=C['green'], width=2), name='Equity'))
        fig_eq.update_layout(**PLOT_LAYOUT, title='Loan Balance vs Equity Buildup',
                             height=360, title_font=dict(color='#E2E8F0', size=14),
                             yaxis_tickprefix='$', yaxis_tickformat=',.0f')
        st.plotly_chart(fig_eq, use_container_width=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monthly P&I", f"${r['payment']:,.0f}")
    c2.metric("I/O Payment", f"${io_payment:,.0f}", delta=f"Saves ${r['payment'] - io_payment:,.0f}/mo")
    c3.metric("Total Interest", f"${r['total_interest'] / 1e6:.2f}M")
    c4.metric("Equity Yr 5",
              f"${am[am['Month'] == min(60, len(am))]['Equity'].values[-1]:,.0f}" if len(am) >= 60 else "N/A")

    am_display = am.copy()
    for c in ['Payment', 'Principal', 'Interest', 'Balance', 'Cumul. Interest', 'Equity']:
        am_display[c] = am_display[c].apply(lambda x: f"${x:,.0f}")
    st.dataframe(am_display, use_container_width=True, hide_index=True, height=400)

# ════════════════════════════════════════════════════════════
# TAB 5 — PROJECTIONS
# ════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">📈 <span>Hold Period Projections & Exit</span></div>',
                unsafe_allow_html=True)

    years = list(range(1, hold_yrs + 1))
    prop_vals, noi_proj, cf_proj, coc_proj, equity_proj, value_cap_proj = [], [], [], [], [], []

    for y in years:
        r_sf_y = rent_per_sf * (1 + rent_escal / 100) ** y
        r_mo_y = r_sf_y * total_sqft / 12
        prop_v = price * (1 + app_rate / 100) ** y
        noi_y = calc_noi(r_mo_y, vacancy_pct, opex_total, tax_pct, ins_pct)
        val_cap = noi_y / (exit_cap / 100) if exit_cap > 0 else 0
        bal_row = am[am['Month'] == min(y * 12, len(am))]
        bal = float(bal_row['Balance'].values[-1]) if not bal_row.empty else 0
        eq = prop_v - bal
        rr = full_analysis(price, r_mo_y, closing, loan, rate, term, vacancy_pct, opex_total, tax_pct, ins_pct)
        prop_vals.append(prop_v)
        noi_proj.append(noi_y)
        cf_proj.append(rr['annual_cf'])
        coc_proj.append(rr['coc'])
        equity_proj.append(eq)
        value_cap_proj.append(val_cap)

    col1, col2 = st.columns(2)
    with col1:
        fig_val = go.Figure()
        fig_val.add_trace(go.Scatter(x=years, y=prop_vals, name='Appreciation Value',
                                     line=dict(color=C['gold'], width=2.5),
                                     fill='tozeroy', fillcolor='rgba(212,168,67,0.06)'))
        fig_val.add_trace(go.Scatter(x=years, y=value_cap_proj, name='Cap Rate Value',
                                     line=dict(color=C['teal'], width=2.5, dash='dot')))
        fig_val.add_trace(go.Scatter(x=years, y=equity_proj, name='Equity',
                                     line=dict(color=C['green'], width=2),
                                     fill='tozeroy', fillcolor='rgba(34,197,94,0.06)'))
        fig_val.add_hline(y=price, line=dict(color='#5A7090', dash='dash', width=1),
                          annotation_text='Acq. Price', annotation_font_color='#5A7090')
        fig_val.update_layout(**PLOT_LAYOUT, title=f'Value & Equity Projection ({app_rate}% appreciation)',
                              height=360, title_font=dict(color='#E2E8F0', size=14),
                              yaxis_tickprefix='$', yaxis_tickformat=',.0f', xaxis_title='Year')
        st.plotly_chart(fig_val, use_container_width=True)

    with col2:
        fig_noi = go.Figure()
        fig_noi.add_trace(go.Bar(x=years, y=noi_proj,
                                  marker_color=C['gold'], name='NOI',
                                  text=[f'${v / 1e3:.0f}K' for v in noi_proj],
                                  textposition='outside', textfont=dict(color='#E2E8F0', size=9)))
        fig_noi.add_trace(go.Scatter(x=years, y=cf_proj, name='Cash Flow',
                                      line=dict(color=C['green'], width=2.5), mode='lines+markers',
                                      marker=dict(size=6)))
        fig_noi.update_layout(**PLOT_LAYOUT, title=f'NOI & Cash Flow ({rent_escal}% rent escalation)',
                              height=360, title_font=dict(color='#E2E8F0', size=14),
                              yaxis_tickprefix='$', yaxis_tickformat=',.0f', xaxis_title='Year',
                              barmode='overlay')
        st.plotly_chart(fig_noi, use_container_width=True)

    st.markdown(f'<div class="section-title">🏁 <span>Exit Analysis — Year {hold_yrs}</span></div>',
                unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Exit Value (Cap Rate)", f"${value_cap_proj[-1] / 1e6:.2f}M")
    c2.metric("Exit Value (Appreciation)", f"${prop_vals[-1] / 1e6:.2f}M")
    c3.metric("Loan Balance at Exit", f"${exit_balance / 1e3:.0f}K")
    c4.metric("Equity at Exit", f"${equity_exit / 1e3:.0f}K")
    c5.metric("Total Cash Flow (hold)", f"${sum(cf_proj) / 1e3:.0f}K")
    c6.metric("Estimated IRR", f"{irr_approx:.1f}%", delta="Leveraged")

# ════════════════════════════════════════════════════════════
# TAB 6 — DEAL SCORE
# ════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-title">🏗️ <span>Commercial Deal Scorecard</span></div>',
                unsafe_allow_html=True)

    benchmarks = {
        "Last Mile Warehouse": {'cap_min': 5.0, 'cap_target': 6.5, 'coc_min': 7, 'dscr_min': 1.25, 'ltv_max': 65,
                                'grm_max': 14, 'yoc_spread': 1.0},
        "Multi-Family Apartments": {'cap_min': 4.5, 'cap_target': 5.5, 'coc_min': 6, 'dscr_min': 1.20,
                                    'ltv_max': 75, 'grm_max': 18, 'yoc_spread': 0.75},
        "Mixed-Use": {'cap_min': 5.0, 'cap_target': 6.0, 'coc_min': 7, 'dscr_min': 1.25, 'ltv_max': 70,
                      'grm_max': 15, 'yoc_spread': 1.0},
        "Cold Storage": {'cap_min': 5.5, 'cap_target': 7.0, 'coc_min': 8, 'dscr_min': 1.30, 'ltv_max': 60,
                         'grm_max': 13, 'yoc_spread': 1.5},
        "Flex Industrial": {'cap_min': 5.0, 'cap_target': 6.5, 'coc_min': 7, 'dscr_min': 1.25, 'ltv_max': 65,
                            'grm_max': 14, 'yoc_spread': 1.0},
    }
    bm = benchmarks.get(asset_type, benchmarks["Last Mile Warehouse"])

    col1, col2 = st.columns([3, 2])
    with col1:
        checks = [
            (f"Cap Rate ≥ {bm['cap_min']}%", r['cap_rate'] >= bm['cap_min'],
             f"{r['cap_rate']:.2f}% (target ≥ {bm['cap_min']}%, ideal {bm['cap_target']}%)",
             "NOI / Acquisition Price — primary CRE return metric"),
            (f"Yield on Cost Spread ≥ {bm['yoc_spread']}%", spread_to_cap >= bm['yoc_spread'],
             f"Spread: {spread_to_cap:+.2f}% (YoC {yield_on_cost:.2f}% − Cap {r['cap_rate']:.2f}%)",
             "Value creation buffer above market cap rate"),
            (f"DSCR ≥ {bm['dscr_min']}x", r['dscr'] >= bm['dscr_min'],
             f"{r['dscr']:.2f}x (lenders require ≥ {bm['dscr_min']}x)",
             "Net Operating Income ÷ Annual Debt Service"),
            (f"CoC Return ≥ {bm['coc_min']}%", r['coc'] >= bm['coc_min'],
             f"{r['coc']:.2f}% (target ≥ {bm['coc_min']}%)",
             "Annual cash flow ÷ total equity invested"),
            (f"LTV ≤ {bm['ltv_max']}%", r['ltv'] <= bm['ltv_max'],
             f"{r['ltv']:.1f}% (CRE max {bm['ltv_max']}%)",
             "Loan ÷ Appraised Value — controls leverage risk"),
            ("Breakeven Occupancy < 80%", breakeven_occ < 80,
             f"{breakeven_occ:.1f}% (lower = more resilient)",
             "Minimum occupancy needed to cover debt service"),
            ("Positive Cash Flow", r['annual_cf'] > 0,
             f"${r['annual_cf']:,.0f} annual / ${r['monthly_cf']:,.0f} monthly",
             "After all expenses and debt service"),
            ("IRR > 12% (levered)", irr_approx > 12,
             f"{irr_approx:.1f}% over {hold_yrs} years",
             "Internal rate of return including equity appreciation at exit"),
            ("Value-Add Spread Positive", value_add > 0,
             f"${value_add / 1e3:+.0f}K vs acquisition price",
             "Stabilized value minus acquisition price"),
            ("Stress Test: Anchor Loss Positive CF",
             float(stress_df[stress_df['Scenario'] == '⚡ Anchor Loss (25%)']['Cash Flow'].min()) > -r[
                 'payment'] * 0.5,
             f"Worst month: ${float(stress_df[stress_df['Scenario'] == '⚡ Anchor Loss (25%)']['Cash Flow'].min()):,.0f}",
             "Anchor tenant departure stress test"),
        ]
        for name, passed, detail, tooltip in checks:
            icon = "✅" if passed else "❌"
            border_col = "#22C55E" if passed else "#EF4444"
            bg_col = "#0F2A1A" if passed else "#2A0F0F"
            st.markdown(f"""
            <div style="background:{bg_col};border:1px solid {border_col}33;
                        border-left:3px solid {border_col};
                        border-radius:8px;padding:10px 14px;margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-weight:600;color:#E2E8F0;font-family:'IBM Plex Sans',sans-serif">{icon} {name}</span>
                <span class="badge {'badge-green' if passed else 'badge-red'}">{'PASS' if passed else 'FAIL'}</span>
              </div>
              <div style="font-size:11px;color:#5A7090;margin-top:4px;font-family:'IBM Plex Mono',monospace">{detail}</div>
              <div style="font-size:10px;color:#3A5070;margin-top:2px">{tooltip}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        score_raw = [
            min(r['cap_rate'] / bm['cap_target'] * 100, 100),
            min(max(spread_to_cap / bm['yoc_spread'] * 100, 0), 100),
            min(r['dscr'] / 1.5 * 100, 100),
            min(max(r['coc'] / bm['coc_min'] * 100, 0), 100),
            min((100 - r['ltv']) / (100 - bm['ltv_max']) * 50, 100),
            min(max((100 - breakeven_occ) / 30 * 100, 0), 100),
            min(max(irr_approx / 15 * 100, 0), 100),
        ]
        cats_radar = ['Cap Rate', 'YoC Spread', 'DSCR', 'CoC Return', 'LTV Buffer', 'Occ. Cushion', 'Est. IRR']
        fig_r = go.Figure(go.Scatterpolar(
            r=score_raw + [score_raw[0]], theta=cats_radar + [cats_radar[0]],
            fill='toself', fillcolor='rgba(212,168,67,0.12)',
            line=dict(color=C['gold'], width=2.5), name='Deal Score'
        ))
        fig_r.update_layout(
            **{k: v for k, v in PLOT_LAYOUT.items() if k not in ['xaxis', 'yaxis']},
            polar=dict(
                bgcolor='rgba(20,28,40,0.5)',
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#243045',
                                tickfont=dict(color='#5A7090', size=8)),
                angularaxis=dict(gridcolor='#243045', tickfont=dict(color='#E2E8F0', size=10))
            ),
            title=f'CRE Deal Quality — {asset_type}', height=360,
            title_font=dict(color='#E2E8F0', size=13), showlegend=False
        )
        st.plotly_chart(fig_r, use_container_width=True)

        overall = int(sum(score_raw) / len(score_raw))
        score_col = C['green'] if overall >= 70 else C['amber'] if overall >= 50 else C['red']
        label = 'STRONG BUY' if overall >= 70 else 'INVESTABLE' if overall >= 50 else 'NEEDS WORK'
        passed_count = sum(1 for _, p, *_ in checks if p)
        st.markdown(f"""
        <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;
                    padding:20px;text-align:center;margin-top:8px">
          <div style="font-size:10px;color:#5A7090;text-transform:uppercase;letter-spacing:2px;
                      font-family:'IBM Plex Mono',monospace">Overall Deal Score</div>
          <div style="font-family:'Syne',sans-serif;font-size:56px;font-weight:800;
                      color:{score_col};line-height:1.1;margin:8px 0">{overall}</div>
          <div class="badge {'badge-green' if overall >= 70 else 'badge-amber' if overall >= 50 else 'badge-red'}"
               style="font-size:12px">{label}</div>
          <div style="font-size:11px;color:#5A7090;margin-top:8px;font-family:'IBM Plex Mono',monospace">
            {passed_count} / {len(checks)} checks passed · {asset_type}
          </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 7 — FULL REPORT
# ════════════════════════════════════════════════════════════
with tab7:
    st.markdown('<div class="section-title">📋 <span>Full Investment Report</span></div>', unsafe_allow_html=True)
    st.markdown(f"**{project_name}** · {asset_type} · {total_sqft:,} SF · {num_units} Tenants")

    report_rows = [
        ('── PROPERTY ──', '', ''),
        ('Acquisition Price', f'${price:,.0f}', f'${price_per_sf:.0f}/SF'),
        ('Total Leasable Area', f'{total_sqft:,} SF', f'{num_units} tenants'),
        ('Stabilized Value', f'${stabilized_value:,.0f}', f'@ {exit_cap}% cap'),
        ('Value-Add Spread', f'${value_add:,.0f}', ''),
        ('CapEx / TI Allowance', f'${capex:,.0f}', f'${capex / total_sqft:.0f}/SF'),
        ('Closing Costs', f'${closing:,.0f}', ''),
        ('', '', ''),
        ('── FINANCING ──', '', ''),
        ('Loan Amount', f'${loan:,.0f}', f'{r["ltv"]:.1f}% LTV'),
        ('Down Payment', f'${r["down_payment"]:,.0f}', ''),
        ('Interest Rate', f'{rate:.3f}%', f'{term // 12} yr term'),
        ('Monthly P&I', f'${r["payment"]:,.0f}', f'I/O: ${io_payment:,.0f}'),
        ('I/O Period', f'{io_period} months', f'Monthly CF: ${io_cf_monthly:,.0f}'),
        ('Total Interest', f'${r["total_interest"]:,.0f}', ''),
        ('', '', ''),
        ('── INCOME ──', '', ''),
        ('Gross Rent / Year', f'${rent_annual:,.0f}', f'${rent_per_sf:.2f}/SF'),
        ('Gross Rent / Month', f'${rent_monthly:,.0f}', ''),
        ('Vacancy Assumption', f'{vacancy_pct:.1f}%', ''),
        ('Effective Gross Income', f'${rent_monthly * (1 - vacancy_pct / 100) * 12:,.0f}', ''),
        ('', '', ''),
        ('── EXPENSES ──', '', ''),
        (f'OpEx ({opex_type})', f'{opex_total:.1f}%', ''),
        ('Property Tax', f'{tax_pct:.1f}% of price', f'${price * tax_pct / 100:,.0f}/yr'),
        ('Insurance', f'{ins_pct:.1f}% of price', f'${price * ins_pct / 100:,.0f}/yr'),
        ('', '', ''),
        ('── RETURNS ──', '', ''),
        ('Net Operating Income', f'${noi_annual:,.0f}', f'${noi_per_sf:.2f}/SF'),
        ('Annual Cash Flow', f'${r["annual_cf"]:,.0f}', f'${r["monthly_cf"]:,.0f}/mo'),
        ('Cap Rate', f'{r["cap_rate"]:.2f}%', ''),
        ('Yield on Cost', f'{yield_on_cost:.2f}%', f'Spread: {spread_to_cap:+.2f}%'),
        ('Cash-on-Cash', f'{r["coc"]:.2f}%', ''),
        ('DSCR', f'{r["dscr"]:.2f}x', ''),
        ('Breakeven Occupancy', f'{breakeven_occ:.1f}%', ''),
        ('', '', ''),
        ('── STRESS TEST ──', '', ''),
        ('Anchor Loss — Worst Month CF',
         f'${float(stress_df[stress_df["Scenario"] == "⚡ Anchor Loss (25%)"]["Cash Flow"].min()):,.0f}', ''),
        ('Cascade Vacancy — Worst Month CF',
         f'${float(stress_df[stress_df["Scenario"] == "⚠️ Cascade Vacancy (40%)"]["Cash Flow"].min()):,.0f}', ''),
        ('Re-Leasing Period', f'{reabsorption} months', ''),
        ('Total Re-Leasing Cost', f'${total_relet_cost:,.0f}', f'{num_units} tenants'),
        ('', '', ''),
        (f'── EXIT (YEAR {hold_yrs}) ──', '', ''),
        ('Exit NOI', f'${exit_noi:,.0f}', f'{rent_escal}% escalation'),
        ('Exit Value (Cap Rate)', f'${exit_value_cap:,.0f}', f'@ {exit_cap}% cap'),
        ('Exit Value (Appreciation)', f'${prop_vals[-1]:,.0f}', f'{app_rate}% / yr'),
        ('Net Sale Proceeds', f'${sale_net:,.0f}', '3% selling costs'),
        ('Equity at Exit', f'${equity_exit:,.0f}', ''),
        ('Total Cash Flow (hold)', f'${sum(cf_proj):,.0f}', ''),
        ('Estimated IRR', f'{irr_approx:.1f}%', 'Levered, approximate'),
    ]
    df_report = pd.DataFrame(report_rows, columns=['Item', 'Value', 'Notes'])
    st.dataframe(df_report, use_container_width=True, hide_index=True, height=900)

    csv = df_report.to_csv(index=False)
    st.download_button("⬇️ Download Full Report (CSV)", data=csv,
                       file_name=f"{project_name.replace(' ', '_')}_PropIQ_CRE.csv", mime='text/csv')

# ── FOOTER ────────────────────────────────────────────────────
st.markdown(f"""
<div style='text-align:center;padding:40px 0 20px;color:#243045;font-size:11px;
            font-family:"IBM Plex Mono",monospace'>
  PropIQ Commercial · CRE Investment Analyzer · Not financial advice · {asset_type}
</div>
""", unsafe_allow_html=True)
