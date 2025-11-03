#!/usr/bin/env python3
import sys
import heapq

objects = 'ABCD'
costs = (1, 10, 100, 1000)
doors = (2, 4, 6, 8)
spots = (0, 1, 3, 5, 7, 9, 10)


def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """

    def parse_state(src: list[str]):
        hall = None
        room_rows = []
        for raw in src:
            s = raw.rstrip('\n')
            if s.startswith('#') and s.endswith('#'):
                core = s[1:-1]
                if len(core) == 11 and all(ch in '.ABCD' for ch in core):
                    hall = tuple(core)
            letters = [ch for ch in s if ch in objects]
            if len(letters) == 4:
                room_rows.append(letters)

        if hall is None:
            hall = tuple('.' for _ in range(11))

        rooms = []
        depth = len(room_rows)
        for r in range(4):
            col = tuple(room_rows[d][r] for d in range(depth))
            rooms.append(col)
        return (hall, tuple(rooms))

    start_state = parse_state(lines)
    STOP_ORDER = {}
    for door in doors:
        stops = []
        for s in spots:
            stops.append((abs(s - door), s))
        stops.sort()
        stops = [s for dist, s in stops]
        STOP_ORDER[door] = tuple(stops)

    def is_finished(state) -> bool:
        hall, rooms = state
        for c in hall:
            if c != '.':
                return False
        for r in range(4):
            need = chr(ord('A') + r)
            for ch in rooms[r]:
                if ch != need:
                    return False
        return True

    def path_open(hall: tuple[str, ...], a: int, b: int) -> bool:
        step = 1 if b > a else -1
        pos = a + step
        while True:
            if hall[pos] != '.':
                return False
            if pos == b:
                return True
            pos += step

    def can_enter(room: tuple[str, ...], who: str) -> bool:
        for ch in room:
            if ch != '.' and ch != who:
                return False
        return True

    def first_occupied(room: tuple[str, ...]) -> int:
        for i, ch in enumerate(room):
            if ch != '.':
                return i
        return -1

    def deepest_free(room: tuple[str, ...]) -> int:
        for i in range(len(room) - 1, -1, -1):
            if room[i] == '.':
                return i
        return -1

    def generate_moves(state):
        hall, rooms = state
        out = []
        DOOR = doors
        COST = costs
        STOP_BY_DOOR = STOP_ORDER

        for hpos, who in enumerate(hall):
            if who == '.':
                continue
            t = ord(who) - 65  # тип A->0, B->1, ...
            room = rooms[t]
            if not can_enter(room, who):
                continue
            j = deepest_free(room)
            if j == -1:
                continue
            door = DOOR[t]
            if not path_open(hall, hpos, door):
                continue

            steps = abs(hpos - door) + (j + 1)
            cost = steps * COST[t]
            new_h = list(hall)
            new_h[hpos] = '.'
            new_room = list(room)
            new_room[j] = who
            new_rooms = list(rooms)
            new_rooms[t] = tuple(new_room)
            out.append(((tuple(new_h), tuple(new_rooms)), cost))

        for r_idx, room in enumerate(rooms):
            i = first_occupied(room)
            if i == -1:
                continue
            who = room[i]
            t = ord(who) - 65
            if t == r_idx:
                settled = True
                for ch in room[i:]:
                    if ch != '.' and ch != who:
                        settled = False
                        break
                if settled:
                    continue
            door = DOOR[r_idx]
            if hall[door] != '.':
                continue
            for hpos in STOP_BY_DOOR[door]:
                if path_open(hall, door, hpos):
                    steps = (i + 1) + abs(hpos - door)
                    cost = steps * COST[t]
                    new_h = list(hall)
                    new_h[hpos] = who
                    new_room = list(room)
                    new_room[i] = '.'
                    new_rooms = list(rooms)
                    new_rooms[r_idx] = tuple(new_room)
                    out.append(((tuple(new_h), tuple(new_rooms)), cost))
        return out

    pq = [(0, start_state)]
    best = {start_state: 0}

    while pq:
        cur, st = heapq.heappop(pq)
        if cur != best.get(st, 10**18):
            continue
        if is_finished(st):
            return cur
        for nxt, w in generate_moves(st):
            nc = cur + w
            if nc < best.get(nxt, 10**18):
                best[nxt] = nc
                heapq.heappush(pq, (nc, nxt))

    return 0


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
