import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage, ttk
import random, sys, os, csv

WIDTH = 360
HEIGHT = 450
GRID_SIZE = 8
MINES_COUNT = 8
CELL_COUNT = GRID_SIZE**2
gameRunning = False
time = 0
app_path = "."


if not os.path.isfile(f"{app_path}/leaderboard.csv"):
    with open(f"{app_path}/leaderboard.csv", "w", newline="") as file:
        pass


def height_prct(percentage):
    return (HEIGHT / 100) * percentage

def width_prct(percentage):
    return (WIDTH / 100) * percentage


class Cell:
    cells_left = CELL_COUNT
    mines_left = MINES_COUNT
    all = []

    def __init__(self, x, y):
        self.is_mine = False
        self.is_opened = False
        self.is_marked = False
        self.x = x
        self.y = y

        Cell.all.append(self)

    def create_btn(self, location):
        btn = tk.Button(location, width=4, height=2)
        btn.bind("<Button-1>", self.left_click)
        btn.bind("<Button-3>", self.right_click)
        self.cell_btn_obj = btn

    def left_click(self, event):
        global gameRunning, time
        if self.is_mine:
            self.reveal_mine()
        else:
            self.reveal_cell()
            if Cell.cells_left == MINES_COUNT:
                gameRunning = False
                messagebox.showinfo("Game Over", "Congratulations! You won the game.")

                write_lb()
                sys.exit()

    def right_click(self, event):
        if not self.is_marked:
            self.cell_btn_obj.configure(bg="orange")
            self.is_marked = True
            Cell.mines_left -= 1
            mines_left_label.configure(text=Cell.mines_left)
        else:
            self.cell_btn_obj.configure(bg="SystemButtonFace")
            self.is_marked = False
            Cell.mines_left += 1
            mines_left_label.configure(text=Cell.mines_left)

    def reveal_mine(self):
        global gameRunning
        gameRunning = False
        self.cell_btn_obj.configure(bg="red")
        messagebox.showinfo("Game Over", "You Clicked on a Mine!")
        sys.exit()

    def reveal_cell(self):
        if not self.is_opened:
            self.cell_btn_obj.configure(
                text=self.surrounded_mines if self.surrounded_mines != 0 else "",
                bg="lightgrey",
            )
            self.is_opened = True
            Cell.cells_left -= 1

            self.cell_btn_obj.unbind("<Button-1>")
            self.cell_btn_obj.unbind("<Button-3>")

            if self.surrounded_mines == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.reveal_cell()

    def get_cell(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        surr_cells = [
            self.get_cell(self.x - 1, self.y - 1),
            self.get_cell(self.x, self.y - 1),
            self.get_cell(self.x + 1, self.y - 1),
            self.get_cell(self.x - 1, self.y),
            self.get_cell(self.x + 1, self.y),
            self.get_cell(self.x - 1, self.y + 1),
            self.get_cell(self.x, self.y + 1),
            self.get_cell(self.x + 1, self.y + 1),
        ]
        surr_cells = [cell for cell in surr_cells if cell is not None]
        return surr_cells

    @property
    def surrounded_mines(self):
        mines_nearby = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                mines_nearby += 1
        return mines_nearby

    @staticmethod
    def create_mines():
        mines = random.sample(Cell.all, MINES_COUNT)
        for mine in mines:
            mine.is_mine = True

    def __repr__(self):
        return f"({self.x},{self.y})"


def update_timer():
    global gameRunning, time
    if gameRunning:
        time += 1
        timer_label["text"] = f"{time}s"
        window.after(1000, update_timer)
    else:
        window.after(1000, update_timer)


def write_lb():
    while True:
        pname = simpledialog.askstring(title="Minesweeper", prompt="What's your Name?:")
        if pname != "":
            break
        else:
            messagebox.showerror("Invalid", "Please enter name")

    if pname != None:
        with open(f"{app_path}/leaderboard.csv", "a", newline="") as file:
            cw = csv.writer(file)
            cw.writerow((pname, f"{time}s"))
    clear_lb(f"{app_path}/leaderboard.csv", 10)


def clear_lb(file, limit):
    with open(file) as f:
        cr = csv.reader(f)
        res = list(cr)
    if len(res) > limit:
        res.pop(0)
        with open(file, "w", newline="") as f:
            cw = csv.writer(f)
            cw.writerows(res)


def show_lb():
    global gameRunning
    gameRunning = False
    window.withdraw()
    lbwin = tk.Toplevel(window)
    lbwin.title("Leaderboard")
    lbwin.geometry("360x220")
    with open(f"{app_path}/leaderboard.csv") as file:
        cr = csv.reader(file)
        lbdata = list(cr)
    table = ttk.Treeview(lbwin, columns=("c1", "c2"), show="headings")
    table.column("#1", anchor=tk.CENTER)
    table.heading("#1", text="Name")
    table.column("#2", anchor=tk.CENTER)
    table.heading("#2", text="Highscore")
    table.pack()
    for row in lbdata:
        table.insert("", tk.END, values=row)

    window.wait_window(lbwin)
    window.deiconify()
    gameRunning = True


if __name__ == "__main__":
    window = tk.Tk()
    window.geometry(f"{WIDTH}x{HEIGHT}")
    window.title("Minesweeper")

    app_icon = PhotoImage(file=f"{app_path}/appicon.png")
    window.iconphoto(True, app_icon)

    window.configure(bg="#568a35")
    window.resizable(False, False)

    top_frame = tk.Frame(window, bg="#4a752d", width=WIDTH, height=height_prct(10))
    top_frame.place(relx=0.5, anchor="n")

    title_label = tk.Label(
        top_frame, text="MINESWEEPER", bg="#4a752d", fg="white", font=("Arial", 28)
    )
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    info_frame = tk.Frame(window, bg="darkgreen", width=WIDTH, height=height_prct(8))
    info_frame.place(relx=0.5, rely=0.1, anchor="n")

    timer_label = tk.Label(
        info_frame,
        font=("verdana", 12),
        fg="white",
        text="00:00:00",
        width=10,
        bg="darkgreen",
    )
    timer_label.place(relx=0.5, rely=0.5, anchor="center")

    mines_left_label = tk.Label(
        info_frame,
        font=("verdana", 12),
        fg="white",
        bg="darkgreen",
        text=Cell.mines_left,
    )
    mines_left_label.place(relx=0.3, rely=0.5, anchor="center")

    Lb = tk.Button(
        info_frame,
        text="Leaderboard",
        command=show_lb,
    )
    Lb.place(relx=0.8, rely=0.5, anchor="center")

    centre_frame = tk.Frame(
        window, bg="black", width=width_prct(75), height=height_prct(75)
    )
    centre_frame.place(relx=0.5, rely=0.59, anchor="center")

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            c = Cell(x, y)
            c.create_btn(centre_frame)
            c.cell_btn_obj.grid(column=x, row=y)

    Cell.create_mines()

    gameRunning = True
    timer_label["text"] = "0s"
    window.after(1000, update_timer)

    window.mainloop()