# Content Pipeline Weekly Automation

## Cron Jobs

Two cron jobs are configured in Hermes for automatic weekly content generation:

1. **flux-conteudo-semanal**: Every Monday at 09:00 UTC (06:00 BRT)
   - Triggers: flux-agencia-conteudo, flux-agencia-pipeline
   - Generates: Weekly editorial calendar (7 days of content)

2. **flux-anuncios-semanal**: Every Monday at 09:30 UTC (06:30 BRT)
   - Triggers: flux-agencia-copywriting, flux-agencia-trafego, flux-agencia-pipeline
   - Generates: 8 ad copies + traffic strategy

## Manual Triggers

- "pipeline flux" → full pipeline (content + ads + traffic)
- "gerar conteúdo semanal" → editorial calendar only
- "criar campanha" → ads + traffic strategy only

## Pipeline Flow

```
Client Briefing → Pipeline
  ├── 📊 Conteúdo Semanal (7 days)
  │   ├── Carrosséis (SVG)
  │   ├── Reels roteiros
  │   ├── Posts de feed
  │   └── Stories sequência
  ├── 🔥 Anúncios (8 cópias)
  │   ├── Topo funil (3 cópias)
  │   ├── Meio funil (3 cópias)
  │   └── Fundo funil (2 cópias)
  ├── 📈 Estratégia de Tráfego
  │   ├── Orçamento distribuído
  │   ├── Públicos segmentados
  │   └── KPIs metas
  └── ⚙️ CRM (se solicitado)
      ├── Tags
      ├── Automações
      └── Templates WhatsApp
```