# Template de Entrega Semanal — Agência Flux

> Entrega: Domingo noite → Segunda manhã
> Responsável: Atlas (geração) + Mauricio (aprovação)
> Formato: PDF profissional + resumo Telegram
>
> *Versão 1.0 · 2026-05-12*

---

## 📅 Cronograma

| Quando | O quê | Quem |
|---|---|---|
| **Sexta 18h** | Atlas coleta dados da semana (Meta Ads, GHL, Google Ads) | Atlas |
| **Sábado 10h** | Atlas gera primeira versão dos relatórios | Atlas |
| **Sábado 18h** | Versão preliminar disponível para revisão | Atlas → Mauricio |
| **Domingo 15h** | Mauricio revisa e solicita ajustes | Mauricio |
| **Domingo 20h** | Atlas aplica correções e gera PDFs finais | Atlas |
| **Segunda 9h** | Relatórios finais enviados aos clientes | Atlas |

---

## 📊 Estrutura do Relatório Semanal por Cliente

### Capa
- Logo da clínica
- Nome do cliente
- Período: `DD/MM/AAAA — DD/MM/AAAA`
- "Relatório Semanal de Performance — [Plano: Start/Conversão/Autônomo]"

### Seção 1: Resumo Executivo (1 página)
```
📈 RESULTADOS DA SEMANA

Investimento total: R$ X.XXX,XX
Leads gerados: XX
Custo por lead: R$ XX,XX
Mensagens recebidas: XX
Agendamentos realizados: XX
Taxa de conversão lead → agendamento: XX%

📊 Comparação com semana anterior:
- Investimento: +X% / -X%
- Leads: +X% / -X%
- CPL: +X% / -X%
```

### Seção 2: Meta Ads Performance
- Métricas principais (impressões, alcance, CTR, CPC, CPM)
- TOP 5 criativos com links do Instagram
- Gráfico de tendência (investimento × leads nos últimos 30 dias)
- Distribuição por posicionamento (Feed, Stories, Reels)

### Seção 3: Funil de Conversão (GHL)
- Leads novos → Mensagens → Agendamentos → Comparecimentos
- Taxa de conversão em cada etapa
- Gargalos identificados (ex: "30% dos leads não respondem após primeiro contato")
- Oportunidades de automação sugeridas

### Seção 4: Google Ads (se aplicável)
- Métricas principais
- TOP 5 palavras-chave
- TOP 3 anúncios

### Seção 5: Análise Qualitativa
- O que funcionou essa semana (2-3 insights)
- O que pode melhorar (2-3 pontos)
- Oportunidades identificadas (1-2)
- Recomendações para próxima semana

### Seção 6: Próximos Passos
```
✅ Ações concluídas esta semana:
1. [Ação]
2. [Ação]

🔄 Em andamento:
1. [Ação] — previsão: [data]

📋 Planejado para próxima semana:
1. [Ação]
2. [Ação]
```

---

## 📋 Checklist de Geração

### Coleta de Dados (sexta)
- [ ] Puxar métricas Meta Ads (todas as contas ativas)
- [ ] Puxar dados do GHL (pipeline, conversões)
- [ ] Puxar dados Google Ads (se aplicável)
- [ ] Calcular variação vs semana anterior
- [ ] Salvar dados brutos em `data/semanal/YYYY-MM-DD/`

### Geração (sábado)
- [ ] Gerar relatório individual por cliente ativo
- [ ] Aplicar template visual (HTML → PDF via Puppeteer)
- [ ] Incluir gráficos (CSS/SVG inline)
- [ ] Verificar glossario.md — "Sistema Flux 360", nunca "GHL"
- [ ] Salvar PDFs em `entregas/semanal/YYYY-MM-DD/`

### Revisão (domingo)
- [ ] Enviar resumo Telegram para Mauricio com link dos PDFs
- [ ] Aguardar feedback
- [ ] Aplicar correções
- [ ] Gerar versão final

### Envio (segunda)
- [ ] Enviar relatório para cada cliente via Telegram/WhatsApp
- [ ] Arquivar versão final no GHL (Documents)
- [ ] Atualizar `status-flux.md` com métricas da semana

---

## 🎨 Template Visual (HTML)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Relatório Semanal — {NOME_CLIENTE}</title>
  <style>
    @page { size: A4; margin: 20mm; }
    body { font-family: 'Inter', sans-serif; color: #1a1a1a; }
    .capa { 
      background: linear-gradient(135deg, {COR_PRIMARIA}, {COR_SECUNDARIA});
      color: white; padding: 60px 40px; page-break-after: always;
    }
    .metrica-card {
      background: #f8f9fa; border-radius: 8px; padding: 16px;
      text-align: center; flex: 1;
    }
    .metrica-valor { font-size: 28px; font-weight: 700; color: {COR_PRIMARIA}; }
    .metrica-label { font-size: 12px; color: #666; text-transform: uppercase; }
    .top-criativo { 
      display: flex; align-items: center; gap: 12px; 
      padding: 12px; border-bottom: 1px solid #eee;
    }
    .insight-box { 
      border-left: 4px solid {COR_PRIMARIA}; 
      padding: 12px 16px; margin: 12px 0; background: #f0f4ff;
    }
  </style>
</head>
<body>
  <!-- CAPA -->
  <div class="capa">
    <h1>Relatório Semanal</h1>
    <h2>{NOME_CLIENTE}</h2>
    <p>{PERIODO}</p>
  </div>

  <!-- RESUMO EXECUTIVO -->
  <h2>📈 Resumo da Semana</h2>
  <div style="display: flex; gap: 12px;">
    <div class="metrica-card">
      <div class="metrica-valor">{INVESTIMENTO}</div>
      <div class="metrica-label">Investimento</div>
    </div>
    <!-- ... mais cards ... -->
  </div>
  
  <!-- ... resto das seções ... -->
</body>
</html>
```

O template completo está em `templates/relatorio-semanal.html`.

---

## 📝 Regras de Marca (SEMPRE aplicar)

- ❌ **NUNCA:** "GHL", "GoHighLevel", "Conversation AI", "Hermes", "MCP"
- ✅ **SEMPRE:** "Sistema Flux 360", "nossa plataforma", "assistente virtual"
- ❌ **NUNCA:** "lead", "CPL", "ROAS", "pipeline"
- ✅ **SEMPRE:** "potencial cliente", "investimento por paciente", "resultado do investimento", "jornada"
- Consultar `shared/glossario.md` para tabela completa de substituições

---

> **Automação futura:** Quando GHL MCP estiver 100% funcional, puxar métricas de pipeline direto da API e preencher seção 3 automaticamente.
>
> **Para Mauricio:** Revisar frequência e profundidade. Quanto mais enxuto, mais chance de o cliente realmente ler.
