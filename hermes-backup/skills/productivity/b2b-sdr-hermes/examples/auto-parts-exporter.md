# Example: Auto Parts Exporter SDR Configuration

## Company Profile

```
Brand: Zhonghe Auto Parts Co., Ltd (中和汽配)
Industry: Automotive aftermarket parts
Products: Brake pads, filters, suspension components
Target Markets: Russia, Kazakhstan, UAE, Nigeria, Saudi Arabia
Owner Language: zh (Chinese)
CRM: Google Sheets
Channels: WhatsApp (primary), Email (formal), Telegram (Russia/CIS)
```

## Setup Commands

```bash
# Install the skill
hermes skills install github:iPythoning/b2b-sdr-hermes-skill

# Configure
hermes config set sdr.brand_name "Zhonghe Auto Parts"
hermes config set sdr.industry "automotive aftermarket"
hermes config set sdr.owner_language "zh"
hermes config set sdr.crm_type "google_sheets"

# Connect WhatsApp
hermes whatsapp

# Start a session and say:
# "Set up SDR for Zhonghe Auto Parts. We export brake pads, filters, and
#  suspension parts to Russia, Middle East, and Africa. CRM in Google Sheets."
```

## Expected Behavior

### Inbound WhatsApp (Russian buyer)

```
Buyer: Добрый день, нужны колодки для Toyota Camry, 500 комплектов
SDR:   Добрый день! Для Toyota Camry у нас есть керамические и полуметаллические
       колодки. 500 комплектов — FOB Шанхай, отгрузка за 7 дней.
       Какой тип колодок предпочитаете?
```

CRM auto-created: name=unknown, country=RU, language=ru, product_interest=brake_pads, quantity_signal=500, status=new, icp_score=7

### Weekly Report to Owner

```
## 本周销售报告 (2026-W15)

| 指标 | 本周 | 上周 | 变化 |
|------|------|------|------|
| 新线索 | 12 | 8 | +50% |
| 合格线索 | 5 | 3 | +67% |
| 报价发送 | 3 | 2 | +50% |
| 成交 | 1 | 0 | ↑ |

### Top 5 机会
| 客户 | 国家 | 产品 | 数量 | 状态 |
|------|------|------|------|------|
| Avtodetal LLC | 🇷🇺 | 刹车片 | 2000套 | negotiating |
| Al-Faisal Trading | 🇸🇦 | 滤芯 | 5000件 | quote_sent |
| ...
```
