# Meta Ads MCP — Referência Técnica

## Visão Geral

O `pipeboard-co/meta-ads-mcp` (⭐881) é o MCP server mais usado para gerenciar campanhas Meta Ads via IA. Permite criar, analisar e otimizar campanhas Facebook/Instagram diretamente pelo agente.

## Modos de Uso

### Remoto (Pipeboard) — MAIS FÁCIL
- URL: `https://mcp.pipeboard.co/meta-ads-mcp`
- Token em: pipeboard.co/api-tokens
- Zero setup técnico, autentica pelo Pipeboard
- Também disponível: Google Ads e TikTok Ads
- **Risco**: Token passa pelo servidor do Pipeboard (intermediação)

### Local (Self-Hosted) — MAIS SEGURO
- Instalar via: `npx -y meta-ads-mcp`
- Requer Meta Developer App + OAuth
- Token fica local, comunicação direta com Meta API
- Config no Hermes config.yaml:
```yaml
mcp_servers:
  meta-ads:
    command: "npx"
    args: ["-y", "meta-ads-mcp"]
    env:
      META_ACCESS_TOKEN: "${META_ACCESS_TOKEN}"
      META_AD_ACCOUNT_ID: "${META_AD_ACCOUNT_ID}"
```

## 29 Ferramentas Disponíveis

- **Contas**: get_ad_accounts, get_account_info, get_account_pages
- **Campanhas**: get_campaigns, get_campaign_details, create_campaign, get_insights
- **Conjuntos**: get_adsets, get_adset_details, create_adset, update_adset
- **Anúncios**: get_ads, get_ad_details, get_ad_creatives, create_ad, update_ad
- **Criativos**: create_ad_creative, update_ad_creative, upload_ad_image, get_ad_image
- **Segmentação**: search_interests, get_interest_suggestions, validate_interests, search_behaviors, search_demographics, search_geo_locations
- **Orçamento**: create_budget_schedule
- **Busca**: search (genérico)
- **Auth**: get_login_link

## Notas de Segurança

- Auditoria (issue #69): score 0/100 — 167 vulnerabilidades encontradas
- Riscos: exfiltração de dados, injeção, exposição de credenciais
- Para uso com campanhas de clínica de estética: risco gerenciável (dados não são sensíveis tipo CPF/cartão)
- Recomendação: usar modo LOCAL (self-hosted) quando possível
- Escopo OAuth limitado: `business_management, public_profile, pages_show_list, pages_read_engagement`

## Status de Configuração em Hermes

- Configurado no config.yaml como `meta-ads` (modo local via npx)
- **PENDENTE**: precisam das variáveis META_ACCESS_TOKEN e META_AD_ACCOUNT_ID no .env
- Também configurados: `ghl` (GoHighLevel MCP) e `n8n` (n8n MCP server)