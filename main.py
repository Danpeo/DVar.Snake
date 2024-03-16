import raylibpy as rl
from raylibpy import Vector2
from collections import deque

yellow_clr = rl.Color(255, 212, 73, 255)
black_clr = rl.Color(10, 9, 8, 255)
brightred_clr = rl.Color(239, 35, 60, 255)

cell_size = 30
cell_count = 25

def is_in_deque(element: rl.Vector2, deque: deque[Vector2]) -> bool:
    for i in deque:
        if rl.vector2_equals(element, i):
            return True
    return False


class CountdownTimer:
    def __init__(self) -> None:
        self.last_update_time = 0.0
    
    def event_triggered(self, interval: float) -> bool:
        curr_time = rl.get_time()
        if curr_time - self.last_update_time >= interval:
            self.last_update_time = curr_time
            return True
        return False        


class Game:
    def __init__(self) -> None:
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.is_running = True
        
    def draw(self):
        self.snake.draw()
        self.food.draw()
        
    def update(self):
        if not self.is_running: return
        self.snake.update()
        self.check_snake_collision_with_food()
        self.check_snake_collision_with_bounds()
        
    def check_snake_collision_with_food(self):
        if rl.vector2_equals(self.snake.body[0], self.food.position):
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            
    def check_snake_collision_with_bounds(self):
        if self.snake.body[0].x < 0 or self.snake.body[0].x >= cell_count or self.snake.body[0].y < 0 or self.snake.body[0].y >= cell_count:
            self.game_over()
            
    def game_over(self):
        self.snake.initialize()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.is_running = False
        
class Snake:
    def __init__(self) -> None:
        self.initialize()
        self.add_segment = False
        
    def draw(self):
        for i in range(len(self.body)):
            x = self.body[i].x
            y = self.body[i].y
            rl.draw_rectangle(x * cell_size, y * cell_size, cell_size, cell_size, black_clr)
            
    def update(self):
        self.body.appendleft(rl.vector2_add(self.body[0], self.direction))
        if self.add_segment:
            self.add_segment = False
        else:
            self.body.pop()
            
    def initialize(self):
        self.body = self.set_init_pos()
        self.direction = Vector2(1, 0)
    
    def set_init_pos(self):
        x = cell_count/2
        y = cell_count/2
        return deque([Vector2(x, y), Vector2(x-1, y), Vector2(x-2, y)])

class Food:
    def __init__(self, snakeBody: deque[Vector2]):
        self.position = self.generate_random_pos(snakeBody)
        
    def draw(self):
        body = rl.Rectangle(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        rl.draw_rectangle_rounded(body, 0.5, 1, brightred_clr)
        
    def generate_random_pos(self, snakeBody: deque[Vector2]) -> rl.Vector2:
        def generate_random_cell():
            x = rl.get_random_value(0, cell_count - 1)
            y = rl.get_random_value(0, cell_count - 1)
            return Vector2(x, y)
        
        pos = generate_random_cell()
        while is_in_deque(pos, snakeBody):
            pos = generate_random_cell()  
        return pos

def main():
    screen_size = cell_size * cell_count
    rl.init_window(screen_size, screen_size, "SNAKE THE GAME")
    rl.set_target_fps(60)
    
    game = Game()
    countdown = CountdownTimer()
    
    while not rl.window_should_close():
        rl.begin_drawing()
        
        if countdown.event_triggered(0.2):
            game.update()
            
        if rl.is_key_pressed(rl.KEY_SPACE):
            game.is_running = not game.is_running
            
        
        if rl.is_key_pressed(rl.KEY_UP) and game.snake.direction.y != 1:
            game.snake.direction = rl.Vector2(0, -1)
        
        if rl.is_key_pressed(rl.KEY_DOWN) and game.snake.direction.y != -1:
            game.snake.direction = rl.Vector2(0, 1)
        
        if rl.is_key_pressed(rl.KEY_LEFT) and game.snake.direction.x != 1:
            game.snake.direction = rl.Vector2(-1, 0)
            
        if rl.is_key_pressed(rl.KEY_RIGHT) and game.snake.direction.x != -1:
            game.snake.direction = rl.Vector2(1, 0)
        
        
        rl.clear_background(yellow_clr)
        
        game.draw()
        
        rl.end_drawing()
    
    rl.close_window()
    
if __name__ == "__main__":
    main()
