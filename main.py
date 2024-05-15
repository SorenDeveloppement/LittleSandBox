import pyxel as p
import random


class Element: pass


class ElementType:
    AIR: int = 0
    LAND: int = 1
    LIQUID: int = 2
    UNMOVABLE: int = 3


class GameGrid:
    def __init__(self, cell_size: int, window_size) -> None:
        self.cell_size: int = cell_size
        self.window_size: int = window_size
        
        self.__grid: list[list[Element]] = [[Element(x, y, ElementType.AIR, self) for x in range(self.window_size // self.cell_size)] for y in range(self.window_size // self.cell_size)]
        
    def add_element(self, x: int, y: int, elem_type: ElementType) -> None:
        self.__grid[y][x] = Element(x, y, elem_type, self)
        
    def move_element(self, x: int, y: int, new_x: int, new_y: int) -> None:
        if not self.__grid[new_y][new_x] == 0:
            self.__grid[y][x], self.__grid[new_y][new_x] = self.__grid[new_y][new_x], self.__grid[y][x]
    
    def is_empty(self, x: int, y: int) -> bool:
        max_range: int = self.window_size // self.cell_size - 1
        if 0 <= x <= max_range and 0 <= y <= max_range:
            return self.__grid[y][x].get_type() == ElementType.AIR
        return False
    
    def is_liquid(self, x: int, y: int) -> bool:
        max_range: int = self.window_size // self.cell_size - 1
        if 0 <= x <= max_range and 0 <= y <= max_range:
            return self.__grid[y][x].get_type() == ElementType.LIQUID
        return False
    
    def get_cell_size(self) -> int:
        return self.cell_size
    
    def get_window_size(self) -> int:
        return self.window_size
    
    def get_grid(self) -> list[list[Element]]:
        return self.__grid.copy()
    
    def get_element_at(self, x: int, y: int) -> Element:
        return self.__grid[y][x]
    
    
class Element:
    def __init__(self, x: int, y: int, elem_type: ElementType, grid: GameGrid) -> None:
        self.x: int = x
        self.y: int = y
        self.type: ElementType = elem_type
        self.grid: GameGrid = grid
        
    def fall(self) -> None:
        if self.type == ElementType.UNMOVABLE:
            return
        
        max_range: int = self.grid.get_window_size() // self.grid.get_cell_size()
        if self.y < max_range:
            d: int = random.choice([-1, 1])
            if self.grid.is_empty(self.x, self.y + 1):
                self.grid.move_element(self.x, self.y, self.x, self.y + 1)
                self.y += 1
                return
            elif self.grid.is_empty(self.x + d, self.y + 1):
                self.grid.move_element(self.x, self.y, self.x + d, self.y + 1)
                self.y += 1
                self.x += d
                return
            elif self.grid.is_empty(self.x - d, self.y + 1):
                self.grid.move_element(self.x, self.y, self.x - d, self.y + 1)
                self.y += 1
                self.x -= d
                return
            
            if self.type == ElementType.LIQUID:
                if self.grid.is_empty(self.x + d, self.y):
                    self.grid.move_element(self.x, self.y, self.x + d, self.y)
                    self.x += d
                    return
                elif self.grid.is_empty(self.x - d, self.y):
                    self.grid.move_element(self.x, self.y, self.x - d, self.y)
                    self.x -= d
                    return
                
    def reset_height(self, other_element: Element) -> None:
        self.y = other_element.get_y() - self.y
            
    def get_type(self) -> ElementType:
        return self.type
    
    def get_x(self) -> int:
        return self.x
    
    def get_y(self) -> int:
        return self.y


class App:
    def __init__(self, side_length: int, cell_size: int) -> None:
        self.side_length: int = side_length
        self.cell_size: int = cell_size
        
        self.__game_grid: GameGrid = GameGrid(self.cell_size, self.side_length)
        
        p.init(self.side_length, self.side_length, "App To Learn Pyxel", 120, p.KEY_ESCAPE)
        # Set mouse visible
        p.mouse(True)
        # Run the game loop
        p.run(self.update, self.draw)
        
    def update(self) -> None:
        if p.btn(p.KEY_E) and p.btn(p.MOUSE_BUTTON_LEFT):
            self.__game_grid.add_element(
                p.mouse_x // self.__game_grid.get_cell_size(),
                p.mouse_y // self.__game_grid.get_cell_size(),
                ElementType.AIR
            )
            return
        
        if p.btnp(p.MOUSE_BUTTON_MIDDLE, 30, 60):
            self.__game_grid.add_element(
                p.mouse_x // self.__game_grid.get_cell_size(),
                p.mouse_y // self.__game_grid.get_cell_size(),
                ElementType.LAND
            )
        elif p.btn(p.MOUSE_BUTTON_RIGHT):
            self.__game_grid.add_element(
                p.mouse_x // self.__game_grid.get_cell_size(),
                p.mouse_y // self.__game_grid.get_cell_size(),
                ElementType.LIQUID
            )
        elif p.btnp(p.MOUSE_BUTTON_LEFT, 30, 60):
            self.__game_grid.add_element(
                p.mouse_x // self.__game_grid.get_cell_size(),
                p.mouse_y // self.__game_grid.get_cell_size(),
                ElementType.UNMOVABLE
            )

        i: int = 0
        if i == 0:
            grid: list[list[Element]] = self.__game_grid.get_grid()
            grid.reverse()  # Reverse the grid to avoid the infinite fall of all elements
            for line in grid:
                for elem in line:
                    elem.fall()
        i = (i + 1) if i != 5 else 0
        
    def draw(self) -> None:
        p.cls(p.COLOR_BLACK)
        
        for y, line in enumerate(self.__game_grid.get_grid()):
            for x, elem in enumerate(line):
                if elem.get_type() == ElementType.LAND:
                    p.rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, p.COLOR_YELLOW)
                elif elem.get_type() == ElementType.LIQUID:
                    p.rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, p.COLOR_DARK_BLUE)
                elif elem.get_type() == ElementType.UNMOVABLE:
                    p.rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, p.COLOR_WHITE)
                    
        
if __name__ == "__main__":
    app: App = App(800, 20)