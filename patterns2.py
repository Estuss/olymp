# ==================================================================================

from typing import List, Tuple, Dict, Set, Optional
from collections import defaultdict, deque
import math
import heapq
import bisect
import sys

# ==================================================================================
# 1. БИТОВЫЕ ОПЕРАЦИИ
# ==================================================================================
# КОГДА:
# - Задачи на подмножества (n <= 20-25)
# - Динамика по маскам (коммивояжёр, назначения)
# - Оптимизация перебора
# - Проверка степеней двойки, чётности
# - Игры с битами

def bit_usage_examples():
    """Практические примеры использования битовых операций"""
    
    # === Задача 1: Проверить, является ли число степенью двойки ===
    def is_power_of_two(x: int) -> bool:
        # Число степени двойки: 1, 2, 4, 8, 16...
        # У них только один бит установлен в 1
        # Пример: 8 = 1000, 8-1 = 0111, 8 & 7 = 0
        return x > 0 and (x & (x - 1)) == 0
    
    # === Задача 2: Найти единственный неповторяющийся элемент ===
    # В массиве все элементы повторяются дважды, кроме одного
    def find_unique(arr: List[int]) -> int:
        # XOR всех элементов: a^a=0, 0^b=b
        result = 0
        for x in arr:
            result ^= x
        return result
    
    # === Задача 3: Подсчитать количество единичных битов ===
    def count_bits(x: int) -> int:
        return x.bit_count()  # Python 3.8+
        # Или вручную:
        # cnt = 0
        # while x:
        #     cnt += x & 1
        #     x >>= 1
        # return cnt
    
    # === Задача 4: Генерация всех подмножеств ===
    # Дано множество из n элементов, нужно перебрать все подмножества
    def all_subsets(items: List[int]) -> List[List[int]]:
        n = len(items)
        subsets = []
        for mask in range(1 << n):  # 0 .. 2^n - 1
            subset = [items[i] for i in range(n) if mask & (1 << i)]
            subsets.append(subset)
        return subsets
        # Применение: перебор всех комбинаций, задача о рюкзаке для n<=20
    
    # === Задача 5: Перебор подмасок заданной маски ===
    def iterate_submasks(mask: int):
        # Нужно перебрать все подмножества множества mask
        sub = mask
        while sub:
            # обрабатываем submask
            sub = (sub - 1) & mask
    
    # === Задача 6: Динамика по маскам (TSP) ===
    # Задача коммивояжёра: найти кратчайший путь, посещающий все города
    def tsp(dist: List[List[int]]) -> int:
        n = len(dist)
        INF = 10**18
        # dp[mask][v] = минимальная стоимость посетить города в mask, закончить в v
        dp = [[INF] * n for _ in range(1 << n)]
        dp[1][0] = 0  # начали в городе 0
        
        for mask in range(1 << n):
            for v in range(n):
                if dp[mask][v] == INF:
                    continue
                for u in range(n):
                    if not (mask & (1 << u)):
                        dp[mask | (1 << u)][u] = min(
                            dp[mask | (1 << u)][u],
                            dp[mask][v] + dist[v][u]
                        )
        return dp[(1 << n) - 1][0]
        # Сложность: O(n^2 * 2^n), работает при n <= 20

    return {
        "is_power_of_two": is_power_of_two,
        "find_unique": find_unique,
        "all_subsets": all_subsets
    }


# ==================================================================================
# 2. ТЕОРИЯ ИГР
# ==================================================================================
# КОГДА:
# - Задачи, где два игрока делают ходы
# - Определение выигрышной/проигрышной позиции
# - Игры: Ним, Георгий, Баше, Шпрага-Гранди

def game_theory_examples():
    """Примеры игровых задач"""
    
    # === Задача 1: Игра Баше ===
    # Условие: куча из n камней, за ход можно взять 1..k камней
    # Проигрывает тот, кто не может сделать ход
    def bash_game(n: int, k: int) -> str:
        # Выигрышная позиция, если n % (k+1) != 0
        return "First" if n % (k+1) != 0 else "Second"
    
    # === Задача 2: Игра Ним ===
    # Условие: несколько куч камней, за ход можно взять любое количество из одной кучи
    def nim_game(heaps: List[int]) -> str:
        # XOR всех размеров куч
        xor_sum = 0
        for h in heaps:
            xor_sum ^= h
        return "First" if xor_sum != 0 else "Second"
        # Применение: классическая задача на Codeforces, Timus
    
    # === Задача 3: Числа Гранди для произвольной игры ===
    # Условие: есть игра с одним объектом (куча, позиция на поле)
    # Нужно определить Grundy число для каждого состояния
    def grundy_number(n: int, moves: List[int]) -> int:
        """
        Пример: есть куча из n камней, можно брать 1, 3 или 4 камня
        """
        grundy = [0] * (n + 1)
        
        for i in range(1, n + 1):
            reachable = set()
            for m in moves:
                if i >= m:
                    reachable.add(grundy[i - m])
            # mex - минимальное неотрицательное число, не входящее в reachable
            g = 0
            while g in reachable:
                g += 1
            grundy[i] = g
        
        return grundy[n]
        # Применение: анализ сложных игр, где нет простой формулы
    
    # === Задача 4: Сумма игр (теорема Шпрага-Гранди) ===
    # Если игра состоит из нескольких независимых подыгр,
    # то общее Grundy = XOR Grundy подыгр
    def sum_of_games(heaps: List[int], moves: List[int]) -> bool:
        xor_sum = 0
        for h in heaps:
            xor_sum ^= grundy_number(h, moves)
        return xor_sum != 0  # True - выигрышная позиция
    
    # === Задача 5: Георгий (теорема Цермело) ===
    # Для конечной игры без ничьих с полной информацией
    # можно определить выигрышные и проигрышные позиции DFS'ом
    def game_on_graph(adj: List[List[int]], start: int) -> str:
        """
        Граф состояний игры. Из вершины v можно перейти в adj[v]
        Проигрышная позиция - если нет ходов или все ходы ведут в выигрышные
        Выигрышная - если есть ход в проигрышную
        """
        n = len(adj)
        dp = [-1] * n  # -1 не определено, 0 проигрыш, 1 выигрыш
        
        def dfs(v: int) -> int:
            if dp[v] != -1:
                return dp[v]
            if not adj[v]:  # нет ходов
                dp[v] = 0
                return 0
            
            # Если есть ход в проигрышную позицию - текущая выигрышная
            for u in adj[v]:
                if dfs(u) == 0:
                    dp[v] = 1
                    return 1
            
            dp[v] = 0
            return 0
        
        return "First" if dfs(start) == 1 else "Second"

    return {
        "bash_game": bash_game,
        "nim_game": nim_game,
        "grundy_number": grundy_number
    }


# ==================================================================================
# 3. МОДУЛЬНАЯ АРИФМЕТИКА
# ==================================================================================
# КОГДА:
# - Задачи с большими числами (результат нужно вывести по модулю)
# - Задачи на комбинаторику (C(n,k) mod M)
# - Вычисление обратных элементов
# - Решение сравнений

MOD = 10**9 + 7

def modular_arithmetic_examples():
    """Примеры модульной арифметики"""
    
    # === Быстрое возведение в степень ===
    def binpow(a: int, n: int, mod: int = MOD) -> int:
        # Применение: вычисление a^n mod M за O(log n)
        res = 1
        a %= mod
        while n > 0:
            if n & 1:
                res = (res * a) % mod
            a = (a * a) % mod
            n >>= 1
        return res
    
    # === Обратный элемент (через малую теорему Ферма) ===
    def mod_inv(a: int, mod: int = MOD) -> int:
        # Работает только когда mod простое!
        return binpow(a, mod - 2, mod)
    
    # === Расширенный алгоритм Евклида ===
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """Возвращает (gcd, x, y): a*x + b*y = gcd"""
        if b == 0:
            return a, 1, 0
        g, x1, y1 = extended_gcd(b, a % b)
        return g, y1, x1 - (a // b) * y1
    
    def mod_inv_extended(a: int, mod: int) -> int:
        # Работает для любого mod (если gcd(a,mod)=1)
        g, x, _ = extended_gcd(a, mod)
        if g != 1:
            raise ValueError("Обратный элемент не существует")
        return x % mod
    
    # === Предвычисление факториалов ===
    def precompute_factorials(n: int, mod: int = MOD) -> Tuple[List[int], List[int]]:
        # Применение: быстрый расчёт C(n,k) для множества запросов
        fact = [1] * (n + 1)
        for i in range(2, n + 1):
            fact[i] = (fact[i - 1] * i) % mod
        
        inv_fact = [1] * (n + 1)
        inv_fact[n] = mod_inv(fact[n], mod)
        for i in range(n - 1, -1, -1):
            inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % mod
        
        return fact, inv_fact
    
    def comb(n: int, k: int, fact: List[int], inv_fact: List[int], mod: int = MOD) -> int:
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % mod * inv_fact[n - k] % mod
    
    # === Линейное решето для обратных элементов ===
    def linear_inv(n: int, mod: int = MOD) -> List[int]:
        # inv[i] = i^(-1) mod mod для всех i от 1 до n
        inv = [0] * (n + 1)
        inv[1] = 1
        for i in range(2, n + 1):
            inv[i] = mod - (mod // i) * inv[mod % i] % mod
        return inv
    
    # === Китайская теорема об остатках ===
    def crt(remainders: List[int], moduli: List[int]) -> Tuple[int, int]:
        """
        Решение системы:
        x ≡ r1 (mod m1)
        x ≡ r2 (mod m2)
        ...
        Возвращает (x, M) где M = m1*m2*... и x - решение по модулю M
        """
        x = 0
        M = 1
        for r, m in zip(remainders, moduli):
            # Решаем x ≡ r (mod m)
            g, s, _ = extended_gcd(M, m)
            if (r - x) % g != 0:
                return None  # Решения нет
            lcm = M // g * m
            t = ((r - x) // g) * s % (m // g)
            x = (x + t * M) % lcm
            M = lcm
        return x, M

    return {
        "binpow": binpow,
        "mod_inv": mod_inv,
        "comb": comb,
        "crt": crt
    }


# ==================================================================================
# 4. ХЭШИРОВАНИЕ
# ==================================================================================
# КОГДА:
# - Быстрое сравнение строк/подстрок
# - Поиск подстроки в тексте (алгоритм Рабина-Карпа)
# - Поиск повторяющихся подстрок
# - Проверка палиндромов за O(1)

def hashing_examples():
    """Примеры использования хэширования"""
    
    class StringHash:
        """
        Полиномиальный хэш строки
        Позволяет за O(1) получить хэш любой подстроки
        """
        def __init__(self, s: str, p: int = 911382323, m: int = 10**9 + 7):
            self.s = s
            self.p = p
            self.m = m
            self.n = len(s)
            
            self.prefix = [0] * (self.n + 1)
            self.powers = [1] * (self.n + 1)
            
            for i in range(1, self.n + 1):
                self.powers[i] = (self.powers[i - 1] * p) % m
            
            for i in range(self.n):
                self.prefix[i + 1] = (self.prefix[i] + 
                                      (ord(s[i]) - ord('a') + 1) * self.powers[i]) % m
            
            # Предвычисляем обратные степени
            inv_p = modular_arithmetic_examples()["mod_inv"](p, m)
            self.inv_powers = [1] * (self.n + 1)
            for i in range(1, self.n + 1):
                self.inv_powers[i] = (self.inv_powers[i - 1] * inv_p) % m
        
        def get_hash(self, l: int, r: int) -> int:
            """Хэш подстроки s[l:r] (l включительно, r исключительно)"""
            res = (self.prefix[r] - self.prefix[l]) % self.m
            res = (res * self.inv_powers[l]) % self.m
            return res
        
        def compare(self, l1: int, r1: int, l2: int, r2: int) -> bool:
            """Сравнение двух подстрок"""
            if r1 - l1 != r2 - l2:
                return False
            return self.get_hash(l1, r1) == self.get_hash(l2, r2)
    
    class DoubleHash:
        """Двойной хэш для надёжности (устраняет коллизии)"""
        def __init__(self, s: str):
            p1, m1 = 911382323, 10**9 + 7
            p2, m2 = 972663749, 10**9 + 9
            self.h1 = StringHash(s, p1, m1)
            self.h2 = StringHash(s, p2, m2)
        
        def get_hash(self, l: int, r: int) -> Tuple[int, int]:
            return (self.h1.get_hash(l, r), self.h2.get_hash(l, r))
    
    # === Поиск всех вхождений подстроки (алгоритм Рабина-Карпа) ===
    def rabin_karp(text: str, pattern: str) -> List[int]:
        if len(pattern) > len(text):
            return []
        
        th = DoubleHash(text)
        ph = DoubleHash(pattern)
        pattern_hash = ph.get_hash(0, len(pattern))
        
        occurrences = []
        m = len(pattern)
        for i in range(len(text) - m + 1):
            if th.get_hash(i, i + m) == pattern_hash:
                if text[i:i+m] == pattern:  # финальная проверка
                    occurrences.append(i)
        
        return occurrences
    
    # === Проверка на палиндром ===
    def is_palindrome(s: str, l: int, r: int) -> bool:
        # Предвычисляем прямой и обратный хэши
        h = DoubleHash(s)
        rev_s = s[::-1]
        h_rev = DoubleHash(rev_s)
        
        # Индекс в перевёрнутой строке
        rev_l = len(s) - 1 - r
        rev_r = len(s) - l
        
        return h.get_hash(l, r) == h_rev.get_hash(rev_l, rev_r)
    
    # === Поиск наибольшей общей подстроки двух строк ===
    def longest_common_substring(s1: str, s2: str) -> str:
        """
        Бинарный поиск по длине + хэширование
        Сложность: O(N log N)
        """
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        
        def has_common(length: int) -> Tuple[bool, str]:
            h2 = DoubleHash(s2)
            hashes = set()
            for i in range(len(s2) - length + 1):
                hashes.add(h2.get_hash(i, i + length))
            
            h1 = DoubleHash(s1)
            for i in range(len(s1) - length + 1):
                if h1.get_hash(i, i + length) in hashes:
                    return True, s1[i:i+length]
            return False, ""
        
        left, right = 0, len(s1)
        result = ""
        while left <= right:
            mid = (left + right) // 2
            found, substr = has_common(mid)
            if found:
                result = substr
                left = mid + 1
            else:
                right = mid - 1
        
        return result

    return {
        "StringHash": StringHash,
        "DoubleHash": DoubleHash,
        "rabin_karp": rabin_karp,
        "longest_common_substring": longest_common_substring
    }


# ==================================================================================
# 5. ВЕКТОРНАЯ АЛГЕБРА (ГЕОМЕТРИЯ)
# ==================================================================================
# КОГДА:
# - Задачи с точками, прямыми, многоугольниками
# - Проверка пересечений, принадлежность точки
# - Площадь многоугольника
# - Выпуклая оболочка

def geometry_examples():
    """Примеры геометрических алгоритмов"""
    
    class Point:
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y
        
        def __sub__(self, other: 'Point') -> 'Point':
            return Point(self.x - other.x, self.y - other.y)
        
        def __add__(self, other: 'Point') -> 'Point':
            return Point(self.x + other.x, self.y + other.y)
        
        def __mul__(self, scalar: float) -> 'Point':
            return Point(self.x * scalar, self.y * scalar)
        
        def dot(self, other: 'Point') -> float:
            """Скалярное произведение"""
            return self.x * other.x + self.y * other.y
        
        def cross(self, other: 'Point') -> float:
            """Псевдоскалярное произведение (2D векторное)"""
            return self.x * other.y - self.y * other.x
        
        def len2(self) -> float:
            return self.x * self.x + self.y * self.y
        
        def len(self) -> float:
            return math.sqrt(self.len2())
    
    # === Ориентация трёх точек ===
    def orientation(a: Point, b: Point, c: Point) -> int:
        """
        Возвращает:
          >0 - против часовой стрелки (left turn)
          <0 - по часовой стрелке (right turn)
          =0 - коллинеарны
        """
        val = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
        if abs(val) < 1e-9:
            return 0
        return 1 if val > 0 else -1
    
    # === Проверка пересечения отрезков ===
    def segments_intersect(a1: Point, a2: Point, b1: Point, b2: Point) -> bool:
        o1 = orientation(a1, a2, b1)
        o2 = orientation(a1, a2, b2)
        o3 = orientation(b1, b2, a1)
        o4 = orientation(b1, b2, a2)
        
        # Общий случай
        if o1 != o2 and o3 != o4:
            return True
        
        # Частные случаи (коллинеарность)
        if o1 == 0 and on_segment(a1, a2, b1): return True
        if o2 == 0 and on_segment(a1, a2, b2): return True
        if o3 == 0 and on_segment(b1, b2, a1): return True
        if o4 == 0 and on_segment(b1, b2, a2): return True
        
        return False
    
    def on_segment(a: Point, b: Point, c: Point) -> bool:
        """Проверка, лежит ли точка c на отрезке [a,b]"""
        return (min(a.x, b.x) <= c.x <= max(a.x, b.x) and
                min(a.y, b.y) <= c.y <= max(a.y, b.y))
    
    # === Площадь многоугольника (формула Гаусса) ===
    def polygon_area(points: List[Point]) -> float:
        area = 0
        n = len(points)
        for i in range(n):
            j = (i + 1) % n
            area += points[i].x * points[j].y
            area -= points[j].x * points[i].y
        return abs(area) / 2
    
    # === Проверка точки внутри многоугольника (Ray casting) ===
    def point_in_polygon(point: Point, polygon: List[Point]) -> bool:
        n = len(polygon)
        inside = False
        for i in range(n):
            j = (i + 1) % n
            if ((polygon[i].y > point.y) != (polygon[j].y > point.y)) and \
               (point.x < (polygon[j].x - polygon[i].x) * (point.y - polygon[i].y) /
                (polygon[j].y - polygon[i].y) + polygon[i].x):
                inside = not inside
        return inside
    
    # === Выпуклая оболочка (алгоритм Эндрю) ===
    def convex_hull(points: List[Point]) -> List[Point]:
        points.sort(key=lambda p: (p.x, p.y))
        
        def build_hull(points):
            hull = []
            for p in points:
                while len(hull) >= 2 and orientation(hull[-2], hull[-1], p) <= 0:
                    hull.pop()
                hull.append(p)
            return hull
        
        lower = build_hull(points)
        upper = build_hull(list(reversed(points)))
        return lower[:-1] + upper[:-1]
    
    # === Расстояние от точки до прямой ===
    def point_line_distance(p: Point, a: Point, b: Point) -> float:
        # Площадь параллелограмма = |AB × AP|
        cross = abs((b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x))
        return cross / math.hypot(b.x - a.x, b.y - a.y)

    return {
        "Point": Point,
        "orientation": orientation,
        "segments_intersect": segments_intersect,
        "polygon_area": polygon_area,
        "point_in_polygon": point_in_polygon,
        "convex_hull": convex_hull
    }


# ==================================================================================
# 6. ДРУГИЕ ВАЖНЫЕ ТЕМЫ
# ==================================================================================

# --- Meet-in-the-Middle ---
# КОГДА: Перебор 2^n слишком большой (n=40), но можно разделить на две половины
def meet_in_the_middle(arr: List[int], target: int) -> bool:
    """
    Пример: найти подмножество с суммой target
    Сложность: O(2^(n/2) * n)
    """
    n = len(arr)
    left = arr[:n//2]
    right = arr[n//2:]
    
    # Генерируем все суммы для левой половины
    left_sums = []
    for mask in range(1 << len(left)):
        s = 0
        for i in range(len(left)):
            if mask & (1 << i):
                s += left[i]
        left_sums.append(s)
    
    # Генерируем для правой
    right_sums = []
    for mask in range(1 << len(right)):
        s = 0
        for i in range(len(right)):
            if mask & (1 << i):
                s += right[i]
        right_sums.append(s)
    
    right_sums.sort()
    for s in left_sums:
        # Ищем target - s в right_sums
        idx = bisect.bisect_left(right_sums, target - s)
        if idx < len(right_sums) and right_sums[idx] == target - s:
            return True
    return False


# --- Алгоритм сканирующей прямой (Sweep Line) ---
# КОГДА: Задачи на интервалы, пересечения отрезков, прямоугольники
def sweep_line_intervals(intervals: List[Tuple[int, int]]) -> int:
    """
    Пример: найти максимальное количество пересекающихся интервалов
    """
    events = []
    for l, r in intervals:
        events.append((l, 1))   # начало
        events.append((r, -1))  # конец
    events.sort()
    
    max_overlap = 0
    current = 0
    for _, delta in events:
        current += delta
        max_overlap = max(max_overlap, current)
    return max_overlap


# --- Корневая декомпозиция (sqrt decomposition) ---
# КОГДА: Нужно делать запросы и обновления, но лень писать дерево отрезков
class SqrtDecomposition:
    """
    Пример: сумма на отрезке с обновлениями
    Сложность: O(sqrt(n)) на операцию
    """
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.block_size = int(math.sqrt(self.n)) + 1
        self.blocks = [0] * ((self.n + self.block_size - 1) // self.block_size)
        self.arr = arr[:]
        
        for i, val in enumerate(arr):
            self.blocks[i // self.block_size] += val
    
    def update(self, idx: int, new_val: int):
        diff = new_val - self.arr[idx]
        self.arr[idx] = new_val
        self.blocks[idx // self.block_size] += diff
    
    def query(self, l: int, r: int) -> int:
        left_block = l // self.block_size
        right_block = r // self.block_size
        
        if left_block == right_block:
            return sum(self.arr[l:r+1])
        
        res = 0
        # Левая часть
        res += sum(self.arr[l:(left_block+1)*self.block_size])
        # Средние блоки
        for b in range(left_block+1, right_block):
            res += self.blocks[b]
        # Правая часть
        res += sum(self.arr[right_block*self.block_size:r+1])
        return res


# ==================================================================================

"""
По условию задачи:

1. ДП по маскам, перебор подмножеств -> БИТОВЫЕ ОПЕРАЦИИ
2. Два игрока, ходы, кто выигрывает -> ТЕОРИЯ ИГР
3. Результат нужно по модулю, большие числа -> МОДУЛЬНАЯ АРИФМЕТИКА
4. Сравнение строк, поиск подстрок, палиндромы -> ХЭШИРОВАНИЕ
5. Точки, прямые, многоугольники -> ГЕОМЕТРИЯ
6. 2^40 > перебор, но можно разделить -> MEET-IN-THE-MIDDLE
7. Много интервалов, найти пересечения -> СКАНИРУЮЩАЯ ПРЯМАЯ
8. N до 10^5, запросы и обновления -> ДЕРЕВО ОТРЕЗКОВ (в основном файле)
9. Объединение множеств, компоненты связности -> DSU (в основном файле)

Сложности:
- O(2^n) - битовые маски (n <= 20)
- O(2^(n/2)) - meet-in-the-middle (n <= 40)
- O(sqrt(N)) - корневая декомпозиция
- O(log N) - дерево отрезков, бинарный поиск
- O(α(N)) - DSU (почти константа)
"""


if __name__ == "__main__":
    print("Сборник алгоритмов загружен")
    print("Используйте:")
    print("  bit_usage_examples() - битовые операции")
    print("  game_theory_examples() - теория игр")
    print("  modular_arithmetic_examples() - модулярная арифметика")
    print("  hashing_examples() - хэширование")
    print("  geometry_examples() - геометрия")
