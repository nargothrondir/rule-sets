# rule-sets

Списки доменов и IP-сетей для [mihomo](https://github.com/MetaCubeX/mihomo) в формате `.mrs`.

| Список | Подключение |
|---|---|
| `proxy` | `https://cdn.jsdelivr.net/gh/nargothrondir/rule-sets@main/mrs/proxy.mrs` |
| `direct` | `https://cdn.jsdelivr.net/gh/nargothrondir/rule-sets@main/mrs/direct.mrs` |
| `discord-voice` (ipcidr) | `https://cdn.jsdelivr.net/gh/nargothrondir/rule-sets@main/mrs/discord-voice.mrs` |

Для IP-списков — `behavior: ipcidr`.

```yaml
rule-providers:
  proxy:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/nargothrondir/rule-sets@main/mrs/proxy.mrs
    path: ./rule-sets/proxy.mrs
    interval: 86400
```

| Путь | Что это |
|---|---|
| [`src/domain/`](src/domain) | исходники списков доменов |
| [`src/ipcidr/`](src/ipcidr) | исходники списков IP-сетей |
| [`mrs/`](mrs) | собранные списки — их пишет только сборка |
| [`docs/lists.md`](docs/lists.md) | что в каких списках, формат записей |
| [`docs/ci.md`](docs/ci.md) | как устроена сборка и что она проверяет |
| [`tools/`](tools) | вспомогательные скрипты сборки |

## Правка

Правьте `src/<тип>/*.yaml` и пушьте: GitHub Actions соберёт `.mrs`, распакует их обратно, сверит с исходником
и только тогда закоммитит. Сломанный список в `mrs/` не попадёт.

jsdelivr кеширует ветку до 12 часов. Чтобы изменения разошлись сразу, откройте
`https://purge.jsdelivr.net/gh/nargothrondir/rule-sets@main/mrs/proxy.mrs`.
