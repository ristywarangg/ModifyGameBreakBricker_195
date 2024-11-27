import tkinter as tk
import random
import pygame


class GameObject(object): #Kelas induk dasar untuk semua objek dalam game (bola, paddle, brick, dll.).
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)

class Ball(GameObject): #Mengelola logika bola, termasuk gerakan, arah, kecepatan, dan interaksi dengan objek lain.
    def __init__(self, x, y):
        self.radius = 10
        self.direction[1, -1]
        self.speed = 5
        item = canvas.create_oval(x - self.radius. y- self.radius,
                                      x + self.radius, y + self.radious,
                                      fill='red')
        super(Ball, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y) 
    
    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()
            if isinstance(game_object, PowerUp):
                game_object.activate(self.canvas.master)

class Paddle(GameObject): #Mengontrol paddle yang digunakan untuk memantulkan bola.
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='blue')
        super(Paddle, self).__init__(canvas, item)
    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)

class Brick(GameObject): #Mewakili setiap brick yang harus dihancurkan oleh bola.
    COLORS = {1: 'green', 2: 'orange', 3: 'yellow'}

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        self.hits = hits
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            if random.randint(1, 5) == 1:  # 20% chance for power-up
                power_up = PowerUp(self.canvas, self.get_position()[0], self.get_position()[1])
                self.canvas.master.items[power_up.item] = power_up
            self.delete()
            self.canvas.master.update_score(100)
        else:
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])

class PowerUp(GameObject): #Mewakili item power-up yang dapat memberikan efek khusus (misalnya, menambah nyawa).
    def __init__(self, canvas, x, y):
        self.width = 20
        self.height = 20
        item = canvas.create_oval(x - self.width / 2, y - self.height / 2,
                                  x + self.width / 2, y + self.height / 2,
                                  fill='gold', tags='powerup')
        super(PowerUp, self).__init__(canvas, item)

    def activate(self, game):
        game.lives += 1
        game.update_lives_text()
        self.delete()

class Game(tk.Frame):#Mengelola seluruh logika dan antarmuka permainan, termasuk kontrol pemain, level, skor, dan loop permainan.
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3
        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg='black',
                                width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self.score = 0
        self.level = 1

        self.paddle = Paddle(self.canvas, self.width / 2, 326)
        self.items[self.paddle.item] = self.paddle
        self.setup_level()

        self.hud = None
        self.score_hud = None
        self.setup_game()
        self.canvas.focus_set()
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(10))

    def setup_game(self):
        self.add_ball()
        self.update_lives_text()
        self.update_score_text()
        self.text = self.draw_text(300, 200, f'Press Space to start Level {self.level}')
        self.canvas.bind('<space>', lambda _: self.start_game())

    def setup_level(self):
        for x in range(5, self.width - 5, 75):
            self.add_brick(x + 37.5, 50, 3)
            self.add_brick(x + 37.5, 70, 2)
            self.add_brick(x + 37.5, 90, 1)

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def draw_text(self, x, y, text, size='40'):
        font = ('Forte', size)
        return self.canvas.create_text(x, y, text=text, font=font, fill='white')

    def update_lives_text(self):
        text = f'Lives: {self.lives}'
        if self.hud is None:
            self.hud = self.draw_text(50, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def update_score_text(self):
        text = f'Score: {self.score}'
        if self.score_hud is None:
            self.score_hud = self.draw_text(550, 20, text, 15)
        else:
            self.canvas.itemconfig(self.score_hud, text=text)

    def update_score(self, points):
        self.score += points
        self.update_score_text()

    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.level += 1
            self.ball.speed += 2
            self.setup_level()
            self.setup_game()
        elif self.ball.get_position()[3] >= self.height:
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, 'Game Over! You Lose!')
            else:
                self.setup_game()
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.play(-1)

    root = tk.Tk()
    root.title('Break Bricker - Modifikasi')
    game = Game(root)
    game.mainloop()