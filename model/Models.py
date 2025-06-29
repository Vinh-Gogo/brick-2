from typing import List, Union, Any
import numpy as np
from enum import Enum
from itertools import groupby


class Point:

    def __init__(self, x=0, y=0, value=None, group=None) -> None:
        ''' 
            x: horizontal
            y: vertical 
            value: expression properties of that point
            group: Things in common in a group have the same value
            
            intput: [int, int, int, int]
        '''
        self.x = x
        self.y = y
        self.value = value
        self.group = group

    def __str__(self) -> str:
        return f"Point: x={self.x}, y={self.y}, value={self.value}, group={self.group}"

    def values(self) -> List[Union[int, Any]]:
        return [self.x, self.y, self.value, self.group]


class BorderPoint:

    def __init__(self):
        self.border_line = None

    def values(self):
        return self.border_line

    def transposition(self, positions):
        minx = min(np.array(positions)[:, 0])
        miny = min(np.array(positions)[:, 1])
        if minx < miny:
            positions = positions - minx + 4
        else:
            positions = positions - miny + 4

        minx = min(np.array(positions)[:, 0])
        miny = min(np.array(positions)[:, 1])

        if minx > miny:
            positions = [[x - minx + 4, y] for x, y in positions]
        else:
            positions = [[x, y - miny + 4] for x, y in positions]
        return positions


    def create_line_border_all(self, positions):
        result = []

        for i in range(0, len(positions) - 1):
            item = positions[i]
            next_item = positions[i + 1]
            if item[0] == next_item[0]:
                if item[1] < next_item[1]:
                    # dọc thuận - done
                    for i in range(item[1], next_item[1] + 1):
                        result.append([item[0], i])
                if item[1] > next_item[1]:
                    # dọc ngược - done
                    for i in range(next_item[1], item[1] + 1):
                        result.append([item[0], i])

            elif item[1] == next_item[1]:
                if item[0] < next_item[0]:
                    # ngang thuan - done
                    for i in range(item[0], next_item[0] + 1):
                        result.append([i, item[1]])
                if item[0] > next_item[0]:
                    # ngang nguoc - done
                    for i in range(next_item[0], item[0] + 1):
                        result.append([i, item[1]])

        unique_coordinates = []
        seen_coordinates = set()

        for x, y in result:
            if (x, y) not in seen_coordinates:
                unique_coordinates.append([x, y])
                seen_coordinates.add((x, y))

        return unique_coordinates

    def create_line_border(self, point, border_line):

        line_top_left, line_top_right, line_bottom_right, line_bottom_left = [], [], [], []
        min_point = [min(np.array(border_line)[:, 0]), min(np.array(border_line)[:, 1])]
        max_point = [max(np.array(border_line)[:, 0]), max(np.array(border_line)[:, 1])]

        for [x, y] in border_line:
            if x >= point[0] and y <= point[1]:
                line_top_right.append([x, y])

            if x <= point[0] and y <= point[1]:
                line_top_left.append([x, y])

            if x >= point[0] and y >= point[1]:
                line_bottom_right.append([x, y])

            if x <= point[0] and y >= point[1]:
                line_bottom_left.append([x, y])

        for x in range(point[0], min_point[0] - 1, -1):
            for y in range(point[1], min_point[1] - 1, -1):
                if x == point[0] or y == point[1]:  # là vị trí đường lưới
                    arrX_item = [i for [i, j] in border_line if j == y]
                    arrY_item = [j for [i, j] in border_line if i == x]
                    if arrY_item and arrX_item:
                        _x_ = [min(arrX_item), max(arrX_item)]
                        _y_ = [min(arrY_item), max(arrY_item)]
                        if ((x >= _x_[0]) and (x <= _x_[1])) and (y >= _y_[0] and y <= _y_[1]):  # bên trong
                            line_top_left.append([x, y])

        for x in range(point[0], max_point[0] + 1, 1):
            for y in range(point[1], min_point[1] - 1, -1):
                if (x == point[0] or y == point[1]):  # là vị trí đường lưới
                    arrX_item = [i for [i, j] in border_line if j == y]
                    arrY_item = [j for [i, j] in border_line if i == x]
                    if arrY_item and arrX_item:
                        _x_ = [min(arrX_item), max(arrX_item)]
                        _y_ = [min(arrY_item), max(arrY_item)]
                        if ((x >= _x_[0]) and (x <= _x_[1])) and (y >= _y_[0] and y <= _y_[1]):  # bên trong
                            line_top_right.append([x, y])

        for x in range(point[0], max_point[0]):
            for y in range(point[1], max_point[1]):
                if (x == point[0] or y == point[1]):  # là vị trí đường lưới
                    arrX_item = [i for [i, j] in border_line if j == y]
                    arrY_item = [j for [i, j] in border_line if i == x]
                    if arrY_item and arrX_item:
                        _x_ = [min(arrX_item), max(arrX_item)]
                        _y_ = [min(arrY_item), max(arrY_item)]
                        if ((x >= _x_[0]) and (x <= _x_[1])) and (y >= _y_[0] and y <= _y_[1]):  # bên trong
                            line_bottom_right.append([x, y])

        for x in range(point[0], min_point[0] - 1, -1):
            for y in range(point[1], max_point[1] + 1, 1):
                if (x == point[0] or y == point[1]):  # là vị trí đường lưới
                    arrX_item = [i for [i, j] in border_line if j == y]
                    arrY_item = [j for [i, j] in border_line if i == x]
                    if arrY_item and arrX_item:
                        _x_ = [min(arrX_item), max(arrX_item)]
                        _y_ = [min(arrY_item), max(arrY_item)]
                        if ((x >= _x_[0]) and (x <= _x_[1])) and (y >= _y_[0] and y <= _y_[1]):  # bên trong
                            line_bottom_left.append([x, y])

        return line_top_left, line_top_right, line_bottom_right, line_bottom_left


class Matrix:

    def __init__(self, border_line, trung_diem, grid_size):
        self.border_line = border_line
        self.trung_diem = trung_diem
        self.grid_size = grid_size

        self.matrix = np.empty((max(np.array(border_line)[:,0]) + 4, max(np.array(border_line)[:,1]) + 4, 4))

    def values(self):
        return self.matrix

    def create_matrix(self):

        bd_point = BorderPoint()
        border1, border2, border3, border4 = bd_point.create_line_border(self.trung_diem, self.border_line)

        # top left
        for x in range(0, self.trung_diem[0] + 1):
            for y in range(0, self.trung_diem[1] + 1):
                self.matrix[x, y, 0] = x
                self.matrix[x, y, 1] = y
                self.matrix[x, y, 2] = -1
                self.matrix[x, y, 3] = -1
                arrX_item = [i for [i, j] in border1 if y == j]
                arrY_item = [j for [i, j] in border1 if x == i]
                if arrY_item and arrX_item:
                    mmx_ = [min(arrX_item), max(arrX_item)]
                    mmy_ = [min(arrY_item), max(arrY_item)]
                    if ((x >= mmx_[0]) and (x <= mmx_[1])) and ((mmy_[0] <= y) and (y <= mmy_[1])):  # bên trong
                        self.matrix[x, y, 2] = 0
                        if (self.trung_diem[0] - x) % self.grid_size[0] == 0 or (self.trung_diem[1] - y) % self.grid_size[1] == 0:
                            self.matrix[x, y, 2] = 1
                        elif [x, y] in border1:
                            self.matrix[x, y, 2] = 1
        print(1)
        # top right
        for x in range(self.trung_diem[0], self.matrix.shape[0]-1):
            for y in range(0, self.trung_diem[1] + 1):
                self.matrix[x, y, 0] = x
                self.matrix[x, y, 1] = y
                self.matrix[x, y, 2] = -1
                self.matrix[x, y, 3] = -1
                arrX_item = [i for [i, j] in border2 if y == j]
                arrY_item = [j for [i, j] in border2 if x == i]
                if arrY_item and arrX_item:
                    mmx_ = [min(arrX_item), max(arrX_item)]
                    mmy_ = [min(arrY_item), max(arrY_item)]
                    if ((x >= mmx_[0]) and (x <= mmx_[1])) and ((mmy_[0] <= y) and (y <= mmy_[1])):  # bên trong
                        self.matrix[x, y, 2] = 0
                        if (self.trung_diem[0] - x) % self.grid_size[0] == 0 or (self.trung_diem[1] - y) % self.grid_size[1] == 0:
                            self.matrix[x, y, 2] = 1
                        elif [x, y] in border2:
                            self.matrix[x, y, 2] = 1
        print(2)
        # bottom right
        for x in range(self.trung_diem[0], self.matrix.shape[0]):
            for y in range(self.trung_diem[1], self.matrix.shape[1]):
                self.matrix[x, y, 0] = x
                self.matrix[x, y, 1] = y
                self.matrix[x, y, 2] = -1
                self.matrix[x, y, 3] = -1
                arrX_item = [i for [i, j] in border3 if y == j]
                arrY_item = [j for [i, j] in border3 if x == i]
                if arrY_item and arrX_item:
                    mmx_ = [min(arrX_item), max(arrX_item)]
                    mmy_ = [min(arrY_item), max(arrY_item)]
                    if ((x >= mmx_[0]) and (x <= mmx_[1])) and ((mmy_[0] <= y) and (y <= mmy_[1])):  # bên trong
                        self.matrix[x, y, 2] = 0
                        if (self.trung_diem[0] - x) % self.grid_size[0] == 0 or (self.trung_diem[1] - y) % self.grid_size[1] == 0:
                            self.matrix[x, y, 2] = 1
                        elif [x, y] in border3:
                            self.matrix[x, y, 2] = 1
        print(3)
        # top left
        for x in range(0, self.trung_diem[0] + 1):
            for y in range(self.trung_diem[1], self.matrix.shape[1]):
                self.matrix[x, y, 0] = x
                self.matrix[x, y, 1] = y
                self.matrix[x, y, 2] = -1
                self.matrix[x, y, 3] = -1
                arrX_item = [i for [i, j] in border4 if y == j]
                arrY_item = [j for [i, j] in border4 if x == i]
                if arrY_item and arrX_item:
                    mmx_ = [min(arrX_item), max(arrX_item)]
                    mmy_ = [min(arrY_item), max(arrY_item)]
                    if ((x >= mmx_[0]) and (x <= mmx_[1])) and ((mmy_[0] <= y) and (y <= mmy_[1])):  # bên trong
                        self.matrix[x, y, 2] = 0
                        if (self.trung_diem[0] - x) % self.grid_size[0] == 0 or (self.trung_diem[1] - y) % self.grid_size[1] == 0:
                            self.matrix[x, y, 2] = 1
                        elif [x, y] in border4:
                            self.matrix[x, y, 2] = 1

        print(4, 'DONE !')
        print(self.matrix.shape)

        # Lấy các góc
        corners = self.take_all_corners()
        # Cập nhật các góc có giá trị 2
        self.add_corners_to_matrix(corners)
        # Đánh dấu cho phần thịt
        self.matrix = self.label_group_for_0()

        return self.matrix

    def take_all_corners(self):

        ''' TÌM tất cả các đỉnh '''
        result_22 = []
        shape_res = np.array(self.matrix).shape
        res = self.matrix
        for i in range(2, shape_res[0] - 2):
            for j in range(2, shape_res[1] - 2):
                cell = res[i, j]
                if cell[2] == 0:
                    cell_trai = res[i - 1, j]
                    cell_phai = res[i + 1, j]
                    cell_duoi = res[i, j - 1]
                    cell_tren = res[i, j + 1]
                    cell_duoiTrai = res[i - 1, j - 1]
                    cell_duoiPhai = res[i + 1, j - 1]
                    cell_trenTrai = res[i - 1, j + 1]
                    cell_trenPhai = res[i + 1, j + 1]

                    #    |
                    #    x __ : trên phải
                    cell_tren_cua_trenPhai = res[i + 1, j + 2]
                    cell_phai_cua_trenPhai = res[i + 2, j + 1]
                    #  |
                    #  x __: trên trái
                    cell_tren_cua_trenTrai = res[i - 1, j + 2]
                    cell_trai_cua_trenTrai = res[i - 2, j + 1]
                    # __x duoi trai
                    #   |
                    cell_duoi_cua_duoiTrai = res[i - 1, j - 2]
                    cell_trai_cua_duoiTrai = res[i - 2, j - 1]
                    # duoi phai x__
                    #           |
                    cell_duoi_cua_duoiPhai = res[i + 1, j - 2]
                    cell_phai_cua_duoiPhai = res[i + 2, j - 1]

                    if cell_duoiTrai[2] == 1 and cell_duoi[2] == 1 and cell_trai[2] == 1:  # 1
                        result_22.append([int(cell_duoiTrai[0]), int(cell_duoiTrai[1]), 2, cell[3]])
                    elif cell_duoiPhai[2] == 1 and cell_duoi[2] == 1 and cell_phai[2] == 1:  # 2
                        result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], 2, cell[3]])
                    elif cell_trenTrai[2] == 1 and cell_tren[2] == 1 and cell_trai[2] == 1:  # 3
                        result_22.append([cell_trenTrai[0], cell_trenTrai[1], 2, cell[3]])
                    elif cell_trenPhai[2] == 1 and cell_tren[2] == 1 and cell_phai[2] == 1:  # 4
                        result_22.append([cell_trenPhai[0], cell_trenPhai[1], 2, cell[3]])

                    elif cell_trenPhai[2] == 1 and cell_tren_cua_trenPhai[2] == 1 and cell_phai_cua_trenPhai[
                        2] == 1:  # 5
                        result_22.append([cell_trenPhai[0], cell_trenPhai[1], 2, cell[3]])
                    elif cell_trenTrai[2] == 1 and cell_tren_cua_trenTrai[2] == 1 and cell_trai_cua_trenTrai[
                        2] == 1:  # 6
                        result_22.append([cell_trenTrai[0], cell_trenTrai[1], 2, cell[3]])
                    elif cell_duoiPhai[2] == 1 and cell_duoi_cua_duoiPhai[2] == 1 and cell_phai_cua_duoiPhai[
                        2] == 1:  # 7
                        result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], 2, cell[3]])
                    elif cell_duoiTrai[2] == 1 and cell_duoi_cua_duoiTrai[2] == 1 and cell_trai_cua_duoiTrai[
                        2] == 1:  # 8
                        result_22.append([cell_duoiTrai[0], cell_duoiTrai[1], cell_duoiTrai[2], cell[3]])

        return result_22

    def add_corners_to_matrix(self, corners):

        """ Thêm đỉnh (value = 2) vào ma trận """

        ''' Loại bỏ các đỉnh trùng lặp '''
        result = [[x, y] for [x, y, v, g] in corners]
        unique_coordinates = []
        seen_coordinates = set()

        for x, y in result:
            if (x, y) not in seen_coordinates:
                unique_coordinates.append([x, y])
                seen_coordinates.add((x, y))

        shape_res = np.array(self.matrix).shape

        for i in range(0, shape_res[0]):
            for j in range(0, shape_res[1]):
                [x, y, v, g] = self.matrix[i][j]
                if [x, y] in result:
                    self.matrix[i][j][2] = 2
        return self.matrix

    def label_group_for_0(self):
        shape_res = np.array(self.matrix).shape
        index = 1
        for i in range(1, shape_res[1] - 1):
            for j in range(1, shape_res[0] - 1):
                cell = self.matrix[j, i]
                cell_trai = self.matrix[j - 1, i]
                cell_duoi = self.matrix[j, i - 1]
                cell_duoitrai = self.matrix[j - 1, i - 1]
                if cell[2] == 0:
                    if cell_duoitrai[2] == 2 and cell_duoi[2] == 1 and cell_trai[2] == 1:
                        self.matrix[j, i, 3] = index
                        index += 1
                    if cell_trai[3] != -1:
                        self.matrix[j, i, 3] = cell_trai[3]
                    if cell_duoi[3] != -1:
                        self.matrix[j, i, 3] = cell_duoi[3]

        # Đồng nhất các nhóm nằm chung 1 mảnh
        checks = []
        for i in range(0, shape_res[1] - 1):
            for j in range(0, shape_res[0] - 1):
                cell = self.matrix[j, i]
                cell_trai = self.matrix[j - 1, i]
                cell_phai = self.matrix[j + 1, i]
                if (cell[3] != -1 and cell_phai[3] != -1) and cell[3] - cell_phai[3] != 0:
                    checks.append([cell[3], cell_phai[3]])

        c4 = list(set(tuple(x) for x in checks))

        for (grx, gry) in c4:
            for i in range(0, shape_res[1] - 1):
                for j in range(0, shape_res[0] - 1):
                    if self.matrix[j, i, 3] == gry:
                        self.matrix[j, i, 3] = grx

        return self.matrix

    def getGroup(self, matrix1):
        result_22 = []
        shape_res = np.array(self.matrix).shape
        res = self.matrix
        for i in range(3, shape_res[0] - 3):
            for j in range(3, shape_res[1] - 3):
                cell = res[i, j]
                if cell[2] == 0:
                    cell_trai = res[i - 1, j]
                    cell_phai = res[i + 1, j]
                    cell_duoi = res[i, j - 1]
                    cell_tren = res[i, j + 1]
                    cell_duoiTrai = res[i - 1, j - 1]
                    cell_duoiPhai = res[i + 1, j - 1]
                    cell_trenTrai = res[i - 1, j + 1]
                    cell_trenPhai = res[i + 1, j + 1]

                    #    |
                    #    x __ : trên phải
                    cell_tren_cua_trenPhai = res[i + 1, j + 2]
                    cell_phai_cua_trenPhai = res[i + 2, j + 1]
                    #  |
                    #  x __: trên trái
                    cell_tren_cua_trenTrai = res[i - 1, j + 2]
                    cell_trai_cua_trenTrai = res[i - 2, j + 1]
                    # __x duoi trai
                    #   |
                    cell_duoi_cua_duoiTrai = res[i - 1, j - 2]
                    cell_trai_cua_duoiTrai = res[i - 2, j - 1]
                    # duoi phai x__
                    #           |
                    cell_duoi_cua_duoiPhai = res[i + 1, j - 2]
                    cell_phai_cua_duoiPhai = res[i + 2, j - 1]

                    if cell_duoiTrai[2] == 2 and cell_duoi[2] == 1 and cell_trai[2] == 1:  # 1
                        result_22.append([int(cell_duoiTrai[0]), int(cell_duoiTrai[1]), 2, int(cell[3])])
                    elif cell_duoiPhai[2] == 2 and cell_duoi[2] == 1 and cell_phai[2] == 1:  # 2
                        result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], 2, int(cell[3])])
                    elif cell_trenTrai[2] == 2 and cell_tren[2] == 1 and cell_trai[2] == 1:  # 3
                        result_22.append([cell_trenTrai[0], cell_trenTrai[1], 2, int(cell[3])])
                    elif cell_trenPhai[2] == 2 and cell_tren[2] == 1 and cell_phai[2] == 1:  # 4
                        result_22.append([cell_trenPhai[0], cell_trenPhai[1], 2, int(cell[3])])

                    elif cell_trenPhai[2] == 2 and cell_tren_cua_trenPhai[2] == 1 and cell_phai_cua_trenPhai[
                        2] == 1:  # 5
                        result_22.append([cell_trenPhai[0], cell_trenPhai[1], 2, int(cell[3])])
                    elif cell_trenTrai[2] == 2 and cell_tren_cua_trenTrai[2] == 1 and cell_trai_cua_trenTrai[
                        2] == 1:  # 6
                        result_22.append([cell_trenTrai[0], cell_trenTrai[1], 2, int(cell[3])])
                    elif cell_duoiPhai[2] == 2 and cell_duoi_cua_duoiPhai[2] == 1 and cell_phai_cua_duoiPhai[
                        2] == 1:  # 7
                        result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], 2, int(cell[3])])
                    elif cell_duoiTrai[2] == 2 and cell_duoi_cua_duoiTrai[2] == 1 and cell_trai_cua_duoiTrai[
                        2] == 1:  # 8
                        result_22.append([cell_duoiTrai[0], cell_duoiTrai[1], cell_duoiTrai[2], int(cell[3])])

        return result_22


class Cross:

    def __init__(self, point):
        self.point = point
        self.TOP = False
        self.BOTTOM = False
        self.LEFT = False
        self.RIGHT = False

    def __init(self):
        pass

    def set_top(self, boolean=False):
        self.TOP = boolean

    def set_bottom(self, boolean=False):
        self.BOTTOM = boolean

    def set_left(self, boolean=False):
        self.LEFT = boolean

    def set_right(self, boolean=False):
        self.RIGHT = boolean

    def getpoint(self):
        return self.point

    def getcore(self, point):
        num = 0
        if self.TOP:
            num += 1
        if self.BOTTOM:
            num += 1
        if self.LEFT:
            num += 1
        if self.RIGHT:
            num += 1
        return num

    def values(self):
        """ POINT, TOP, RIGHT, BOTTOM, LEFT """
        return [self.point, self.TOP, self.RIGHT, self.BOTTOM, self.LEFT]

    def __str__(self):
        return f'p:{self.point}, cross: {self.getcore(self.point)}, top:{self.TOP}, right:{self.RIGHT}, bottom:{self.BOTTOM}, left:{self.LEFT}'

    def show(self):
        strings = f"{self.point}: {self.getcore(self.point)} =>"
        if self.TOP:
            strings += "TOP "
        if self.BOTTOM:
            strings += "BOTTOM "
        if self.LEFT:
            strings += "LEFT "
        if self.RIGHT:
            strings += "RIGHT "
        return strings

class ListCross:

    def __init__(self):
        self.cross = []

    def values(self):
        return self.cross

    def create_cross(self, matrix, shape_pieces_1, shape_pieces_2):
        self.cross = []
        [start, end] = [[min(np.array(shape_pieces_1)[:, 0] - 1), min(np.array(shape_pieces_1)[:, 1] - 1)],
                         [max(np.array(shape_pieces_2)[:, 0] + 1), max(np.array(shape_pieces_2)[:, 1] + 1)]]

        mt_temp = np.empty((matrix.shape[0], matrix.shape[1], 4))
        mt_temp[start[0]+1:end[0], start[1]+1:end[1]] = matrix[start[0]+1:end[0], start[1]+1:end[1]]

        for x in range(0, mt_temp.shape[0]):
            for y in range(0, mt_temp.shape[1]):
                if mt_temp[x, y, 2] == 2:
                    cross = Cross([int(mt_temp[x, y, 0]), int(mt_temp[x, y, 1])])
                    cell_trai = mt_temp[x - 1, y]
                    cell_phai = mt_temp[x + 1, y]
                    cell_duoi = mt_temp[x, y + 1]
                    cell_tren = mt_temp[x, y - 1]

                    if cell_trai[2] == 1:
                        cross.set_left(True)
                    if cell_phai[2] == 1:
                        cross.set_right(True)
                    if cell_duoi[2] == 1:
                        cross.set_bottom(True)
                    if cell_tren[2] == 1:
                        cross.set_top(True)

                    self.cross.append(cross)

        return self.cross

    def find_core(self, point):
        for core in self.cross:
            if point[0] == core.point[0] and point[1] == core.point[1]:
                return core



class State:
    def __init__(self, group):
        result_all = sorted(group, key=lambda x: x[3])
        result = [list(group) for key, group in groupby(result_all, key=lambda x: x[3])]
        self.state = [[[int(x), int(y), int(v), int(g)] for x, y, v, g in group] for group in result]
        self.state_sort = self.sort_state(self.state)

    def find_group(self, group_int):
        res = []
        for arr in self.state_sort:
            for x, y, v, g in arr:
                if g == group_int:
                    res.append([int(x), int(y)])
        return res

    def sort_state(self, state):
        res = []
        for points in state:
            state = [points[0]]
            item = points[0]
            points.pop(0)
            for i in range(0, len(points)):
                for point in points:
                    if point[0] == state[-1][0] or point[1] == state[-1][1]:
                        state.append(point)
                        points.remove(point)
                        break
            res.append(state)
        return res


