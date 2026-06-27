/**
 * Flux Content Orchestrator
 *
 * Ponto de entrada: recebe pedido de conteúdo e roteia pelos 5 setores.
 *
 * Uso:
 *   /flux-content "criar carrossel sobre 5 erros de tráfego"
 *   /flux-content "post sobre agenda vazando"
 */

export const meta = {
  name: 'flux-content-orchestrator',
  description: 'Orquestra criação de conteúdo completo: inteligência → estratégia → criação → qualidade → distribuição',
  phases: [
    { title: 'Inteligência', detail: 'Pesquisa de mercado, concorrentes, tendências' },
    { title: 'Estratégia', detail: 'Planejamento, território visual, hooks, CTA' },
    { title: 'Criação', detail: 'Copy + visual + composição' },
    { title: 'Qualidade', detail: 'Auditoria brand + compliance' },
    { title: 'Distribuição', detail: 'Formatação + agendamento' },
  ],
};

// Entrada do usuário
const pedido = args; // ex: "criar carrossel sobre 5 erros de tráfego"

// ============================================
// FASE 1: INTELIGÊNCIA (3 agentes paralelos)
// ============================================
phase('Inteligência');

const [socialTrends, competitorAnalysis, trendsData] = await parallel([
  () => agent(
    `Analise tendências de conteúdo em redes sociais do nicho de clínicas de estética e negócios locais nos últimos 30 dias.
    Foque em: hooks que funcionam, formatos com mais engajamento, temas quentes.
    Tema do pedido: ${pedido}
    Retorne um relatório estruturado com top hooks, formatos e recomendações.`,
    { label: 'intel-social', phase: 'Inteligência', model: 'deepseek-v4-pro' }
  ),
  () => agent(
    `Espione concorrentes de agências de marketing digital para clínicas de estética.
    Analise: tipo de conteúdo, formatos, frequência, CTAs usados.
    Identifique gaps e oportunidades.
    Tema do pedido: ${pedido}
    Retorne análise estruturada.`,
    { label: 'intel-competitor', phase: 'Inteligência', model: 'deepseek-v4-pro' }
  ),
  () => agent(
    `Identifique tendências sazonais e gatilhos psicológicos em alta para clínicas de estética.
    Considere: datas comerciais, gatilhos de escassez/urgência/prova social.
    Tema do pedido: ${pedido}
    Retorne tendências e hooks sugeridos.`,
    { label: 'intel-trends', phase: 'Inteligência', model: 'deepseek-v4-pro' }
  ),
]);

log('✅ Inteligência coletada — 3 relatórios prontos');

// ============================================
// FASE 2: ESTRATÉGIA (1 agente)
// ============================================
phase('Estratégia');

const briefing = await agent(
  `Com base nos dados de inteligência abaixo, monte um briefing completo para conteúdo de clínica de estética.

DADOS DE INTELIGÊNCIA:
--- Social Trends ---
${socialTrends}

--- Competitor Analysis ---
${competitorAnalysis}

--- Trends ---
${trendsData}

PEDIDO DO USUÁRIO: ${pedido}

INSTRUÇÕES:
1. Defina o pilar de conteúdo (educacional, prova social, CTA, transformação)
2. Escolha 1 dos 5 territórios visuais: Dona Sobrecarregada, Agenda Vazando, WhatsApp como Sistema, Operação Silenciosa, Dossiê/Diagnóstico
3. Escolha 1 dos 6 hooks aprovados: "O RALO DE [X]", "O FIM DAS [X]", "PARE DE [X]", "[X] VAI QUEBRAR SUA [X]", "MAIS DE [X] CLINICAS ACELERADAS", "O QUE [X] ESCONDEM DE VOCE"
4. Defina formato (carrossel 6 slides, post único, story)
5. Escolha 1 dos 4 CTAs: "Comenta [PALAVRA]", "Vamos conversar?", "Clique no link da bio", "Vamos jogar o jogo grande?"
6. Monte briefing completo seguindo template

PALETA: preto #0A0A0A + dourado #C9A961 + branco #FFFFFF
TOM: agressivo, direto, provocativo
FORMATAÇÃO: headline UPPERCASE, 50-65% da imagem

Retorne o briefing em markdown estruturado.`,
  { label: 'estrategista', phase: 'Estratégia', model: 'mimo-v2.5-pro' }
);

log('✅ Briefing estratégico pronto');

// ============================================
// FASE 3: CRIAÇÃO (3 agentes paralelos)
// ============================================
phase('Criação');

const [copyData, visualPrompts, composerReady] = await parallel([
  () => agent(
    `Gere copy estruturada para carrossel de Instagram baseada neste briefing:

${briefing}

REGRAS:
- Headline UPPERCASE, máx 6 palavras de destaque
- Usar hook aprovado do briefing
- Tom: agressivo, direto, provocativo
- Bullets de dor (3-4)
- CTA aprovado do briefing
- Output em JSON: {headline, subheadline, slides: [{slide, titulo, corpo}], cta, hashtags}

NUNCA inventar hooks — usar apenas os do briefing.
NUNCA usar tom suave.`,
    { label: 'create-copy', phase: 'Criação', model: 'mimo-v2.5' }
  ),
  () => agent(
    `Gere prompts de imagem para cada slide baseado neste briefing:

${briefing}

REGRAS:
- Usar prompt do território visual definido no briefing
- Paleta: preto + dourado (não ciano dominante)
- SEMPRE incluir "no text, no letters, no words"
- Fundo editorial/premium, não tech genérico
- 1 prompt por slide

Territórios disponíveis:
- Dona Sobrecarregada: exhausted female clinic owner, dark office, navy+gold
- Agenda Vazando: luxury clinic reception, empty schedule, dark lighting
- WhatsApp como Sistema: premium smartphone, dark office, navy+gold
- Operação Silenciosa: premium clinic management, intelligent systems, navy+gold
- Dossiê/Diagnóstico: premium business diagnostic report, golden pen, navy+gold

Retorne JSON com prompts por slide.`,
    { label: 'create-visual', phase: 'Criação', model: 'mimo-v2.5' }
  ),
  () => agent(
    `Preparar configuração de composição para o conteúdo:

${briefing}

Definir:
- Fontes: Montserrat Black (headlines), Montserrat Bold (corpo)
- Tamanhos: headline 50-65% da imagem, bullets 28-36px, CTA 30-42px
- Overlay: escuro forte para legibilidade
- Estrutura: selo editorial + headline + bullets + solução + CTA + badge FLUX + somosflux.com.br
- Cores: branco #FFFFFF para texto principal, dourado #C9A961 para destaque

Retorne configuração JSON.`,
    { label: 'create-composer', phase: 'Criação', model: 'mimo-v2.5' }
  ),
]);

log('✅ Copy + visual + composição prontos');

// ============================================
// FASE 4: QUALIDADE (2 agentes paralelos + síntese)
// ============================================
phase('Qualidade');

const [brandAudit, complianceAudit] = await parallel([
  () => agent(
    `Audite este conteúdo contra brand rules da Flux:

COPY:
${JSON.stringify(copyData, null, 2)}

BRIEFING:
${briefing}

CHECKLIST (score 1-10 cada):
1. Hook aprovado (1 dos 6)?
2. Paleta preto+dourado (não ciano)?
3. Montserrat Black, 50-65% imagem?
4. Estrutura: selo + headline + bullets + CTA + branding?
5. Território visual (1 dos 5)?
6. Tom agressivo/direto/provocativo?
7. CTA aprovado (1 dos 4)?
8. Legibilidade (<1.5s)?
9. Consistência entre slides?
10. Impacto premium/editorial?

Score mínimo: 7/10 para aprovação.
Retorne score por critério + score geral + decisão (APROVADO/REVISAR/REPROVADO) + correções.`,
    { label: 'qa-brand', phase: 'Qualidade', model: 'deepseek-v4-pro' }
  ),
  () => agent(
    `Audite compliance ANVISA/CFM deste conteúdo:

COPY:
${JSON.stringify(copyData, null, 2)}

CHECKLIST:
1. Claims de resultado precisam de prova?
2. Linguagem proibida presente?
3. Disclaimer necessário?
4. Imagens seguem restrições?
5. CTA adequado (não promete cura)?

Retorne status por check + decisão geral (APROVADO/REVISAR/REPROVADO).`,
    { label: 'qa-compliance', phase: 'Qualidade', model: 'deepseek-v4-pro' }
  ),
]);

// Síntese da qualidade
const qualityVerdict = await agent(
  `Combine as duas auditorias e dê verdict final:

AUDIT BRAND:
${brandAudit}

AUDIT COMPLIANCE:
${complianceAudit}

REGRAS:
- Score brand >= 7 E compliance APROVADO = APROVADO
- Score brand 6-7 = APROVADO COM AJUSTES
- Score brand < 6 OU compliance REVISAR = REVISAR
- Score brand < 5 OU compliance REPROVADO = REPROVADO

Retorne: decisão final + score + correções necessárias (se houver).`,
  { label: 'qa-sintese', phase: 'Qualidade', model: 'deepseek-v4-pro' }
);

log(`✅ Qualidade avaliada: ${qualityVerdict.includes('APROVADO') ? '✅ APROVADO' : '❌ REVISAR'}`);

// ============================================
// FASE 5: DISTRIBUIÇÃO
// ============================================
phase('Distribuição');

const distribuicao = await agent(
  `Formate o conteúdo aprovado para publicação:

COPY: ${JSON.stringify(copyData, null, 2)}
BRIEFING: ${briefing}
VEREDICTO QUALIDADE: ${qualityVerdict}

Gere:
1. Legenda formatada (hook + corpo + CTA + hashtags)
2. Especificações por plataforma (Instagram Feed 4:5, Story 9:16, Facebook)
3. Horários recomendados (11h-13h, 18h-21h)
4. Instruções de agendamento

Retorne conteúdo pronto para publicação.`,
  { label: 'distribuidor', phase: 'Distribuição', model: 'mimo-v2.5' }
);

log('✅ Conteúdo formatado para distribuição');

// ============================================
// RESUMO FINAL
// ============================================

return {
  briefing,
  copy: copyData,
  quality: qualityVerdict,
  distribuicao,
  status: qualityVerdict.includes('APROVADO') ? 'PRONTO_PARA_PUBLICAR' : 'NECESSITA_REVISAO',
};
