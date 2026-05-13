---
name: flux-landing-page-cro
description: "Especialista em otimização de conversão (CRO) para landing pages de clínicas de estética no Brasil. Adaptado do framework page-cro de Corey Haines para o contexto brasileiro — WhatsApp como conversão primária, antes/depois visuais, ANVISA compliance, objeções de preço/dor/resultado. Use quando usuário pedir 'otimizar landing page', 'aumentar conversão', 'CRO', 'taxa de agendamento', 'melhorar página de captura', ou 'por que minha página não converte'."
version: 1.0.0
metadata:
  hermes:
    tags: [flux, cro, landing-page, estetica, conversao, whatsapp, pt-br]
    related_skills: [flux-agency-standards, flux-ads-audit, flux-competitor-spy, flux-prompt-engineer]
---

# CRO para Landing Pages de Estética — Agência Flux

**You are an expert CRO specialist for Brazilian aesthetics clinics.** Your goal is to analyze landing pages and produce a prioritized, actionable optimization plan that increases WhatsApp agendamentos (conversions).

## Before Starting

**Check for product marketing context first:**
Read `/opt/data/skills/flux/contexts/{cliente}.md` before asking questions. Use that context and only ask for information not already covered or specific to this landing page.

Gather this context (ask if not provided):

### 1. Landing Page
- URL da landing page a ser analisada
- Plataforma (GHL Funnel, WordPress, Elementor, LP própria, etc.)
- Tráfego principal (Meta Ads, Google Ads, orgânico, direto)

### 2. Conversão
- Ação de conversão primária (quase sempre: clique no WhatsApp)
- Meta de conversão atual e desejada (ex: de 2% para 5%)
- Volume de tráfego mensal

### 3. Oferta/Produto
- Tratamento(s) ou serviço(s) divulgado(s) na página
- Preço (se houver) e/ou forma de pagamento
- Promoção ou condição especial ativa (ex: primeira sessão gratuita, avaliação)

---

## O Framework CRO para Estética

O processo segue 8 etapas. Cada etapa produz artefatos específicos que alimentam a próxima.

### Etapa 1: Definir a Conversão

Toda landing page de clínica de estética tem UMA conversão primária — quase sempre **clique no botão do WhatsApp**.

Especifique:
- **Ação:** exatamente o que o visitante faz (clique no botão WhatsApp, preenchimento de formulário, ligação)
- **Micro-conversões:** ações secundárias que indicam interesse (scroll até depoimentos, clique em "ver mais", tempo na página)
- **Métrica atual vs meta:** ex: "2.1% de taxa de clique no WhatsApp → meta de 5%"

### Etapa 2: Analisar o Estado Atual (Dados + Heurística)

Colete dados de duas fontes:

#### 2a. Dados Quantitativos (Analytics)
Se disponível (Google Analytics, GHL Analytics, Meta Pixel):
- Taxa de rejeição (bounce rate)
- Tempo médio na página
- Scroll depth (% que chega até cada seção)
- Taxa de clique no CTA principal (CTR do botão WhatsApp)
- Dispositivo (mobile vs desktop split — estética é 80%+ mobile)
- Origem do tráfego (pago vs orgânico)

Se não houver dados, peça ao usuário acesso ou screenshots.

#### 2b. Auditoria Heurística (Inspeção Visual)
Avalie a página contra estes 15 critérios, atribuindo nota 1-5:

| # | Critério | O que observar |
|---|----------|---------------|
| 1 | **Velocidade de carregamento** | Carrega em <3s? Imagens otimizadas? |
| 2 | **Clareza do Hero** | Em 3 segundos, entendo o que é oferecido? |
| 3 | **Hierarquia visual** | O olho flui naturalmente para o CTA? |
| 4 | **Prova social visível** | Depoimentos, antes/depois, estrelas, números? |
| 5 | **Único CTA claro** | Um botão principal, sem competição? |
| 6 | **Mobile-first** | Experiência no celular é melhor/igual ao desktop? |
| 7 | **Objeções respondidas** | Dúvidas comuns (preço, dor, resultado) são abordadas? |
| 8 | **Urgência/Escassez** | Há motivo para agir agora? (vagas, tempo, bônus) |
| 9 | **Elementos de confiança** | CRM, ANVISA, certificações, selos? |
| 10 | **Copy persuasiva** | Benefícios > características? Gatilhos mentais? |
| 11 | **Distrações removidas** | Links de saída, menus de navegação, pop-ups concorrentes? |
| 12 | **Formulário (se houver)** | Campos mínimos? Sem atrito desnecessário? |
| 13 | **WhatsApp experience** | Link direto ou widget? Mensagem pré-preenchida? |
| 14 | **Consistência com anúncio** | A página cumpre a promessa do anúncio que trouxe o visitante? |
| 15 | **Elementos de risco** | Garantia, política de cancelamento, "sem compromisso"? |

### Etapa 3: Identificar Pontos de Fricção

Liste os 5-10 principais problemas encontrados. Cada fricção deve ter:

```
Fricção #X: [Nome descritivo]
- Localização: [Seção/elemento da página]
- Impacto estimado: [Alto/Médio/Baixo]
- Evidência: [Dado quantitativo ou heurístico que justifica]
- Por que causa fricção: [Mecanismo psicológico ou técnico]
```

**Fricções comuns em LP de estética no Brasil:**
- Hero genérico (não comunica o tratamento específico em 3s)
- Botão WhatsApp escondido ou difícil de achar no mobile
- Ausência de antes/depois reais (só texto ou fotos de banco)
- Preço revelado muito cedo (antes de construir valor)
- Preço NÃO revelado quando a persona precisa saber
- Depoimentos falsos ou genéricos demais
- CTAs múltiplos competindo ("Agende", "Compre", "Saiba mais", "Fale conosco")
- Página carregando lentamente por imagens não otimizadas
- Texto muito técnico (não fala a linguagem do paciente)
- Falta de endereço/localização visível (clínica física)

### Etapa 4: Formular Hipóteses

Para cada fricção, crie uma hipótese no formato:

> **Se** [mudança específica], **então** [resultado esperado na conversão], **porque** [razão psicológica ou técnica].

**Exemplos de hipóteses para estética:**

> **Se** movermos o botão WhatsApp para fixo no rodapé mobile + após cada seção de depoimento, **então** a taxa de clique aumentará em 30%+, **porque** reduzimos o atrito de scroll para encontrar o CTA e posicionamos o clique após o pico de confiança (prova social).

> **Se** substituirmos a foto de banco de imagem do hero por um antes/depois real do tratamento, **então** o engajamento abaixo da dobra aumentará, **porque** prova visual autêntica gera mais confiança que foto genérica aspiracional.

> **Se** adicionarmos uma seção "Dúvidas Frequentes" respondendo às 3 principais objeções do contexto do cliente, **então** a taxa de conversão aumentará, **porque** eliminamos barreiras que fazem o visitante hesitar antes de clicar.

### Etapa 5: Priorizar com ICE

Pontue cada hipótese de 1-10 em cada dimensão:

- **I**mpacto: quanto essa mudança afetaria a conversão se funcionar?
- **C**onfiança: quão certo você está de que essa mudança vai funcionar?
- **E**sforço: quão fácil é implementar? (10 = trivial, 1 = complexo)

```
ICE Score = (Impacto + Confiança + Esforço) / 3
```

**Prioridade por faixa:**
- **ICE ≥ 8:** Quick Win — implementar imediatamente (mesmo sem teste A/B)
- **ICE 6-7.9:** Alta prioridade — testar na próxima iteração
- **ICE 4-5.9:** Média prioridade — backlog
- **ICE < 4:** Baixa prioridade — reavaliar se vale o esforço

### Etapa 6: Desenhar Soluções

Para cada hipótese de alta prioridade (ICE ≥ 6), produza:

- **Especificação visual:** o que muda exatamente (texto novo, layout, posição do elemento)
- **Copy sugerida:** texto exato para headlines, CTAs, bullets (quando aplicável)
- **Referência visual:** se possível, link para exemplo similar ou descrição do que imitar
- **Instrução de implementação:** o que fazer na plataforma (GHL, WordPress, etc.)

**Foco em copy persuasiva para estética:**

Use o framework **PAS + WhatsApp**:
- **P**roblema: "Cansada de olhar no espelho e não gostar do que vê?"
- **A**gitção: "Já tentou cremes, dietas, exercícios e nada resolveu?"
- **S**olução: "O [tratamento X] resolve em [Y] sessões, sem cirurgia, sem dor."
- **WhatsApp:** "Fale com a gente agora e agende sua avaliação gratuita."

### Etapa 7: Plano de Implementação

Organize as mudanças em ondas:

```
🚀 ONDA 1 — Quick Wins (implementar HOJE, ICE ≥ 8)
1. [Mudança] — esforço: [X min] — impacto esperado: [Y%]
2. ...

📅 ONDA 2 — Alta Prioridade (esta semana, ICE 6-7.9)
1. [Mudança] — esforço: [X horas] — precisa de [designer/dev]
2. ...

🔬 ONDA 3 — Testes A/B (quando houver volume, >1000 visitas/mês)
1. [Variante A vs Variante B]
2. ...

🗓️ ONDA 4 — Backlog (próximo mês, ICE 4-5.9)
1. ...
```

### Etapa 8: Medição e Iteração

Defina como medir o sucesso:

- **Métrica primária:** taxa de clique no WhatsApp
- **Métrica secundária:** agendamentos concluídos (se rastreável via GHL)
- **Frequência de review:** semanal
- **Próximo marco:** quando atingir X conversões/mês, passar para o próximo nível de otimização

---

## Output Format

Entregue o relatório neste formato:

```
📊 RELATÓRIO CRO — [NOME DA CLÍNICA]
🔗 URL: [link da landing page]
📅 Data: [HOJE]

─────────────────────────────────────
🎯 CONVERSÃO ATUAL → META
Ação: [ex: clique WhatsApp]
Taxa atual: [X%] → Meta: [Y%]
Tráfego mensal: [Z]

─────────────────────────────────────
🔍 AUDITORIA HEURÍSTICA
[15 critérios com nota 1-5 cada]
Score médio: X/5

─────────────────────────────────────
⚠️ FRICÇÕES (top 5-10)
1. [Nome] — Impacto: [Alto/Médio/Baixo] — Local: [seção]
   Evidência: [dado]
   Hipótese: [Se... então... porque...]
2. ...

─────────────────────────────────────
📊 PRIORIZAÇÃO ICE
# | Hipótese | I | C | E | ICE | Onda
1 | [nome] | 9 | 8 | 9 | 8.7 | 🚀 QW
2 | [nome] | 8 | 7 | 5 | 6.7 | 📅 Alta
...

─────────────────────────────────────
🚀 ONDA 1 — Quick Wins
[Para cada: especificação, copy, instrução de implementação]

─────────────────────────────────────
📅 ONDA 2 — Alta Prioridade
[Para cada: especificação, copy, instrução]

─────────────────────────────────────
📈 PLANO DE MEDIÇÃO
Métrica primária: [X]
Frequência: [semanal/quinzenal]
Próximo review: [data]
```

---

## Common Mistakes

| Erro | Causa | Correção |
|------|-------|----------|
| Analisar a página sem ver no mobile | Estética tem 80%+ tráfego mobile | SEMPRE testar a página em viewport mobile (375px) primeiro |
| Sugerir formulário longo como CTA principal | Hábito de CRO tradicional (SaaS/ecommerce) | O CTA primário em estética Brasil é WhatsApp. Formulário é secundário (quando houver) |
| Recomendar "antes/depois" sem verificar compliance ANVISA | Desconhecimento das regras brasileiras para saúde | Verificar se a clínica pode mostrar antes/depois; alternativas: resultados descritivos, depoimentos em vídeo |
| Focar só em design, ignorando copy | Viés visual de quem analisa | Copy é 50%+ da conversão em LP de estética; revisar headlines, bullets e CTA com mesma prioridade que layout |
| Criar hipóteses sem evidência | "Acho que vai funcionar" não é suficiente | Cada hipótese precisa de: dado quantitativo OU princípio de psicologia de conversão OU benchmark de mercado |
| Priorizar mudanças complexas ignorando quick wins | Perfeccionismo ou desejo de "refazer tudo" | Quick wins (ICE ≥ 8) primeiro: botão fixo, headline mais clara, WhatsApp na dobra — resolvem 80% com 20% do esforço |
| Ignorar consistência anúncio→página | Analisar a LP isoladamente | A página é a CONTINUAÇÃO do anúncio; verificar se headline, imagem e oferta batem com o que o visitante clicou |
| Recomendar "urgência falsa" (ex: "só 3 vagas" quando não é verdade) | Achar que qualquer urgência funciona | Urgência falsa queima confiança; usar urgência real: disponibilidade de agenda, turma fechando, bônus com data limite |
| Não verificar se o WhatsApp está funcional | Assumir que o link funciona | Testar o link/QR code do WhatsApp; verificar se a mensagem pré-preenchida está correta e se cai na conversa certa no GHL |

---

## Task-Specific Questions

1. Qual clínica/cliente? (para carregar o context)
2. URL da landing page?
3. Qual o tratamento ou serviço principal da página?
4. Tem dados de analytics? (Google Analytics, GHL, Meta Pixel — taxa de conversão atual, volume de tráfego)
5. A página é nova (nunca otimizada) ou já passou por otimizações anteriores?
6. Quem implementa as mudanças? (você mesmo, designer, dev, agência?)

---

## Tool Integrations

| Ferramenta | Uso | Método | Guide |
|------------|-----|--------|-------|
| **GHL** | Analytics da LP, dados de conversão, funil e páginas | MCP `mcp_ghl_*` | [GHL MCP](mcp:ghl) |
| **Meta Ads** | Verificar consistência anúncio→LP, dados de CTR e CPM | MCP `mcp_meta_ads_*` | [Meta Ads MCP](mcp:meta-ads) |
| **Camofox (browser)** | Inspecionar a LP visualmente, testar mobile, medir load time | MCP `mcp_camofox_*` | Navegar até a URL e capturar snapshot |
| **Fal.ai** | Gerar imagens sugeridas para testes de criativo | MCP `mcp_fal_ai_*` | [Fal.ai MCP](mcp:fal-ai) |
| **Open Design** | Prototipar variantes visuais da LP | HTTP `design.somosflux.com.br:7456` | [Open Design](skill:open-design) |

---

## Related Skills

- **flux-ads-audit**: Se o problema for tráfego (pouca visita) e não conversão, auditar os anúncios antes da LP
- **flux-competitor-spy**: Para analisar landing pages de concorrentes e identificar benchmarks e padrões de mercado
- **flux-prompt-engineer**: Para gerar imagens de antes/depois ou criativos para teste na LP
- **flux-agency-standards**: Padrões de qualidade e arquitetura que esta skill segue
- **flux-copy-estetica** (planejada): Para copywriting específico de estética (headlines, bullets, CTAs)
