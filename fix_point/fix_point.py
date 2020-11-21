"""
Модуль содержит класс Fix_Point и класс Comp_Fix_Point.

Класс Fix_Point предназначен для работы с числами с фиксированной точкой.

Класс Comp_Fix_Point предназначен для работы с комплексными числами
с фиксированной точкой.
"""

import numpy as np


class Iterat:
    """
    Класс итератора для создания итераторов.
    """
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def __next__(self):
        if self.offset >= len(self.data):
            raise StopIteration
        else:
            item = self.data[self.offset]
            self.offset += 1
            return item


class Fix_Point:
    '''
    Класс для работы с числами с фиксированной точкой.

    Параметры __init__
    ------------------
    data : входные данные
        Могут быть числом, списком, массивом numpy.
    ball : полная разрядность данных, включая знак.
    bfract : разрядность дробной части данных.
    roundtype : тип округления
        'math' - округление к ближайшему целому.
        'up'   - округление в большую сторону.
        'down' - округление в меньшую сторону.
    roundat : способ округления
        'wrap' - при выходе за пределы разрядности происходит "заворачивание"
                 данных в область с противоположным знаком.
        'saturate' - при выходе за пределы разрядности происходит приведение
                     к максимальному значению для заданной разрядности.
    repres : способ вывода данных в консоль и функцией print
        'float' - выводит данные с фиксированной точкой.
        'int'   - выводит данные в целочисленном представлении.

    Аргументы
    ---------
    lall : полная разрядность данных, включая знак.
    lfract : разрядность дробной части данных.
    roundtype : тип округления.
        'math' - округление к ближайшему целому.
        'up'   - округление в большую сторону.
        'down' - округление в меньшую сторону.
    roundat : способ округления.
        'wrap' - при выходе за пределы разрядности происходит "заворачивание"
                данных в область с противоположным знаком.
        'saturate' - при выходе за пределы разрядности происходит приведение
                     к максимальному значению для заданной
    repres : способ вывода данных.
        'float' - выводит данные с фиксированной точкой.
        'int'   - выводит данные в целочисленном представлении.
    int : возвращает данные в целочисленном представлении.
    float : возвращает данные с фиксированной точкой.
    size : возвращает размер массива данных.
    shape : возвращает количество строк и столбцов массива данных.
    ndim : возвращает количество измерений массива.

    Методы
    ------
    resize : метод изменения разрядности данных
        ball - новая полная разрядность данных
        bfract - новая разрядность дробной части
        roundtype - тип округления:
            'math' - округление к ближайшему целому.
            'up'   - округление в большую сторону.
            'down' - округление в меньшую сторону.
    dot : метод умножения 2-х матриц
        other - другая матрица типа Fix_Point или Comp_Fix_Point.
    '''

    def __init__(self, data, ball=16, bfract=15, roundtype='math',
                 roundat='wrap', repres='float'):
        if ball <= bfract:
            raise AttributeError("Целая часть должна быть больше дробной!!!")
        self.__lall = Fix_Point.setBall(ball)
        self.__lfract = Fix_Point.setBfract(bfract)
        self.__roundat = Fix_Point.setRoundat(roundat)
        self.__repres = Fix_Point.setRepres(repres)
        self.__roundtype = Fix_Point.setRoundtype(roundtype)
        # На случай долгой работы
        # self.__lall      = ball
        # self.__lfract    = bfract
        # self.__roundat   = roundat
        # self.__repres    = repres
        # self.__roundtype = roundtype
        self.__int = self.genFix(data)
        self.__float = self.genFloat(data)

    def setBall(value):
        if value > 0:
            return value
        else:
            raise AttributeError("Недопустимое значение ball")

    def setBfract(value):
        if value >= 0:
            return value
        else:
            raise AttributeError("Недопустимое значение bfract")

    def setRoundat(value):
        troundat = ('wrap', 'saturate')
        if value in troundat:
            return value
        else:
            raise AttributeError("Недопустимое значение roundat. "
                                 "Разрешены: 'wrap', 'saturate'")

    def setRoundtype(value):
        troundtype = ('math', 'up', 'down')
        if value in troundtype:
            return value
        else:
            raise AttributeError("Недопустимое значение roundtype. "
                                 "Разрешены: 'math', 'up', 'down' ")

    def setRepres(value):
        trepres = ('int', 'float')
        if value in trepres:
            return value
        else:
            raise AttributeError("Недопустимое значение repres. "
                                 "Разрешены: 'int', 'float' ")

    setBall = staticmethod(setBall)
    setBfract = staticmethod(setBfract)
    setRoundat = staticmethod(setRoundat)
    setRoundtype = staticmethod(setRoundtype)
    setRepres = staticmethod(setRepres)

    def get_repres(self):
        return self.__repres

    def set_repres(self, value):
        if value == 'float' or value == 'int':
            self.__repres = value
        else:
            raise AttributeError("Значение может быть 'int' или 'float'")

    repres = property(get_repres, set_repres)

    def get_roundtype(self):
        return self.__roundtype

    def set_roundtype(self):
        raise AttributeError('readonly attribute')

    roundtype = property(get_roundtype, set_roundtype)

    def get_roundat(self):
        return self.__roundat

    def set_roundat(self):
        raise AttributeError('readonly attribute')

    roundat = property(get_roundat, set_roundat)

    def get_lall(self):
        return self.__lall

    def set_lall(self):
        raise AttributeError('readonly attribute')

    lall = property(get_lall, set_lall)

    def get_lfract(self):
        return self.__lfract

    def set_lfract(self):
        raise AttributeError('readonly attribute')

    lfract = property(get_lfract, set_lfract)

    def get_int(self):
        return self.__int

    def set_int(self):
        raise AttributeError('readonly attribute')

    int = property(get_int, set_int)

    def get_float(self):
        return self.__float

    def set_float(self):
        raise AttributeError('readonly attribute')

    float = property(get_float, set_float)

    def get_size(self):
        return self.__int.size

    def set_size(self):
        raise AttributeError('readonly attribute')

    size = property(get_size, set_size)

    def get_shape(self):
        return self.__int.shape

    def set_shape(self):
        raise AttributeError('readonly attribute')

    shape = property(get_shape, set_shape)

    def get_ndim(self):
        return self.__int.ndim

    def set_ndim(self):
        raise AttributeError('readonly attribute')

    ndim = property(get_ndim, set_ndim)

    def reqRoundp(x, alall):
        """
        Функция поиска переполнения для положительных чисел.
        :param x: Входной массив.
        :param alall: Количество значимых разрядов после запятой.
        :return: Массив без переполнения.
        """
        n = np.ceil(x / 2 ** alall)
        n[n % 2 == 1] = n[n % 2 == 1] + 1
        return x - n * (2 ** alall)

    def reqRoundn(x, alall):
        """
        Функция поиска переполнения для положительных чисел.
        :param x: Входной массив.
        :param alall: Количество значимых разрядов после запятой.
        :return: Массив без переполнения.
        """

        n = np.ceil(abs(x / 2 ** alall))
        n[n % 2 == 1] = n[n % 2 == 1] - 1
        x = x + n * (2 ** alall)
        return x

    reqRoundp = staticmethod(reqRoundp)
    reqRoundn = staticmethod(reqRoundn)

    def genFix(self, data):
        """
        Функция преобразования данных в целочисленные данные с
        заданной разрядностью.
        :param data: входные данные.
        :return: выходные данные.
        """
        # Сдвигаем запятую на lfract позицый вправо
        xf = np.array(data) * 2.0 ** self.__lfract
        # Куда округляем
        if self.__roundtype == "math":  # К ближайшему целому
            # Сдвигаем запятую на lfract позицый вправо
            xf = np.array(data) * 2.0 ** self.__lfract
            # Определяем знаки данных
            sig = np.sign(xf)
            # Константа округления
            const_r = sig*0.5
            # Округление
            x = np.trunc(xf + const_r)
        # К большему (для массивов)
        elif self.__roundtype == "up" and xf.shape != ():
            # Сдвигаем запятую на lfract позицый вправо
            xf = np.array(data) * 2.0 ** self.__lfract
            # Обрабатываем отдельно для положительных и отрицательных
            nmax = np.ceil(np.log2(np.max(np.abs(xf))))
            # Округление положительных чисел
            xf[xf >= 0] = np.trunc(xf[xf >= 0] + 0.5)
            # Округление отрицательных чисел через доп код
            xf[xf < 0] = np.trunc(xf[xf < 0] + 2 ** nmax + 0.5) - 2 ** nmax
            x = xf
        # К большему (для чисел)
        elif self.__roundtype == "up" and xf.shape == ():
            # Сдвигаем запятую на lfract позицый вправо
            xf = np.array([data]) * 2.0 ** self.__lfract
            # Находим максимальную степень 2
            nmax = np.ceil(np.log2(np.max(np.abs(xf))))
            # Округление положительных чисел
            xf[xf >= 0] = np.trunc(xf[xf >= 0] + 0.5)
            # Округление отрицательных чисел через доп код
            xf[xf < 0] = np.trunc(xf[xf < 0] + 2 ** nmax + 0.5) - 2 ** nmax
            x = xf
        # К меньшему (для массивов)
        elif self.__roundtype == "down" and xf.shape != ():
            # Сдвигаем запятую на lfract позицый вправо
            xf = np.array(data) * 2.0 ** self.__lfract
            # Находим максимальную степень 2
            nmax = np.ceil(np.log2(np.max(np.abs(xf))))
            # Округление положительных чисел
            xf[xf >= 0] = np.trunc(xf[xf >= 0] - 0.5)
            # Округление отрицательных чисел через доп код
            xf[xf < 0] = np.trunc(xf[xf < 0] + 2 ** nmax - 0.5) - 2 ** nmax
            x = xf
        # К меньшему (для чисел)
        elif self.__roundtype == "down" and xf.shape == ():
            # Сдвигаем запятую на lfract позицый вправо
            xf = np.array([data]) * 2.0 ** self.__lfract
            # Находим максимальную степень 2
            nmax = np.ceil(np.log2(np.max(np.abs(xf))))
            # Округление положительных чисел
            xf[xf >= 0] = np.trunc(xf[xf >= 0] - 0.5)
            # Округление отрицательных чисел через доп код
            xf[xf < 0] = np.trunc(xf[xf < 0] + 2 ** nmax - 0.5) - 2 ** nmax
            x = xf

        # Определяем количество разрядов после знака
        alall = self.__lall - 1

        if not isinstance(x, np.ndarray):
            # if x.__class__ != np.ndarray:
            # print(y.__class__)
            x = np.array(x)

        # Округление в сторону переполнения
        if self.__roundat == 'wrap':
            x[x > 2 ** alall - 1] = \
                Fix_Point.reqRoundp(x[x > 2 ** alall - 1], alall)
            x[x < -2 ** alall + 1] = \
                Fix_Point.reqRoundn(x[x < -2 ** alall + 1], alall)
        # Округление по максимуму
        elif self.__roundat == 'saturate':
            x[x > 2 ** alall - 1] = 2 ** alall - 1
            x[x < -2 ** alall + 1] = -2 ** alall
        return x

    def genFloat(self, data):
        """
        Функция представления данных с фиксированной разрядностью в
        формате float
        :param data:
        :return:
        """
        return self.genFix(data)/2**self.__lfract

    def resize(self, ball, bfract, roundtype='math'):
        """
        Функция изменения разрядности данных.
        :param : ball - полная разрядность данных.
                 bfract - разрядность дробной части.
                 roundtype - тип округления:
                    'math' - округление к ближайшему целому.
                    'up'   - округление в большую сторону.
                    'down' - округление в меньшую сторону.
        :return: экзэмпляр с новой разрядностью.
        """
        self.__init__(self.__float, ball=ball, bfract=bfract,
                      roundat=self.__roundat, roundtype=roundtype)
        # return Fix_Point(self.__float, ball = lall, bfract = lfract,
        # roundat = self.__roundat)

    def dot(self, other):
        """
        Функция перемножения матриц.
        :param other: вторая матрица.
        :return: результат.
        """
        if isinstance(other, Fix_Point) and self.ndim > 1:
            (_, col) = self.shape
            lall = self.__lall + other.lall - 1 + np.ceil(np.log2(col))
            lfract = self.__lfract + other.lfract
            data = self.__float.dot(other.__float)
            return Fix_Point(data, ball=lall, bfract=lfract,
                             roundat=self.__roundat, repres=self.repres,
                             roundtype=self.__roundtype)
        if isinstance(other, Fix_Point) and self.ndim == 1:
            col = self.size
            lall = self.__lall + other.lall - 1 + np.ceil(np.log2(col))
            lfract = self.__lfract + other.lfract
            data = self.__float.dot(other.__float)
            return Fix_Point(data, ball=lall, bfract=lfract,
                             roundat=self.__roundat, repres=self.repres,
                             roundtype=self.__roundtype)
        elif isinstance(other, Comp_Fix_Point):
            pass

    def __repr__(self):
        """
        Перегрузка метода представления данных в командной строке.
        """
        if self.repres == 'float':
            return "ndarray({0}), bit depth[{1},{2}]".format(self.__float,
                                                             self.__lall,
                                                             self.__lfract)
        elif self.repres == 'int':
            return "ndarray({0}), bit depth[{1},{2}]".format(self.__int,
                                                             self.__lall,
                                                             self.__lfract)

    def __str__(self):
        """
        Перегрузка метода представления данных в строковом виде.
        """
        if self.repres == 'float':
            return "ndarray({0}), bit depth[{1},{2}]".format(self.__float,
                                                             self.__lall,
                                                             self.__lfract)
        elif self.repres == 'int':
            return "ndarray({0}), bit depth[{1},{2}]".format(self.__int,
                                                             self.__lall,
                                                             self.__lfract)

    def __getitem__(self, index):
        """
        Перегрузка метода индексации данных.
        index : индекс.
        """
        return Fix_Point(self.__float[index], ball=self.__lall,
                         bfract=self.__lfract, roundat=self.__roundat,
                         repres=self.repres, roundtype='math')

    def __setitem__(self, index, value):
        """
        Перегрузка метода присвоения данных по индексу.
        :param index: индекс.
        :param value: значение.
        """

        if isinstance(value, Fix_Point) and self.__lall == 1 and \
                self.__lfract == 0:
            self.__int[index] = value.int
            self.__float[index] = value.float
            self.__lall = value.lall
            self.__lfract = value.lfract
            self.__roundat = value.roundat
            self.__repres = value.repres
            self.__roundtype = value.roundtype
        elif isinstance(value, Fix_Point) and self.__lall == value.lall and \
                self.__lfract == value.lfract and \
                self.__roundat == value.roundat and \
                self.__repres == value.repres and \
                self.__roundtype == value.roundtype:
            self.__int[index] = value.int
            self.__float[index] = value.float
        else:
            raise TypeError("Несоответствие типов или аргументов: "
                            "'Fix_Point' and '%s'" % type(value).__name__)

    def __iter__(self):
        """
        Перегрузка метода итерации.
        """
        if self.repres == 'float':
            return Iterat(self.__float)
        elif self.repres == 'int':
            return Iterat(self.__int)

    def __mul__(self, other):
        """
        Перегрузка метода умножения (self слева).
        other: второй множитель.
        """
        # Если перемножается Fix_Point на Fix_Point
        if isinstance(other, Fix_Point):
            lall = self.__lall + other.lall - 1
            lfract = self.__lfract + other.lfract
            data = self.__float * other.__float
            return Fix_Point(data, ball=lall, bfract=lfract,
                             roundat=self.__roundat, repres=self.repres,
                             roundtype='math')
        # Если перемножается Fix_Point на Comp_Fix_Point
        elif isinstance(other, Comp_Fix_Point):
            xy = self.__float.shape
            __imag = Fix_Point(np.zeros(xy), ball=self.__lall,
                               bfract=self.__lfract, roundat=self.__roundat,
                               repres=self.repres, roundtype=self.__roundtype)
            dataC = Comp_Fix_Point(self, __imag, ball=self.__lall,
                                   bfract=self.__lfract,
                                   roundat=self.__roundat,
                                   repres=self.repres, roundtype='math')
            return dataC * other
        # Приведение к комплексным данным
        elif other == 1j:
            xy = self.__float.shape
            __real = Fix_Point(np.zeros(xy), ball=self.__lall,
                               bfract=self.__lfract, roundat=self.__roundat,
                               repres=self.repres, roundtype=self.__roundtype)
            return Comp_Fix_Point(__real, self, ball=self.__lall,
                                  bfract=self.__lfract, roundat=self.__roundat,
                                  repres=self.repres, roundtype='math')
        # Ошибка, если неправильный тип второго множителя
        else:
            raise TypeError("Unsupported operand type(s) for '*': "
                            "'Comp_Fix_Point(Fix_Point)' and '%s'"
                            % type(other).__name__)

    def __rmul__(self, other):
        """
        Перегрузка метода умножения (self справа).
        other: первый множитель.
        """
        # Если перемножается Fix_Point на Fix_Point
        if isinstance(other, Fix_Point):
            lall = self.__lall + other.lall - 1
            lfract = self.__lfract + other.lfract
            data = self.__float * other.__float
            return Fix_Point(data, ball=lall, bfract=lfract,
                             roundat=self.__roundat, repres=self.repres,
                             roundtype=self.__roundtype)
        # Приведение к комплексным данным
        elif other == 1j:
            xy = self.__float.shape
            __real = Fix_Point(np.zeros(xy), ball=self.__lall,
                               bfract=self.__lfract,
                               roundat=self.__roundat,
                               repres=self.repres,
                               roundtype=self.__roundtype)
            return Comp_Fix_Point(__real, self, ball=self.__lall,
                                  bfract=self.__lfract,
                                  roundat=self.__roundat,
                                  repres=self.repres, roundtype='math')
        # Ошибка, если неправильный тип первого множителя
        else:
            raise TypeError("Unsupported operand type(s) for '*': "
                            "'%s' and 'Comp_Fix_Point(Fix_Point)'"
                            % type(other).__name__)

    def __add__(self, other):
        """
        Перегрузка метода сложения (self слева).
        other: второе слагаемое.
        """
        # Если сложение Fix_Point с Fix_Point
        if isinstance(other, Fix_Point):
            lall = max(self.__lall, other.lall) + 1
            lfract = max(self.__lfract, other.lfract)
            data = self.__float + other.__float
            return Fix_Point(data, ball=lall, bfract=lfract,
                             roundat=self.__roundat,
                             repres=self.repres,
                             roundtype='math')
        # Если сложение Fix_Point с Comp_Fix_Point
        elif isinstance(other, Comp_Fix_Point):
            xy = self.__float.shape
            __imag = Fix_Point(np.zeros(xy), ball=self.__lall,
                               bfract=self.__lfract,
                               roundat=self.__roundat,
                               repres=self.repres,
                               roundtype=self.__roundtype)
            dataC = Comp_Fix_Point(self, __imag, ball=self.__lall,
                                   bfract=self.__lfract,
                                   roundat=self.__roundat,
                                   repres=self.repres,
                                   roundtype=self.__roundtype)
            return dataC + other
        # Ошибка, если неправильный тип второго слагаемого
        else:
            raise TypeError("Unsupported operand type(s) for '+': "
                            "'Comp_Fix_Point(Fix_Point)' and '%s'"
                            % type(other).__name__)

    def __radd__(self, other):
        """
        Перегрузка метода сложения (self справа).
        other: первое слагаемое.
        """
        # Если сложение Fix_Point с Fix_Point
        if isinstance(other, Fix_Point):
            lall = max(self.__lall, other.lall) + 1
            lfract = max(self.__lfract, other.lfract)
            data = other.__float + self.__float
            return Fix_Point(data, ball=lall, bfract=lfract,
                             roundat=self.__roundat,
                             repres=self.repres, roundtype='math')
        # Ошибка, если неправильный тип первого слагаемого
        else:
            raise TypeError("Unsupported operand type(s) for '+': "
                            "'%s' and 'Comp_Fix_Point(Fix_Point)'"
                            % type(other).__name__)

    def __sub__(self, other):
        """
        Перегрузка метода вычитания (self слева)
        other: второе слагаемое.
        """
        # Если вычитание Fix_Point из Fix_Point
        if isinstance(other, Fix_Point):
            lall = max(self.__lall, other.lall) + 1
            lfract = max(self.__lfract, other.lfract)
            data = self.__float - other.__float
            return Fix_Point(data, ball=lall, bfract=lfract,
                             roundat=self.__roundat,
                             repres=self.repres, roundtype='math')
        # Если вычитание Comp_Fix_Point из Fix_Point
        elif isinstance(other, Comp_Fix_Point):
            xy = self.__float.shape
            imag = Fix_Point(np.zeros(xy), ball=self.__lall,
                             bfract=self.__lfract,
                             roundat=self.__roundat,
                             repres=self.repres,
                             roundtype=self.__roundtype)
            dataC = Comp_Fix_Point(self, imag, ball=self.__lall,
                                   bfract=self.__lfract,
                                   roundat=self.__roundat,
                                   repres=self.repres,
                                   roundtype=self.__roundtype)
            return dataC - other
        # Ошибка, если неправильный тип второго слагаемого
        else:
            raise TypeError("Unsupported operand type(s) for '-': "
                            "'Comp_Fix_Point(Fix_Point)' and '%s'"
                            % type(other).__name__)

    def __rsub__(self, other):
        """
        Перегрузка метода вычитания (self справа)
        other: первое слагаемое.
        """
        # Если вычитание Fix_Point из Fix_Point
        if isinstance(other, Fix_Point):
            lall = max(self.__lall, other.lall) + 1
            lfract = max(self.__lfract, other.lfract)
            data = other.__float - self.__float
            return Fix_Point(data, ball=lall, bfract=lfract,
                             roundat=self.__roundat, repres=self.repres,
                             roundtype='math')
        # Ошибка, если неправильный тип первого слагаемого
        else:
            raise TypeError("Unsupported operand type(s) for '-': "
                            "'%s' and 'Comp_Fix_Point(Fix_Point)'"
                            % type(other).__name__)


class Comp_Fix_Point:
    '''
    Класс для работы с комплексными числами с фиксированной точкой.

    Параметры __init__
    ------------------
    data : входные данные могут быть числом, списком, массивом numpy,
           комплексными или не комплексными.
    ball : полная разрядность данных, включая знак.
    bfract : разрядность дробной части данных.
    roundtype : тип округления:
        'math' - округление к ближайшему целому.
        'up'   - округление в большую сторону.
        'down' - округление в меньшую сторону.
    roundat : способ округления:
        'wrap' - при выходе за пределы разрядности происходит
                 "заворачивание" данных в область с противоположным знаком.
        'saturate' - при выходе за пределы разрядности происходит приведение
                     к максимальному значению для заданной разрядности.
    repres : способ вывода данных в консоль и функцией print:
        'float' - выводит данные с фиксированной точкой.
        'int'   - выводит данные в целочисленном представлении.

    Аргументы
    ---------
    lall : полная разрядность данных, включая знак.
    lfract : разрядность дробной части данных.
    roundtype : тип округления:
        'math' - округление к ближайшему целому.
        'up'   - округление в большую сторону.
        'down' - округление в меньшую сторону.
    roundat : способ округления:
        'wrap' - при выходе за пределы разрядности происходит "заворачивание"
                 данных в область с противоположным знаком.
        'saturate' - при выходе за пределы разрядности происходит приведение
                     к максимальному значению для заданной
    repres : способ вывода данных:
        'float' - выводит данные с фиксированной точкой.
        'int'   - выводит данные в целочисленном представлении.
    int : возвращает данные в целочисленном представлении.
    float : возвращает данные с фиксированной точкой.
    size : возвращает размер массива данных.
    shape : возвращает количество строк и столбцов массива данных.
    ndim : возвращает количество измерений массива.

    Методы
    ------
    resize : метод изменения разрядности данных.
        ball - новая полная разрядность данных.
        bfract - новая разрядность дробной части.
        roundtype - тип округления:
            'math' - округление к ближайшему целому.
            'up'   - округление в большую сторону.
            'down' - округление в меньшую сторону.
    dot : метод умножения 2-х матриц.
        other - другая матрица типа Fix_Point или Comp_Fix_Point.
    conjugate : Метод возвращаем комплексно сопряженные данные.
    '''

    def __init__(self, *data, ball=16, bfract=15, roundat='wrap',
                 repres='float', roundtype='math'):
        self.__lall = ball
        self.__lfract = bfract
        self.__roundat = roundat
        self.__repres = repres
        self.__roundtype = roundtype
        if isinstance(data[0], Fix_Point) and isinstance(data[1], Fix_Point):
            self.__real = Fix_Point(data[0].float, ball=self.__lall,
                                    bfract=self.__lfract,
                                    roundat=self.__roundat,
                                    repres=self.__repres, roundtype='math')
            self.__imag = Fix_Point(data[1].float, ball=self.__lall,
                                    bfract=self.__lfract,
                                    roundat=self.__roundat,
                                    repres=self.__repres, roundtype='math')
        else:
            self.__real = Fix_Point(data[0].real, ball=self.__lall,
                                    bfract=self.__lfract,
                                    roundat=self.__roundat,
                                    repres=self.__repres,
                                    roundtype=self.__roundtype)
            self.__imag = Fix_Point(data[0].imag, ball=self.__lall,
                                    bfract=self.__lfract,
                                    roundat=self.__roundat,
                                    repres=self.__repres,
                                    roundtype=self.__roundtype)

    def get_repres(self):
        return self.__repres

    def set_repres(self, value):
        if value == 'float' or value == 'int':
            self.__repres = value
        else:
            raise AttributeError("Значение может быть 'int' или 'float'")

    repres = property(get_repres, set_repres)

    def get_roundtype(self):
        return self.__roundtype

    def set_roundtype(self):
        raise AttributeError('readonly attribute')

    roundtype = property(get_roundtype, set_roundtype)

    def get_roundat(self):
        return self.__roundat

    def set_roundat(self):
        raise AttributeError('readonly attribute')

    roundat = property(get_roundat, set_roundat)

    def get_lall(self):
        return self.__lall

    def set_lall(self):
        raise AttributeError('readonly attribute')

    lall = property(get_lall, set_lall)

    def get_lfract(self):
        return self.__lfract

    def set_lfract(self):
        raise AttributeError('readonly attribute')

    lfract = property(get_lfract, set_lfract)

    def get_real(self):
        return self.__real

    def set_real(self):
        raise AttributeError('readonly attribute')

    real = property(get_real, set_real)

    def get_imag(self):
        return self.__imag

    def set_imag(self):
        raise AttributeError('readonly attribute')

    imag = property(get_imag, set_imag)

    def get_int(self):
        return self.__real.int + 1j * self.__imag.int

    def set_int(self):
        raise AttributeError('readonly attribute')

    int = property(get_int, set_int)

    def get_float(self):
        return self.__real.float + 1j * self.__imag.float

    def set_float(self):
        raise AttributeError('readonly attribute')

    float = property(get_float, set_float)

    def get_size(self):
        return self.__real.size

    def set_size(self):
        raise AttributeError('readonly attribute')

    size = property(get_size, set_size)

    def get_shape(self):
        return self.__real.shape

    def set_shape(self):
        raise AttributeError('readonly attribute')

    shape = property(get_shape, set_shape)

    def get_ndim(self):
        return self.__real.ndim

    def set_ndim(self):
        raise AttributeError('readonly attribute')

    ndim = property(get_ndim, set_ndim)

    def conjugate(self):
        """
        :return: возвращаем комплексно сопряженные данные.
        """
        __imag = Fix_Point(-self.__imag.float, ball=self.__lall,
                           bfract=self.__lfract, roundat=self.__roundat,
                           repres=self.__repres, roundtype=self.__roundtype)
        return Comp_Fix_Point(self.__real, __imag, ball=self.__lall,
                              bfract=self.__lfract, roundat=self.__roundat,
                              repres=self.__repres, roundtype=self.__roundtype)

    def resize(self, ball, bfract, roundtype='math'):
        """
        Функция изменения разрядности данных.
        :param : ball - полная разрядность данных.
                 bfract - разрядность дробной части.
                 roundtype - тип округления:
                    'math' - округление к ближайшему целому.
                    'up'   - округление в большую сторону.
                    'down' - округление в меньшую сторону.
        :return: экзэмпляр с новой разрядностью.
        """
        return Comp_Fix_Point(self.__real, self.__imag, ball=ball,
                              bfract=bfract, roundat=self.__roundat,
                              repres=self.__repres, roundtype=roundtype)

    def dot(self, other):
        """
        Функция перемножения матриц.
        :param other: вторая матрица.
        :return: результат.
        """
        if isinstance(other, Fix_Point) and self.ndim > 1:
            (_, col) = self.shape
            lall = self.__lall + other.lall - 1 + np.ceil(np.log2(col)) + 1
            lfract = self.__lfract + other.lfract
            data = self.float.dot(other.float)
            return Comp_Fix_Point(data.real, data.imag, ball=lall,
                                  bfract=lfract, roundat=self.__roundat,
                                  repres=self.__repres,
                                  roundtype=self.__roundtype)
        elif isinstance(other, Comp_Fix_Point) and self.ndim > 1:
            (_, col) = self.shape
            lall = self.__lall + other.lall + np.ceil(np.log2(col)) + 1
            lfract = self.__lfract + other.lfract
            data = self.float.dot(other.float)
            return Comp_Fix_Point(data, ball=lall, bfract=lfract,
                                  roundat=self.__roundat, repres=self.__repres,
                                  roundtype=self.__roundtype)
        if isinstance(other, Fix_Point) and self.ndim == 1:
            col = self.size
            lall = self.__lall + other.lall - 1 + np.ceil(np.log2(col)) + 1
            lfract = self.__lfract + other.lfract
            data = self.float.dot(other.float)
            return Comp_Fix_Point(data.real, data.imag, ball=lall,
                                  bfract=lfract, roundat=self.__roundat,
                                  repres=self.__repres,
                                  roundtype=self.__roundtype)
        elif isinstance(other, Comp_Fix_Point) and self.ndim == 1:
            col = self.size
            lall = self.__lall + other.lall + np.ceil(np.log2(col)) + 1
            lfract = self.__lfract + other.lfract
            data = self.float.dot(other.float)
            return Comp_Fix_Point(data, ball=lall, bfract=lfract,
                                  roundat=self.__roundat, repres=self.__repres,
                                  roundtype=self.__roundtype)

    def __repr__(self):
        """
        Перегрузка метода представления данных в командной строке.
        """
        if self.__repres == 'int':
            return "complex(ndarray({0})), bit depth[{1},{2}]"\
                .format(self.int, self.__lall, self.__lfract)
        else:
            return "complex(ndarray({0})), bit depth[{1},{2}]"\
                .format(self.float, self.__lall, self.__lfract)

    def __str__(self):
        """
        Перегрузка метода представления данных в строковом виде.
        """
        # if self.__real.int.size == self.__real.int.shape[0]:
        # string = "complex(["
        if self.__repres == 'int':
            return "complex(ndarray({0})), bit depth[{1},{2}]"\
                .format(self.int, self.__lall, self.__lfract)
        else:
            return "complex(ndarray({0})), bit depth[{1},{2}]"\
                .format(self.float, self.__lall, self.__lfract)

    def __getitem__(self, index):
        """
        Перегрузка метода индексации данных.
        index : индекс.
        """
        return Comp_Fix_Point(self.__real[index], self.__imag[index],
                              ball=self.__lall, bfract=self.__lfract,
                              roundat=self.__roundat,
                              repres=self.repres, roundtype='math')

    def __setitem__(self, index, value):
        """
        Перегрузка метода присвоения данных по индексу.
        :param index: индекс.
        :param value: значение.
        """
        if isinstance(value, Comp_Fix_Point) and \
                self.__lall == 1 and self.__lfract == 0:
            self.__real[index] = value.real
            self.__imag[index] = value.imag
            self.__lall = value.lall
            self.__lfract = value.lfract
            self.__roundat = value.roundat
            self.__repres = value.repres
            self.__roundtype = value.roundtype
        elif isinstance(value, Comp_Fix_Point) and \
                self.__lall == value.lall and \
                self.__lfract == value.lfract and \
                self.__roundat == value.roundat and \
                self.__repres == value.repres and \
                self.__roundtype == value.roundtype:
            self.__real[index] = value.real
            self.__imag[index] = value.imag
        else:
            raise TypeError("Несоответствие типов или аргументов: "
                            "'Comp_Fix_Point' and '%s'"
                            % type(value).__name__)

    def __iter__(self):
        """
        Перегрузка метода итерации.
        """
        if self.__repres == 'int':
            return Iterat(self.__real.int + 1j * self.__imag.int)
        elif self.__repres == 'float':
            return Iterat(self.__real.float + 1j * self.__imag.float)

    def __mul__(self, other):
        """
        Перегрузка метода умножения (self слева)
        other: второй множитель.
        """
        # Если второй множитель Comp_Fix_Point
        if isinstance(other, Comp_Fix_Point):
            lall = self.__lall + other.lall
            lfract = self.__lfract + other.lfract
            __real = self.__real*other.__real - self.__imag*other.__imag
            __imag = self.__real*other.__imag + self.__imag*other.__real
            return Comp_Fix_Point(__real, __imag, ball=lall, bfract=lfract,
                                  roundat=self.__roundat,
                                  repres=self.__repres, roundtype='math')
        # Если второй множитель Fix_Point
        elif isinstance(other, Fix_Point):
            lall = self.__lall + other.lall-1
            lfract = self.__lfract + other.lfract
            __real = self.__real*other
            __imag = self.__imag*other
            return Comp_Fix_Point(__real, __imag, ball=lall, bfract=lfract,
                                  roundat=self.__roundat,
                                  repres=self.__repres, roundtype='math')
        # Ошибка, если неправильный тип второго множителя
        else:
            raise TypeError("Unsupported operand type(s) for '*': "
                            "'Comp_Fix_Point(Fix_Point)' and '%s'"
                            % type(other).__name__)

    def __rmul__(self, other):
        """
        Перегрузка метода умножения (self справа)
        other: второй множитель.
        """
        # Если первый множитель Comp_Fix_Point
        if isinstance(other, Comp_Fix_Point):
            lall = self.__lall + other.lall
            lfract = self.__lfract + other.lfract
            __real = self.__real*other.__real - self.__imag*other.__imag
            __imag = self.__real*other.__imag + self.__imag*other.__real
            return Comp_Fix_Point(__real, __imag, ball=lall, bfract=lfract,
                                  roundat=self.__roundat, repres=self.__repres,
                                  roundtype='math')
        # Ошибка, если неправильный тип первого множителя
        else:
            raise TypeError("Unsupported operand type(s) for '*': "
                            "'%s' and 'Comp_Fix_Point(Fix_Point)'"
                            % type(other).__name__)

    def __add__(self, other):
        """
        Перегрузка метода сложения (self слева)
        other: второе слагаемое.
        """
        # Если второе слагаемое Comp_Fix_Point
        if isinstance(other, Comp_Fix_Point):
            lall = max(self.__lall, other.lall) + 1
            lfract = max(self.__lfract, other.lfract)
            __real = self.__real + other.__real
            __imag = self.__imag + other.__imag
            return Comp_Fix_Point(__real, __imag, ball=lall, bfract=lfract,
                                  roundat=self.__roundat,
                                  repres=self.__repres,
                                  roundtype='math')
        # Если второе слагаемое Fix_Point
        elif isinstance(other, Fix_Point):
            lall = max(self.__lall, other.lall) + 1
            lfract = max(self.__lfract, other.lfract)
            __real = self.__real + other
            __imag = self.__imag
            return Comp_Fix_Point(__real, __imag, ball=lall, bfract=lfract,
                                  roundat=self.__roundat,
                                  repres=self.__repres,
                                  roundtype='math')
        # Ошибка, если неправильный тип второго слагаемого
        else:
            raise TypeError("Unsupported operand type(s) for '+': "
                            "'Comp_Fix_Point(Fix_Point)' and '%s'"
                            % type(other).__name__)

    def __radd__(self, other):
        """
        Перегрузка метода сложения (self справа)
        other: первое слагаемое.
        """
        # Если первое слагаемое Comp_Fix_Point
        if isinstance(other, Comp_Fix_Point):
            lall = max(self.__lall, other.lall) + 1
            lfract = max(self.__lfract, other.lfract)
            __real = self.__real + other.__real
            __imag = self.__imag + other.__imag
            return Comp_Fix_Point(__real, __imag, ball=lall, bfract=lfract,
                                  roundat=self.__roundat,
                                  repres=self.__repres,
                                  roundtype='math')
        # Ошибка, если неправильный тип первого слагаемого
        else:
            raise TypeError("Unsupported operand type(s) for '+': "
                            "'%s' and 'Comp_Fix_Point(Fix_Point)'"
                            % type(other).__name__)

    def __sub__(self, other):
        """
        Перегрузка метода вычитания (self слева)
        other: второе слагаемое.
        """
        # Если втоорое слагаемое Comp_Fix_Point
        if isinstance(other, Comp_Fix_Point):
            lall = max(self.__lall, other.lall) + 1
            lfract = max(self.__lfract, other.lfract)
            __real = self.__real - other.__real
            __imag = self.__imag - other.__imag
            return Comp_Fix_Point(__real, __imag, ball=lall,
                                  bfract=lfract, roundat=self.__roundat,
                                  repres=self.__repres, roundtype='math')
        # Если втоорое слагаемое Fix_Point
        elif isinstance(other, Fix_Point):
            lall = max(self.__lall, other.lall) + 1
            lfract = max(self.__lfract, other.lfract)
            __real = self.__real - other
            __imag = self.__imag
            return Comp_Fix_Point(__real, __imag, ball=lall, bfract=lfract,
                                  roundat=self.__roundat,
                                  repres=self.__repres, roundtype='math')
        # Ошибка, если неправильный тип второго слагаемого
        else:
            raise TypeError("Unsupported operand type(s) for '-': "
                            "'Comp_Fix_Point(Fix_Point)' and '%s'"
                            % type(other).__name__)

    def __rsub__(self, other):
        """
        Перегрузка метода вычитания (self справа)
        other: первое слагаемое.
        """
        # Если первое слагаемое Comp_Fix_Point
        if isinstance(other, Comp_Fix_Point):
            lall = max(self.__lall, other.lall) + 1
            lfract = max(self.__lfract, other.lfract)
            __real = other.__real - self.__real
            __imag = other.__imag - self.__imag
            return Comp_Fix_Point(__real, __imag, ball=lall, bfract=lfract,
                                  roundat=self.__roundat,
                                  repres=self.__repres,
                                  roundtype='math')
        # Ошибка, если неправильный тип первого слагаемого
        else:
            raise TypeError("Unsupported operand type(s) for '-':"
                            " '%s' and 'Comp_Fix_Point(Fix_Point)'"
                            % type(other).__name__)


def zeros_fp(dim):
    """
    Создает массив Fix_Point с нулевыми значениями.
    :param dim: Размерность массива.
    :return: Массив нулевых значений.
    """
    return Fix_Point(np.zeros(dim), ball=1, bfract=0)


def zeros_cfp(dim):
    """
    Создает массив Comp_Fix_Point с нулевыми значениями.
    :param dim: Размерность массива.
    :return: Массив нулевых значений.
    """
    return Comp_Fix_Point(1j * np.zeros(dim), ball=1, bfract=0)

