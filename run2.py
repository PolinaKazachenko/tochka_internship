import sys
from collections import deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    adj = {}
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    for n in nodes:
        adj.setdefault(n, set())

    gateways = {n for n in nodes if n.isupper()}
    virus = 'a'
    result = []
    if virus not in adj:
        return result

    while True:
        dist_from_virus = {virus: 0}
        dq = deque([virus])
        while dq:
            x = dq.popleft()
            for y in adj.get(x, ()):
                if y not in dist_from_virus:
                    dist_from_virus[y] = dist_from_virus[x] + 1
                    dq.append(y)
        reachable_gateways = sorted([g for g in gateways if g in dist_from_virus])
        if not reachable_gateways:
            break
        adjacent_gateways = sorted([g for g in adj[virus] if g.isupper()])
        if adjacent_gateways:
            g = adjacent_gateways[0]
            if virus in adj[g]:
                adj[g].remove(virus)
            if g in adj[virus]:
                adj[virus].remove(g)
            result.append(f"{g}-{virus}")
        else:
            candidates = []
            for g in gateways:
                for u in adj.get(g, ()):
                    if not u.isupper():
                        candidates.append((g, u))
            if not candidates:
                break
            candidates.sort()
            g, u = candidates[0]
            if u in adj[g]:
                adj[g].remove(u)
            if g in adj[u]:
                adj[u].remove(g)
            result.append(f"{g}-{u}")

        dist_from_virus = {virus: 0}
        dq = deque([virus])
        while dq:
            x = dq.popleft()
            for y in adj.get(x, ()):
                if y not in dist_from_virus:
                    dist_from_virus[y] = dist_from_virus[x] + 1
                    dq.append(y)

        reachable_gateways = [g for g in gateways if g in dist_from_virus]
        if not reachable_gateways:
            break

        best_dist = min(dist_from_virus[g] for g in reachable_gateways)
        targets = sorted([g for g in reachable_gateways if dist_from_virus[g] == best_dist])
        target = targets[0]
        dist_to_target = {target: 0}
        dq = deque([target])
        while dq:
            x = dq.popleft()
            for y in adj.get(x, ()):
                if y not in dist_to_target:
                    dist_to_target[y] = dist_to_target[x] + 1
                    dq.append(y)

        dv = dist_to_target.get(virus)
        if dv is None:
            continue

        next_candidates = [u for u in adj[virus] if dist_to_target.get(u) == dv - 1]
        if next_candidates:
            next_node = sorted(next_candidates)[0]
            virus = next_node

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
