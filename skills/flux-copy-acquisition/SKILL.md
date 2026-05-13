---
name: flux-copy-acquisition
description: "Copywriting system for customer acquisition focused on clinic owners. Extracts avatars, builds offers, maps awareness levels, constructs unique mechanisms, generates headline matrices, crushes objections, multiplies ad angles, and creates scroll-stopping hooks. Based on Kim Barrett's customer acquisition messaging framework, adapted for Flux Agency's B2B aesthetic clinic market. Use when user says copy, headline, offer, avatar, objection, mechanism, awareness, ad angles, scroll stopper, or wants to write acquisition copy for clinics."
user-invokable: true
---

<!-- Updated: 2026-05-12 | v1.0 | Framework: Kim Barrett Customer Acquisition -->

# Flux Copy Acquisition System

Sistema completo de copywriting para aquisicao de clientes B2B — adaptado para donos de clinicas de estetica, harmonizacao facial, dermatologia e odontologia estetica.

---

## 1. Avatar Extraction (Quem e o comprador?)

### Processo
1. Coletar dados da pesquisa de mercado (`/market-research` ou docs de pesquisa)
2. Entrevistar 3+ clientes ou leads qualificados (se disponivel)
3. Mapear 4 camadas do avatar

### Template Avatar Flux

```markdown
### Perfil Demografico
- Idade:
- Genero:
- Formacao:
- Faturamento mensal da clinica:
- Cidade / tamanho:
- Tempo de mercado:

### Psicografico
- O que le no Instagram: [perfis que segue, conteudo que consome]
- O que compra antes de contratar agencia: [curso, mentoria, CRM]
- O que ja tentou e falhou: [agencia generalista, postar sozinha, indicacao]
- Medo mais profundo: [perder a clinica, ser enganada de novo, nao saber o que esta acontecendo]
- Desejo mais intenso: [agenda cheia, faturamento previsivel, liberdade]

### Jornada de Consciencia (Schwartz)
[Ver Secao 3]

### Frase que ela diria em voz alta
"_________________________"

### Frase que ela so pensa, nao fala
"_________________________"
```

**Output:** `AVATAR-CLINICA-[NOME].md`

---

## 2. Offer Extraction (Transformar servico em oferta irresistivel)

### Formula Flux de Oferta

```
[SERVICO] + [MECANISMO UNICO] + [GARANTIA DE PROCESSO] + [BONUS] = OFERTA
```

### Exemplo — Flux Conversao
```
Gestao de trafego pago (Meta + Google)
+ Sistema Flux 360 (atendimento automatizado + pipeline comercial)
+ Inteligencia quinzenal de mercado
+ 4 posts/mes + relatorio
+ Garantia de processo: se em 30 dias nao houver melhora no CPL, reestruturamos campanha sem custo
= "Time completo de marketing por menos do que 1 funcionario CLT"
```

### Checklist de Oferta Forte
- [ ] Nomeia o resultado (nao o servico)
- [ ] Tem mecanismo unico (nao e "gestao de ads" generica)
- [ ] Inclui garantia de processo (nunca de resultado — CFM/ANVISA)
- [ ] Tem componente de urgencia ou escassez
- [ ] Preço ancorado com contexto ("menos que 1 CLT")
- [ ] Remove risco percebido

---

## 3. Schwartz Awareness Mapper (Nivel de consciencia do publico)

### Os 5 Niveis de Consciencia

| Nivel | Dono de Clinica Pensa... | Abordagem Flux |
|---|---|---|
| 1. **Inconsciente** | "Minha clinica ta bem." | Despertar dor: "Post bonito nao paga boleto." |
| 2. **Consciente do problema** | "Agenda ta vazia, preciso de pacientes." | Educar sobre causa: "O problema nao e falta de post." |
| 3. **Consciente da solucao** | "Preciso de trafego pago e automacao." | Posicionar Flux como solucao integrada. |
| 4. **Consciente do produto** | "Vi a Flux. Parece diferente." | Prova social + cases + diagnostico gratuito. |
| 5. **Mais consciente** | "Ja sei que a Flux e a melhor opcao." | Fechar: proposta clara, contrato, onboarding. |

### Como usar
1. Mapear em qual nivel esta a maioria do publico-alvo atual
2. Escrever copy ANTES do nivel deles (nao assume que ja sabem)
3. Criar conteudo para cada nivel (funil completo)

---

## 4. Mechanism Builder (Por que a Flux funciona?)

### Formula do Mecanismo Unico

```
[A maioria das agencias faz X, que leva a Y ruim.]
[A Flux faz Z, que leva a W bom.]
[O diferencial e M.]
```

### Exemplo Flux

```
A maioria das agencias de estetica so gerencia anuncios.
Resultado: lead chega no WhatsApp e nao converte porque ninguem conduz a venda.

A Flux gerencia trafego + comercial + automacao como um unico time.
Resultado: cada real investido em ads tem um processo de vendas por tras.

O diferencial: o Sistema Flux 360 integra captacao, atendimento e follow-up
em uma maquina que funciona 24h — mesmo quando sua recepcionista esta de folga.
```

### Variacoes de Mecanismo

| Contexto | Mecanismo |
|---|---|
| Meta Ads | "Anuncio com copy de avaliacao + bot que agenda em 30s" |
| Google Ads | "Busca ativa + landing otimizada + WhatsApp com script" |
| WhatsApp | "Automaçao treinada para conduzir avaliacao, nao so passar preco" |
| Full Funnel | "Trafego + comercial + automacao = maquina de pacientes" |

---

## 5. Headline Matrix (Matriz de titulos)

### Frameworks de Headline

#### A. Dor + Promessa
- "Sua clinica pode estar linda no Instagram e invisivel para quem precisa agendar."
- "Agenda vazia na terca? O problema nao e o procedimento. E a captacao."

#### B. Numero + Beneficio
- "7 sinais de que sua clinica esta perdendo pacientes no WhatsApp."
- "Como uma clinica de estetica lotou a agenda em 47 dias."

#### C. Pergunta Provocativa
- "Seu WhatsApp esta matando suas vendas?"
- "Voce sabe quanto custa cada paciente que chega?"

#### D. Mecanismo + Resultado
- "A unica agencia que integra trafego + comercial + automacao para clinicas."
- "Sistema Flux 360: captacao que funciona ate quando voce dorme."

#### E. Contrarian (vai contra o obvio)
- "Postar antes/depois nao vende mais. O que vende agora e isso."
- "Nao contrate uma agencia de estetica antes de ver isso."

### Matriz de Teste

Para cada campanha, gerar 10 headlines usando:
- 2x Dor + Promessa
- 2x Numero + Beneficio
- 2x Pergunta Provocativa
- 2x Mecanismo + Resultado
- 2x Contrarian

**Output:** `HEADLINE-MATRIX-[CAMPANHA].md`

---

## 6. Objection Crusher (Quebrador de objecoes)

### Top 7 Objeções do Dono de Clinica

| # | Objeçao | Resposta Flux |
|---|---|---|
| 1 | "Ja queimei dinheiro com agencia." | "Por isso a Flux comeca com diagnostico gratuito. Voce ve antes de pagar." |
| 2 | "E caro demais." | "R$ 2.500/mes e menos que 1 funcionario CLT. E o time inteiro de marketing." |
| 3 | "Nao tenho tempo." | "Voce nao gerencia nada. A Flux opera. Voce so aprova." |
| 4 | "Quero ver resultado rapido." | "Primeiros leads em 72h. Primeira avaliacao agendada na primeira semana." |
| 5 | "Minha concorrencia e forte." | "A gente espiona a concorrencia e encontra o gap que eles nao veem." |
| 6 | "Nao entendo de marketing." | "Voce nao precisa. A gente traduz em relatorio simples: quanto entrou, quanto converteu." |
| 7 | "Tenho medo de vinculo de contrato." | "Contrato minimo 6 meses. Mas voce pode cancelar a qualquer momento com 30 dias." |

### Formula de Quebra de Objeçao

```
[Reconhecer objeçao] + [Validar sentimento] + [Reframe] + [Prova social]
```

**Exemplo:**
```
"Se voce ja queimou dinheiro com agencia, tem todo direito de desconfiar.
A maioria das agencias entrega relatorio de leads, nao de vendas.
Por isso a Flux comeca com diagnostico gratuito.
Voce ve exatamente onde sua clinica perde pacientes antes de investir 1 real."
```

---

## 7. Ad Angle Multiplier (Multiplicador de angulos)

### Formula: 1 Conceito → 10 Angulos

**Conceito central:** "Clinica Bonita, Agenda Vazia"

| # | Angulo | Formato | Plataforma |
|---|---|---|---|
| 1 | Dor direta: agenda vazia | Carrossel | Instagram |
| 2 | Prova social: caso de resultado | Reel | Instagram/TikTok |
| 3 | Espionagem: analisando concorrencia | Reel | Instagram |
| 4 | Educacao: como funciona o funil | Carrossel | Instagram/LinkedIn |
| 5 | Mitos: 5 mentiras sobre marketing de estetica | Carrossel | Instagram |
| 6 | Urgencia: vaga aberta para proximo mes | Story/Reel | Instagram |
| 7 | Comparativo: com Flux vs sem Flux | Carrossel | Instagram/LinkedIn |
| 8 | FAQ: respondendo duvidas | Reel | Instagram |
| 9 | Bastidores: como fazemos diagnostico | Reel/Story | Instagram |
| 10 | Autoridade: tendencias do mercado | Carrossel | LinkedIn |

### Variacoes de Angulo por Pilar

**Pilar: Agenda Vazia**
- "3 motivos pelos quais sua agenda esta vazia (e nenhum e falta de post)"
- "Sua clinica pode ser a melhor da cidade e ninguem saber."
- "O erro que 90% das clinicas cometem no Instagram."

**Pilar: WhatsApp**
- "Se seu WhatsApp demora mais de 5 min, voce ja perdeu o paciente."
- "Por que leads chegam no WhatsApp e nao agendam?"
- "Como uma clinica converteu 3x mais sem contratar recepcionista."

**Pilar: Trafego**
- "R$ 1.000 em ads sem processo comercial = dinheiro queimado."
- "O anuncio de estetica que mais converte agora nao e antes/depois."
- "Como saber se sua agencia esta te enganando."

---

## 8. Scroll-Stopping Creative (Ganchos de 0-3 segundos)

### Framework de Hook por Formato

#### Reel / Video (0-3s)
| Tipo | Exemplo |
|---|---|
| Dor direta | "Agenda vazia na terca-feira?" |
| Numero chocante | "R$ 3.000/mes em ads. Zero pacientes." |
| Pergunta pessoal | "Seu WhatsApp esta matando suas vendas?" |
| Declaracao ousada | "Post bonito nao paga boleto." |
| Curiosidade | "Gastei a madrugada analisando anuncios de estetica. Tem um padrao." |
| Urgencia | "Vaga aberta para 3 clinicas em maio." |

#### Carrossel (Slide 1 — Capa)
| Tipo | Exemplo |
|---|---|
| Lista numerica | "7 sinais de que sua clinica esta perdendo pacientes" |
| Checklist | "O checklist da clinica que lota a agenda" |
| Erro comum | "O erro que 90% das clinicas cometem no WhatsApp" |
| Antes/Depois mental | "Como uma clinica foi de agenda vazia para 2 semanas lotadas" |

#### Meta/Google Ads Headline
| Tipo | Exemplo |
|---|---|
| Pergunta | "Agenda vazia na sua clinica?" |
| Beneficio numerico | "+47 pacientes em 30 dias" |
| Mecanismo | "Sistema Flux 360 para clinicas" |
| Urgencia | "Diagnostico gratuito — vagas limitadas" |

---

## 9. Conversion Path Builder (Caminho da conversao)

### Funil Flux para Clinicas

```
[TOFU] Atencao
  → Reel/Carrossel no Instagram (hook: dor/agenda vazia)
  → Lead magnet: "Diagnostico gratuito da captacao"

[MOFU] Interesse
  → Formulario simples: @ do Instagram + print do WhatsApp
  → Video Loom personalizado (5-10 min)
  → Proposta de valor enviada

[BOFU] Decisao
  → Call de 15 min (opcional)
  → Proposta com 3 planos (Start/Conversao/Autonomo)
  → Contrato + onboarding

[RETENCAO] 
  → Onboarding em 48h
  → Primeiro relatorio em 7 dias
  → Inteligencia quinzenal
  → Reuniao mensal de estrategia
```

### Pontos de Friccao a Eliminar
1. Formulario longo → maximo 3 campos
2. Demora no diagnostico → entregar em 24h
3. Call obrigatoria → opcional (proposta pode ser assincrona)
4. Contrato complexo → 2 paginas, claro

---

## 10. Performance Diagnosis (Diagnostico de performance)

### Checklist de Campanha em Queda

| Sintoma | Causa provavel | Acao Flux |
|---|---|---|
| CPL subiu 50%+ | Criativo cansado / aumento de concorrencia | Gerar novos angulos, testar hooks |
| CTR < 1% | Copy fraca / criativo irrelevante | Refazer headline, mudar imagem |
| Leads chegam, nao agendam | Script de WhatsApp ruim | Revisar bot/script, adicionar urgencia |
| Agendam, nao comparecem | Falta de confirmacao / lembrete | Implementar confirmacao automatica |
| CAC alto | Funnel quebrado / qualidade do lead ruim | Revisar targeting, landing page, qualificacao |
| ROAS baixo | Preco errado / oferta fraca / concorrencia | Revisar oferta, mecanismo, pricing |

---

## 11. Generic Language Killer (Removedor de linguagem generica)

### Palavras Proibidas na Copy Flux

| Generico (proibido) | Especifico (Flux) |
|---|---|
| "Resultados excepcionais" | "47 pacientes em 30 dias para clinica X" |
| "Gestao de trafego" | "Captacao de pacientes via Meta + Google" |
| "Estrategia digital" | "Maquina de pacientes: ads + WhatsApp + follow-up" |
| "Aumentar visibilidade" | "Agenda cheia com 2-3 dias de antecedencia" |
| "Automacao inteligente" | "Atendimento que responde em 30s, 24h por dia" |
| "Marketing de performance" | "Cada real investido tem ROI rastreado ate a venda" |
| "Cresca sua clinica" | "Lotar a agenda sem depender de indicacao" |
| "Solucao completa" | "Time de marketing por menos que 1 CLT" |

### Teste de Especificidade
Antes de publicar qualquer copy, perguntar:
1. **Quanto?** "Aumentar" → "+47 pacientes"
2. **Quem?** "Clientes" → "Donos de clinicas de estetica"
3. **Como?** "Automacao" → "Bot treinado para agendar avaliacao"
4. **Quando?** "Em breve" → "Primeiro lead em 72h"
5. **Onde?** "Online" → "WhatsApp Business da sua clinica"

---

## Output Padrao

Cada execuçao desta skill gera:
- `AVATAR-[CLINICA].md` — perfil do comprador
- `OFFER-[CAMPANHA].md` — oferta estruturada
- `HEADLINE-MATRIX-[CAMPANHA].md` — 10+ titulos prontos
- `OBJECTION-CRUSHER-[CAMPANHA].md` — respostas para objecoes
- `AD-ANGLES-[CAMPANHA].md` — 10 angulos de criativo
- `SCROLL-STOPPERS-[CAMPANHA].md` — hooks de 0-3s
- `FUNNEL-PATH-[CAMPANHA].md` — caminho da conversao
- `COPY-FINAL-[PECAS].md` — copy pronta para carrossel, Reel, anuncio, WhatsApp

---

## Brand Rules (CRITICO)
- NUNCA mencionar GHL/GoHighLevel/HighLevel em copy client-facing
- Usar: "Sistema Flux 360", "nosso sistema", "atendimento automatizado Flux"
- Garantia sempre de PROCESSO, nunca de RESULTADO (CFM/ANVISA)
- Falar como "dono para dono", nunca como "agencia para cliente"

---

## Referencias
- Framework base: Kim Barrett Customer Acquisition Messaging
- Adaptaçao: Flux Agency B2B Clinicas de Estetica
- Pesquisa de mercado: `docs/pesquisas/2026-05-12-b2b-estetica-flux.md`
