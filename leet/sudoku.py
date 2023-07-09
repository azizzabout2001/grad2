class Solution(object):
    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: None Do not return anything, modify board in-place instead.
        """
        Row = []
        Column =[]
        Box =[]
        rows=[]
        columns=[]
        boxes=[]
        slices =[]
        slices.append([])
        slices.append([])
        slices.append([])

        for row in board:
            rows.append(row)
            
        
        for i in range(0,9):
            columns.append([])
            for row in rows :
                columns[i].append(row[i])
            
        for row in rows:
            
            for i in range(0,9) :
                if i in range (0,3) :
                    slices[0].append(row[i])
                elif i in range (3,6) :
                    slices[1].append(row[i])
                else :
                    slices[2].append(row[i])
                        

        chunked_list = list()
        chunk_size = 3
        for slice in slices :
            for i in range(0, len(slice), 9):
                chunked_list.append(slice[i:i+9])

        print(chunked_list)
        for row in board:
            for num in row :
                if num == '.':
                    if 



