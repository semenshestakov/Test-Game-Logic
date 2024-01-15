# Вопрос 1
# На языке Python написать алгоритм (функцию) определения четности целого числа, который будет аналогичен нижеприведенному по функциональности, но отличен по своей сути.
# Объяснить плюсы и минусы обеих реализаций.
# Пример:
# def isEven(value):
# return value % 2 == 0

def isEven(value):
    """
    ИДЕЯ
    Число value можно записать в двоичной СС, например 5 = 0x101, 6 = 0x110 1 = 0x1
    И все нечетные числа заканчиваються на 1 и если применить операцию конъюнкция,
    то число & 0000....01, будет == 0 или 1, взависмости от последнего бита (первый)
    """
    return ((value & 0x01) == 0)

# Вопрос 2
# На языке Python написать минимум по 2 класса реализовывающих циклический буфер FIFO.
# Объяснить плюсы и минусы каждой реализации.
# Оценивается:
# 1. Полнота и качество реализации
# _ 2. Оформление кода
# 3. Наличие сравнения и пояснения по быстродействию


class FIFOv1:
    """
    Гибкость размера: Списки смежности могут легко изменять размер, не требуя заранее определенного максимального размера.

    Эффективность вставки и удаления: Вставка и удаление элементов в середине списка смежности происходят относительно быстро
    без необходимости перемещения других элементов.

    Минусы:
    Больше памяти: В списке смежности требуется дополнительная память для хранения связей между элементами,
    что может стать недостатком при работе с большими объемами данных.
    """

    class __Node:
        def __init__(self, value, next=None):
            self.value = value
            self.next = next

    def __init__(self):
        self.__head = None
        self.__last = None

    def append(self, value):
        new_node = self.__Node(value)

        if self.__head is None:
            self.__head = new_node

        elif self.__last is None:
            self.__last = new_node
            self.__head.next = new_node

        else:
            self.__last.next = new_node
            self.__last = new_node

    def empty(self):
        if self.__head is None:
            return True
        return False

    def first(self):
        if self.empty():
            return None
        return self.__head.value

    def pop(self):
        if self.empty():
            raise IndexError()

        result = self.__head.value
        self.__head = self.__head.next
        return result

    def __iter__(self):
        self.__elm = self.__head
        return self

    def __next__(self):
        if self.__elm is None:
            self.__elm = self.__head
            raise StopIteration()

        res = self.__elm
        self.__elm = self.__elm.next
        return res.value


class FIFOv2:
    """
    Плюсы:
    Эффективные операции доступа: Доступ к элементам в массиве осуществляется за константное время,
    что делает операции вставки и извлечения быстрее по сравнению с некоторыми другими структурами данных.

    Минусы:
    Фиксированный размер: Динамический массив может иметь фиксированный размер, что может стать ограничением при необходимости увеличения размера.

    В   ставка и удаление в середине массива неэффективны: Если нужно вставить или удалить элемент в середине массива,
    это может потребовать переноса всех последующих элементов.
    """

    def __init__(self):
        self.__buffer = []

    def append(self, value):
        self.__buffer.append(value)

    def empty(self):
        return len(self.__buffer) == 0

    def first(self):
        if self.empty():
            return None
        return self.__buffer[0]

    def pop(self):
        if self.empty():
            raise IndexError()

        return self.__buffer.pop(0)

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index >= len(self.__buffer):
            raise StopIteration()

        result = self.__buffer[self.__index]
        self.__index += 1
        return result


# Вопрос 3
# На языке Python предложить алгоритм, который быстрее всего (по процессорным тикам) отсортирует данный ей массив чисел.
# Массив может быть любого размера со случайным порядком чисел (в том числе и отсортированным).
# Объяснить, почему вы считаете, что функция соответствует заданным критериям.

def insertion_sort(arr, low, high):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def quicksort(arr, low, high):
    if low < high:
        # Переключение на insertion sort, если размер массива меньше 32
        if high - low + 1 <= 32:
            insertion_sort(arr, low, high)
            return

        # Быстрая сортировка с тремя указателями
        pivot1 = arr[low]
        pivot2 = arr[high]
        if pivot1 > pivot2:
            arr[low], arr[high] = arr[high], arr[low]
            pivot1, pivot2 = pivot2, pivot1

        low_ptr = low + 1
        high_ptr = high - 1
        i = low + 1
        while i <= high_ptr:
            if arr[i] < pivot1:
                arr[i], arr[low_ptr] = arr[low_ptr], arr[i]
                low_ptr += 1
            elif arr[i] > pivot2:
                while i <= high_ptr and arr[high_ptr] > pivot2:
                    high_ptr -= 1
                arr[i], arr[high_ptr] = arr[high_ptr], arr[i]
                high_ptr -= 1
                if arr[i] < pivot1:
                    arr[i], arr[low_ptr] = arr[low_ptr], arr[i]
                    low_ptr += 1
            i += 1

        low_ptr -= 1
        high_ptr += 1
        arr[low], arr[low_ptr] = arr[low_ptr], arr[low]
        arr[high], arr[high_ptr] = arr[high_ptr], arr[high]

        quicksort(arr, low, low_ptr - 1)
        quicksort(arr, low_ptr + 1, high_ptr - 1)
        quicksort(arr, high_ptr + 1, high)


if __name__ == '__main__':
    # V1
    # v1 = FIFOv1()
    # [v1.append(i) for i in range(5)] # 0 1 2 3 4
    #
    # v1.pop() # 1 2 3 4
    # print(v1.first())
    # v1.pop() # 2 3 4
    # print(v1.first())
    # v1.pop() # 3 4
    # print(v1.first(), "\n")
    #
    # [print(i) for i in v1]
    #
    # V2
    # v2 = FIFOv2()
    # [v2.append(i) for i in range(5)]  # 0 1 2 3 4
    # # [print(i) for i in v2]
    #
    # v2.pop()  # 1 2 3 4
    # print(v2.first())
    # v2.pop()  # 2 3 4
    # print(v2.first())
    # v2.pop()  # 3 4
    # print(v2.first(), "\n")
    #
    # [print(i) for i in v2]

    arr = [64, 25, 12, 22, 11, 33, 55, 88, 67, 89.3, 1, 99.2, 42, -123]
    quicksort(arr, 0, len(arr) - 1)
    print("Отсортированный массив:", arr)

