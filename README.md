# rule-sets

Списки доменов для [mihomo](https://github.com/MetaCubeX/mihomo) в формате `.mrs`.

| Список | Подключение |
|---|---|
| `proxy` | `https://cdn.jsdelivr.net/gh/nargothrondir/rule-sets@main/proxy.mrs` |
| `direct` | `https://cdn.jsdelivr.net/gh/nargothrondir/rule-sets@main/direct.mrs` |

```yaml
rule-providers:
  proxy:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/nargothrondir/rule-sets@main/proxy.mrs
    path: ./rule-sets/proxy.mrs
    interval: 86400
```

## Правка

Исходники — `*.yaml` в корне. Записи: `example.com` — только сам домен, `+.example.com` — домен
и все поддомены. При пуше GitHub Actions собирает `.mrs` и проверяет результат, сломанный список
не коммитится:

- запись с пробелом внутри или ссылка вместо домена — ошибка: mihomo такие молча выбрасывает
  или хранит как мусор, поэтому собранный файл распаковывается обратно и сверяется с исходником;
- пустой список — ошибка;
- повтор записи — предупреждение.

jsdelivr кеширует ветку до 12 часов. Чтобы изменения разошлись сразу, откройте
`https://purge.jsdelivr.net/gh/nargothrondir/rule-sets@main/proxy.mrs`.
