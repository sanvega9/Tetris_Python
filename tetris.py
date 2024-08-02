import pygame
import random

#Window size and game block
Screen_Width = 300
Screen_Height = 600
Block_size = 30
Board_width = Screen_Width // Block_size
Board_Height = Screen_Height // Block_size
fps = 20 # increased FPS to make the game faster

#Tetromino shape and colors
SHAPES = [
    [[1,1,1,1]], #I
    [[1,1], [1,1]], #O
    [[1,1,0], [0,1,1]], #s
    [[0,1,1], [0,1,1]], #z
    [[1,1,1], [0,1,0]], #T
    [[1,1,1], [1,0,0]], #l
    [[1,1,1], [0,0,1]] #J
]
COLOR =[
    (0,255,255), #cyan
    (255, 255, 0), #Yellow
    (0,255,0), #Green
    (255,0,0),#RED
    (255,0,255), #Magenta
    (255,165,0), #Orange
    (0,0,255) #Blue
]

class Game_tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Screen_Width,Screen_Height))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = [[0] * Board_width for _ in range(Board_Height)]
        self.gameover= False
        self.teteromino = self.new_teteromino()
        self.next_teteromino = self.new_teteromino()
        self.x, self.y = Board_width //2, 0
        self.fall = 0
        self.score = 0 
        self.level = 1
        self.line_clear = 0

    def new_teteromino(self):
        shape = random.choice(SHAPES)
        color = COLOR[SHAPES.index(shape)]
        return {'shape':shape,'color':color}
    
    def board_line(self):
        self.screen.fill((0,0,0))
        for y in range(Board_Height):
            for x in range(Board_width):
                if self.board[y][x]:
                    pygame.draw.rect(self.screen,COLOR[self.board[y][x] - 1],
                                     (x *Block_size, y*Block_size, Block_size,Block_size))
                    
    def draw_tetromino(self):
        shape = self.teteromino['shape']
        color = self.teteromino['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, color, 
                                     ((self.x + x) * Block_size,(self.y + y)*Block_size,Block_size,Block_size))
    
    def draw_txt(self,text,size,color,x,y):
        font = pygame.font.SysFont("comicsansms",size)
        label = font.render(text,True,color) 
        self.screen.blit(label,(x,y))      

    def check(self,dx,dy):
        shape = self.teteromino['shape']
        for y, row in enumerate(shape):
            for x,cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >=Board_width or new_y >= Board_Height:
                        return True
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return True
        return False
    
    def merge(self):
        shape = self.teteromino['shape']
        color = self.teteromino['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.y + y][self.x + x] = COLOR.index(color) + 1

    def clear_line(self):
        lines_clear = [i for i, row in enumerate(self.board)if all(row)]   
        for i in lines_clear:
            self.board.pop(i)
            self.board.insert(0, [0] * Board_width)
        self.line_clear += len(lines_clear)
        self.score += len(lines_clear) * 100

        if self.line_clear // 10 > self.level - 1:
            self.level += 1
            self.fps = fps+self.level

    def move(self,dx,dy):
        if not self.gameover:
            if not self.check(dx,dy):
                self.x += dx
                self.y += dy
            elif dy:
                self.merge()
                self.clear_line()
                self.teteromino = self.next_teteromino
                self.next_teteromino = self.new_teteromino()
                self.x, self.y = Board_width // 2, 0
                if self.check(0,0):
                    self.gameover=True

    def rotate(self):
        shape = self.teteromino['shape']
        rotate_shape = list(zip(*shape[::-1]))
        K =self.teteromino['shape']
        self.teteromino['shape'] = rotate_shape
        if self.check(0,0):
            self.teteromino['shape'] = K
          

    def run(self):
        while not self.gameover:
            self.fall +=self.clock.get_rawtime()
            self.clock.tick(fps)
            
            self.screen.fill((0,0,0))
            self.board_line()
            self.draw_tetromino()
            self.draw_txt(f"Score: {self.score}", 18,(255,255,255), 10, 10)
            self.draw_txt(f"Level: {self.level}", 18, (255,255,255),10, 40)
            pygame.display.flip()

            if self.fall > 1000 // fps:
                self.move(0,1)
                self.fall = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1,0)
                    if event.key == pygame.K_RIGHT:
                        self.move(1,0)
                    if event.key == pygame.K_DOWN:
                        self.move(0,1)
                    if event.key == pygame.K_UP:
                        self.rotate()
        pygame.quit()  

if __name__ == "__main__":
    game_tetris = Game_tetris()
    game_tetris.run()