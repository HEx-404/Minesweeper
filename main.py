import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random, sys, os, csv
#from PIL import Image, ImageTk

width = 360
height = 450
grid_size = 8
mines_count = 10
cell_count = grid_size**2
gameRunning = False
timer = 0
app_path = '.'
modes = {
    'easy': ((400, 480), (8, 10)),
    'medium': ((460, 600), (10, 15)),
    'hard': ((720, 720), (15, 20))
}
#app_icon_img0 = Image.open(f'{app_path}/assets/icons/appicon.png')
#app_icon_img = app_icon_img0.resize((60,60))
#flag_img0 = Image.open(f'{app_path}/assets/icons/flag.png')
#flag_img = flag_img0.resize((20,20))

if not os.path.isfile(f'{app_path}/data/leaderboard.csv'):
    os.system('mkdir data')
    with open(f"{app_path}/data/leaderboard.csv", 'w') as file:
        pass


def height_prct(percentage):
    return (height / 100) * percentage


def width_prct(percentage):
    return (width / 100) * percentage


class Cell:
    cells_left = cell_count
    mines_left = mines_count
    all = []

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_marked = False
        self.cell_btn_obj = None
        self.x = x
        self.y = y

        Cell.all.append(self)

    def create_btn(self, location):
        btn = tk.Button(location, width=2, height=2, image='')
        btn.bind('<Button-1>', self.left_click)
        btn.bind('<Button-3>', self.right_click)
        self.cell_btn_obj = btn

    def left_click(self, event):
        global gameRunning, timer
        if self.is_mine:
            self.reveal_mine()
        else:
            self.reveal_cell()
            if Cell.cells_left == mines_count:
                gameRunning = False
                messagebox.showinfo("Game Over",
                                    "Congratulations! You won the game.")

                while True:
                    pname = simpledialog.askstring(title="Minesweeper",
                                                   prompt="What's your Name?:")
                    if pname != '':
                        break
                    else:
                        messagebox.showerror("Invalid", "Please enter name")

                if pname != None:
                    with open(f"{app_path}/data/leaderboard.csv", 'a') as file:
                        cw = csv.writer(file)
                        cw.writerow((pname, f"{timer}s"))
                clear_lb(f'{app_path}/data/leaderboard.csv', 10)
                window.quit()

    def right_click(self, event):
        if not self.is_marked:
            self.cell_btn_obj.configure(bg='orange')
            self.is_marked = True
            Cell.mines_left -= 1
            mines_left_label.configure(text=Cell.mines_left)
        else:
            self.cell_btn_obj.configure(bg='SystemButtonFace')
            self.is_marked = False
            Cell.mines_left += 1
            mines_left_label.configure(text=Cell.mines_left)

    def reveal_mine(self):
        global gameRunning
        gameRunning = False
        self.cell_btn_obj.configure(bg='red')
        for cell in Cell.all:
            cell.cell_btn_obj.unbind('<Button-1>')
            cell.cell_btn_obj.unbind('<Button-3>')
        tksleep(1)
        for cell in Cell.all:
            if cell.is_mine:
                cell.cell_btn_obj.configure(bg='red')
                tksleep(0.2)
        tksleep(2)
        messagebox.showinfo("Game Over", "You Clicked on a Mine!")
        window.quit()
        sys.exit()

    def reveal_cell(self):
        if not self.is_opened:
            self.cell_btn_obj.configure(text=self.surrounded_mines
                                        if self.surrounded_mines != 0 else '',
                                        bg='lightgrey')
            self.is_opened = True
            Cell.cells_left -= 1

            self.cell_btn_obj.unbind('<Button-1>')
            self.cell_btn_obj.unbind('<Button-3>')

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
            self.get_cell(self.x + 1, self.y + 1)
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
        mines = random.sample(Cell.all, mines_count)
        for mine in mines:
            mine.is_mine = True

    def __repr__(self):
        return f'({self.x},{self.y})'


def tksleep(t):
    'emulating time.sleep(seconds)'
    ms = int(t * 1000)
    root = tk._get_default_root('sleep')
    var = tk.IntVar(root)
    root.after(ms, var.set, 1)
    root.wait_variable(var)


def update_timer():
    global gameRunning, timer
    if gameRunning:
        timer += 1
        timer_label['text'] = f"{timer}s"
        window.after(1000, update_timer)
    else:
        window.after(1000, update_timer)


def clear_lb(file, limit):
    with open(file, newline='') as f:
        cr = csv.reader(f)
        res = list(cr)
    if len(res) > limit:
        res.pop(0)
        with open(file, 'w') as f:
            cw = csv.writer(f)
            cw.writerows(res)


def show_lb():
    global gameRunning
    gameRunning = False
    window.withdraw()
    lbwin = tk.Toplevel(window)
    lbwin.title("Leaderboard")
    lbwin.geometry("360x220")
    with open(f'{app_path}/data/leaderboard.csv') as file:
        cr = csv.reader(file)
        lbdata = list(cr)
    table = ttk.Treeview(lbwin, column=("c1", "c2"), show='headings')
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


def select_mode(level, window):
    global width, height, grid_size, mines_count, cell_count
    width = modes[level][0][0]
    height = modes[level][0][1]
    grid_size = modes[level][1][0]
    cell_count = modes[level][1][0]**2
    mines_count = modes[level][1][1]
    Cell.cells_left = cell_count
    Cell.mines_left = mines_count
    window.destroy()

def on_closing(win):
    if messagebox.askokcancel('Quit', "Do you want to quit?"):
        win.destroy()
        sys.exit()


if __name__ == '__main__':
    window = tk.Tk()

    window.withdraw()
    modewin = tk.Toplevel(window)
    modewin.title('Select Level')
    modewin.geometry('200x150')
    modewin.protocol("WM_DELETE_WINDOW", lambda: on_closing(modewin))
    mode_frame = tk.LabelFrame(modewin, text='Select Level')
    mode_frame.pack(expand=True, fill='both')
    easybtn = tk.Button(mode_frame,
                        text='Easy',
                        command=lambda: select_mode('easy', modewin))
    easybtn.pack(pady=5)
    mediumbtn = tk.Button(mode_frame,
                          text='Medium',
                          command=lambda: select_mode('medium', modewin))
    mediumbtn.pack(pady=5)
    hardbtn = tk.Button(mode_frame,
                        text='Hard',
                        command=lambda: select_mode('hard', modewin))
    hardbtn.pack(pady=5)
    window.wait_window(modewin)
    window.deiconify()

    #app_icon = PhotoImage(file=f"{app_path}/appicon.png")
    #flag_icon = PhotoImage(file=f'{app_path}/assets/icons/flag.png')
    #app_icon = ImageTk.PhotoImage(app_icon_img)
    #flag_icon = ImageTk.PhotoImage(flag_img)

    window.geometry(f'{width}x{height}')
    window.title("Minesweeper")
    #window.iconphoto(True, app_icon)
    window.configure(bg='#568a35')
    window.resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))

    top_frame = tk.Frame(window,
                         bg='#4a752d',
                         width=width,
                         height=height_prct(10))
    top_frame.place(relx=0.5, anchor='n')

    title_label = tk.Label(top_frame,
                           text="MINESWEEPER",
                           bg='#4a752d',
                           fg='white',
                           font=('Arial', 28))
    title_label.place(relx=0.5, rely=0.5, anchor='center')

    info_frame = tk.Frame(window,
                          bg='darkgreen',
                          width=width,
                          height=height_prct(8))
    info_frame.place(relx=0.5, rely=0.1, anchor='n')

    timer_label = tk.Label(info_frame,
                           font=('verdana', 12),
                           fg='white',
                           text='00:00:00',
                           width=10,
                           bg='darkgreen')
    timer_label.place(relx=0.5, rely=0.5, anchor='center')

    mines_left_label = tk.Label(info_frame,
                                font=('verdana', 12),
                                fg='white',
                                bg='darkgreen',
                                text=Cell.mines_left)
    mines_left_label.place(relx=0.3, rely=0.5, anchor='center')

    Lb = tk.Button(info_frame, text='Leaderboard', command=show_lb)
    Lb.place(relx=0.8, rely=0.5, anchor='center')

    centre_frame = tk.Frame(window,
                            bg="black",
                            width=width_prct(75),
                            height=height_prct(75))
    centre_frame.place(relx=0.5, rely=0.59, anchor='center')

    for x in range(grid_size):
        for y in range(grid_size):
            c = Cell(x, y)
            c.create_btn(centre_frame)
            c.cell_btn_obj.grid(column=x, row=y)

    Cell.create_mines()

    gameRunning = True
    timer_label['text'] = "0s"
    window.after(1000, update_timer)

    window.mainloop()