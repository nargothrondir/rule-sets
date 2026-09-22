---
name: bump-mihomo
description: Обновление закреплённой версии mihomo в сборке .mrs — версия, SHA256 с перекрёстной проверкой, контроль версии формата .mrs. Использовать, когда пользователь просит обновить mihomo в CI или когда нужно новое поведение конвертера.
---

# Обновление версии mihomo в сборке

Версия закреплена не случайно: версия формата зашита в заголовок `.mrs`, и старые ядра не читают
другие версии (`rules/provider/mrs_reader.go`, `MrsMagicBytes`). Обновлять только ради нужного
изменения и проверять формат.

## 1. Версия и контрольная сумма

```bash
gh release list -R MetaCubeX/mihomo --limit 5
```

Файл — `mihomo-linux-amd64-compatible-<версия>.gz`. Сумма из двух независимых источников:

```bash
gh release view <версия> -R MetaCubeX/mihomo --json assets --jq '.assets[] | select(.name=="mihomo-linux-amd64-compatible-<версия>.gz") | .digest'
```

```bash
curl -fsSL -o m.gz "https://github.com/MetaCubeX/mihomo/releases/download/<версия>/mihomo-linux-amd64-compatible-<версия>.gz" && sha256sum m.gz
```

Скачивать во временный каталог, не в репозиторий. Если суммы не совпали — остановиться и сообщить.

## 2. Формат `.mrs`

Версий две (`docs/ci.md`, «Версии и совместимость»), проверить обе в исходниках новой версии:

```bash
V=<версия>; B="https://cdn.jsdelivr.net/gh/MetaCubeX/mihomo@$V"
curl -sSL "$B/rules/provider/mrs_reader.go" | grep -n "MrsMagicBytes ="
curl -sSL "$B/component/trie/domain_set_bin.go" | grep -n -A1 "// version"
```

Ожидается `{'M', 'R', 'S', 1}` и запись байта `{1}`. Если хоть одна изменилась — **не обновлять**:
файлы нового формата не прочтут клиенты со старым ядром. Сообщить пользователю и без его решения
дальше не двигаться. Сборка это тоже поймает (`MRS_MAGIC`, `SET_VERSION`), но лучше узнать заранее.

## 3. Правка и проверка

В `.github/workflows/compile-rules.yml` поменять `MIHOMO_VERSION` и `MIHOMO_SHA256`. Правка workflow
запускает сборку сама.

```bash
gh run watch <id> -R nargothrondir/rule-sets --exit-status
```

Ожидается: проверка суммы `OK`, в логе новая версия, сборка зелёная. Если сборка сделала коммит
`rebuild .mrs` — байты изменились при новой версии; содержимое при этом уже сверено сборкой. Упомянуть
это пользователю.

Обновить значения в `docs/ci.md`, если там указана версия.
