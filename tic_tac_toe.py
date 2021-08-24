import tkinter as tk
from PIL import ImageTk, Image
from T_model import *
import pygame
import sys


class TicTakToe:
    MASSAGES = {"x_turn": "It's X's turn", "O_turn": "It's O's turn", "x_score": "X: ", "O_score": "O: ",
                "total": "Games played so far: "}
    XO_LOCATIONS = {1: [275, 150, True], 2: [425, 150, True], 3: [575, 150, True], 4: [275, 300, True],
                    5: [425, 300, True], 6: [575, 300, True], 7: [275, 450, True], 8: [425, 450, True],
                    9: [575, 450, True]}
    WIN_LOCATIONS = {"r1": [250, 175], "r2": [250, 325], "r3": [250, 475], "c1": [300, 125], "c2": [450, 125],
                     "c3": [600, 125], "d": [275, 150]}

    def __init__(self):
        self.board = Board()
        self.root = tk.Tk()
        self.root.title("Tic-Tak-Toe")
        self.root.resizable(False, False)

        # Main canvas
        self._canvas = tk.Canvas(self.root, width=1000, height=700, highlightbackground="black")
        self.BACKGROUND = Image.open("graphics/background.png")
        self.BACKGROUND = self.BACKGROUND.resize((1000, 700), Image.ANTIALIAS)
        self.BACKGROUND = ImageTk.PhotoImage(self.BACKGROUND)
        self._canvas.create_image(0, 0, image=self.BACKGROUND, anchor="nw")

        self.logo = Image.open("graphics/logo.png")
        self.logo = self.logo.resize((600, 100), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self._canvas.create_image(175, 10, image=self.logo, anchor="nw")

        # Board & Lines
        for x in range(400, 700, 150):
            self._canvas.create_line(x, 125, x, 575, fill="white")
        for y in range(275, 575, 150):
            self._canvas.create_line(250, y, 700, y, fill="white")
        self.BLOCKS = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}

        # X & O
        self.X = Image.open("graphics/x.png")
        self.O = Image.open("graphics/o.png")
        self.X = self.X.resize((100, 100), Image.ANTIALIAS)
        self.O = self.O.resize((100, 100), Image.ANTIALIAS)
        self.X = ImageTk.PhotoImage(self.X)
        self.O = ImageTk.PhotoImage(self.O)

        self.little_x = Image.open("graphics/x.png")
        self.little_o = Image.open("graphics/o.png")
        self.little_x = self.little_x.resize((50, 50), Image.ANTIALIAS)
        self.little_o = self.little_o.resize((50, 50), Image.ANTIALIAS)
        self.little_x = ImageTk.PhotoImage(self.little_x)
        self.little_o = ImageTk.PhotoImage(self.little_o)

        self.turn = self.X
        self.turn_num = 1

        # Management
        self.freeze = False
        self.turn_img = Image.open("graphics/turn.png")
        self.turn_img = self.turn_img.resize((160, 250), Image.ANTIALIAS)
        self.turn_img = ImageTk.PhotoImage(self.turn_img)
        self._canvas.create_image(40, 225, image=self.turn_img, anchor="nw")
        self.turn_display = self._canvas.create_image(70, 325, image=self.little_x, anchor="nw")

        self.music = True
        self.exit_img = Image.open("graphics/exit.png")
        self.exit_img = self.exit_img.resize((30, 30), Image.ANTIALIAS)
        self.exit_img = ImageTk.PhotoImage(self.exit_img)
        self.exit_btn = tk.Button(self.root, image=self.exit_img, command=sys.exit, borderwidth=0)
        self.exit_btn.place(x=5, y=665)
        self.sound_on_img = Image.open("graphics/sound_on.png")
        self.sound_on_img = self.sound_on_img.resize((30, 30), Image.ANTIALIAS)
        self.sound_on_img = ImageTk.PhotoImage(self.sound_on_img)
        self.sound_on_btn = tk.Button(self.root, image=self.sound_on_img, command=self.music_mode, borderwidth=0)
        self.sound_on_btn.place(x=40, y=665)
        self.sound_off_img = Image.open("graphics/sound_off.png")
        self.sound_off_img = self.sound_off_img.resize((30, 30), Image.ANTIALIAS)
        self.sound_off_img = ImageTk.PhotoImage(self.sound_off_img)

        # Score display
        self.score = Score()
        self.score_img = Image.open("graphics/score.png")
        self.score_img = self.score_img.resize((125, 50), Image.ANTIALIAS)
        self.score_img = ImageTk.PhotoImage(self.score_img)
        self._canvas.create_image(800, 175, image=self.score_img, anchor="nw")
        self._canvas.create_image(800, 275, image=self.little_x, anchor="nw")
        self._canvas.create_image(800, 375, image=self.little_o, anchor="nw")
        self.x_score_display = self._canvas.create_text(900, 300, text=self.score.get_x(), fill="white", font=("david", 40))
        self.o_score_display = self._canvas.create_text(900, 400, text=self.score.get_o(), fill="white", font=("david", 40))

        self.reset_score_img = Image.open("graphics/reset_score.png")
        self.reset_score_img = self.reset_score_img.resize((190, 35), Image.ANTIALIAS)
        self.reset_score_img = ImageTk.PhotoImage(self.reset_score_img)
        self.reset_score_btn = tk.Button(self.root, background="#06031F", image=self.reset_score_img, command=self.reset_score, borderwidth=2)
        self.reset_score_btn.config(image=self.reset_score_img)
        self.reset_score_btn.place(x=760, y=480)


        # Game Over
        self.WIN_LINES = {"r1": None, "r2": None, "r3": None, "c1": None, "c2": None, "c3": None, "d1": None, "d2": None}
        self.row_win = Image.open("graphics/r.png")
        self.row_win = self.row_win.resize((450, 50), Image.ANTIALIAS)
        self.row_win = ImageTk.PhotoImage(self.row_win)
        self.col_win = Image.open("graphics/c.png")
        self.col_win = self.col_win.resize((50, 450), Image.ANTIALIAS)
        self.col_win = ImageTk.PhotoImage(self.col_win)
        self.diagonal1_win = Image.open("graphics/d1.png")
        self.diagonal1_win = self.diagonal1_win.resize((400, 400), Image.ANTIALIAS)
        self.diagonal1_win = ImageTk.PhotoImage(self.diagonal1_win)
        self.diagonal2_win = Image.open("graphics/d2.png")
        self.diagonal2_win = self.diagonal2_win.resize((400, 400), Image.ANTIALIAS)
        self.diagonal2_win = ImageTk.PhotoImage(self.diagonal2_win)

        # Reset button
        self.reset = Image.open("graphics/reset.png")
        self.reset = self.reset.resize((150, 50), Image.ANTIALIAS)
        self.reset = ImageTk.PhotoImage(self.reset)
        self.reset_btn = tk.Button(self.root, background="#06031F", image=self.reset, command=self.reset_game, borderwidth=0)
        self.reset_btn.config(image=self.reset)
        self.reset_btn.place(x=397, y=610)

        # self.frame = tk.Frame(self._canvas, height=700, width=1000, bg="green").grid()

        # Music
        pygame.mixer.init()

        self.run()

    def run(self):
        self._canvas.grid()
        self.root.bind('<Button-1>', self.game_management)
        for i in range(1, 10):
            self.root.bind(str(i), self.game_management)
        self.root.mainloop()

    def game_management(self, event):
        if self.freeze:
            return

        if self.place(event):
            if self.music:
                self.play_music()
            self.manage_insertion()

    def play_music(self, win=False):
        pygame.mixer.music.load("sounds/placing.mp3")
        pygame.mixer.music.play()

        if win:
            pygame.mixer.music.load("sounds/win.mp3")
            pygame.mixer.music.play()

    def manage_insertion(self):
        self.change_turn()
        self.change_display_turn()
        if self.handle_game_over(self.board.check_victory()):
            self.freeze = True

    def process_event(self, event):
        if event.char == "1":
            return self.XO_LOCATIONS[7][0], self.XO_LOCATIONS[7][1]
        elif event.char == '2':
            return self.XO_LOCATIONS[8][0], self.XO_LOCATIONS[8][1]
        elif event.char == "3":
            return self.XO_LOCATIONS[9][0], self.XO_LOCATIONS[9][1]
        elif event.char == "4":
            return self.XO_LOCATIONS[4][0], self.XO_LOCATIONS[4][1]
        elif event.char == "5":
            return self.XO_LOCATIONS[5][0], self.XO_LOCATIONS[5][1]
        elif event.char == "6":
            return self.XO_LOCATIONS[6][0], self.XO_LOCATIONS[6][1]
        elif event.char == "7":
            return self.XO_LOCATIONS[1][0], self.XO_LOCATIONS[1][1]
        elif event.char == "8":
            return self.XO_LOCATIONS[2][0], self.XO_LOCATIONS[2][1]
        elif event.char == "9":
            return self.XO_LOCATIONS[3][0], self.XO_LOCATIONS[3][1]

    def place(self, event):
        if event.num != 1:
            x, y = self.process_event(event)
            print(x, y)
        else:
            x, y = event.x, event.y
            # print('{}, {}'.format(x, y))

        if 250 < x < 400 and 125 < y < 275 and self.check_availability(1):
            self.BLOCKS[1] = self._canvas.create_image(self.XO_LOCATIONS[1][0], self.XO_LOCATIONS[1][1], image=self.turn, anchor="nw")
            self.board.insert_value(self.turn_num, [0, 0])
            return True
        elif 400 < x < 550 and 125 < y < 275 and self.check_availability(2):
            self.BLOCKS[2] = self._canvas.create_image(self.XO_LOCATIONS[2][0], self.XO_LOCATIONS[2][1], image=self.turn, anchor="nw")
            self.board.insert_value(self.turn_num, [0, 1])
            return True
        elif 550 < x < 700 and 125 < y < 275 and self.check_availability(3):
            self.BLOCKS[3] = self._canvas.create_image(self.XO_LOCATIONS[3][0], self.XO_LOCATIONS[3][1], image=self.turn, anchor="nw")
            self.board.insert_value(self.turn_num, [0, 2])
            return True
        elif 250 < x < 400 and 275 < y < 425 and self.check_availability(4):
            self.BLOCKS[4] = self._canvas.create_image(self.XO_LOCATIONS[4][0], self.XO_LOCATIONS[4][1], image=self.turn, anchor="nw")
            self.board.insert_value(self.turn_num, [1, 0])
            return True
        elif 400 < x < 550 and 275 < y < 425 and self.check_availability(5):
            self.BLOCKS[5] = self._canvas.create_image(self.XO_LOCATIONS[5][0], self.XO_LOCATIONS[5][1], image=self.turn, anchor="nw")
            self.board.insert_value(self.turn_num, [1, 1])
            return True
        elif 550 < x < 700 and 275 < y < 425 and self.check_availability(6):
            self.BLOCKS[6] = self._canvas.create_image(self.XO_LOCATIONS[6][0], self.XO_LOCATIONS[6][1], image=self.turn, anchor="nw")
            self.board.insert_value(self.turn_num, [1, 2])
            return True
        elif 250 < x < 400 and 425 < y < 575 and self.check_availability(7):
            self.BLOCKS[7] = self._canvas.create_image(self.XO_LOCATIONS[7][0], self.XO_LOCATIONS[7][1], image=self.turn, anchor="nw")
            self.board.insert_value(self.turn_num, [2, 0])
            return True
        elif 400 < x < 550 and 425 < y < 575 and self.check_availability(8):
            self.BLOCKS[8] = self._canvas.create_image(self.XO_LOCATIONS[8][0], self.XO_LOCATIONS[8][1], image=self.turn, anchor="nw")
            self.board.insert_value(self.turn_num, [2, 1])
            return True
        elif 550 < x < 700 and 425 < y < 575 and self.check_availability(9):
            self.BLOCKS[9] = self._canvas.create_image(self.XO_LOCATIONS[9][0], self.XO_LOCATIONS[9][1], image=self.turn, anchor="nw")
            self.board.insert_value(self.turn_num, [2, 2])
            return True

    def handle_game_over(self, direction):
        if not direction:
            return False

        if direction[0] == "r":
            if direction[1] == 1:
                self.WIN_LINES["r1"] = self._canvas.create_image(self.WIN_LOCATIONS["r1"][0],
                                                                 self.WIN_LOCATIONS["r1"][1], image=self.row_win,
                                                                 anchor="nw")
            if direction[1] == 2:
                self.WIN_LINES["r2"] = self._canvas.create_image(self.WIN_LOCATIONS["r2"][0],
                                                                 self.WIN_LOCATIONS["r2"][1], image=self.row_win,
                                                                 anchor="nw")
            if direction[1] == 3:
                self.WIN_LINES["r3"] = self._canvas.create_image(self.WIN_LOCATIONS["r3"][0],
                                                                 self.WIN_LOCATIONS["r3"][1], image=self.row_win,
                                                                 anchor="nw")
        elif direction[0] == "c":
            if direction[1] == 1:
                self.WIN_LINES["c1"] = self._canvas.create_image(self.WIN_LOCATIONS["c1"][0],
                                                                 self.WIN_LOCATIONS["c1"][1], image=self.col_win,
                                                                 anchor="nw")
            if direction[1] == 2:
                self.WIN_LINES["c2"] = self._canvas.create_image(self.WIN_LOCATIONS["c2"][0],
                                                                 self.WIN_LOCATIONS["c2"][1], image=self.col_win,
                                                                 anchor="nw")
            if direction[1] == 3:
                self.WIN_LINES["c3"] = self._canvas.create_image(self.WIN_LOCATIONS["c3"][0],
                                                                 self.WIN_LOCATIONS["c3"][1], image=self.col_win,
                                                                 anchor="nw")
        elif direction[0] == "d1":
            self.WIN_LINES["d1"] = self._canvas.create_image(self.WIN_LOCATIONS["d"][0], self.WIN_LOCATIONS["d"][1],
                                                             image=self.diagonal1_win, anchor="nw")
        elif direction[0] == "d2":
            self.WIN_LINES["d2"] = self._canvas.create_image(self.WIN_LOCATIONS["d"][0], self.WIN_LOCATIONS["d"][1],
                                                             image=self.diagonal2_win, anchor="nw")
        if self.music:
            self.play_music(True)

        self.change_turn()  # Cause the current winner to start the next game.
        self.change_display_turn()

        self.score.add(self.turn_num)
        self.update_score_display()

        return True

    def check_availability(self, num):
        if self.XO_LOCATIONS[num][2]:
            self.XO_LOCATIONS[num][2] = False
            return True
        return False

    def change_turn(self):
        if self.turn == self.X:
            self.turn = self.O
            self.turn_num = -1
        else:
            self.turn = self.X
            self.turn_num = 1

    def change_display_turn(self):
        self._canvas.delete(self.turn_display)
        if self.turn == self.X:
            self.turn_display = self._canvas.create_image(70, 325, image=self.little_x, anchor="nw")
        else:
            self.turn_display = self._canvas.create_image(70, 325, image=self.little_o, anchor="nw")

    def music_mode(self):
        if self.music:
            self.music = False
            self.sound_on_btn.config(image=self.sound_off_img)
        else:
            self.music = True
            self.sound_on_btn.config(image=self.sound_on_img)

    def update_score_display(self):
        self._canvas.delete(self.x_score_display)
        self._canvas.delete(self.o_score_display)
        self.x_score_display = self._canvas.create_text(900, 300, text=self.score.get_x(), fill="white", font=("david", 40))
        self.o_score_display = self._canvas.create_text(900, 400, text=self.score.get_o(), fill="white", font=("david", 40))

    def reset_score(self):
        self.score.reset()
        self.update_score_display()
        if self.freeze:
            self.reset_game()

    def reset_game(self):
        self.freeze = False

        self.board.reset()

        for key in self.BLOCKS.keys():
            self._canvas.delete(self.BLOCKS[key])

        for key in self.WIN_LINES.keys():
            self._canvas.delete(self.WIN_LINES[key])

        for i in range(1, 10):
            self.XO_LOCATIONS[i][2] = True


if __name__ == '__main__':
    new_game = TicTakToe()
