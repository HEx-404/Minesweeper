from tkinter import *
from tkinter import messagebox
import random, sys

width=540
height=594
grid_size=6
mines_count=10
cell_count=grid_size**2
seconds=0

def height_prct(percentage):
  return (height/100)*percentage
def width_prct(percentage):
  return (width/100)*percentage

class Cell:
  cells_left=cell_count
  all=[]
  def __init__(self,x,y,is_mine=False):
    self.is_mine = is_mine
    self.is_opened = False
    self.is_marked = False
    self.cell_btn_obj = None
    self.x = x
    self.y = y

    Cell.all.append(self)
    
  def create_btn(self, location):
    btn = Button(
      location,
      width=8,
      height=4
    )
    btn.bind('<Button-1>', self.left_click)
    btn.bind('<Button-3>', self.right_click)
    self.cell_btn_obj = btn

  def left_click(self,event):
    if self.is_mine:
      self.reveal_mine()
    else:
      if self.surrounded_mines == 0:
        for cell_obj in self.surrounded_cells:
          cell_obj.reveal_cell()
      self.reveal_cell()
      
  def right_click(self,event):
    if not self.is_marked:
      self.cell_btn_obj.configure(bg='orange')
      self.is_marked = True
    else:
      self.cell_btn_obj.configure(bg='SystemButtonFace')
      self.is_marked = False

  def reveal_mine(self):
    self.cell_btn_obj.configure(bg='red')
    self.game_over()
    sys.exit()

  def game_over(self):
    messagebox.showinfo("Game Over","You Clicked on a Mine!")

  def reveal_cell(self):
    if not self.is_opened:
      self.cell_btn_obj.configure(text=f'{self.surrounded_mines}')
      print(self.surrounded_mines)
      self.is_opened = True
      Cell.cells_left -=1

  def get_cell(self,x,y):
    for cell in Cell.all:
      if cell.x == x and cell.y == y:
        return cell
        
  @property
  def surrounded_cells(self):
    surr_cells = [
     self.get_cell(self.x-1,self.y-1),
     self.get_cell(self.x,self.y-1),
     self.get_cell(self.x+1,self.y-1),
     self.get_cell(self.x-1,self.y),
     self.get_cell(self.x+1,self.y),
     self.get_cell(self.x-1,self.y+1),
     self.get_cell(self.x,self.y+1),
     self.get_cell(self.x+1,self.y+1)
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
    mines=random.sample(Cell.all,6)
    print(mines)
    for mine in mines:
      mine.is_mine = True
      
  
  def __repr__(self):
    return f'({self.x},{self.y})'

def update_timer():
  global seconds
  seconds += 1


def main():
  window = Tk()
  window.geometry(f'{width}x{height}')
  window.title("Minesweeper")
  window.configure(bg='#568a35')
  window.resizable(False, False)
  
  top_frame = Frame(window,
                    bg='#4a752d',
                    width=width,
                    height=height_prct(10))
  
  top_frame.place(x=0, y=0)

  timer = Label(top_frame,text="000s", font=('Arial',32),bg='#4a752d',fg='orange')
  timer.place(x=0,y=0)

  centre_frame = Frame(window,
                       bg="black",
                       width=width_prct(75),
                       height=height_prct(75))
  
  centre_frame.place(x=width_prct(12.5), y=height_prct(12.5+5))
  
  for x in range(grid_size):
      for y in range(grid_size):
          c = Cell(x,y)
          c.create_btn(centre_frame)
          c.cell_btn_obj.grid(column=x, row=y)
  
  Cell.create_mines()
  window.mainloop()

if __name__ == '__main__':
 main()