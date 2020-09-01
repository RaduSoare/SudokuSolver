from selenium import webdriver
import pyautogui as pg
from selenium.webdriver.common.keys import Keys
import time

# path for webDriver executable
PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)
driver.get("https://grid.websudoku.com/?level=4")

def possible(x, y, n):
    # Checks if n exists in row
    for i in range(0, 9):
        if grid[i][x] == n and i != y:
            return False

    # Checks if n exists in column
    for i in range(0, 9):
        if grid[y][i] == n and i != x:
            return False

    # Hack to check if n exists in box
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for X in range(x0, x0 + 3):
        for Y in range(y0, y0 + 3):
            if grid[Y][X] == n:
                return False
    return True



def readSudokuGrid():

    sudoku_grid = []

    for x in range(9):
        grid_line = []
        for y in range(9):
            cell_path = "f" + str(y) + str(x)
            inp = "input[id*='{}']".format(cell_path)
            # get cell value (x, y) from WebPage Table
            cellValue = driver.find_element_by_css_selector("{}".format(inp)).get_attribute("value")
            if not cellValue:
                cell_value_integer = 0
            else:
                cell_value_integer = int(cellValue)
            grid_line.append(cell_value_integer)
        # creates sudoku grid as a matrix
        sudoku_grid.append(grid_line)
    return  sudoku_grid


grid = readSudokuGrid()

def output_result(matrix):
    for x in range(9):
        for y in range(9):
            cell_path = "f" + str(y) + str(x)
            inp = "input[id*='{}']".format(cell_path)
            target_cell = driver.find_element_by_css_selector("{}".format(inp))
            # insert values in WebSite table
            target_cell.click()
            target_cell.send_keys(str(matrix[x][y]))

    # click submit button
    button_submit = driver.find_element_by_xpath('/html/body/table/tbody/tr/td[3]/table/tbody/tr[2]/td/form/p[4]/input[1]')
    button_submit.click()


def solve():
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(x, y, n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    output_result(grid)

# This is where MAGIC begins
solve()
