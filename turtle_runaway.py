import tkinter as tk
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50, game_time=60, canvas_width=700, canvas_height=700):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.game_time = game_time  # 게임 제한 시간 (초)
        self.start_time = None  # 게임 시작 시간
        self.score = 0  # 점수
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        # Add a title drawer for the game title
        self.title_drawer = turtle.RawTurtle(canvas)
        self.title_drawer.hideturtle()
        self.title_drawer.penup()

    def draw_title(self):
        """게임 화면 상단에 제목을 표시"""
        self.title_drawer.clear()
        self.title_drawer.setpos(0, self.canvas_height // 2 - 40)
        self.title_drawer.write("너에게 닿기를,,,", align="center", font=("Arial", 24, "bold"))

    def is_catched(self):
        """사용자가 거북이를 잡았는지 확인하는 함수"""
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, ai_timer_msec=100):
        """게임을 시작하는 함수"""
        self.draw_title() # 게임 제목 표시
        self.place_runner()  # 캔버스 안에서 도망자 배치
        self.chaser.setpos(0, 0)  # 추적자는 중앙에서 시작
        self.chaser.setheading(0)

        self.ai_timer_msec = ai_timer_msec
        self.start_time = time.time()  # 게임 시작 시간 기록
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def place_runner(self):
        """도망자(runner)를 캔버스 크기 안에서 랜덤하게 배치"""
        x = random.randint(-self.canvas_width // 2 + 20, self.canvas_width // 2 - 20)
        y = random.randint(-self.canvas_height // 2 + 20, self.canvas_height // 2 - 20)
        self.runner.setpos(x, y)
        self.runner.setheading(random.randint(0, 360))

    def step(self):
        """게임의 한 단계마다 실행되는 함수"""
        elapsed_time = time.time() - self.start_time  # 경과 시간 계산

        if elapsed_time > self.game_time:  # 제한 시간이 지났으면 게임 종료
            self.end_game(f'Time Over! Final Score: {self.score}')
            return

        # 사용자(chaser)가 거북이를 추적하고 도망자(runner)가 움직임
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # 거북이가 잡혔는지 확인
        if self.is_catched():
            self.score += 1  # 점수 증가
            self.place_runner()  # 새 위치에 도망자 배치

        # 상태 업데이트 출력
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Score: {self.score}, Timer: {int(self.game_time - elapsed_time)}', font=("Arial", 16, "normal"))

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def end_game(self, message):
        """게임 종료 시 호출되는 함수"""
        self.drawer.clear()
        self.drawer.setpos(-100, 0)
        self.drawer.write(message, font=("Arial", 24, "bold"))
        self.runner.hideturtle()
        self.chaser.hideturtle()

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10, canvas_width=700, canvas_height=700):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Register event handlers
        canvas.onkeypress(self.move_up, 'Up')
        canvas.onkeypress(self.move_down, 'Down')
        canvas.onkeypress(self.turn_left, 'Left')
        canvas.onkeypress(self.turn_right, 'Right')
        canvas.listen()

    def move_up(self):
        self.forward(self.step_move)
        self.check_boundary()

    def move_down(self):
        self.backward(self.step_move)
        self.check_boundary()

    def turn_left(self):
        self.left(self.step_turn)

    def turn_right(self):
        self.right(self.step_turn)

    def check_boundary(self):
        """추적자가 화면 밖으로 나가지 않도록 경계 체크"""
        x, y = self.pos()

        # 경계 체크: 캔버스 크기 밖으로 나가면 다시 경계 안으로 위치 조정
        if x < -self.canvas_width // 2:
            self.setx(-self.canvas_width // 2)
        elif x > self.canvas_width // 2:
            self.setx(self.canvas_width // 2)

        if y < -self.canvas_height // 2:
            self.sety(-self.canvas_height // 2)
        elif y > self.canvas_height // 2:
            self.sety(self.canvas_height // 2)

    def run_ai(self, opp_pos, opp_heading):
        pass  # 추적자는 사용자가 직접 조작하므로 AI는 필요 없음

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10, canvas_width=700, canvas_height=700):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def run_ai(self, opp_pos, opp_heading):
        """도망자가 화면 밖으로 나가지 않도록 경계 체크"""
        x, y = self.pos()

        # 경계 체크: 캔버스의 크기에서 벗어나지 않도록 제어
        if x < -self.canvas_width // 2 or x > self.canvas_width // 2 or y < -self.canvas_height // 2 or y > self.canvas_height // 2:
            self.setheading(self.towards(0, 0))  # 중심(0, 0) 쪽으로 방향 전환
        else:
            mode = random.randint(0, 2)
            if mode == 0:
                self.forward(self.step_move)
            elif mode == 1:
                self.left(self.step_turn)
            elif mode == 2:
                self.right(self.step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # 사용자가 chaser를 제어, 도망자는 AI가 움직임
    runner = RandomMover(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
