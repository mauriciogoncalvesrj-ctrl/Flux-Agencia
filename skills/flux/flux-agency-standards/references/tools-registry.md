# Flux Tools Registry

Catálogo unificado de ferramentas disponíveis para skills da Agência Flux. Consultar este arquivo ao decidir qual ferramenta usar para implementação.

---

## Ferramentas Ativas

### Meta Ads
| Atributo | Valor |
|----------|-------|
| **Tipo** | Advertising |
| **Método** | MCP `mcp_meta_ads_*` + Graph API direta |
| **MCP** | ✅ (insights, campaigns, ad accounts, ad creatives) |
| **CLI** | ✅ (`/opt/data/hermes-agent/tools/clis/meta-ads.js`) |
| **Guide** | `flux-meta-ads-balance-alert` (saldo), `flux-meta-ads-relatorio` (relatórios) |

**Pitfall crítico:** `balance` do MCP é saldo contábil, não real. Para saldo pré-pago, usar Graph API `funding_source_details.display_string` com `act_` prefixado.

**Contas mapeadas:**
| Cliente | Account ID | act_ ID |
|---------|------------|---------|
| Taciana | TLERdShLsQMxv59zM9Yw | act_911737697183748 |
| Alpha | zyGxJmMNtmVauwSV18XH | act_912031229902602 |
| Proton | ajkGuHbvw1zQYAJ3Nz9i | act_392106056202806 |
| Luana | uJQ9bW3rTXMd4si0eNqZ | act_1073353887241970 |

---

### GoHighLevel (GHL)
| Atributo | Valor |
|----------|-------|
| **Tipo** | CRM / Marketing Automation |
| **Método** | MCP `mcp_ghl_*` |
| **MCP** | ✅ (contacts, pipelines, campaigns, SMS, email, automations) |
| **Guide** | `ghl-mcp-server` skill |

---

### Fal.ai
| Atributo | Valor |
|----------|-------|
| **Tipo** | AI Image/Video/Audio Generation |
| **Método** | MCP `mcp_fal_ai_*` |
| **MCP** | ✅ (text-to-image, image-to-image, video, audio, upscale) |
| **Guide** | `fal-ai` skill |

**Modelo padrão do usuário:** `fal-ai/bytedance/seedream/v4.5/text-to-image`

---

### Open Design
| Atributo | Valor |
|----------|-------|
| **Tipo** | Design UI / Visual Editor |
| **Método** | HTTP API |
| **URL** | `design.somosflux.com.br:7456` |
| **Guide** | `open-design` skill |

---

### Paperclip
| Atributo | Valor |
|----------|-------|
| **Tipo** | Document Management |
| **Método** | HTTP API |
| **URL** | `paperclip.somosflux.com.br` |
| **Guide** | `paperclip-admin` skill |
| **Credenciais** | `FluxIA2026!` (reset 2026-05-09) |

---

### Traefik
| Atributo | Valor |
|----------|-------|
| **Tipo** | Reverse Proxy / Routing |
| **Método** | Docker labels + config files |
| **Guide** | `docker-traefik-routing` skill |

---

## Ferramentas com Setup Pendente

### X/Twitter
| Atributo | Valor |
|----------|-------|
| **Tipo** | Social Media Monitoring |
| **Método** | xurl CLI (`~/.local/bin/xurl`) |
| **Status** | ⚠️ Instalado mas sem credenciais de API |
| **Guide** | `flux-x-monitor` skill |

---

### Google Ads
| Atributo | Valor |
|----------|-------|
| **Tipo** | Advertising |
| **Método** | MCP `mcp_google_ads_*` |
| **Status** | 🔧 Setup pendente |
| **Guide** | `google-ads-mcp-setup` skill |

---

## Scripts Fixos

| Script | Propósito | Cron Job |
|--------|-----------|----------|
| `/opt/data/scripts/meta_ads_real_balance.py` | Consulta saldo real via Graph API | `1ca2c29ca1d8` — 9AM BRT diário |
| `/opt/data/scripts/meta_ads_motiva_sms_context.sh` | Wrapper SMS teste Motiva | `744263672cb4` — 9AM BRT diário (TESTE) |

---

## Cron Jobs da Flux

| Job ID | Nome | Schedule | Modo |
|--------|------|----------|------|
| `1ca2c29ca1d8` | Meta Ads - Alerta Diário de Saldo | `0 12 * * *` (9AM BRT) | Script determinístico |
| `744263672cb4` | Flux Meta Ads Balance Check (TESTE SMS) | `0 12 * * *` (9AM BRT) | Script + SMS teste |
| `e3325069a1b1` | Hermes GitHub Backup | `0 3 * * *` (00:00 BRT) | Script Python |

---

## Serviços e Domínios

| Serviço | Domínio | Porta |
|---------|---------|-------|
| Hermes Agent | (interno) | 7777 |
| OpenClaw | (interno) | 3101 |
| Paperclip | paperclip.somosflux.com.br | 3100 |
| WebUI | hub.somosflux.com.br | (Traefik) |
| Open Design | design.somosflux.com.br | 7456 |

---

## Como usar este registry

1. Skills devem referenciar ferramentas desta tabela na seção "Tool Integrations"
2. Sempre preferir MCP quando disponível (integração nativa)
3. Scripts fixos são para tarefas determinísticas que não dependem de LLM
4. Atualizar este arquivo quando novas ferramentas forem adicionadas
