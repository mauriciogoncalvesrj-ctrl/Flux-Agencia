#!/usr/bin/env python3
"""
Gera relatório semanal/mensal de campanhas Meta Ads por cliente.
Suporta separação por unidades (ex: Luana Jundiaí / Cajamar).
Uso: python3 gerar-relatorio.py [--semanal|--mensal] [--contas act_xxx,act_yyy] [--all]
Output: JSON com relatórios por conta/unidade.
"""
import json
import urllib.parse
import subprocess
import sys
import re
import copy
from datetime import datetime, timedelta

# --- Config ---
ENV_PATH = "/opt/data/.env"

DISPLAY_NAMES = {
    "act_912031229902602": "ALPHA TRANSFORMADORES",
    "act_3572634436284536": "C01 - ALPHA TRANSFORMADORES",
    "act_392106056202806": "PROTON TRANSFORMADORES",
    "act_1073353887241970": "Luana Sampaio",
    "act_1308631537809149": "BORGATTE",
    "act_911737697183748": "TACIANA",
    "act_5182254948472799": "THABATA CAMARGO",
    "act_802273699351886": "KORP NUTRA",
    "act_1415550266416617": "FLUX",
    "act_26835555129380153": "LARISSA MANSO",
    "act_153133192304265": "GABI GONÇALVES",
    "act_1755778031574400": "TACIANA BKP",
    "act_1095489361869934": "MEDECINE",
}

# Accounts that need unit-level splitting
# Format: act_id -> list of unit definitions
# Each unit: {"name": "Display Name", "match": regex_pattern}
# "shared" campaigns are split 50/50 among all units
UNIT_SPLIT = {
    "act_1073353887241970": {
        "units": [
            {"name": "Jundiaí", "match": r"\[JUNDIA[IÍ]\]"},
            {"name": "Cajamar", "match": r"\[CAJAMAR\]"},
        ],
        "shared_match": r"Cajamar e Jundia[iíí]",
        "shared_split": ["Jundiaí", "Cajamar"],  # split 50/50
    },
}

ALL_ACCOUNTS = list(DISPLAY_NAMES.keys())

def get_token():
    with open(ENV_PATH, 'r') as f:
        for line in f:
            if line.startswith('META_ACCESS_TOKEN='):
                return line.strip().split('=', 1)[1]
    raise ValueError("META_ACCESS_TOKEN not found")

def api(path, token, params=None, timeout=15):
    """Call Graph API and return parsed JSON."""
    url = f"https://graph.facebook.com/v22.0{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    sep = "&" if "?" in url else "?"
    url += f"{sep}access_token={token}"
    result = subprocess.run(["curl", "-s", "-m", str(timeout), url], capture_output=True, text=True, timeout=timeout+5)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stdout[:500]}

def fmt_brl(value, decimals=2):
    if isinstance(value, str): value = float(value)
    if value >= 1000:
        return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{value:.{decimals}f}".replace(".", ",")

def fmt_int(value):
    if isinstance(value, str): value = int(value)
    return f"{value:,}".replace(",", ".")

def get_date_range(mode):
    today = datetime.now()
    if mode == "semanal":
        until_day = today - timedelta(days=1)
        since = until_day - timedelta(days=6)
    else:
        last_day = today.replace(day=1) - timedelta(days=1)
        since = last_day.replace(day=1)
        until_day = last_day
    display = f"{since.strftime('%d/%m/%Y')} até {until_day.strftime('%d/%m/%Y')}"
    return since.strftime("%Y-%m-%d"), until_day.strftime("%Y-%m-%d"), display

def extract_metric(row, action_type, is_cost=False):
    key = "cost_per_action_type" if is_cost else "actions"
    for item in row.get(key, []):
        if item.get("action_type") == action_type:
            return float(item["value"]) if is_cost else int(item["value"])
    return 0

def get_campaign_insights(act_id, token, since, until):
    data = api(f"/{act_id}/insights", token, {
        "time_range": json.dumps({"since": since, "until": until}),
        "fields": "campaign_name,campaign_id,objective,impressions,reach,clicks,spend,ctr,actions,cost_per_action_type",
        "level": "campaign",
        "limit": "20",
    })
    return data.get("data", [])

def get_ad_insights(act_id, token, since, until):
    data = api(f"/{act_id}/insights", token, {
        "time_range": json.dumps({"since": since, "until": until}),
        "fields": "ad_name,ad_id,campaign_name,impressions,spend,ctr,actions,cost_per_action_type",
        "level": "ad",
        "limit": "50",
    })
    return data.get("data", [])

def get_account_insights(act_id, token, since, until):
    data = api(f"/{act_id}/insights", token, {
        "time_range": json.dumps({"since": since, "until": until}),
        "fields": "impressions,reach,clicks,spend,ctr,actions,cost_per_action_type",
        "level": "account",
    })
    rows = data.get("data", [])
    return rows[0] if rows else None

def get_ig_permalink(ad_id, token):
    ad = api(f"/{ad_id}", token, {"fields": "creative{id}"})
    cid = ad.get("creative", {}).get("id", "")
    if not cid: return ""
    c = api(f"/{cid}", token, {"fields": "effective_instagram_media_id"})
    mid = c.get("effective_instagram_media_id", "")
    if not mid: return ""
    m = api(f"/{mid}", token, {"fields": "permalink"})
    return m.get("permalink", "").replace("\\/", "/")

def get_balance(act_id, token):
    data = api(f"/{act_id}", token, {"fields": "funding_source_details,spend_cap,amount_spent,currency"})
    fsd = data.get("funding_source_details", {})
    display = fsd.get("display_string", "N/A")
    ftype = fsd.get("type", 0)
    if ftype == 1:
        return "💳 Cartão de crédito", None
    if "R$" in display:
        nums = re.findall(r'R\$\s*([\d.,]+)', display)
        bal = float(nums[0].replace(".", "").replace(",", ".")) if nums else 0
        return f"R$ {fmt_brl(bal)}", bal
    return "R$ 0,00", 0

def detect_unit(campaign_name, unit_config):
    """Detect which unit a campaign/ad belongs to."""
    # Check shared campaigns first (split among multiple units)
    shared_pattern = unit_config.get("shared_match", "")
    if shared_pattern and re.search(shared_pattern, campaign_name, re.IGNORECASE):
        return "shared"
    
    # Check unit-specific patterns
    for unit_def in unit_config["units"]:
        if re.search(unit_def["match"], campaign_name, re.IGNORECASE):
            return unit_def["name"]
    
    return None  # Unknown - will go to general report

def build_report_text(name, period_display, metrics, top5=None, balance_line=""):
    """Build report text from metrics dict."""
    report = f"Olá {name}! Segue abaixo relatório das campanhas do META ADS\n"
    if balance_line:
        report += f"{balance_line}\n"
    report += f"\nPeríodo: {period_display}\n\n"
    report += f"Impressões: {fmt_int(metrics['impressions'])}\n"
    report += f"Alcance: {fmt_int(metrics['reach'])}\n"
    report += f"Taxa de Interação: {metrics['eng_rate']:.2f}%".replace(".", ",") + "\n"
    report += f"Cliques: {fmt_int(metrics['clicks'])}\n"
    if metrics['msgs'] > 0:
        report += f"Mensagem: {metrics['msgs']}\n"
        report += f"Custo por mensagem: R$ {fmt_brl(metrics['cpm'])}\n"
    report += f"Valor investido: R$ {fmt_brl(metrics['spend'])}"

    if top5:
        report += "\n\nRanking TOP 5 Criativos:"
        medals = ["🏆", "🥈", "🥉", "4.", "5."]
        for i, ad in enumerate(top5):
            ctr_str = f"{ad['ctr']:.2f}%".replace(".", ",")
            report += f"\n{medals[i]} {i+1}. {ad['name']}"
            report += f"\nMensagens: {ad['msgs']} | CPA: R$ {fmt_brl(ad['cpa'])} | CTR: {ctr_str}"
            if ad.get("ig_link"):
                report += f"\n🔗 {ad['ig_link']}"
            report += "\n"
    
    return report

def generate_report(act_id, act_name, token, since, until, period_display, include_balance=False):
    """Generate report(s) for an account. Returns list of reports."""
    acct = get_account_insights(act_id, token, since, until)
    if not acct or float(acct.get("spend", 0)) == 0:
        return []
    
    # Check if this account needs unit splitting
    if act_id in UNIT_SPLIT:
        return generate_unit_reports(act_id, act_name, token, since, until, period_display, include_balance)
    
    # Single-unit account (standard report)
    metrics = {
        "impressions": int(acct.get("impressions", 0)),
        "reach": int(acct.get("reach", 0)),
        "clicks": int(acct.get("clicks", 0)),
        "spend": float(acct.get("spend", 0)),
        "msgs": extract_metric(acct, "onsite_conversion.total_messaging_connection"),
        "cpm": extract_metric(acct, "onsite_conversion.total_messaging_connection", is_cost=True),
        "eng_rate": 0,
    }
    engagement = extract_metric(acct, "page_engagement")
    metrics["eng_rate"] = (engagement / metrics["impressions"] * 100) if metrics["impressions"] > 0 else 0

    balance_line = ""
    if include_balance:
        bal_str, _ = get_balance(act_id, token)
        balance_line = f"\n💰 Saldo atual: {bal_str}"

    # Top 5 ads
    ads_data = get_ad_insights(act_id, token, since, until)
    top5 = build_top5(ads_data, token)

    report = build_report_text(act_name, period_display, metrics, top5, balance_line)
    return [{"act_id": act_id, "name": act_name, "unit": None, "report": report}]

def build_top5(ads_data, token, unit_filter=None):
    """Build TOP 5 ads list from ad-level insights."""
    ad_list = []
    for row in ads_data:
        # If unit filtering, skip ads not in this unit
        if unit_filter and row.get("campaign_name"):
            continue  # This is handled externally
        
        name = row.get("ad_name", "?")
        ad_id = row.get("ad_id", "")
        ad_spend = float(row.get("spend", 0))
        ad_ctr = float(row.get("ctr", 0))
        ad_msgs = extract_metric(row, "onsite_conversion.total_messaging_connection")
        ad_cpa = ad_spend / ad_msgs if ad_msgs > 0 else 0
        ad_list.append({"name": name, "ad_id": ad_id, "msgs": ad_msgs, "cpa": ad_cpa, "ctr": ad_ctr, "ig_link": None})
    
    ad_list.sort(key=lambda x: x["msgs"], reverse=True)
    top5 = [a for a in ad_list[:5] if a["msgs"] > 0]
    
    # Get Instagram links (only for top 5 to save API calls)
    for ad in top5:
        ad["ig_link"] = get_ig_permalink(ad["ad_id"], token)
    
    return top5

def generate_unit_reports(act_id, act_name, token, since, until, period_display, include_balance):
    """Generate separate reports for each unit within an account."""
    unit_config = UNIT_SPLIT[act_id]
    unit_names = [u["name"] for u in unit_config["units"]]
    
    # Get campaign-level insights
    campaigns = get_campaign_insights(act_id, token, since, until)
    
    # Initialize unit metrics
    unit_metrics = {}
    for uname in unit_names:
        unit_metrics[uname] = {
            "impressions": 0, "reach": 0, "clicks": 0, "spend": 0.0,
            "msgs": 0, "cpm_total": 0.0, "engagement": 0, "campaigns": []
        }
    
    # Get ad-level insights grouped by unit
    ads_data = get_ad_insights(act_id, token, since, until)
    unit_ads = {uname: [] for uname in unit_names}
    
    # Assign campaigns to units
    for camp in campaigns:
        cname = camp.get("campaign_name", "")
        unit = detect_unit(cname, unit_config)
        
        camp_spend = float(camp.get("spend", 0))
        camp_imp = int(camp.get("impressions", 0))
        camp_reach = int(camp.get("reach", 0))
        camp_clicks = int(camp.get("clicks", 0))
        camp_msgs = extract_metric(camp, "onsite_conversion.total_messaging_connection")
        camp_cpm = extract_metric(camp, "onsite_conversion.total_messaging_connection", is_cost=True)
        camp_eng = extract_metric(camp, "page_engagement")
        
        if unit == "shared":
            # Split evenly among shared units
            split_units = unit_config["shared_split"]
            per_unit = len(split_units)
            for su in split_units:
                if su in unit_metrics:
                    unit_metrics[su]["impressions"] += camp_imp // per_unit
                    unit_metrics[su]["reach"] += camp_reach // per_unit
                    unit_metrics[su]["clicks"] += camp_clicks // per_unit
                    unit_metrics[su]["spend"] += camp_spend / per_unit
                    unit_metrics[su]["msgs"] += camp_msgs // per_unit
                    unit_metrics[su]["cpm_total"] += camp_cpm / per_unit
                    unit_metrics[su]["engagement"] += camp_eng // per_unit
        elif unit and unit in unit_metrics:
            unit_metrics[unit]["impressions"] += camp_imp
            unit_metrics[unit]["reach"] += camp_reach
            unit_metrics[unit]["clicks"] += camp_clicks
            unit_metrics[unit]["spend"] += camp_spend
            unit_metrics[unit]["msgs"] += camp_msgs
            unit_metrics[unit]["cpm_total"] += camp_cpm
            unit_metrics[unit]["engagement"] += camp_eng
            unit_metrics[unit]["campaigns"].append(cname)
    
    # Assign ads to units
    for ad in ads_data:
        ad_name = ad.get("ad_name", "")
        camp_name = ad.get("campaign_name", "")
        
        # Try to detect unit from ad name or campaign name
        unit = detect_unit(ad_name, unit_config)
        if not unit or unit == "shared":
            unit = detect_unit(camp_name, unit_config)
        
        if unit == "shared":
            split_units = unit_config["shared_split"]
            for su in split_units:
                if su in unit_ads:
                    unit_ads[su].append(ad)
        elif unit and unit in unit_ads:
            unit_ads[unit].append(ad)
    
    # Generate per-unit reports
    reports = []
    
    for uname in unit_names:
        m = unit_metrics[uname]
        if m["spend"] == 0:
            continue  # Skip units with no spend
        
        # Calculate CPM from individual values
        cpm = m["spend"] / m["msgs"] if m["msgs"] > 0 else 0
        eng_rate = (m["engagement"] / m["impressions"] * 100) if m["impressions"] > 0 else 0
        
        metrics = {
            "impressions": m["impressions"],
            "reach": m["reach"],
            "clicks": m["clicks"],
            "spend": m["spend"],
            "msgs": m["msgs"],
            "cpm": cpm,
            "eng_rate": eng_rate,
        }
        
        # Get TOP 5 for this unit
        unit_ad_list = []
        for row in unit_ads[uname]:
            ad_spend = float(row.get("spend", 0))
            ad_ctr = float(row.get("ctr", 0))
            ad_msgs = extract_metric(row, "onsite_conversion.total_messaging_connection")
            ad_cpa = ad_spend / ad_msgs if ad_msgs > 0 else 0
            unit_ad_list.append({
                "name": row.get("ad_name", "?"),
                "ad_id": row.get("ad_id", ""),
                "msgs": ad_msgs,
                "cpa": ad_cpa,
                "ctr": ad_ctr,
            })
        
        unit_ad_list.sort(key=lambda x: x["msgs"], reverse=True)
        top5_unit = [a for a in unit_ad_list[:5] if a["msgs"] > 0]
        
        # Get Instagram links for top 5
        for ad in top5_unit:
            ad["ig_link"] = get_ig_permalink(ad["ad_id"], token)
        
        display_name = f"{act_name} — UNIDADE {uname.upper()}"
        balance_line = ""
        if include_balance:
            bal_str, _ = get_balance(act_id, token)
            balance_line = f"\n💰 Saldo atual: {bal_str}"
        
        report = build_report_text(display_name, period_display, metrics, top5_unit, balance_line)
        reports.append({"act_id": act_id, "name": display_name, "unit": uname, "report": report})
    
    return reports

def main():
    mode = "semanal"
    accounts_filter = None
    for arg in sys.argv[1:]:
        if arg == "--mensal": mode = "mensal"
        elif arg == "--semanal": mode = "semanal"
        elif arg.startswith("--contas="): accounts_filter = arg.split("=")[1].split(",")
        elif arg == "--all": accounts_filter = None

    token = get_token()
    since, until, period_display = get_date_range(mode)
    accounts = accounts_filter if accounts_filter else ALL_ACCOUNTS

    all_reports = []
    for act_id in accounts:
        if act_id not in DISPLAY_NAMES: continue
        name = DISPLAY_NAMES[act_id]
        include_balance = (mode == "mensal")
        reports = generate_report(act_id, name, token, since, until, period_display, include_balance)
        all_reports.extend(reports)

    output = {"mode": mode, "period": period_display, "since": since, "until": until, "reports": all_reports}
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()