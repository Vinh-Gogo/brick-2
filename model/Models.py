import numpy as np


class Point:

    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

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

    def values(self) -> int:
        return self.x, self.y, self.value, self.group


class BorderPoint:

    def __init__(self):
        self.arrays = []

    def values(self):
        return self.arrays

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

        self.arrays = unique_coordinates
        return unique_coordinates

    def create_line_border(self, point=[]):

        line_top_left, line_top_right, line_bottom_right, line_bottom_left = [], [], [], []
        min_point = [min(np.array(self.arrays)[:, 0]), min(np.array(self.arrays)[:, 1])]
        max_point = [max(np.array(self.arrays)[:, 0]), max(np.array(self.arrays)[:, 1])]

        for [x, y] in self.arrays:
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
                if (x == point[0] or y == point[1]):  # là vị trí đường lưới
                    arrX_item = [i for [i, j] in self.arrays if j == y]
                    arrY_item = [j for [i, j] in self.arrays if i == x]
                    if arrY_item and arrX_item:
                        _x_ = [min(arrX_item), max(arrX_item)]
                        _y_ = [min(arrY_item), max(arrY_item)]
                        if ((x >= _x_[0]) and (x <= _x_[1])) and (y >= _y_[0] and y <= _y_[1]):  # bên trong
                            line_top_left.append([x, y])

        for x in range(point[0], max_point[0] + 1, 1):
            for y in range(point[1], min_point[1] - 1, -1):
                if (x == point[0] or y == point[1]):  # là vị trí đường lưới
                    arrX_item = [i for [i, j] in self.arrays if j == y]
                    arrY_item = [j for [i, j] in self.arrays if i == x]
                    if arrY_item and arrX_item:
                        _x_ = [min(arrX_item), max(arrX_item)]
                        _y_ = [min(arrY_item), max(arrY_item)]
                        if ((x >= _x_[0]) and (x <= _x_[1])) and (y >= _y_[0] and y <= _y_[1]):  # bên trong
                            line_top_right.append([x, y])

        for x in range(point[0], max_point[0] + 1, 1):
            for y in range(point[1], max_point[1] + 1, 1):
                if (x == point[0] or y == point[1]):  # là vị trí đường lưới
                    arrX_item = [i for [i, j] in self.arrays if j == y]
                    arrY_item = [j for [i, j] in self.arrays if i == x]
                    if arrY_item and arrX_item:
                        _x_ = [min(arrX_item), max(arrX_item)]
                        _y_ = [min(arrY_item), max(arrY_item)]
                        if ((x >= _x_[0]) and (x <= _x_[1])) and (y >= _y_[0] and y <= _y_[1]):  # bên trong
                            line_bottom_right.append([x, y])

        for x in range(point[0], min_point[0] - 1, -1):
            for y in range(point[1], max_point[1] + 1, 1):
                if (x == point[0] or y == point[1]):  # là vị trí đường lưới
                    arrX_item = [i for [i, j] in self.arrays if j == y]
                    arrY_item = [j for [i, j] in self.arrays if i == x]
                    if arrY_item and arrX_item:
                        _x_ = [min(arrX_item), max(arrX_item)]
                        _y_ = [min(arrY_item), max(arrY_item)]
                        if ((x >= _x_[0]) and (x <= _x_[1])) and (y >= _y_[0] and y <= _y_[1]):  # bên trong
                            line_bottom_left.append([x, y])

        # unique_coordinates = []
        # seen_coordinates = set()

        # for x, y in line_top_left:
        #     if (x, y) not in seen_coordinates:
        #         unique_coordinates.append([x, y])
        #         seen_coordinates.add((x, y))
        return line_top_left, line_top_right, line_bottom_right, line_bottom_left


class Matrix:

    def create_matrix(self, trung_diem, grid_size, border1, border2, border3, border4):
        ## 1
        # Lấy tọa độ "lớn nhất" vào "nhỏ nhất" của trục hoành (trục x)
        mmx = [min(np.array(border1)[:, 0]), max(np.array(border1)[:, 0])]
        # Lấy tọa độ "lớn nhất" vào "nhỏ nhất" của trục tung (trục y)
        mmy = [min(np.array(border1)[:, 1]), max(np.array(border1)[:, 1])]

        matrix1, matrix2, matrix3, matrix4 = [], [], [], []
        for x in range(trung_diem[0] + 1, mmx[0] - 1, -1):
            arr = []
            for y in range(trung_diem[1] + 1, mmy[0] - 1, -1):
                cell = [x, y, None, None]
                arrX_item = [i for [i, j] in border1 if y == j]
                arrY_item = [j for [i, j] in border1 if x == i]
                if arrY_item and arrX_item:
                    mmx_ = [min(arrX_item), max(arrX_item)]
                    mmy_ = [min(arrY_item), max(arrY_item)]
                    if ((x >= mmx_[0]) and (x <= mmx_[1])) and ((mmy_[0] <= y) and (y <= mmy_[1])):  # bên trong
                        cell = [x, y, 0, None]
                        if (trung_diem[0] - x) % grid_size[0] == 0 or (trung_diem[1] - y) % grid_size[1] == 0:
                            cell = [x, y, 1, None]
                        elif [x, y] in border1:
                            cell = [x, y, 1, None]
                arr.append(cell)
            matrix1.append(arr)
        print(1)
        #~ 2
        # Lấy tọa độ "lớn nhất" vào "nhỏ nhất" của trục hoành (trục x)
        mmx = [min(np.array(border2)[:, 0]), max(np.array(border2)[:, 0])]
        # Lấy tọa độ "lớn nhất" vào "nhỏ nhất" của trục tung (trục y)
        mmy = [min(np.array(border2)[:, 1]), max(np.array(border2)[:, 1])]

        for x in range(trung_diem[0] - 1, mmx[1] + 1, 1):
            arr = []
            for y in range(trung_diem[1] + 1, mmy[0] - 1, -1):
                cell = [x, y, None, None]
                arrX_item = [i for [i, j] in border2 if y == j]
                arrY_item = [j for [i, j] in border2 if x == i]
                if arrY_item and arrX_item:
                    mmx_ = [min(arrX_item), max(arrX_item)]
                    mmy_ = [min(arrY_item), max(arrY_item)]
                    if ((x >= mmx_[0]) and (x <= mmx_[1])) and (y >= mmy_[0] and y <= mmy_[1]):  # bên trong
                        cell = [x, y, 0, None]
                        if (x - trung_diem[0]) % grid_size[0] == 0 or (y - trung_diem[1]) % grid_size[1] == 0:
                            cell = [x, y, 1, None]
                        elif [x, y] in border2:
                            cell = [x, y, 1, None]
                arr.append(cell)
            matrix2.append(arr)
        print(2)
        # 3
        # Lấy tọa độ "lớn nhất" vào "nhỏ nhất" của trục hoành (trục x)
        mmx = [min(np.array(border3)[:, 0]), max(np.array(border3)[:, 0])]
        # Lấy tọa độ "lớn nhất" vào "nhỏ nhất" của trục tung (trục y)
        mmy = [min(np.array(border3)[:, 1]), max(np.array(border3)[:, 1])]

        for x in range(trung_diem[0] - 1, mmx[1] + 1, 1):
            arr = []
            for y in range(trung_diem[1] - 1, mmy[1] + 1, 1):
                cell = [x, y, None, None]
                arrX_item = [i for [i, j] in border3 if y == j]
                arrY_item = [j for [i, j] in border3 if x == i]
                if arrY_item and arrX_item:
                    mmx_ = [min(arrX_item), max(arrX_item)]
                    mmy_ = [min(arrY_item), max(arrY_item)]
                    if ((x >= mmx_[0]) and (x <= mmx_[1])) and (y >= mmy_[0] and y <= mmy_[1]):  # bên trong
                        cell = [x, y, 0, None]
                        if (x - trung_diem[0]) % grid_size[0] == 0 or (y - trung_diem[1]) % grid_size[1] == 0:
                            cell = [x, y, 1, None]
                        elif [x, y] in border3:
                            cell = [x, y, 1, None]
                arr.append(cell)
            matrix3.append(arr)
        print(3)

        # 4
        # Lấy tọa độ "lớn nhất" vào "nhỏ nhất" của trục hoành (trục x)
        mmx = [min(np.array(border4)[:, 0]), max(np.array(border4)[:, 0])]
        # Lấy tọa độ "lớn nhất" vào "nhỏ nhất" của trục tung (trục y)
        mmy = [min(np.array(border4)[:, 1]), max(np.array(border4)[:, 1])]

        for x in range(trung_diem[0] + 1, mmx[0] - 1, - 1):
            arr = []
            for y in range(trung_diem[1] - 1, mmy[1] + 1, 1):
                cell = [x, y, None, None]
                arrX_item = [i for [i, j] in border4 if y == j]
                arrY_item = [j for [i, j] in border4 if x == i]
                if arrY_item and arrX_item:
                    mmx_ = [min(arrX_item), max(arrX_item)]
                    mmy_ = [min(arrY_item), max(arrY_item)]
                    if ((x >= mmx_[0]) and (x <= mmx_[1])) and (y >= mmy_[0] and y <= mmy_[1]):  # bên trong
                        cell = [x, y, 0, None]
                        if (x - trung_diem[0]) % grid_size[0] == 0 or (y - trung_diem[1]) % grid_size[1] == 0:
                            cell = [x, y, 1, None]
                        elif [x, y] in border4:
                            cell = [x, y, 1, None]
                arr.append(cell)
            matrix4.append(arr)
        print(4)
        return matrix1, matrix2, matrix3, matrix4

    def take_all_corners(self, matrix):

        ''' TÌM tất cả các đỉnh '''
        result_22 = []
        shape_res = np.array(matrix).shape
        res = matrix
        for i in range(0, shape_res[0]):
            for j in range(0, shape_res[1]):
                cell = res[i][j]
                if cell[2] == 0:
                    cell_trai = res[i - 1][j]
                    cell_phai = res[i + 1][j]
                    cell_duoi = res[i][j - 1]
                    cell_tren = res[i][j + 1]
                    cell_duoiTrai = res[i - 1][j - 1]
                    cell_duoiPhai = res[i + 1][j - 1]
                    cell_trenTrai = res[i - 1][j + 1]
                    cell_trenPhai = res[i + 1][j + 1]

                    if (i > 2 and j > 2) and (i < shape_res[0] - 2 and j < shape_res[1] - 2):
                        if (res[i + 1][j + 2] and res[i + 2][j + 1] and
                                res[i - 1][j + 2] and res[i - 2][j + 1] and
                                res[i - 1][j - 2] and res[i - 2][j - 1] and
                                res[i + 1][j - 2] and res[i + 2][j - 1]):
                            #    |
                            #    x __ : trên phải
                            cell_tren_cua_trenPhai = res[i + 1][j + 2]
                            cell_phai_cua_trenPhai = res[i + 2][j + 1]
                            #  |
                            #  x __: trên trái
                            cell_tren_cua_trenTrai = res[i - 1][j + 2]
                            cell_trai_cua_trenTrai = res[i - 2][j + 1]
                            # __x duoi trai
                            #   |
                            cell_duoi_cua_duoiTrai = res[i - 1][j - 2]
                            cell_trai_cua_duoiTrai = res[i - 2][j - 1]
                            # duoi phai x__
                            #           |
                            cell_duoi_cua_duoiPhai = res[i + 1][j - 2]
                            cell_phai_cua_duoiPhai = res[i + 2][j - 1]

                            if cell_duoiTrai[2] == 1 and cell_duoi[2] == 1 and cell_trai[2] == 1:  # 1
                                result_22.append([cell_duoiTrai[0], cell_duoiTrai[1], 2, cell[3]])
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
                    else:
                        if cell_duoiTrai[2] == 1 and cell_duoi[2] == 1 and cell_trai[2] == 1:  # 1
                            result_22.append([cell_duoiTrai[0], cell_duoiTrai[1], 2, cell[3]])
                        elif cell_duoiPhai[2] == 1 and cell_duoi[2] == 1 and cell_phai[2] == 1:  # 2
                            result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], 2, cell[3]])
                        elif cell_trenTrai[2] == 1 and cell_tren[2] == 1 and cell_trai[2] == 1:  # 3
                            result_22.append([cell_trenTrai[0], cell_trenTrai[1], 2, cell[3]])
                        elif cell_trenPhai[2] == 1 and cell_tren[2] == 1 and cell_phai[2] == 1:  # 4
                            result_22.append([cell_trenPhai[0], cell_trenPhai[1], 2, cell[3]])
        return result_22

    def add_corners_to_matrix(self, corners, matrix):

        """ Thêm đỉnh (value = 2) vào ma trận """

        ''' Loại bỏ các đỉnh trùng lặp '''
        result = [[x, y] for [x, y, v, g] in corners]
        unique_coordinates = []
        seen_coordinates = set()

        for x, y in result:
            if (x, y) not in seen_coordinates:
                unique_coordinates.append([x, y])
                seen_coordinates.add((x, y))

        shape_res = np.array(matrix).shape

        for i in range(0, shape_res[0]):
            for j in range(0, shape_res[1]):
                [x, y, v, g] = matrix[i][j]
                if [x, y] in result:
                    matrix[i][j][2] = 2
        return matrix

    def label_group_for_0(self, matrix):
        shape_res = np.array(matrix).shape
        index = 1
        for i in range(0, shape_res[1] - 1):
            for j in range(0, shape_res[0] - 1):
                cell = matrix[j][i]
                cell_trai = matrix[j - 1][i]
                cell_duoi = matrix[j][i - 1]
                cell_duoitrai = matrix[j - 1][i - 1]
                if cell[2] == 0:
                    if cell_duoitrai[2] == 2 and cell_duoi[2] == 1 and cell_trai[2] == 1:
                        matrix[j][i][3] = index
                        index += 1
                    if cell_trai[3] != None:
                        matrix[j][i][3] = cell_trai[3]
                    if cell_duoi[3] != None:
                        matrix[j][i][3] = cell_duoi[3]

        # Đồng nhất các nhóm nằm chung 1 mảnh
        checks = []
        for i in range(0, shape_res[1] - 1):
            for j in range(0, shape_res[0] - 1):
                cell = matrix[j][i]
                cell_trai = matrix[j - 1][i]
                cell_phai = matrix[j + 1][i]
                if (cell[3] != None and cell_phai[3] != None) and cell[3] - cell_phai[3] != 0:
                    checks.append([cell[3], cell_phai[3]])

        c4 = list(set(tuple(x) for x in checks))

        for (grx, gry) in c4:
            for i in range(0, shape_res[1] - 1):
                for j in range(0, shape_res[0] - 1):
                    cell = matrix[j][i]
                    if cell[3] == gry:
                        matrix[j][i][3] = grx

        return matrix

    def getGroup(self, matrix1):
        result_22 = []
        shape_res = np.array(matrix1).shape
        res = matrix1
        for i in range(0, shape_res[0]):
            for j in range(0, shape_res[1]):
                cell = res[i][j]
                if cell[2] == 0:
                    cell_trai = res[i - 1][j]
                    cell_phai = res[i + 1][j]
                    cell_duoi = res[i][j - 1]
                    cell_tren = res[i][j + 1]
                    cell_duoiTrai = res[i - 1][j - 1]
                    cell_duoiPhai = res[i + 1][j - 1]
                    cell_trenTrai = res[i - 1][j + 1]
                    cell_trenPhai = res[i + 1][j + 1]

                    if (i > 2 and j > 2) and (i < shape_res[0] - 2 and j < shape_res[1] - 2):
                        if (res[i + 1][j + 2] and res[i + 2][j + 1] and
                                res[i - 1][j + 2] and res[i - 2][j + 1] and
                                res[i - 1][j - 2] and res[i - 2][j - 1] and
                                res[i + 1][j - 2] and res[i + 2][j - 1]):
                            #    |
                            #    x __ : trên phải
                            cell_tren_cua_trenPhai = res[i + 1][j + 2]
                            cell_phai_cua_trenPhai = res[i + 2][j + 1]
                            #  |
                            #  x __: trên trái
                            cell_tren_cua_trenTrai = res[i - 1][j + 2]
                            cell_trai_cua_trenTrai = res[i - 2][j + 1]
                            # __x duoi trai
                            #   |
                            cell_duoi_cua_duoiTrai = res[i - 1][j - 2]
                            cell_trai_cua_duoiTrai = res[i - 2][j - 1]
                            # duoi phai x__
                            #           |
                            cell_duoi_cua_duoiPhai = res[i + 1][j - 2]
                            cell_phai_cua_duoiPhai = res[i + 2][j - 1]

                            if cell_duoiTrai[2] == 2 and cell_duoi[2] == 1 and cell_trai[2] == 1:  # 1
                                result_22.append([cell_duoiTrai[0], cell_duoiTrai[1], 2, cell[3]])
                            elif cell_duoiPhai[2] == 2 and cell_duoi[2] == 1 and cell_phai[2] == 1:  # 2
                                result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], 2, cell[3]])
                            elif cell_trenTrai[2] == 2 and cell_tren[2] == 1 and cell_trai[2] == 1:  # 3
                                result_22.append([cell_trenTrai[0], cell_trenTrai[1], 2, cell[3]])
                            elif cell_trenPhai[2] == 2 and cell_tren[2] == 1 and cell_phai[2] == 1:  # 4
                                result_22.append([cell_trenPhai[0], cell_trenPhai[1], 2, cell[3]])

                            elif cell_trenPhai[2] == 2 and cell_tren_cua_trenPhai[2] == 1 and cell_phai_cua_trenPhai[
                                2] == 1:  # 5
                                result_22.append([cell_trenPhai[0], cell_trenPhai[1], 2, cell[3]])
                            elif cell_trenTrai[2] == 2 and cell_tren_cua_trenTrai[2] == 1 and cell_trai_cua_trenTrai[
                                2] == 1:  # 6
                                result_22.append([cell_trenTrai[0], cell_trenTrai[1], 2, cell[3]])
                            elif cell_duoiPhai[2] == 2 and cell_duoi_cua_duoiPhai[2] == 1 and cell_phai_cua_duoiPhai[
                                2] == 1:  # 7
                                result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], 2, cell[3]])
                            elif cell_duoiTrai[2] == 2 and cell_duoi_cua_duoiTrai[2] == 1 and cell_trai_cua_duoiTrai[
                                2] == 1:  # 8
                                result_22.append([cell_duoiTrai[0], cell_duoiTrai[1], cell_duoiTrai[2], cell[3]])
                    else:
                        if cell_duoiTrai[2] == 2 and cell_duoi[2] == 1 and cell_trai[2] == 1:  # 1
                            result_22.append([cell_duoiTrai[0], cell_duoiTrai[1], 2, cell[3]])
                        elif cell_duoiPhai[2] == 2 and cell_duoi[2] == 1 and cell_phai[2] == 1:  # 2
                            result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], 2, cell[3]])
                        elif cell_trenTrai[2] == 2 and cell_tren[2] == 1 and cell_trai[2] == 1:  # 3
                            result_22.append([cell_trenTrai[0], cell_trenTrai[1], 2, cell[3]])
                        elif cell_trenPhai[2] == 2 and cell_tren[2] == 1 and cell_phai[2] == 1:  # 4
                            result_22.append([cell_trenPhai[0], cell_trenPhai[1], 2, cell[3]])
        return result_22

class Core:

    def __init__(self):

        ''' Gồm có 3 loại core (core 90 độ, core 180 độ và core 360 độ) '''

        self.core90 = []
        self.core180 = []
        self.core360 = []

    def create_core(self, matrix):

        ''' input: ma trận đã được phân loại đỉnh, cạnh và thịt '''

        shape_res = np.array(matrix).shape
        res = matrix
        for i in range(0, shape_res[0]):
            for j in range(0, shape_res[1]):
                cell = res[i][j]
                x, y, v, g = cell
                if v == 2:
                    if (i > 0 and j > 0) and (i < shape_res[0] - 1 and j < shape_res[1] - 1):
                        # cv2.line(image, (x,y), (x,y), (0,0,0), 5)
                        lenght = 0
                        if res[i - 1][j][2] == 1:  # trai
                            lenght += 1
                        if res[i + 1][j][2] == 1:  # phai
                            lenght += 1
                        if res[i][j - 1][2] == 1:  # duoi
                            lenght += 1
                        if res[i][j + 1][2] == 1:  # tren
                            lenght += 1

                        if lenght == 2:
                            self.core90.append([x, y])
                        elif lenght == 3:
                            self.core180.append([x, y])
                        elif lenght == 4:
                            self.core360.append([x, y])

        return self.core90, self.core180, self.core360

    def values(self):
        return self.core90, self.core180, self.core360


from enum import Enum


class Core90(Enum):
    BOTTOM_RIGHT = [[0, 0, 0], [0, 1, 1], [0, 1, 0]]
    BOTTOM_LEFT = [[0, 0, 0], [1, 1, 0], [0, 1, 0]]
    TOP_RIGHT = [[0, 1, 0], [0, 1, 1], [0, 0, 0]]
    TOP_LEFT = [[0, 1, 0], [1, 1, 0], [0, 0, 0]]


class Core180(Enum):
    TOP = [[0, 1, 0], [1, 1, 1], [0, 0, 0]]
    RIGHT = [[0, 1, 0], [0, 1, 1], [0, 1, 0]]
    BOTTOM = [[0, 0, 0], [1, 1, 1], [0, 1, 0]]
    LEFT = [[0, 1, 0], [1, 1, 0], [0, 1, 0]]


class Core360(Enum):
    FULL = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
