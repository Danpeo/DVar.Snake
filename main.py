import raylibpy as rl
from raylibpy import Vector2
from collections import deque

yellow_clr = rl.Color(255, 212, 73, 255)
black_clr = rl.Color(10, 9, 8, 255)
brightred_clr = rl.Color(239, 35, 60, 255)

cell_size = 30
cell_count = 25
offset = 75

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
        self.check_snake_collision_with_tail()
        
        
    def check_snake_collision_with_food(self):
        if rl.vector2_equals(self.snake.body[0], self.food.position):
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            
    def check_snake_collision_with_bounds(self):
        if self.snake.body[0].x < 0 or self.snake.body[0].x >= cell_count or self.snake.body[0].y < 0 or self.snake.body[0].y >= cell_count:
            self.game_over()
            
    def check_snake_collision_with_tail(self):
        for i in range(1, len(self.snake.body)):
            if rl.vector2_equals(self.snake.body[0], self.snake.body[i]):
                self.game_over()
                break

            
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
            rl.draw_rectangle(offset + x * cell_size, offset + y * cell_size, cell_size, cell_size, black_clr)
            
    def update(self):
        self.body.appendleft(rl.vector2_add(self.body[0], self.direction))
        if self.add_segment:
            self.add_segment = False
        else:
            self.body.pop()
            
    def initialize(self):
        self.body = deque([Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)])
        self.direction = Vector2(1, 0)
    


class Food:
    def __init__(self, snakeBody: deque[Vector2]):
        self.position = self.generate_random_pos(snakeBody)
        
    def draw(self):
        body = rl.Rectangle(offset + self.position.x * cell_size, offset + self.position.y * cell_size, cell_size, cell_size)
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
    screen_size = 2 * offset + cell_size * cell_count
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
        rl.draw_rectangle_lines_ex(rl.Rectangle(offset - 5, offset - 5, cell_size * cell_count + 10, cell_size * cell_count + 10), 5, black_clr)
        rl.draw_text("SNAKE", offset - 5, 20, 40, brightred_clr);

        game.draw()
        
        rl.end_drawing()
    
    rl.close_window()
    
if __name__ == "__main__":
    main()
