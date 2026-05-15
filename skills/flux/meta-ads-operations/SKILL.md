---
name: meta-ads-operations
description: "Operational Meta Ads workflows for Agência Flux: create/upload ads, prepare paused drafts, inspect creatives, troubleshoot Marketing API writes, and safely verify that no spend is activated. Use when the user asks to subir anúncios, criar criativos, duplicar ads, deixar em rascunho/pausado, or fix Meta Marketing API creation errors."
version: 1.0.0
metadata:
  hermes:
    tags: [flux-agency, meta-ads, marketing-api, ads-creation, drafts, operations]
    related_skills: [flux-ads-audit, flux-meta-ads-relatorio, flux-copy-estetica, flux-orchestrator]
---

# Meta Ads Operations — Agência Flux

Use esta skill para tarefas operacionais no Meta Ads: criar anúncios, subir imagens, montar criativos, deixar anúncios em rascunho/pausados, duplicar estruturas e diagnosticar erros de escrita da Marketing API.

## Princípios de segurança

- **Nunca ativar verba sem pedido explícito.** Para rascunho operacional via API, criar anúncios com `status=PAUSED`.
- Antes de qualquer write, confirmar conta, ad set e objetivo do usuário.
- Depois de qualquer tentativa de criação, verificar com `list_ads` ou Graph API se os anúncios existem e se não ficaram `ACTIVE`.
- Se uma chamada de criação falhar, consultar pelo nome planejado para confirmar que nada parcial foi criado.
- Reportar IDs criados, status, nomes de ad sets e qualquer bloqueio relevante.

## Fluxo: subir anúncios em rascunho/pausados

1. **Carregar contexto do cliente** quando existir skill/contexto específico.
   - Luana Sampaio: carregar `flux-luana-context`.
2. **Localizar a conta correta.**
   - Luana Sampaio: `act_1073353887241970`.
3. **Listar ad sets e confirmar os destinos.**
   - Use `mcp_meta_ads_list_ad_sets(account_id, limit=100)`.
   - Preferir ad sets ativos e nomeados conforme cidade/procedimento.
4. **Inspecionar anúncios/criativos existentes.**
   - Use `mcp_meta_ads_list_ads` e Graph API em creatives existentes para recuperar padrões de `page_id`, `instagram_user_id`, CTA, WhatsApp e `asset_feed_spec`.
5. **Preparar os assets.**
   - Verificar caminhos de imagens e copies finais.
   - Upload: `/{ad_account_id}/adimages` com arquivo local; salvar `image_hash`.
6. **Criar o creative.**
   - Para Click-to-WhatsApp, replicar padrão existente da conta quando possível: `object_story_spec`, `asset_feed_spec`, `WHATSAPP_MESSAGE`, `https://api.whatsapp.com/send`.
7. **Criar anúncio pausado.**
   - Endpoint: `/{ad_account_id}/ads`.
   - Campos mínimos: `name`, `adset_id`, `creative={"creative_id":"..."}`, `status=PAUSED`.
8. **Verificar.**
   - Confirmar IDs, `status=PAUSED`, `effective_status` e nenhum anúncio ativo.

## Exemplo de padrões observados — Luana Sampaio

- Conta: `act_1073353887241970` / CA - Atual Luana.
- Page ID observado em creatives: `145852745270558`.
- Instagram user ID observado: `17841449430355386`.
- CTA observado: `WHATSAPP_MESSAGE`.
- URL observada: `https://api.whatsapp.com/send`.
- Ad set Cajamar Facial ativo observado: `120235800586100206` — `C1 - [FB/IG] [CAJAMAR][FACIAL] [C1][OPEN]`.
- Ad set Jundiaí Facial ativo observado: `120235950978670206` — `J1 - [FB/IG] [JUNDIAÍ] [FACIAL][OPEN] — Cópia`.

## Pitfalls da Marketing API

### App Meta em modo desenvolvimento bloqueia criação

Se a criação de creative/ad retornar erro `OAuthException`, `code=100`, `error_subcode=1885183`, com mensagem dizendo que o app está em modo desenvolvimento, a leitura da conta pode funcionar, mas writes de criativo/anúncio ficam bloqueados.

Soluções:

- colocar o app Meta em modo público/live com permissões de Ads;
- usar `META_ACCESS_TOKEN` emitido por app público/aprovado para criação;
- subir manualmente no Ads Manager com as imagens/copies preparadas.

Ver detalhes em `references/meta-ads-draft-creation-pitfalls.md`.

### Creative top-level legacy pode ser recusado

Criar creative com campos top-level (`title`, `body`, `image_hash`, `link_url`, `call_to_action_type`) pode retornar `(#3) Application does not have the capability to make this API call`. Preferir replicar o padrão de creatives existentes com `asset_feed_spec` + `object_story_spec` quando a conta usa Advantage/asset customization/click-to-message.

## Checklist de resposta ao usuário

Quando concluir ou bloquear:

- Conta consultada.
- Ad sets de destino com nome + ID.
- Quantos anúncios foram criados ou planejados.
- Status final (`PAUSED`, `ACTIVE`, falha etc.).
- Se falhou, erro resumido e confirmação se nenhum anúncio foi criado/ativado.
- Próximo passo prático para destravar.

## Related Skills

- `flux-ads-audit`: auditoria/performance e inventário de anúncios.
- `flux-meta-ads-relatorio`: relatórios semanais/mensais.
- `flux-copy-estetica`: copy de anúncios para estética.
- `flux-orchestrator`: decomposição multi-domínio quando envolve criativo + ads + CRM.
