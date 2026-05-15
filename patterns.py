# ==================================================================================
#                        ОЛИМПИАДНЫЕ АЛГОРИТМЫ И СТРУКТУРЫ ДАННЫХ
#                                   (Python версия)
# ==================================================================================
# Сборник содержит реализации классических алгоритмов с подробными комментариями
# Для каждого алгоритма указаны:
# - Назначение (для чего применяется)
# - Асимптотическая сложность по времени и памяти
# - Описание всех параметров функций
# - Пошаговое объяснение логики работы
# ==================================================================================

from typing import List, Tuple, Optional, Union
from collections import deque
import heapq
import bisect
import sys

# =========================== 1. БИНАРНЫЙ ПОИСК ====================================
# НАЗНАЧЕНИЕ: поиск элемента в отсортированном массиве или бинарный поиск по ответу
# СЛОЖНОСТЬ: время O(log N), память O(1)
# ==================================================================================

def binary_search(arr: List[int], target: int) -> int:
    """
    Бинарный поиск в отсортированном массиве
    
    Args:
        arr: Отсортированный список целых чисел (по возрастанию)
        target: Искомое значение
    
    Returns:
        int: Индекс первого вхождения target или -1, если элемент не найден
    
    Details:
        Алгоритм на каждой итерации делит интервал поиска пополам:
        1. Вычисляется средний индекс mid = left + (right - left) // 2
        2. Если arr[mid] == target -> элемент найден
        3. Если arr[mid] < target -> искомое в правой половине (left = mid + 1)
        4. Если arr[mid] > target -> искомое в левой половине (right = mid - 1)
    """
    left = 0                        # Левая граница поиска (включительно)
    right = len(arr) - 1            # Правая граница поиска (включительно)
    
    while left <= right:
        # Предотвращаем переполнение при вычислении среднего индекса
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid              # Элемент найден, возвращаем его индекс
        elif arr[mid] < target:
            left = mid + 1          # Ищем в правой половине
        else:
            right = mid - 1         # Ищем в левой половине
    
    return -1                       # Элемент не найден


def lower_bound(arr: List[int], target: int) -> int:
    """
    Бинарный поиск первого элемента >= target (аналог C++ lower_bound)
    
    Args:
        arr: Отсортированный список целых чисел
        target: Пороговое значение
    
    Returns:
        int: Индекс первого элемента >= target или len(arr), если все элементы меньше
    
    Details:
        Используется для поиска позиции вставки и решения задач типа
        "найти минимальное значение, удовлетворяющее условию"
    """
    left = 0
    right = len(arr)                # right указывает за последний элемент
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1          # Все элементы слева от mid строго меньше target
        else:
            right = mid             # arr[mid] >= target, сужаем правую границу
    
    return left                     # Первый индекс, где arr[i] >= target


def upper_bound(arr: List[int], target: int) -> int:
    """
    Бинарный поиск первого элемента > target (аналог C++ upper_bound)
    
    Args:
        arr: Отсортированный список целых чисел
        target: Пороговое значение
    
    Returns:
        int: Индекс первого элемента > target или len(arr)
    """
    left = 0
    right = len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left


# =========================== 2. ПРЕФИКСНЫЕ СУММЫ ==================================
# НАЗНАЧЕНИЕ: вычисление суммы на любом подотрезке массива за O(1)
# СЛОЖНОСТЬ: предобработка O(N), запрос O(1), память O(N)
# ==================================================================================

def build_prefix_sums(arr: List[int]) -> List[int]:
    """
    Построение массива префиксных сумм
    
    Args:
        arr: Исходный список целых чисел
    
    Returns:
        List[int]: Массив pref, где pref[i] = сумма первых i элементов
    
    Details:
        Формула: pref[0] = 0, pref[i] = pref[i-1] + arr[i-1]
        Тогда сумма на отрезке [L, R] = pref[R+1] - pref[L]
    """
    n = len(arr)
    pref = [0] * (n + 1)            # pref[0] = 0 для удобства
    
    for i in range(n):
        pref[i + 1] = pref[i] + arr[i]  # Накапливаем сумму
    
    return pref


def range_sum(pref: List[int], L: int, R: int) -> int:
    """
    Вычисление суммы на отрезке [L, R] с использованием префиксных сумм
    
    Args:
        pref: Массив префиксных сумм, построенный функцией build_prefix_sums
        L: Левая граница отрезка (включительно, 0-indexed)
        R: Правая граница отрезка (включительно, 0-indexed)
    
    Returns:
        int: Сумма элементов от L до R включительно
    
    Details:
        Математически: sum[L..R] = pref[R+1] - pref[L]
        Пример: arr = [2, 3, 5], L=0, R=2
        pref = [0, 2, 5, 10], ответ = 10 - 0 = 10
    """
    return pref[R + 1] - pref[L]


def build_prefix_sums_2d(matrix: List[List[int]]) -> List[List[int]]:
    """
    Построение двумерных префиксных сумм
    
    Args:
        matrix: Двумерный список целых чисел размера N x M
    
    Returns:
        List[List[int]]: Массив префиксных сумм размера (N+1) x (M+1)
    
    Details:
        pref[i][j] = сумма элементов в прямоугольнике (0,0) - (i-1, j-1)
        Позволяет за O(1) находить сумму в любом прямоугольнике
    """
    n, m = len(matrix), len(matrix[0])
    pref = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n):
        for j in range(m):
            pref[i + 1][j + 1] = (pref[i][j + 1] + pref[i + 1][j] - 
                                  pref[i][j] + matrix[i][j])
    
    return pref


def range_sum_2d(pref: List[List[int]], r1: int, c1: int, r2: int, c2: int) -> int:
    """
    Вычисление суммы в прямоугольнике [r1..r2] x [c1..c2]
    
    Args:
        pref: Двумерные префиксные суммы
        r1, c1: Координаты верхнего левого угла (0-indexed)
        r2, c2: Координаты нижнего правого угла (0-indexed)
    
    Returns:
        int: Сумма элементов в прямоугольнике
    """
    return (pref[r2 + 1][c2 + 1] - pref[r1][c2 + 1] - 
            pref[r2 + 1][c1] + pref[r1][c1])


# =========================== 3. МЕТОД ДВУХ УКАЗАТЕЛЕЙ ==============================
# НАЗНАЧЕНИЕ: решение задач на подотрезки/подпоследовательности за линейное время
# СЛОЖНОСТЬ: время O(N), память O(1)
# ==================================================================================

def two_sum_sorted(arr: List[int], target: int) -> Tuple[int, int]:
    """
    Поиск пары элементов с заданной суммой в отсортированном массиве
    
    Args:
        arr: Отсортированный по возрастанию список целых чисел
        target: Целевая сумма
    
    Returns:
        Tuple[int, int]: Индексы пары элементов или (-1, -1), если пара не найдена
    
    Details:
        Алгоритм использует два указателя: left в начале, right в конце.
        На каждом шаге вычисляется сумма arr[left] + arr[right]:
        - Если сумма == target -> решение найдено
        - Если сумма < target -> нужно увеличить сумму (left++)
        - Если сумма > target -> нужно уменьшить сумму (right--)
    """
    left = 0                         # Левый указатель (минимальный элемент)
    right = len(arr) - 1             # Правый указатель (максимальный элемент)
    
    while left < right:
        current_sum = arr[left] + arr[right]
        
        if current_sum == target:
            return left, right       # Пара найдена
        elif current_sum < target:
            left += 1                # Увеличиваем сумму, двигая левый указатель
        else:
            right -= 1               # Уменьшаем сумму, двигая правый указатель
    
    return -1, -1                    # Пара не найдена


def max_subarray_length_with_sum_limit(arr: List[int], limit: int) -> int:
    """
    Поиск длины максимального подотрезка с суммой <= limit
    
    Args:
        arr: Список неотрицательных целых чисел
        limit: Максимально допустимая сумма
    
    Returns:
        int: Длина самого длинного подотрезка с суммой <= limit
    
    Details:
        Используется скользящее окно (разновидность двух указателей).
        right указатель расширяет окно, left - сужает, когда сумма превышает лимит.
    """
    n = len(arr)
    left = 0                         # Левая граница окна
    current_sum = 0                  # Текущая сумма в окне
    max_length = 0                   # Максимальная длина подходящего окна
    
    for right in range(n):
        current_sum += arr[right]    # Расширяем окно вправо
        
        # Если сумма превысила лимит, сдвигаем левую границу
        while current_sum > limit and left <= right:
            current_sum -= arr[left]
            left += 1
        
        # Обновляем максимальную длину
        max_length = max(max_length, right - left + 1)
    
    return max_length


def three_sum(arr: List[int], target: int) -> List[Tuple[int, int, int]]:
    """
    Поиск всех троек элементов с заданной суммой
    
    Args:
        arr: Список целых чисел (будет отсортирован внутри)
        target: Целевая сумма
    
    Returns:
        List[Tuple[int, int, int]]: Список троек индексов
    
    Details:
        Сложность O(N^2). Фиксируем первый элемент, для остальных
        используем метод двух указателей
    """
    n = len(arr)
    arr_sorted = sorted(enumerate(arr), key=lambda x: x[1])
    result = []
    
    for i in range(n - 2):
        if i > 0 and arr_sorted[i][1] == arr_sorted[i - 1][1]:
            continue  # Пропускаем дубликаты
        
        left, right = i + 1, n - 1
        while left < right:
            current_sum = (arr_sorted[i][1] + arr_sorted[left][1] + 
                          arr_sorted[right][1])
            
            if current_sum == target:
                result.append((arr_sorted[i][0], arr_sorted[left][0], 
                              arr_sorted[right][0]))
                left += 1
                right -= 1
                # Пропускаем дубликаты
                while (left < right and 
                       arr_sorted[left][1] == arr_sorted[left - 1][1]):
                    left += 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result


# =========================== 4. ДЕРЕВО ОТРЕЗКОВ ===================================
# НАЗНАЧЕНИЕ: запросы на отрезках (сумма, min, max) и обновления за O(log N)
# СЛОЖНОСТЬ: построение O(N), запрос O(log N), память O(4N)
# ==================================================================================

class SegmentTree:
    """
    Дерево отрезков для операции суммы с возможностью обновления элементов
    
    Details:
        Структура данных хранит элементы в виде полного бинарного дерева.
        Корень (вершина 1) отвечает за весь массив [0, n-1].
        Левое поддерево отвечает за [tl, tm], правое за [tm+1, tr].
    """
    
    def __init__(self, arr: List[int]):
        """
        Конструктор дерева отрезков
        
        Args:
            arr: Исходный массив для построения дерева
        """
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)  # Дереву нужно до 4n памяти
        self._build(arr, 1, 0, self.n - 1)
    
    def _build(self, arr: List[int], v: int, tl: int, tr: int) -> None:
        """
        Рекурсивное построение дерева отрезков
        
        Args:
            arr: Исходный массив
            v: Номер текущей вершины
            tl: Левая граница отрезка, за который отвечает вершина v
            tr: Правая граница отрезка, за который отвечает вершина v
        """
        if tl == tr:
            # Лист дерева - хранит один элемент массива
            self.tree[v] = arr[tl]
        else:
            tm = (tl + tr) // 2
            # Рекурсивно строим левое и правое поддеревья
            self._build(arr, v * 2, tl, tm)
            self._build(arr, v * 2 + 1, tm + 1, tr)
            # Значение в вершине - сумма значений детей
            self.tree[v] = self.tree[v * 2] + self.tree[v * 2 + 1]
    
    def _query(self, v: int, tl: int, tr: int, l: int, r: int) -> int:
        """
        Запрос суммы на отрезке [l, r]
        
        Args:
            v: Номер текущей вершины
            tl: Левая граница отрезка вершины v
            tr: Правая граница отрезка вершины v
            l: Левая граница запроса
            r: Правая граница запроса
        
        Returns:
            int: Сумма на отрезке [l, r]
        """
        if l > r:
            return 0                 # Пустой запрос
        if l == tl and r == tr:
            return self.tree[v]      # Отрезок полностью совпадает с запросом
        
        tm = (tl + tr) // 2
        # Разбиваем запрос на две части и суммируем результаты
        return (self._query(v * 2, tl, tm, l, min(r, tm)) +
                self._query(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r))
    
    def _update(self, v: int, tl: int, tr: int, pos: int, new_val: int) -> None:
        """
        Обновление значения элемента в позиции pos
        
        Args:
            v: Номер текущей вершины
            tl: Левая граница отрезка вершины v
            tr: Правая граница отрезка вершины v
            pos: Индекс обновляемого элемента
            new_val: Новое значение
        """
        if tl == tr:
            # Дошли до листа - обновляем значение
            self.tree[v] = new_val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                # Элемент в левом поддереве
                self._update(v * 2, tl, tm, pos, new_val)
            else:
                # Элемент в правом поддереве
                self._update(v * 2 + 1, tm + 1, tr, pos, new_val)
            # Обновляем значения всех вершин на пути к корню
            self.tree[v] = self.tree[v * 2] + self.tree[v * 2 + 1]
    
    def get_sum(self, l: int, r: int) -> int:
        """
        Публичный метод для запроса суммы на отрезке
        
        Args:
            l: Левая граница запроса (0-indexed)
            r: Правая граница запроса (0-indexed)
        
        Returns:
            int: Сумма на отрезке [l, r]
        """
        return self._query(1, 0, self.n - 1, l, r)
    
    def set_value(self, pos: int, new_val: int) -> None:
        """
        Публичный метод для обновления элемента
        
        Args:
            pos: Индекс обновляемого элемента (0-indexed)
            new_val: Новое значение
        """
        self._update(1, 0, self.n - 1, pos, new_val)


class SegmentTreeMinMax:
    """
    Дерево отрезков с поддержкой операций минимума, максимума и суммы
    
    Details:
        Расширенная версия дерева отрезков, которая хранит в каждой вершине
        сразу три значения: сумму, минимум и максимум на соответствующем отрезке.
        Это позволяет отвечать на разнообразные запросы за O(log N).
    """
    
    def __init__(self, arr: List[int]):
        """
        Конструктор дерева отрезков с поддержкой min/max
        
        Args:
            arr: Исходный массив для построения дерева
        """
        self.n = len(arr)
        self.sum_tree = [0] * (4 * self.n)
        self.min_tree = [0] * (4 * self.n)
        self.max_tree = [0] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)
    
    def _build(self, arr: List[int], v: int, tl: int, tr: int) -> None:
        """Рекурсивное построение всех трёх деревьев"""
        if tl == tr:
            self.sum_tree[v] = arr[tl]
            self.min_tree[v] = arr[tl]
            self.max_tree[v] = arr[tl]
        else:
            tm = (tl + tr) // 2
            self._build(arr, v * 2, tl, tm)
            self._build(arr, v * 2 + 1, tm + 1, tr)
            self.sum_tree[v] = self.sum_tree[v * 2] + self.sum_tree[v * 2 + 1]
            self.min_tree[v] = min(self.min_tree[v * 2], self.min_tree[v * 2 + 1])
            self.max_tree[v] = max(self.max_tree[v * 2], self.max_tree[v * 2 + 1])
    
    def _query_sum(self, v: int, tl: int, tr: int, l: int, r: int) -> int:
        """Запрос суммы на отрезке [l, r]"""
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.sum_tree[v]
        tm = (tl + tr) // 2
        return (self._query_sum(v * 2, tl, tm, l, min(r, tm)) +
                self._query_sum(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r))
    
    def _query_min(self, v: int, tl: int, tr: int, l: int, r: int) -> int:
        """
        Запрос минимума на отрезке [l, r]
        
        Returns:
            int: Минимальное значение на отрезке [l, r]
        """
        if l > r:
            return float('inf')      # Для пустого запроса возвращаем "бесконечность"
        if l == tl and r == tr:
            return self.min_tree[v]
        tm = (tl + tr) // 2
        return min(self._query_min(v * 2, tl, tm, l, min(r, tm)),
                   self._query_min(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r))
    
    def _query_max(self, v: int, tl: int, tr: int, l: int, r: int) -> int:
        """
        Запрос максимума на отрезке [l, r]
        
        Returns:
            int: Максимальное значение на отрезке [l, r]
        """
        if l > r:
            return float('-inf')     # Для пустого запроса возвращаем "минус бесконечность"
        if l == tl and r == tr:
            return self.max_tree[v]
        tm = (tl + tr) // 2
        return max(self._query_max(v * 2, tl, tm, l, min(r, tm)),
                   self._query_max(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r))
    
    def _update(self, v: int, tl: int, tr: int, pos: int, new_val: int) -> None:
        """Обновление значения элемента в позиции pos"""
        if tl == tr:
            self.sum_tree[v] = new_val
            self.min_tree[v] = new_val
            self.max_tree[v] = new_val
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self._update(v * 2, tl, tm, pos, new_val)
            else:
                self._update(v * 2 + 1, tm + 1, tr, pos, new_val)
            self.sum_tree[v] = self.sum_tree[v * 2] + self.sum_tree[v * 2 + 1]
            self.min_tree[v] = min(self.min_tree[v * 2], self.min_tree[v * 2 + 1])
            self.max_tree[v] = max(self.max_tree[v * 2], self.max_tree[v * 2 + 1])
    
    def get_sum(self, l: int, r: int) -> int:
        """Получение суммы на отрезке [l, r]"""
        return self._query_sum(1, 0, self.n - 1, l, r)
    
    def get_min(self, l: int, r: int) -> int:
        """
        Получение минимума на отрезке [l, r]
        
        Args:
            l: Левая граница запроса (0-indexed, включительно)
            r: Правая граница запроса (0-indexed, включительно)
        
        Returns:
            int: Минимальное значение на отрезке [l, r]
        
        Example:
            массив [3, 1, 4, 1, 5], запрос get_min(1, 3) вернёт 1
        """
        return self._query_min(1, 0, self.n - 1, l, r)
    
    def get_max(self, l: int, r: int) -> int:
        """
        Получение максимума на отрезке [l, r]
        
        Args:
            l: Левая граница запроса (0-indexed, включительно)
            r: Правая граница запроса (0-indexed, включительно)
        
        Returns:
            int: Максимальное значение на отрезке [l, r]
        
        Example:
            массив [3, 1, 4, 1, 5], запрос get_max(0, 3) вернёт 4
        """
        return self._query_max(1, 0, self.n - 1, l, r)
    
    def set_value(self, pos: int, new_val: int) -> None:
        """Обновление значения элемента в позиции pos"""
        self._update(1, 0, self.n - 1, pos, new_val)
    
    def get_stats(self, l: int, r: int) -> Tuple[int, int, int]:
        """
        Получение всех трёх статистик на отрезке [l, r] за один проход
        
        Returns:
            Tuple[int, int, int]: Кортеж (сумма, минимум, максимум)
        """
        return self.get_sum(l, r), self.get_min(l, r), self.get_max(l, r)


# =========================== 5. DSU (СИСТЕМА НЕПЕРЕСЕКАЮЩИХСЯ МНОЖЕСТВ) ==============
# НАЗНАЧЕНИЕ: работа с разбиением множества на компоненты (алгоритм Краскала и др.)
# СЛОЖНОСТЬ: практически O(1) на операцию, память O(N)
# ==================================================================================

class DSU:
    """
    Disjoint Set Union (Union-Find) с эвристиками сжатия путей и размера
    
    Details:
        Структура поддерживает операции:
        - find(x): найти представителя множества, содержащего x
        - union(x, y): объединить множества, содержащие x и y
        - get_size(x): получить размер множества, содержащего x
    """
    
    def __init__(self, n: int):
        """
        Конструктор DSU
        
        Args:
            n: Количество элементов (0..n-1)
        
        Details:
            Изначально каждый элемент в своём множестве
        """
        self.parent = list(range(n))  # parent[i] - родитель элемента i
        self.size = [1] * n           # size[i] - размер множества с корнем i
    
    def find(self, x: int) -> int:
        """
        Поиск корня множества с эвристикой сжатия путей
        
        Args:
            x: Элемент, для которого ищем представителя
        
        Returns:
            int: Корень (представитель) множества
        
        Details:
            Сжатие путей: parent[x] = find(parent[x]) делает дерево плоским,
            ускоряя последующие запросы практически до O(1)
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Рекурсивно поднимаемся и сжимаем путь
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """
        Объединение множеств, содержащих x и y
        
        Args:
            x: Первый элемент
            y: Второй элемент
        
        Returns:
            bool: True, если множества были объединены, False если уже в одном
        
        Details:
            Используется эвристика размера: меньшее множество присоединяется
            к большему для сохранения баланса дерева
        """
        x = self.find(x)
        y = self.find(y)
        
        if x == y:
            return False             # Уже в одном множестве
        
        # Присоединяем меньшее множество к большему
        if self.size[x] < self.size[y]:
            x, y = y, x
        
        self.parent[y] = x
        self.size[x] += self.size[y]
        return True
    
    def get_size(self, x: int) -> int:
        """
        Получение размера множества, содержащего элемент x
        
        Args:
            x: Элемент множества
        
        Returns:
            int: Размер множества
        """
        return self.size[self.find(x)]
    
    def same_set(self, x: int, y: int) -> bool:
        """
        Проверка, находятся ли два элемента в одном множестве
        
        Args:
            x: Первый элемент
            y: Второй элемент
        
        Returns:
            bool: True, если в одном множестве
        """
        return self.find(x) == self.find(y)


class DSUWithRank:
    """
    Альтернативная реализация DSU с ранговой эвристикой
    """
    
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        
        if self.rank[xr] < self.rank[yr]:
            xr, yr = yr, xr
        self.parent[yr] = xr
        if self.rank[xr] == self.rank[yr]:
            self.rank[xr] += 1
        return True


# =========================== 6. ОБХОДЫ ГРАФА (BFS И DFS) ===========================
# НАЗНАЧЕНИЕ: базовые алгоритмы обхода графа для поиска компонент связности и др.
# СЛОЖНОСТЬ: время O(V + E), память O(V)
# ==================================================================================

def dfs(v: int, visited: List[bool], adj: List[List[int]], 
        component: Optional[List[int]] = None) -> None:
    """
    Поиск в глубину (DFS) с рекурсивной реализацией
    
    Args:
        v: Текущая вершина
        visited: Список посещённых вершин (изменяется в процессе)
        adj: Список смежности графа
        component: Список для сохранения вершин текущей компоненты (опционально)
    
    Details:
        Алгоритм рекурсивно посещает все непосещённые вершины,
        доступные из текущей. Используется для:
        - Поиска компонент связности
        - Проверки наличия циклов
        - Топологической сортировки (с дополнительным стеком)
    """
    visited[v] = True
    if component is not None:
        component.append(v)          # Сохраняем вершину в компоненту
    
    # Рекурсивно посещаем всех соседей
    for u in adj[v]:
        if not visited[u]:
            dfs(u, visited, adj, component)


def dfs_iterative(start: int, adj: List[List[int]]) -> List[int]:
    """
    Итеративный DFS с использованием стека
    
    Args:
        start: Стартовая вершина
        adj: Список смежности графа
    
    Returns:
        List[int]: Порядок обхода вершин
    """
    n = len(adj)
    visited = [False] * n
    order = []
    stack = [start]
    
    while stack:
        v = stack.pop()
        if not visited[v]:
            visited[v] = True
            order.append(v)
            # Добавляем соседей в обратном порядке для сохранения порядка обхода
            for u in reversed(adj[v]):
                if not visited[u]:
                    stack.append(u)
    
    return order


def bfs(start: int, adj: List[List[int]]) -> List[int]:
    """
    Поиск в ширину (BFS) для нахождения кратчайших расстояний
    
    Args:
        start: Стартовая вершина
        adj: Список смежности графа
    
    Returns:
        List[int]: Массив кратчайших расстояний от start до всех вершин
    
    Details:
        Используется очередь для обхода вершин по уровням.
        BFS гарантирует, что вершины посещаются в порядке увеличения
        расстояния от стартовой вершины.
    """
    n = len(adj)
    dist = [-1] * n                 # -1 означает, что вершина недостижима
    q = deque([start])
    dist[start] = 0
    
    while q:
        v = q.popleft()
        for u in adj[v]:
            if dist[u] == -1:       # Вершина ещё не посещена
                dist[u] = dist[v] + 1
                q.append(u)
    
    return dist


def bfs_with_path(start: int, end: int, adj: List[List[int]]) -> Optional[List[int]]:
    """
    BFS с восстановлением кратчайшего пути
    
    Args:
        start: Стартовая вершина
        end: Конечная вершина
        adj: Список смежности
    
    Returns:
        Optional[List[int]]: Кратчайший путь или None, если путь не существует
    """
    n = len(adj)
    dist = [-1] * n
    parent = [-1] * n
    q = deque([start])
    dist[start] = 0
    
    while q:
        v = q.popleft()
        if v == end:
            break
        for u in adj[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                parent[u] = v
                q.append(u)
    
    if dist[end] == -1:
        return None                 # Путь не найден
    
    # Восстановление пути
    path = []
    curr = end
    while curr != -1:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    
    return path


def find_connected_components(n: int, adj: List[List[int]]) -> List[List[int]]:
    """
    Поиск компонент связности в неориентированном графе
    
    Args:
        n: Количество вершин в графе
        adj: Список смежности
    
    Returns:
        List[List[int]]: Список компонент связности (каждая - список вершин)
    """
    visited = [False] * n
    components = []
    
    for v in range(n):
        if not visited[v]:
            component = []
            dfs(v, visited, adj, component)
            components.append(component)
    
    return components


def topological_sort(n: int, adj: List[List[int]]) -> Optional[List[int]]:
    """
    Топологическая сортировка ориентированного графа (алгоритм Кана)
    
    Args:
        n: Количество вершин
        adj: Список смежности
    
    Returns:
        Optional[List[int]]: Топологический порядок или None, если есть цикл
    """
    # Подсчёт входящих степеней
    in_degree = [0] * n
    for v in range(n):
        for u in adj[v]:
            in_degree[u] += 1
    
    # Очередь вершин с нулевой входящей степенью
    q = deque([v for v in range(n) if in_degree[v] == 0])
    order = []
    
    while q:
        v = q.popleft()
        order.append(v)
        for u in adj[v]:
            in_degree[u] -= 1
            if in_degree[u] == 0:
                q.append(u)
    
    # Если посетили не все вершины, значит есть цикл
    if len(order) != n:
        return None
    return order


# =========================== 7. АЛГОРИТМ ДЕЙКСТРЫ =================================
# НАЗНАЧЕНИЕ: поиск кратчайших путей от одной вершины в графе с неотрицательными весами
# СЛОЖНОСТЬ: время O((V + E) log V), память O(V + E)
# ==================================================================================

def dijkstra(start: int, adj: List[List[Tuple[int, int]]]) -> Tuple[List[int], List[int]]:
    """
    Алгоритм Дейкстры для поиска кратчайших расстояний и путей
    
    Args:
        start: Стартовая вершина
        adj: Список смежности графа в формате: adj[v] = List[(u, w)],
             где u - соседняя вершина, w - вес ребра
    
    Returns:
        Tuple[List[int], List[int]]: (массив кратчайших расстояний, массив предков)
    
    Details:
        Использует приоритетную очередь (min-heap) для выбора вершины с
        минимальным текущим расстоянием. Работает только с неотрицательными весами.
    """
    n = len(adj)
    INF = float('inf')
    
    dist = [INF] * n
    parent = [-1] * n
    dist[start] = 0
    
    # Приоритетная очередь хранит пары (расстояние, вершина)
    pq = [(0, start)]
    
    while pq:
        d, v = heapq.heappop(pq)
        
        # Если извлекли устаревшее расстояние - пропускаем
        if d != dist[v]:
            continue
        
        # Релаксация всех рёбер из текущей вершины
        for u, w in adj[v]:
            if dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
                parent[u] = v
                heapq.heappush(pq, (dist[u], u))
    
    return dist, parent


def get_path(parent: List[int], end: int) -> List[int]:
    """
    Восстановление пути из массива предков
    
    Args:
        parent: Массив предков
        end: Конечная вершина
    
    Returns:
        List[int]: Путь от стартовой вершины до end
    """
    path = []
    curr = end
    while curr != -1:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path


# =========================== 8. ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ =====================
# НАЗНАЧЕНИЕ: решение оптимизационных задач путём разбиения на подзадачи
# ПРИМЕР: задача о рюкзаке 0/1
# СЛОЖНОСТЬ: время O(N * W), память O(W)
# ==================================================================================

def knapsack_01(W: int, weights: List[int], values: List[int]) -> int:
    """
    Решение задачи о рюкзаке 0/1 методом динамического программирования
    
    Args:
        W: Максимально допустимый вес рюкзака
        weights: Список весов предметов
        values: Список стоимостей предметов
    
    Returns:
        int: Максимальная достижимая стоимость
    
    Details:
        Задача: выбрать подмножество предметов с максимальной суммарной
        стоимостью, чтобы суммарный вес не превышал W.
        Каждый предмет можно взять не более одного раза (0/1).
        Формула: dp[w] = max(dp[w], dp[w - weight[i]] + value[i])
        Обратный проход по весам позволяет использовать одномерный массив.
    """
    # dp[w] - максимальная стоимость при вместимости w
    dp = [0] * (W + 1)
    
    for i in range(len(weights)):
        # Обратный проход предотвращает повторное использование предмета
        for w in range(W, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[W]


def knapsack_01_with_items(W: int, weights: List[int], values: List[int]) -> Tuple[int, List[int]]:
    """
    Задача о рюкзаке с возможностью восстановления выбранных предметов
    
    Args:
        W: Максимально допустимый вес
        weights: Веса предметов
        values: Стоимости предметов
    
    Returns:
        Tuple[int, List[int]]: (максимальная стоимость, индексы выбранных предметов)
    """
    n = len(weights)
    # Двумерный массив dp для восстановления ответа
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]  # Не берём предмет i-1
            if w >= weights[i - 1]:
                dp[i][w] = max(dp[i][w], 
                              dp[i - 1][w - weights[i - 1]] + values[i - 1])
    
    # Восстановление выбранных предметов
    selected = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            # Предмет i-1 был взят
            selected.append(i - 1)
            w -= weights[i - 1]
    selected.reverse()
    
    return dp[n][W], selected


def knapsack_unbounded(W: int, weights: List[int], values: List[int]) -> int:
    """
    Неограниченный рюкзак (каждый предмет можно брать сколько угодно раз)
    
    Args:
        W: Максимально допустимый вес
        weights: Веса предметов
        values: Стоимости предметов
    
    Returns:
        int: Максимальная стоимость
    """
    dp = [0] * (W + 1)
    
    for w in range(1, W + 1):
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[W]


def longest_common_subsequence(s1: str, s2: str) -> int:
    """
    Наибольшая общая подпоследовательность (LCS)
    
    Args:
        s1: Первая строка
        s2: Вторая строка
    
    Returns:
        int: Длина наибольшей общей подпоследовательности
    """
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[n][m]


def longest_increasing_subsequence(arr: List[int]) -> int:
    """
    Наибольшая возрастающая подпоследовательность (LIS) за O(N log N)
    
    Args:
        arr: Список чисел
    
    Returns:
        int: Длина наибольшей возрастающей подпоследовательности
    """
    tails = []
    
    for x in arr:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    
    return len(tails)


# =========================== 9. РЕШЕТО ЭРАТОСФЕНА =================================
# НАЗНАЧЕНИЕ: генерация простых чисел до заданного предела N
# СЛОЖНОСТЬ: время O(N log log N), память O(N)
# ==================================================================================

def sieve_of_eratosthenes(n: int) -> List[bool]:
    """
    Генерация простых чисел с помощью решета Эратосфена
    
    Args:
        n: Верхняя граница диапазона (включительно)
    
    Returns:
        List[bool]: Массив размера n+1, где is_prime[i] = True если i простое
    
    Details:
        Алгоритм "вычёркивает" все числа, кратные найденным простым.
        Оптимизация: внутренний цикл начинается с i*i, т.к. меньшие кратные
        уже были вычеркнуты на предыдущих шагах.
    """
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False  # 0 и 1 не являются простыми
    
    # Перебираем возможные делители до sqrt(n)
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            # Вычёркиваем все числа, кратные i, начиная с i*i
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    
    return is_prime


def get_primes_list(n: int) -> List[int]:
    """
    Получение списка простых чисел до n
    
    Args:
        n: Верхняя граница диапазона
    
    Returns:
        List[int]: Список всех простых чисел от 2 до n
    """
    is_prime = sieve_of_eratosthenes(n)
    return [i for i in range(2, n + 1) if is_prime[i]]


def sieve_linear(n: int) -> List[int]:
    """
    Линейное решето Эратосфена за O(N)
    
    Args:
        n: Верхняя граница
    
    Returns:
        List[int]: Список простых чисел
    """
    primes = []
    min_prime = [0] * (n + 1)  # Минимальный простой делитель
    
    for i in range(2, n + 1):
        if min_prime[i] == 0:
            min_prime[i] = i
            primes.append(i)
        
        for p in primes:
            if p > min_prime[i] or i * p > n:
                break
            min_prime[i * p] = p
    
    return primes


# =========================== 10. БЫСТРОЕ ВОЗВЕДЕНИЕ В СТЕПЕНЬ ======================
# НАЗНАЧЕНИЕ: вычисление a^n mod m за логарифмическое время
# СЛОЖНОСТЬ: время O(log n), память O(1)
# ==================================================================================

def binpow(a: int, n: int, mod: Optional[int] = None) -> int:
    """
    Бинарное (быстрое) возведение в степень по модулю
    
    Args:
        a: Основание степени
        n: Показатель степени (неотрицательное целое)
        mod: Модуль (опционально)
    
    Returns:
        int: Результат a^n mod mod (или a^n, если mod не указан)
    
    Details:
        Алгоритм использует двоичное представление показателя степени:
        a^n = (a^(n/2))^2, если n чётное
        a^n = a * (a^(n/2))^2, если n нечётное
    """
    res = 1
    if mod is not None:
        a %= mod
    
    while n > 0:
        if n & 1:                    # Если текущий бит n равен 1
            res = res * a
            if mod is not None:
                res %= mod
        a = a * a
        if mod is not None:
            a %= mod
        n >>= 1                      # Сдвигаем n вправо (делим на 2)
    
    return res


# =========================== 11. СТРОКОВЫЕ АЛГОРИТМЫ ===============================
# НАЗНАЧЕНИЕ: эффективный поиск подстроки в строке, анализ периодичности строк
# ==================================================================================

def prefix_function(s: str) -> List[int]:
    """
    Вычисление префикс-функции для строки
    
    Args:
        s: Исходная строка
    
    Returns:
        List[int]: Массив pi, где pi[i] - длина наибольшего собственного
                   префикса подстроки s[0..i], который является её суффиксом
    
    Details:
        Префикс-функция определяется следующим образом:
        pi[i] = max{k | k < i+1 и s[0..k-1] == s[i-k+1..i]}
        
        Алгоритм работает за O(N) благодаря использованию уже вычисленных
        значений. На каждом шаге пытаемся расширить текущий префикс,
        а если не получается - переходим по pi[k-1].
        
        Пример для строки "abacaba":
        i:   0 1 2 3 4 5 6
        s:   a b a c a b a
        pi:  0 0 1 0 1 2 3
        
        Применение:
        - Поиск подстроки в строке (алгоритм КМП)
        - Поиск всех вхождений подстроки
        - Вычисление периода строки
        - Построение автомата КМП
    """
    n = len(s)
    pi = [0] * n
    
    # pi[0] всегда 0, так как у односимвольной строки нет собственных префиксов
    for i in range(1, n):
        # j - длина текущего совпадающего префикса для позиции i-1
        j = pi[i - 1]
        
        # Пытаемся расширить префикс: проверяем, совпадает ли следующий символ
        # Если не совпадает, переходим к меньшему префиксу-кандидату
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]            # Ключевая оптимизация КМП - используем уже вычисленные pi
        
        # Если символы совпали, увеличиваем длину префикса
        if s[i] == s[j]:
            j += 1
        
        pi[i] = j
    
    return pi


def find_period(s: str) -> int:
    """
    Вычисление периода строки с помощью префикс-функции
    
    Args:
        s: Исходная строка
    
    Returns:
        int: Длина минимального периода строки
    
    Details:
        Строка имеет период длины k, если s[i] == s[i+k] для всех i.
        Используя префикс-функцию, период вычисляется по формуле:
        period = n - pi[n-1], если n % period == 0
        
        Пример: "abcabcabc" -> pi[8]=6, period=9-6=3
    """
    n = len(s)
    pi = prefix_function(s)
    period = n - pi[n - 1]
    
    # Проверяем, действительно ли это период (должен делить длину нацело)
    if n % period == 0:
        return period
    return n  # Строка непериодическая


def get_all_borders(s: str) -> List[int]:
    """
    Вычисление всех бордюров (границ) строки
    
    Args:
        s: Исходная строка
    
    Returns:
        List[int]: Длины всех бордюров строки в порядке убывания
    
    Details:
        Бордюр (граница) - это подстрока, которая одновременно является
        и префиксом, и суффиксом строки. Все бордюры получаются
        рекурсивным применением pi[n-1], pi[pi[n-1]-1], ...
    """
    n = len(s)
    pi = prefix_function(s)
    borders = []
    
    k = pi[n - 1]
    while k > 0:
        borders.append(k)
        k = pi[k - 1]
    
    return borders


def z_function(s: str) -> List[int]:
    """
    Вычисление Z-функции для строки
    
    Args:
        s: Исходная строка
    
    Returns:
        List[int]: Массив z, где z[i] - длина наибольшего общего префикса
                   строки s и подстроки s[i..n-1]
    
    Details:
        Z-функция определяется как:
        z[0] = 0 (или n, по соглашению)
        z[i] = max{k | s[0..k-1] == s[i..i+k-1]}
        
        Алгоритм поддерживает отрезок [l, r] с максимальным r,
        для которого s[l..r] является префиксом строки.
        Это позволяет вычислять z[i] за O(1) в среднем.
        
        Пример для строки "abacaba":
        i:   0 1 2 3 4 5 6
        s:   a b a c a b a
        z:   0 0 1 0 3 0 1
        
        Применение:
        - Поиск подстроки (через строку pattern + '#' + text)
        - Поиск периода строки
        - Сжатие строки (поиск повторяющихся фрагментов)
    """
    n = len(s)
    z = [0] * n
    
    # Границы самого правого найденного отрезка, совпадающего с префиксом
    l = 0  # Левая граница отрезка
    r = 0  # Правая граница отрезка
    
    # z[0] обычно полагают равным 0 (или n, по соглашению)
    for i in range(1, n):
        if i <= r:
            # Если i внутри отрезка [l, r], можем использовать уже вычисленные значения
            # z[i] соответствует z[i-l], но ограничено длиной оставшейся части отрезка
            z[i] = min(r - i + 1, z[i - l])
        
        # Наивно расширяем совпадение, пока символы равны
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        
        # Обновляем границы самого правого отрезка
        if i + z[i] - 1 > r:
            l = i
            r = i + z[i] - 1
    
    # По соглашению z[0] часто полагают равным длине строки
    # z[0] = n  # Раскомментировать, если нужно
    
    return z


def find_occurrences_z(text: str, pattern: str) -> List[int]:
    """
    Поиск всех вхождений подстроки в строку с помощью Z-функции
    
    Args:
        text: Текст, в котором ищем
        pattern: Искомая подстрока (шаблон)
    
    Returns:
        List[int]: Индексы всех вхождений pattern в text
    
    Details:
        Формируем строку pattern + '#' + text и вычисляем Z-функцию.
        Вхождения pattern соответствуют позициям, где z[i] == len(pattern).
        Символ '#' (или любой символ не из алфавита) нужен, чтобы
        избежать ложных срабатываний на границе pattern и text.
    """
    combined = pattern + "#" + text
    z = z_function(combined)
    occurrences = []
    
    pattern_len = len(pattern)
    for i in range(pattern_len + 1, len(combined)):
        if z[i] == pattern_len:
            occurrences.append(i - pattern_len - 1)
    
    return occurrences


def kmp(text: str, pattern: str) -> List[int]:
    """
    Поиск всех вхождений подстроки в строку с помощью алгоритма КМП
    
    Args:
        text: Текст, в котором производится поиск
        pattern: Искомая подстрока (шаблон)
    
    Returns:
        List[int]: Индексы всех вхождений pattern в text (0-indexed)
    
    Details:
        Алгоритм КМП использует префикс-функцию шаблона для того,
        чтобы избежать откатов в тексте. При несовпадении мы сдвигаем
        шаблон не на 1, а на величину, определяемую префикс-функцией.
        
        Принцип работы:
        1. Вычисляем префикс-функцию для шаблона
        2. Проходим по тексту, поддерживая длину совпавшего префикса
        3. При несовпадении используем pi для "перемотки" шаблона
        4. Когда длина совпадения равна длине шаблона - нашли вхождение
    """
    n, m = len(text), len(pattern)
    
    # Предварительно вычисляем префикс-функцию для шаблона
    pi = prefix_function(pattern)
    occurrences = []
    
    j = 0  # Длина текущего совпавшего префикса шаблона
    
    for i in range(n):
        # Пока нет совпадения и j > 0, откатываемся по префикс-функции
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        
        # Если символы совпали, увеличиваем длину совпадения
        if text[i] == pattern[j]:
            j += 1
        
        # Если совпал весь шаблон
        if j == m:
            occurrences.append(i - m + 1)  # Индекс начала вхождения
            j = pi[j - 1]  # Продолжаем поиск следующих вхождений
    
    return occurrences


def kmp_with_overlap_control(text: str, pattern: str, allow_overlap: bool = True) -> List[int]:
    """
    Поиск всех вхождений с учётом перекрытий и без
    
    Args:
        text: Текст
        pattern: Шаблон
        allow_overlap: Разрешить перекрывающиеся вхождения
    
    Returns:
        List[int]: Индексы вхождений
    
    Details:
        По умолчанию КМП находит все вхождения, включая перекрывающиеся.
        Если allow_overlap = False, после нахождения вхождения поиск
        продолжается с позиции после конца найденного шаблона.
    """
    n, m = len(text), len(pattern)
    pi = prefix_function(pattern)
    occurrences = []
    
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        
        if text[i] == pattern[j]:
            j += 1
        
        if j == m:
            occurrences.append(i - m + 1)
            if allow_overlap:
                j = pi[j - 1]  # Продолжаем с учётом возможных перекрытий
            else:
                j = 0  # Начинаем поиск заново после текущего вхождения
    
    return occurrences


def build_kmp_automaton(pattern: str, alphabet_size: int = 26) -> List[List[int]]:
    """
    Построение автомата КМП для многократного поиска
    
    Args:
        pattern: Шаблон, для которого строится автомат
        alphabet_size: Размер алфавита (по умолчанию 26 - латиница)
    
    Returns:
        List[List[int]]: Таблица переходов: automaton[state][char] = next_state
    
    Details:
        Автомат КМП позволяет искать шаблон в разных текстах без
        повторного вычисления префикс-функции. Полезен, когда нужно
        найти один шаблон во многих текстах.
        
        Состояния: 0..m (m - конечное состояние, вхождение найдено)
        Переходы: для каждого состояния и символа алфавита
    """
    m = len(pattern)
    pi = prefix_function(pattern)
    
    # automaton[state][c] = следующее состояние при чтении символа c
    automaton = [[0] * alphabet_size for _ in range(m + 1)]
    
    for state in range(m + 1):
        for c in range(alphabet_size):
            ch = chr(ord('a') + c)
            
            if state < m and ch == pattern[state]:
                automaton[state][c] = state + 1
            elif state > 0:
                automaton[state][c] = automaton[pi[state - 1]][c]
            else:
                automaton[state][c] = 0
    
    return automaton


def find_with_one_mismatch(text: str, pattern: str) -> List[int]:
    """
    Поиск подстроки с одним несовпадением (приближённый поиск)
    
    Args:
        text: Текст
        pattern: Шаблон
    
    Returns:
        List[int]: Позиции, где шаблон совпадает с точностью до 1 ошибки
    
    Details:
        Использует Z-функцию для прямого и обратного совпадения.
        Сложность: O(N + M)
    """
    n, m = len(text), len(pattern)
    
    if m > n:
        return []
    
    # Вычисляем Z-функцию для прямого сравнения: pattern + '#' + text
    z_forward = z_function(pattern + "#" + text)
    
    # Вычисляем Z-функцию для обратного сравнения
    rev_pattern = pattern[::-1]
    rev_text = text[::-1]
    z_backward = z_function(rev_pattern + "#" + rev_text)
    
    occurrences = []
    
    for i in range(n - m + 1):
        # Длина совпадения с начала шаблона
        forward_match = z_forward[m + 1 + i]
        
        if forward_match >= m:
            # Полное совпадение без ошибок
            occurrences.append(i)
            continue
        
        # Длина совпадения с конца шаблона
        backward_match = z_backward[m + 1 + (n - i - m)]
        
        # Проверяем, перекрывают ли совпадения всё, кроме одного символа
        if forward_match + backward_match >= m - 1:
            occurrences.append(i)
    
    return occurrences


# =========================== ДЕМОНСТРАЦИЯ РАБОТЫ ===================================

def demonstrate_all_algorithms() -> None:
    """Демонстрация работы всех алгоритмов"""
    
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМОВ НА PYTHON")
    print("=" * 70)
    
    # 1. Бинарный поиск
    print("\n1. Бинарный поиск:")
    arr = [1, 3, 5, 7, 9, 11, 13]
    print(f"   Массив: {arr}")
    print(f"   Поиск 7: индекс {binary_search(arr, 7)}")
    print(f"   Lower bound для 6: индекс {lower_bound(arr, 6)} (значение {arr[lower_bound(arr, 6)]})")
    
    # 2. Префиксные суммы
    print("\n2. Префиксные суммы:")
    arr = [2, 3, 5, 1, 4]
    pref = build_prefix_sums(arr)
    print(f"   Массив: {arr}")
    print(f"   Сумма на [1, 3] (элементы 3, 5, 1): {range_sum(pref, 1, 3)}")
    
    # 3. Два указателя
    print("\n3. Метод двух указателей:")
    arr = [1, 2, 4, 7, 11, 15]
    i, j = two_sum_sorted(arr, 15)
    print(f"   Массив: {arr}")
    print(f"   Пара с суммой 15: индексы {i} и {j} (значения {arr[i]} + {arr[j]})")
    
    # 4. Дерево отрезков
    print("\n4. Дерево отрезков (min/max):")
    arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    st = SegmentTreeMinMax(arr)
    print(f"   Массив: {arr}")
    print(f"   Отрезок [0, 4]: sum={st.get_sum(0, 4)}, min={st.get_min(0, 4)}, max={st.get_max(0, 4)}")
    st.set_value(3, 10)
    print(f"   После arr[3]=10, [0, 4]: sum={st.get_sum(0, 4)}, min={st.get_min(0, 4)}, max={st.get_max(0, 4)}")
    
    # 5. DSU
    print("\n5. DSU (Система непересекающихся множеств):")
    dsu = DSU(5)
    dsu.union(0, 1)
    dsu.union(1, 2)
    dsu.union(3, 4)
    print("   Объединения: (0,1), (1,2), (3,4)")
    print(f"   0 и 2 в одном множестве? {dsu.same_set(0, 2)}")
    print(f"   0 и 3 в одном множестве? {dsu.same_set(0, 3)}")
    print(f"   Размер множества с 0: {dsu.get_size(0)}")
    
    # 6. BFS
    print("\n6. BFS в графе:")
    graph = [
        [1, 2],     # вершина 0
        [0, 3],     # вершина 1
        [0, 3],     # вершина 2
        [1, 2, 4],  # вершина 3
        [3]         # вершина 4
    ]
    dist = bfs(0, graph)
    print("   Граф: 0-1, 0-2, 1-3, 2-3, 3-4")
    print(f"   Расстояния от 0: {dist}")
    
    # 7. Алгоритм Дейкстры
    print("\n7. Алгоритм Дейкстры:")
    # Граф с весами: (вершина, вес)
    weighted_graph = [
        [(1, 4), (2, 2)],           # вершина 0
        [(2, 1), (3, 5)],           # вершина 1
        [(1, 1), (3, 8), (4, 10)],  # вершина 2
        [(4, 2)],                   # вершина 3
        []                          # вершина 4
    ]
    dist, parent = dijkstra(0, weighted_graph)
    print(f"   Кратчайшие расстояния от 0: {dist}")
    print(f"   Путь до 4: {get_path(parent, 4)}")
    
    # 8. Динамическое программирование (рюкзак)
    print("\n8. Задача о рюкзаке 0/1:")
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    W = 5
    max_val, selected = knapsack_01_with_items(W, weights, values)
    print(f"   Веса: {weights}, стоимости: {values}, вместимость: {W}")
    print(f"   Максимальная стоимость: {max_val}")
    print(f"   Выбранные предметы (индексы): {selected}")
    
    # 9. Решето Эратосфена
    print("\n9. Решето Эратосфена:")
    n = 30
    primes = get_primes_list(n)
    print(f"   Простые числа до {n}: {primes}")
    
    # 10. Быстрое возведение в степень
    print("\n10. Быстрое возведение в степень:")
    a, n, mod = 2, 10, 1000000007
    result = binpow(a, n, mod)
    print(f"   {a}^{n} mod {mod} = {result}")
    
    # 11. Строковые алгоритмы
    print("\n11. Строковые алгоритмы:")
    
    # Префикс-функция
    s = "abacaba"
    pi = prefix_function(s)
    print(f"   Префикс-функция для '{s}': {pi}")
    print(f"   Период строки: {find_period(s)}")
    print(f"   Бордюры: {get_all_borders(s)}")
    
    # Z-функция
    z = z_function(s)
    print(f"   Z-функция для '{s}': {z}")
    
    # КМП
    text = "ababcabcabababd"
    pattern = "ababd"
    occurrences = kmp(text, pattern)
    print(f"   КМП: вхождения '{pattern}' в '{text}': {occurrences}")
    
    # Поиск с одной ошибкой
    text = "hello world, hallo welt"
    pattern = "hello"
    approx = find_with_one_mismatch(text, pattern)
    print(f"   Приближённый поиск '{pattern}' в '{text}': {approx}")


if __name__ == "__main__":
    demonstrate_all_algorithms()