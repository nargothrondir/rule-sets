#!/usr/bin/env python3
"""Сверка IP-списка: исходник против выгрузки собранного .mrs.

mihomo склеивает соседние сети и обнуляет биты хоста, поэтому сравниваются множества адресов,
а не строки. Запись без маски mihomo выбрасывает молча — здесь это ошибка.

    compare_ipcidr.py <исходные записи, по одной в строке> <выгрузка .mrs>
"""
import ipaddress
import sys


def read(path):
    return [line.strip() for line in open(path, encoding="utf-8") if line.strip()]


def collapse(nets):
    v4 = [n for n in nets if n.version == 4]
    v6 = [n for n in nets if n.version == 6]
    return set(ipaddress.collapse_addresses(v4)) | set(ipaddress.collapse_addresses(v6))


def addresses(nets):
    return sum(n.num_addresses for n in nets)


errors = []
source = []
for entry in read(sys.argv[1]):
    if "/" not in entry:
        try:
            bits = ipaddress.ip_address(entry).max_prefixlen
            errors.append(f"запись без маски '{entry}' — mihomo её выбросит, нужно '{entry}/{bits}'")
        except ValueError:
            errors.append(f"не сеть: '{entry}'")
        continue
    try:
        source.append(ipaddress.ip_network(entry, strict=False))
    except ValueError:
        errors.append(f"не сеть: '{entry}'")

built = [ipaddress.ip_network(e, strict=False) for e in read(sys.argv[2])]

expected, actual = collapse(source), collapse(built)
if expected != actual:
    lost = collapse([n for n in expected if not any(n.subnet_of(a) for a in actual if a.version == n.version)])
    extra = collapse([n for n in actual if not any(n.subnet_of(e) for e in expected if e.version == n.version)])
    errors.append(f"содержимое .mrs не совпадает с исходником: потеряно {sorted(map(str, lost))}, "
                  f"лишнее {sorted(map(str, extra))}")

for e in errors:
    print(e)
if not errors:
    print(f"совпадает: {len(source)} записей → {len(actual)} сетей после склейки, {addresses(actual)} адресов")
sys.exit(1 if errors else 0)
