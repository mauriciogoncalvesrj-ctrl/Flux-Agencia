---
name: Stack Flux sem n8n
description: Decisão arquitetural — n8n removido da stack Flux; GHL faz orquestração interna
type: project
originSessionId: fa9626c9-cbb4-4f66-a229-79d66fc3b380
---
n8n foi removido oficialmente da stack Flux. GHL (GoHighLevel) é o CRM unificado E o orquestrador interno de automações via Flow Builder V3 + workflows nativos.

**Why:** O usuário (Maurício) decidiu que o GHL já cobre o trabalho que o n8n faria — manter os dois é complexidade redundante. Foco em uma ferramenta única que ele e os clientes Flux podem operar.

**How to apply:** Não sugerir n8n em nenhum desenho de arquitetura ou solução. Quando precisar de automação interna, pensar primeiro em workflows GHL, Flow Builder V3 ou Custom Triggers GHL. Para automações fora do escopo GHL, considerar Hermes Agent + Paperclip (já na stack VPS Hostinger).

Removidos junto: Postiz, Kit/Beehiiv, Ahrefs, Microsoft Clarity.
