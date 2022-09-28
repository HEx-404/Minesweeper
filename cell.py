from tkinter import Button
import random

class Cell:
  all=[]
  def __init__(self,x,y,is_mine=False):
    self.is_mine = is_mine
    self.cell_btn_obj = None
    self.x = x
    self.y = y

    Cell.all.append(self)
    
  def create_btn(self, location):
    btn = Button(
      location,
      width=3,
      height=3
    )
    btn.bind('<Button-1>', self.left_click)
    btn.bind('<Button-3>', self.right_click)
    self.cell_btn_obj = btn

  def left_click(self,event):
    if self.is_mine:
     self.cell_btn_obj.configure(bg='red')
    else:
      self.cell_btn_obj.configure(text=f'{self.surrounded_mines}')
      print(self.surrounded_mines)
    
  def right_click(self,event):
    print("DyHoEr")
    print(self.y)

  def reveal_mine(self):
    pass

  def reveal_cell():
    pass

  def get_cell(self,x,y):
    for cell in Cell.all:
      if cell.x == x and cell.y == y:
        return cell
        
  @property
  def surrounded_cells(self):
   cells = [
     self.get_cell(self.x-1,self.y-1),
     self.get_cell(self.x,self.y-1),
     self.get_cell(self.x+1,self.y-1),
     self.get_cell(self.x-1,self.y),
     self.get_cell(self.x+1,self.y),
     self.get_cell(self.x-1,self.y+1),
     self.get_cell(self.x,self.y+1),
     self.get_cell(self.x+1,self.y+1)
   ]
    

  @property
  def surrounded_mines(self):
    mines_nearby = 0
    for cell in Cell.all:
      if cell.x in [self.x-1,self.x,self.x+1] and cell.y in [self.y-1,self.y,self.y+1]:
        print(cell)
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
    