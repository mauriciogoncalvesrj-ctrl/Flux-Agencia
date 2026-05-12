---
name: flux-campaign-orchestrator
description: "End-to-end campaign orchestration system for Flux Agency. Chains market research, copy acquisition, creative production, funnel setup, and launch into a unified workflow. Produces a complete campaign package: research, copy, creative brief, funnel config, and launch checklist. Use when user says campaign, orquestrar campanha, lancar campanha, criar campanha completa, or wants to run a full campaign from research to launch."
user-invokable: true
---

<!-- Updated: 2026-05-12 | v1.0 -->

# Flux Campaign Orchestrator

Sistema de orquestracao de campanhas end-to-end para Flux Agency.
Coordena pesquisa de mercado → copy de aquisicao → producao de criativo → configuracao de funil → lancamento.

---

## Fases da Orquestracao

### Fase 1: PESQUISA (Market Intelligence)
**Skill:** `/market-research`
**Tempo estimado:** 30-60 min

**Input:** Nicho / segmento / tema da campanha
**Output:**
- `docs/pesquisas/YYYY-MM-DD-CODIGO-tema.md`
- Concorrentes mapeados
- Persona documentada
- Gaps identificados
- Campanha conceitual pronta

**Gate de aprovacao:** Usuario deve validar a pesquisa antes de prosseguir.

---

### Fase 2: COPY (Acquisition Messaging)
**Skill:** `/flux-copy-acquisition`
**Tempo estimado:** 20-40 min

**Input:** Pesquisa validada + objetivo da campanha
**Output:**
- `AVATAR-[CLINICA].md`
- `OFFER-[CAMPANHA].md`
- `HEADLINE-MATRIX-[CAMPANHA].md`
- `OBJECTION-CRUSHER-[CAMPANHA].md`
- `AD-ANGLES-[CAMPANHA].md`
- `SCROLL-STOPPERS-[CAMPANHA].md`
- `FUNNEL-PATH-[CAMPANHA].md`
- `COPY-FINAL-[PECAS].md`

**Gate de aprovacao:** Usuario deve aprovar oferta e headline principal.

---

### Fase 3: CRIATIVO (Creative Production)
**Skills:** `/ads-creative`, Fal.AI, Canva/Figma
**Tempo estimado:** 30-60 min

**Input:** Copy aprovada + angulos de criativo
**Output:**
- `docs/creative/[campanha]/brief-producao.md`
- Imagens geradas (carrossel, Reel thumb, anuncio)
- Prompts de imagem documentados
- Checklist de producao visual

**Especificacoes tecnicas:**
| Formato | Dimensao | Plataforma |
|---|---|---|
| Carrossel | 1080x1350 (4:5) | Instagram Feed |
| Reel | 1080x1920 (9:16) | Instagram Reels/TikTok |
| Anuncio Feed | 1080x1350 (4:5) | Meta Ads |
| Anuncio Story | 1080x1920 (9:16) | Meta Ads |
| Thumb YouTube | 1280x720 (16:9) | YouTube/Google |

**Gate de aprovacao:** Usuario deve aprovar o brief visual.

---

### Fase 4: FUNIL (Funnel Setup)
**Skill:** Configuracao manual no GHL + Meta Business Suite
**Tempo estimado:** 45-90 min

**Input:** Copy + criativo aprovados + funnel path definido
**Output:**
- Formulario/lead magnet configurado
- Bot de WhatsApp com script aprovado
- Sequencia de e-mail/SMS configurada
- Pipeline de oportunidades no CRM
- Landing page publicada (se aplicavel)

**Checklist de setup:**
- [ ] Pixel Meta instalado e testado
- [ ] Evento "Lead" configurado
- [ ] Formulario de captacao funcionando
- [ ] Bot de WhatsApp com script validado
- [ ] Tag/oportunidade criada automaticamente
- [ ] Pipeline de vendas configurado
- [ ] Template de proposta pronto

**Gate de aprovacao:** Teste completo do funil (preenche formulario → chega no WhatsApp → cria oportunidade).

---

### Fase 5: LANCAMENTO (Launch & Monitoramento)
**Skill:** `/ads-plan` + Meta Ads Manager / Google Ads
**Tempo estimado:** 20-40 min

**Input:** Tudo aprovado e testado
**Output:**
- Campanha publicada nas plataformas escolhidas
- Budget inicial definido
- Metricas de benchmark anotadas
- Relatorio de lancamento

**Checklist de lancamento:**
- [ ] Campanha ativa no Meta/Google
- [ ] Criativos carregados e aprovados
- [ ] Copy inserida corretamente
- [ ] URL de destino funcionando
- [ ] UTM tags aplicadas
- [ ] Pixel disparando eventos
- [ ] Notificacao de lead ativa
- [ ] Primeiro dia de monitoramento agendado

---

### Fase 6: OTIMIZACAO (Post-Launch)
**Skill:** `/ads-audit` + `/flux-copy-acquisition` (performance diagnosis)
**Tempo estimado:** Continuo

**Frequencia:**
- Diario: Primeiros 7 dias (cada lead, cada conversao)
- Quinzenal: Ajustes de criativo e copy
- Mensal: Relatorio completo + inteligencia de mercado

**Metricas-chave:**
| Metrica | Benchmark Flux | Acao se abaixo |
|---|---|---|
| CTR | > 1.5% | Trocar criativo/headline |
| CPL | < R$ 50 | Revisar targeting/copy |
| Taxa de agendamento | > 20% | Revisar script WhatsApp |
| Taxa de comparecimento | > 70% | Confirmacao automatica |
| CAC | < R$ 300 | Revisar oferta/funil |
| ROAS | > 3x | Revisar oferta/pricing |

---

## Comando Unificado

```
/orquestrar-campanha [tema] --plataformas [meta,google,linkedin] --budget [R$X] --prazo [dias]
```

**Exemplo:**
```
/orquestrar-campanha "Clinica Bonita Agenda Vazia" --plataformas meta --budget R$3000 --prazo 14
```

**O que acontece:**
1. Dispara `/market-research` para o tema
2. Valida pesquisa com usuario
3. Dispara `/flux-copy-acquisition` com base na pesquisa
4. Valida copy com usuario
5. Gera brief de criativo + prompts Fal.AI
6. Valida brief com usuario
7. Lista checklist de setup de funil
8. Valida funil testado
9. Lista checklist de lancamento
10. Agenda monitoramento pos-lancamento

---

## Pacote de Entrega Final

Apos execucao completa, o diretorio da campanha contem:

```
campaigns/YYYY-MM-DD-[tema]/
├── 1-research/
│   └── pesquisa-mercado.md
├── 2-copy/
│   ├── avatar.md
│   ├── offer.md
│   ├── headline-matrix.md
│   ├── objection-crusher.md
│   ├── ad-angles.md
│   ├── scroll-stoppers.md
│   ├── funnel-path.md
│   └── copy-final.md
├── 3-creative/
│   ├── brief-producao.md
│   ├── prompts-falai.md
│   ├── imagens/
│   │   ├── slide-1.jpg
│   │   ├── ...
│   │   └── slide-8.jpg
│   └── checklist-designer.md
├── 4-funnel/
│   ├── setup-checklist.md
│   ├── script-whatsapp.md
│   ├── sequencia-email.md
│   └── test-results.md
├── 5-launch/
│   ├── launch-checklist.md
│   ├── campanha-meta-config.md
│   └── campanha-google-config.md
└── 6-monitoramento/
    ├── relatorio-semanal-template.md
    ├── relatorio-mensal-template.md
    └── otimizacoes-aplicadas.md
```

---

## Regras de Execucao

1. **Nunca pular gates de aprovacao.** Cada fase precisa de validacao do usuario.
2. **Documentar tudo.** Cada decisao, teste e resultado deve estar escrito.
3. **Testar o funil antes de lancar.** Preenche o formulario, verifica se chega no WhatsApp, se cria oportunidade.
4. **Garantia de processo, nunca de resultado.** CFM/ANVISA.
5. **Brand rules em todas as pecas.** Nunca GHL/GoHighLevel.

---

## Skills Envolvidas

| Skill | Fase | Funcao |
|---|---|---|
| `/market-research` | 1 | Pesquisa de mercado e inteligencia |
| `/flux-copy-acquisition` | 2 | Copy de aquisicao e oferta |
| `/ads-creative` | 3 | Producao de criativos |
| `/ads-plan` | 5 | Planejamento de campanha |
| `/ads-audit` | 6 | Auditoria e otimizacao |
| `/ads-competitor` | 1/6 | Inteligencia competitiva |
| Fal.AI API | 3 | Geracao de imagens |

---

## Referencias
- Pesquisa de mercado: `docs/pesquisas/`
- Copy acquisition: `skills/flux-copy-acquisition/SKILL.md`
- Creative production: `docs/creative/`
- Funnel setup: Documentacao GHL interna
- Launch checklist: Meta Blueprint + Google Ads best practices
