from tkinter import *
import settings, utils
from cell import Cell

window = Tk()
window.geometry(f'{settings.width}x{settings.height}')
window.title("Minesweeper")
window.configure(bg='#568a35')
window.resizable(False, False)

top_frame = Frame(window,
                  bg='#4a752d',
                  width=settings.width,
                  height=utils.height_prct(10))

top_frame.place(x=0, y=0)

centre_frame = Frame(window,
                     bg="black",
                     width=utils.width_prct(75),
                     height=utils.height_prct(75))

centre_frame.place(x=utils.width_prct(12.5), y=utils.height_prct(12.5+5))

for x in range(settings.grid_size):
    for y in range(settings.grid_size):
        c = Cell(x,y)
        c.create_btn(centre_frame)
        c.cell_btn_obj.grid(column=x, row=y)

Cell.create_mines()
window.mainloop()
