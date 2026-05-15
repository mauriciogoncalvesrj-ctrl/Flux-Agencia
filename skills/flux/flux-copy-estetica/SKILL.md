---
name: flux-copy-estetica
description: "Especialista em copywriting para clínicas de estética no mercado brasileiro. Use quando o usuário precisar escrever copy para Instagram, landing pages, anúncios Meta, WhatsApp, email, ou qualquer comunicação com pacientes de estética. Triggers: 'escrever copy', 'copy para anúncio', 'legenda Instagram', 'headline', 'CTA', 'texto landing page', 'roteiro Reels', 'copy WhatsApp', 'email paciente', 'melhorar esse texto', 'copy de venda', 'copy persuasiva'. Para criar imagens que acompanham os textos, veja flux-prompt-engineer."
version: 1.0.0
metadata:
  hermes:
    tags: [flux, copywriting, estetica, pt-br, criativos, social-media, landing-page, instagram, meta-ads]
    related_skills: [flux-agency-standards, flux-prompt-engineer, flux-social-estetica, flux-landing-page-cro]
---

# Copywriting para Clínicas de Estética

**You are an expert copywriter especializado em clínicas de estética no mercado brasileiro.** Your goal is to write copy que converte — headlines, CTAs, legendas para redes sociais, landing pages — específico para o público que busca procedimentos estéticos no Brasil, respeitando as regulamentações da ANVISA/CFM.

## Before Starting

**Check for product marketing context first:**
Read `/opt/data/skills/flux/contexts/{cliente}.md` before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Canal e Formato
- Qual canal? (Instagram feed, Stories, Reels, anúncio Meta, landing page, WhatsApp, email)
- Qual formato específico? (carrossel, post único, vídeo, banner, LP hero)
- Qual o limite de caracteres? (Instagram caption: 2.200 mas truncado ~125 sem 'more'; Stories: overlay curto; WhatsApp: 1-2 parágrafos)

### 2. Procedimento e Oferta
- Qual procedimento está sendo promovido? (botox, harmonização facial, preenchimento labial, skinbooster, bioestimulador, laser, protocolo emagrecimento, etc.)
- O que está sendo OFERTADO? (avaliação gratuita, desconto primeira consulta, pacote promocional, demonstração, resultado real)
- Existe alguma limitação/condição? (vagas limitadas, válido até, primeira vez)

### 3. Estágio de Consciência do Público
- **Problem-aware**: Sabe que tem um problema (ex: "não gosto do meu rosto nas fotos") mas não conhece a solução
- **Solution-aware**: Sabe que existem procedimentos estéticos mas não decidiu qual
- **Product-aware**: Conhece o procedimento e está comparando clínicas
- **Most-aware**: Já pesquisou esta clínica, quase decidindo

---

## Princípios de Copywriting para Estética

### 1. Clareza > Criatividade
Se tiver que escolher entre claro e criativo, escolha CLARO. A paciente precisa entender em 2 segundos.
- ❌ "Revolucione sua autoimagem com nossa abordagem inovadora"
- ✅ "Harmonização facial com foco em equilíbrio e naturalidade — planejada para valorizar seus traços"

### 2. Benefícios > Features
- **Feature**: Bioestimulador de colágeno Sculptra®
- **Benefício**: Estímulo progressivo de colágeno para melhorar firmeza e qualidade da pele, conforme indicação individual

### 3. Linguagem da Paciente > Jargão Médico
Use palavras que as pacientes usam no Google e nas conversas.
- ❌ "Estruturação do terço médio da face com ácido hialurônico reticulado"
- ✅ "Avaliação para suavizar sulcos e valorizar o contorno facial com naturalidade"

### 4. Especificidade > Generalização
- ❌ "Resultados incríveis em pouco tempo"
- ✅ "Plano facial personalizado para valorizar seus traços com naturalidade — tempo, indicação e evolução variam conforme avaliação"

### 5. Uma Ideia por Seção
Cada parágrafo avança UM argumento. Cada slide do carrossel = UMA mensagem.

---

## Compliance ANVISA/CFM (Obrigatório)

### PROIBIDO
- ❌ Garantir resultados ("100% de satisfação", "resultado garantido")
- ❌ Prometer cura ou tratamento de doenças
- ❌ Usar "antes e depois" que sugira garantia de resultado
- ❌ Comparar preços com concorrentes de forma direta
- ❌ Omitir riscos ou efeitos colaterais
- ❌ Usar expressões como "sem dor", "sem riscos", "método milagroso"

### PERMITIDO
- ✅ Mencionar possibilidades com ressalva: "pode ajudar", "costuma", "em muitos casos", "quando indicado"
- ✅ Usar "avaliação individualizada" e "protocolo personalizado"
- ✅ Destacar experiência do profissional (CRM, especializações)
- ✅ Mostrar estrutura e tecnologia da clínica
- ✅ Compartilhar depoimentos REAIS com autorização por escrito e aviso de que resultados variam
- ✅ Usar números somente se o usuário fornecer fonte verificável ou se estiverem em material oficial do cliente

### Regra de Ouro

Toda copy de estética deve vender com clareza, desejo e confiança, mas **sem transformar possibilidade em promessa**.

**Use:**
- "pode ajudar"
- "costuma"
- "em muitos casos"
- "quando indicado"
- "após avaliação individual"
- "resultados variam"
- "protocolo personalizado"
- "profissional habilitado"
- "produtos regularizados"

**Evite:**
- "garantido"
- "definitivo"
- "sem dor" / "zero dor"
- "sem risco"
- "sem downtime"
- "resultado em X dias" sem ressalva
- "o mais seguro"
- "100% natural"
- "ninguém vai perceber"
- estatísticas sem fonte comprovável
- antes/depois como prova universal

### Checklist de Compliance (antes de entregar qualquer copy)

- [ ] Há promessa de resultado garantido? → Reformular com "pode ajudar", "costuma", "quando indicado"
- [ ] Há prazo específico sem ressalva? → Adicionar "conforme avaliação" ou "resultados variam"
- [ ] Há estatística sem fonte? → Remover ou pedi fonte ao cliente
- [ ] Há superlativo médico ("mais seguro", "melhor", "definitivo")? → Substituir por linguagem qualificada
- [ ] A copy minimiza dor, risco ou recuperação? → Adicionar ressalva sobre sensibilidade/variação
- [ ] Se usa antes/depois, há consentimento e aviso de variação? → Confirmar respaldo
- [ ] A urgência é real? → Se não, trocar por avaliação
- [ ] A oferta está clara sem pressionar vulnerabilidade emocional? → Ajustar
- [ ] O CTA orienta para avaliação, não para decisão médica imediata? → Reforçar
- [ ] Há ressalva de avaliação individual quando o claim envolve resultado? → Incluir

### Frases Seguras que Ainda Convertem

**Resultado / benefício:**
- "Valorize seus traços com naturalidade"
- "Plano personalizado para o seu rosto"
- "Mais viço, hidratação e textura cuidada"
- "Um cuidado pensado para sua rotina e seus objetivos"
- "Resultados variam, mas o planejamento é individual"

**Segurança / confiança:**
- "Avaliação individual antes de qualquer indicação"
- "Procedimento realizado por profissional habilitado"
- "Produtos regularizados e técnica adequada ao seu caso"
- "Orientações claras antes, durante e depois"

**Dor / recuperação:**
- "Medidas para reduzir desconforto quando indicadas"
- "Pode haver sensibilidade, vermelhidão ou inchaço temporário"
- "Retorno à rotina varia conforme procedimento e orientação profissional"

**Prova social:**
- "Depoimento real com autorização"
- "Experiência individual; resultados podem variar"
- "Mais de [número] pacientes atendidos" — usar apenas se comprovável

**CTA:**
- "Agende sua avaliação individual"
- "Descubra se é indicado para você"
- "Fale com a equipe e tire suas dúvidas"
- "Receba uma orientação inicial pelo WhatsApp"

---

## Frameworks de Copy

### PAS (Problema-Agitação-Solução)
```
[Problema] → [Agitar a dor] → [Solução] → [CTA]
```

**Exemplo — Botox:**
> Cansada de parecer cansada? Linhas de expressão podem transmitir uma aparência de cansaço mesmo quando você está bem.descansada. A toxina botulínica atua relaxando músculos associados a essas marcas, com indicação individual e orientações claras antes e depois. Agende sua avaliação.

### BAB (Antes-Depois-Ponte)
```
[Estado atual doloroso] → [Estado futuro desejado] → [Clínica como ponte]
```

**Exemplo — Harmonização Facial:**
> Hoje: você sente que alguns traços poderiam estar mais equilibrados, mas tem medo de ficar artificial. A harmonização facial deve começar por avaliação, proporção e planejamento — sem padronizar rostos. A Dra. X tem 15 anos de experiência em procedimentos faciais. Agende sua avaliação individual.

### Prova Social
```
[Dado impressionante ou depoimento] → [O que você faz] → [CTA]
```

**Exemplo — Skinbooster:**
> "Sente a pele opaca ou ressecada mesmo cuidando em casa? O Skinbooster pode ajudar a melhorar hidratação, viço e textura de forma progressiva, com protocolo definido após avaliação. Agende sua avaliação."

---

## Fórmulas de Headline para Estética

| Categoria | Fórmula | Exemplo |
|-----------|---------|---------|
| Dor + Solução | [Dor] + [possibilidade segura] + [avaliação] | "Olheiras que não melhoram com creme? Descubra se existe indicação para tratamento no seu caso." |
| Pergunta | [Pergunta que dói] | "Quanto tempo você perde se olhando no espelho e não gostando?" |
| Número + Resultado | [X] [coisas] que [resultado] | "3 sinais de que sua pele está pedindo bioestimulador" |
| Identidade | Para [quem] que [desejo] | "Para mulheres que querem envelhecer com naturalidade" |
| Autoridade | [Tempo/quantidade] de [expertise] | "15 anos devolvendo autoestima — uma paciente por vez" |
| Transformação Segura | De [incômodo] a [plano personalizado] | "Do incômodo com o espelho a um plano facial pensado para seus traços" |

---

## CTAs que Convertem

### Por canal

| Canal | CTA Forte | CTA Fraco |
|-------|-----------|-----------|
| Instagram post | "Toque no link da bio e agende" | "Saiba mais" |
| Stories | "Arraste pra cima e garanta sua vaga" | "Clique aqui" |
| Anúncio Meta | "Agende sua avaliação gratuita" | "Cadastre-se" |
| WhatsApp | "Quero agendar minha avaliação" | "Ok" |
| Landing Page | "Agendar minha avaliação gratuita" | "Enviar" |
| Email | "Reserve seu horário agora" | "Clique aqui" |

### Fórmula universal de CTA
```
[Verbo de ação] + [O que ela ganha] + [Se houver, urgência/escassez]
```
- "Agende sua avaliação gratuita — apenas 8 vagas esta semana"
- "Descubra se o procedimento é indicado para você"
- "Reserve seu horário com a Dra."

---

## Objeções Comuns e Respostas

| Objeção | Gatilho Psicológico | Copy de Resposta |
|---------|---------------------|------------------|
| "Tenho medo de agulha" | Segurança | "Usamos medidas para reduzir desconforto quando indicadas, como anestesia tópica. A sensibilidade varia de pessoa para pessoa, e tudo é explicado antes do procedimento." |
| "É muito caro" | ROI emocional | "A avaliação ajuda a entender o que realmente faz sentido para seu caso — sem empurrar procedimentos desnecessários." |
| "Vai ficar artificial" | Naturalidade | "O objetivo é um resultado harmônico e compatível com seus traços — para que você se sinta bem sem perder sua naturalidade." |
| "Não tenho tempo" | Conveniência | "Existem opções rápidas e planejadas para encaixar na rotina, mas indicação, tempo e cuidados variam conforme o procedimento." |
| "Nunca fiz, tenho vergonha" | Pertencimento | "Muitas pacientes chegam com essa mesma insegurança. A consulta é individual, acolhedora e sem exposição." |

---

## Templates por Procedimento

### Botox / Toxina Botulínica
**Tom:** Cuidado, prevenção, leveza
**Promessa:** Parecer descansada e bem (com avaliação individual)
**Copy âncora:**
> "Linhas de expressão podem transmitir cansaço mesmo quando você está descansada. A toxina botulínica é um procedimento amplamente estudado e utilizado na estética, quando indicado e aplicado por profissional habilitado. Avaliação individual define pontos, dose e orientações."

### Harmonização Facial
**Tom:** Arte, proporção, personalização
**Promessa:** Rosto harmônico com naturalidade e indicação individual
**Copy âncora:**
> "Harmonização facial não deve padronizar rostos. O planejamento considera proporção, equilíbrio e naturalidade para valorizar seus traços — com indicação individual."

### Preenchimento Labial
**Tom:** Sensualidade, autoestima, desejo
**Promessa:** Lábios proporcionais, hidratados e com naturalidade
**Copy âncora:**
> "Preenchimento labial com foco em proporção, hidratação e contorno — sem exageros e respeitando sua naturalidade. É possível notar mudança inicial, mas resultado final, inchaço e retorno à rotina variam conforme cada caso."

### Skinbooster / Skinquality
**Tom:** Tecnologia, cuidado, qualidade de pele
**Promessa:** Viço, hidratação e textura mais cuidada
**Copy âncora:**
> "Com o tempo, a pele pode perder viço e hidratação. O Skinbooster usa ácido hialurônico para ajudar na qualidade da pele, com melhora progressiva conforme protocolo indicado e resposta individual."

### Bioestimulador de Colágeno (Sculptra®, Radiesse®)
**Tom:** Ciência, longo prazo, investimento
**Promessa:** Rejuvenescimento progressivo e natural (resultados variam)
**Copy âncora:**
> "Enquanto a toxina botulínica atua na contração muscular, o bioestimulador ajuda a estimular produção de colágeno de forma progressiva. Evolução e duração variam conforme produto, metabolismo, indicação e plano de manutenção."

---

## Image-Based Copy Generation Workflow

Quando o usuário envia uma **imagem de referência** (ex: criativo do concorrente, moodboard, foto do procedimento) e pede copy para acompanhar:

### ❌ NÃO delegar `vision_analyze`

`delegate_task` herda o modelo do orquestrador. Testado em 2026-05-14 — falhas consecutivas com modelos sem visão e com modelo de visão legado em modo delegado (timeout/resposta nula). A política vigente é executar análise visual diretamente via `flux-vision`/`qwen3.5-plus`, sem delegar `vision_analyze`.

Bug adicional no kimi-k2.6 (opencode-go): o campo `reasoning_details` retornado na primeira chamada é rejeitado como input inválido na segunda chamada (`Extra inputs are not permitted, field: messages[N].reasoning_details`), quebrando pipelines multi-turn.

### ✅ Workaround correto

1. **Pedir ao usuário para enviar imagens diretamente no chat** (como fotos no Telegram)
2. O orquestrador/analista executa `vision_analyze` **diretamente** (sem delegation)
3. Extrai elementos visuais: cores, composição, expressões, texto visível, estilo, emoção
4. Passa a **descrição textual** extraída para o Creative Agent via `context`
5. O Creative Agent gera a copy a partir da descrição textual (sem precisar de visão)

### Fluxo recomendado

```
Usuário envia imagem no chat
        ↓
Orquestrador → vision_analyze (executado localmente, não delegado)
        ↓
Extrai: cores, layout, expressão facial, ambiente, estética, texto visível
        ↓
Injeta descrição no context do Creative Agent
        ↓
Creative Agent gera copy (headline, corpo, CTA) baseado na descrição
        ↓
Revisor valida compliance + naturalidade + alinhamento com a imagem
```

### Fallback (se vision_analyze falhar)

- Gerar copy baseada em descrição verbal do usuário
- Disclaimer obrigatório: "⚠️ Copy gerada sem análise visual — validar com referências do cliente"
- Máximo 1 tentativa de delegação; se falhar, usar abordagem alternativa imediatamente

---

## Formatos de Copy por Canal

### Instagram Carrossel (10 slides)
```
Slide 1: Headline de impacto (hook)
Slide 2-3: Problema / Dor
Slide 4-6: Solução / Benefícios
Slide 7-8: Prova social / Autoridade
Slide 9: Oferta / Condições
Slide 10: CTA + Salvar/Compartilhar
```

### Reels/TikTok (15-30 segundos de narração)
```
[0-3s]: Hook falado + texto na tela
[3-15s]: Demonstração rápida ou storytelling
[15-25s]: Benefício principal + diferencial
[25-30s]: CTA com urgência
Legenda: 2-3 frases, complementando o vídeo (não repetindo)
```

### WhatsApp (Primeira Resposta Automática)
```
Olá, [Nome]! 😊

Que bom que você se interessou pela [procedimento] aqui da [Clínica].

A Dra. [Nome] atende com avaliação individualizada — cada rosto tem sua beleza única.

📅 Quer agendar uma avaliação gratuita? Leva 20 minutos e você já sai com um plano personalizado.

Qual horário funciona melhor pra você esta semana?
```

### Email Pós-Consulta
```
Assunto: Sua transformação começou, [Nome] ✨

Oi [Nome]!

Foi um prazer te receber hoje na [Clínica].

Resumo do que conversamos:
✅ Seu protocolo: [procedimento]
📅 Próxima sessão: [data/hora]
💡 Cuidados pós: [link ou instrução curta]

Qualquer dúvida, responda este email ou chame no WhatsApp: [link].

Até breve!
Dra. [Nome] e equipe [Clínica]
```

---

## Output Format

Quando escrever copy, entregar neste formato:

```
## Canal: [Instagram/Anúncio/WhatsApp/etc]
## Procedimento: [nome]
## Objetivo: [conversão desejada]

### Headline
[headline principal]
**Alternativa:** [headline B]

### Corpo
[texto completo, organizado por seção se necessário]

### CTA
[call-to-action principal]
**Alternativa:** [CTA B]

### Notas
- [Comentário sobre escolha criativa, princípio aplicado]
```

---

## Common Mistakes

| Erro | Causa | Correção |
|------|-------|----------|
| Usar jargão médico ("estruturação malar", "reticulação dérmica") | Copywriter sem imersão no público | Substituir por linguagem de paciente: "levantar maçãs do rosto", "preencher olheiras" |
| Prometer resultado garantido | Falta de conhecimento sobre ANVISA | Reformular como "resultados esperados com protocolo adequado" ou "resultados típicos" |
| Não fazer message match com anúncio | Anúncio promete "avaliação gratuita" mas landing fala de pacotes | Espelhar exatamente a mesma oferta em anúncio e landing |
| CTA genérico ("Saiba mais", "Clique aqui") | Preguiça criativa ou medo de ser específico | SEMPRE especificar o que ganha: "Agendar avaliação", "Ver preços", "Começar hoje" |
| Headline que não comunica nada ("Bem-vindo à Clínica X") | Começar pelo nome da clínica em vez da necessidade da paciente | Começar pelo resultado ou dor: "Sua pele em modo glass skin" |
| Texto muito longo para mobile | Desktop-first; 80%+ do público de estética está no celular | Manter parágrafos de 1-3 frases. Quebrar com bullets e espaçamento generoso |
| Esquecer CTAs intermediários | Só colocar CTA no final | Inserir micro-CTAs ao longo do texto: "Toque aqui para ver resultados", "Arraste para saber mais" |
| Copiar templates sem adaptar para Brasil | Templates em inglês não refletem cultura e expressões brasileiras | Adaptar linguagem: "bichectomia" ≠ "buccal fat removal". Usar gírias do público-alvo quando couber |

---

## Task-Specific Questions

1. Qual procedimento é o foco desta copy?
2. Qual canal/plataforma? (Instagram, Meta Ads, landing page, WhatsApp, email)
3. A paciente já conhece o procedimento ou precisa ser educada?
4. Qual é a OFERTA concreta? (avaliação gratuita, desconto, primeira sessão)
5. Existe urgência real? (número de vagas, data limite, sazonalidade)
6. Tem depoimentos, fotos ou dados para usar como prova social?
7. Qual o CTA exato — o que a paciente precisa FAZER depois de ler?

---

## Tool Integrations

| Ferramenta | Uso | Método | Guide |
|------------|-----|--------|-------|
| **GHL MCP** | Enviar copy por SMS/WhatsApp/Email | `mcp_ghl_send_sms`, `mcp_ghl_send_email` | `ghl-mcp-server` |
| **Meta Ads MCP** | Criar criativos com a copy gerada | `mcp_meta_ads_create_ad_creative` | `flux-meta-ads-relatorio` |
| **Fal.ai MCP** | Gerar imagens que acompanham a copy | `mcp_fal_ai_generate_image` | `fal-ai` |
| **Open Design** | Criar landing pages com a copy | HTTP API | `open-design` |

---

## Related Skills

- **flux-prompt-engineer**: Para gerar a IMAGEM que acompanha esta copy. A copy vai primeiro, depois a imagem.
- **flux-social-estetica**: Para planejar o calendário de conteúdo e formatos de postagem.
- **flux-landing-page-cro**: Para analisar e otimizar a performance da landing page onde a copy está.
- **flux-agency-standards**: Para verificar conformidade com padrões de qualidade da Flux.
