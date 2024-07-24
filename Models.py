import numpy as np

class Point:
    
    def __init__(self, x = 0, y = 0) -> None:
        self.x = x
        self.y = y
    
    def __init__(self, x = 0, y = 0, value = None, group = None) -> None:
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
    
class grid_size:

    def __init__(self, horizontal, vertical):
        ''' 
            x: horizontal (trục ngang), y: vertical (trục dọc) 

            intput: [int, int]
        '''
        self.x = horizontal
        self.y = vertical
      
    def values(self) -> int:
        return self.x, self.y

class BorderPoint:
    
    def __init__(self, arrays):
        '''
            Coordinates of the frame
           
            input: [[x1, y1], [x2, y2], ... [xn, yn]]
        '''
        self.arrays = arrays
    
    def values(self):
        return self.arrays
    
    def create_border_lines(self):
        result = []
        
        for i in range(0, len(self.arrays) - 1):
            item = self.arrays[i]
            next_item = self.arrays[i+1]
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


class Matrix:
    def __init__(self):
        self.matrix = []
        
    def create_matrix(self, grid_size = grid_size(None, None), positions = []):
        
        bbp = BorderPoint(positions)
        border_line = bbp.create_border_lines()
        
        # lấy trung điểm
        trung_diem = (int(np.mean(np.array(border_line)[:,0])), int(np.mean(np.array(border_line)[:,1])))
        # Lấy tọa độ "lớn nhất" vào "nhỏ nhất" của trục hoành (trục x)
        mmx = (min(np.array(positions)[:,0]), max(np.array(positions)[:,0]))
        # Lấy tọa độ "lớn nhất" vào "nhỏ nhất" của trục tung (trục y)
        mmy = (min(np.array(positions)[:,1]), max(np.array(positions)[:,1]))
        
        for x in range(mmx[0]-2, mmx[1]+2, 1):
            arr = []
            for y in range(mmy[0]-2, mmy[1]+2, 1):
                cell = [x,y,None, None]
                arrX_item = [i for [i, j] in border_line if y == j]
                arrY_item = [j for [i, j] in border_line if x == i]
                if arrY_item and arrX_item:
                    mmx_ = [min(arrX_item), max(arrX_item)]
                    mmy_ = [min(arrY_item), max(arrY_item)]
                    if ((x >= mmx_[0]) and (x <= mmx_[1])) and (y >= mmy_[0] and y <= mmy_[1]):  # bên trong
                        cell = [x, y, 0, None]
                        if (trung_diem[0] - x) % grid_size[0] == 0 or (trung_diem[1] - y) % grid_size[1] == 0: 
                            cell = [x, y, 1, None]
                        elif [x, y] in border_line:
                            cell = [x, y, 1, None]
                            
                arr.append(cell)
            self.matrix.append(arr)
        
        return self.matrix
    
    def take_all_corners(self):
        
        ''' Duyệt lấy tất cả các đỉnh '''
        result_22 = []
        shape_res = np.array(self.matrix).shape
        res = self.matrix
        for i in range(0, shape_res[0]):
            for j in range(0, shape_res[1]):
                cell = res[i][j]  
                if cell[2] == 0:
                    cell_trai = res[i-1][j]
                    cell_phai = res[i+1][j]
                    cell_duoi = res[i][j-1]
                    cell_tren = res[i][j+1]
                    cell_duoiTrai = res[i-1][j-1]
                    cell_duoiPhai = res[i+1][j-1]
                    cell_trenTrai = res[i-1][j+1]
                    cell_trenPhai = res[i+1][j+1]
                    
                    if (i > 2 and j > 2) and (i < shape_res[0]-2 and j < shape_res[1] - 2):
                        if (res[i+1][j+2] and res[i+2][j+1] and
                            res[i-1][j+2] and res[i-2][j+1] and
                            res[i-1][j-2] and res[i-2][j-1] and
                            res[i+1][j-2] and res[i+2][j-1]):
                            #    |
                            #    x __ : trên phải
                            cell_tren_cua_trenPhai = res[i+1][j+2]
                            cell_phai_cua_trenPhai = res[i+2][j+1]
                            #  |
                            #  x __: trên trái
                            cell_tren_cua_trenTrai = res[i-1][j+2]
                            cell_trai_cua_trenTrai = res[i-2][j+1]
                            # __x duoi trai
                            #   |
                            cell_duoi_cua_duoiTrai = res[i-1][j-2]
                            cell_trai_cua_duoiTrai = res[i-2][j-1]
                            # duoi phai x__
                            #           |
                            cell_duoi_cua_duoiPhai = res[i+1][j-2]
                            cell_phai_cua_duoiPhai = res[i+2][j-1]
                            
                            if cell_duoiTrai[2] == 1 and cell_duoi[2] == 1 and cell_trai[2] == 1: # 1
                                result_22.append([cell_duoiTrai[0], cell_duoiTrai[1], cell_duoiTrai[2] , cell[3]])
                            elif cell_duoiPhai[2] == 1 and cell_duoi[2] == 1 and cell_phai[2] == 1: # 2
                                result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], cell_duoiPhai[2] , cell[3]])
                            elif cell_trenTrai[2] == 1 and cell_tren[2] == 1 and cell_trai[2] == 1: # 3
                                result_22.append([cell_trenTrai[0], cell_trenTrai[1], cell_trenTrai[2] , cell[3]])
                            elif cell_trenPhai[2] == 1 and cell_tren[2] == 1 and cell_phai[2] == 1: # 4
                                result_22.append([cell_trenPhai[0], cell_trenPhai[1], cell_trenPhai[2] , cell[3]])

                            elif cell_trenPhai[2] == 1 and cell_tren_cua_trenPhai[2] == 1 and cell_phai_cua_trenPhai[2] == 1: # 5
                                result_22.append([cell_trenPhai[0], cell_trenPhai[1], cell_trenPhai[2] , cell[3]])
                            elif cell_trenTrai[2] == 1 and cell_tren_cua_trenTrai[2] == 1 and cell_trai_cua_trenTrai[2] == 1: # 6
                                result_22.append([cell_trenTrai[0], cell_trenTrai[1], cell_trenTrai[2] , cell[3]])
                            elif cell_duoiPhai[2] == 1 and cell_duoi_cua_duoiPhai[2] == 1 and cell_phai_cua_duoiPhai[2] == 1: # 7
                                result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], cell_duoiPhai[2] , cell[3]])
                            elif cell_duoiTrai[2] == 1 and cell_duoi_cua_duoiTrai[2] == 1 and cell_trai_cua_duoiTrai[2] == 1: # 8
                                result_22.append([cell_duoiTrai[0], cell_duoiTrai[1], cell_duoiTrai[2] , cell[3]])
                    else:
                        if cell_duoiTrai[2] == 1 and cell_duoi[2] == 1 and cell_trai[2] == 1: # 1
                            result_22.append([cell_duoiTrai[0], cell_duoiTrai[1], cell_duoiTrai[2] , cell[3]])
                        elif cell_duoiPhai[2] == 1 and cell_duoi[2] == 1 and cell_phai[2] == 1: # 2
                            result_22.append([cell_duoiPhai[0], cell_duoiPhai[1], cell_duoiPhai[2] , cell[3]])
                        elif cell_trenTrai[2] == 1 and cell_tren[2] == 1 and cell_trai[2] == 1: # 3
                            result_22.append([cell_trenTrai[0], cell_trenTrai[1], cell_trenTrai[2] , cell[3]])
                        elif cell_trenPhai[2] == 1 and cell_tren[2] == 1 and cell_phai[2] == 1: # 4
                            result_22.append([cell_trenPhai[0], cell_trenPhai[1], cell_trenPhai[2] , cell[3]])
        
        ''' Loại bỏ các đỉnh trùng lặp '''
        result = [[x,y] for [x,y,v,g] in result_22]
        unique_coordinates = []
        seen_coordinates = set()

        for x, y in result:
            if (x, y) not in seen_coordinates:
                unique_coordinates.append([x, y])
                seen_coordinates.add((x, y))

        return unique_coordinates
    
    def add_corners_to_matrix(self, corners):
        
        ''' Thêm đỉnh vào ma trận '''
        
        shape_res = np.array(self.matrix).shape

        for i in range(0, shape_res[0]):
            for j in range(0, shape_res[1]):
                [x,y,v,g] = self.matrix[i][j]
                if [x,y] in corners:
                    self.matrix[i][j][2] = 2
    
        return self.matrix
    
    
    def values(self):
        return self.matrix
    

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
                x,y,v,g = cell
                if v == 2:
                    if (i > 0 and j > 0) and (i < shape_res[0] - 1 and j < shape_res[1] - 1):
                        # cv2.line(image, (x,y), (x,y), (0,0,0), 5)
                        lenght = 0
                        if res[i-1][j][2] == 1: # trai
                            lenght += 1
                        if res[i+1][j][2] == 1: # phai
                            lenght += 1
                        if res[i][j-1][2] == 1: # duoi
                            lenght += 1
                        if res[i][j+1][2] == 1: # tren
                            lenght += 1
                        
                        if lenght == 2:
                            self.core90.append([x,y])
                        elif lenght == 3:
                            self.core180.append([x,y])
                        elif lenght == 4:
                            self.core360.append([x,y])
                            
        return self.core90, self.core180, self.core360 
    
    def values(self):
        return self.core90, self.core180, self.core360    