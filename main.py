from tkinter import *
from tkinter import messagebox
from datetime import datetime
import random,sys,os,csv

width=360
height=450
grid_size=8
mines_count=8
cell_count=grid_size**2
gameRunning = False
time=''

if not os.path.isfile('leaderboard.csv'):
  with open ("leaderboard.csv",'w',newline='') as file:
    cw = csv.writer(file)
    cw.writerow(("Name","Highscore"))

def height_prct(percentage):
  return (height/100)*percentage
def width_prct(percentage):
  return (width/100)*percentage

class Cell:
  cells_left=cell_count
  mines_left=mines_count
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
      width=4,
      height=2
    )
    btn.bind('<Button-1>', self.left_click)
    btn.bind('<Button-3>', self.right_click)
    self.cell_btn_obj = btn

  def left_click(self,event):
    global gameRunning,time
    if self.is_mine:
      self.reveal_mine()
    else:
      self.reveal_cell()
      if Cell.cells_left == mines_count:
        gameRunning = False
        messagebox.showinfo("Game Over","Congratulations! You won the game.")
        name=input("Enter your name: ")
        with open("leaderboard.csv",'a',newline='') as file:
          cw = csv.writer(file)
          cw.writerow((name,time))
        clear_lb('leaderboard.csv',6)
        with open('leaderboard.csv','r') as file:
          cr=csv.reader(file)
          for i in cr:
            print(f'{i[0]}\t{i[1]}')
        sys.exit()
  
  def right_click(self,event):
    if not self.is_marked:
      self.cell_btn_obj.configure(bg='orange')
      self.is_marked = True
      Cell.mines_left-=1
      mines_left_label.configure(text=Cell.mines_left)
    else:
      self.cell_btn_obj.configure(bg='SystemButtonFace')
      self.is_marked = False
      Cell.mines_left+=1
      mines_left_label.configure(text=Cell.mines_left)
      
  def reveal_mine(self):
    global gameRunning
    gameRunning = False
    self.cell_btn_obj.configure(bg = 'red')
    messagebox.showinfo("Game Over","You Clicked on a Mine!")
    sys.exit()

  def reveal_cell(self):
    if not self.is_opened:
      self.cell_btn_obj.configure(text=self.surrounded_mines if self.surrounded_mines!=0 else '',
                                  bg='lightgrey')
      self.is_opened = True
      Cell.cells_left -=1

      self.cell_btn_obj.unbind('<Button-1>')
      self.cell_btn_obj.unbind('<Button-3>')
      
      if self.surrounded_mines == 0:
        for cell_obj in self.surrounded_cells:
          cell_obj.reveal_cell()

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
    mines=random.sample(Cell.all,mines_count)
    for mine in mines:
      mine.is_mine = True
      
  def __repr__(self):
    return f'({self.x},{self.y})'

def update_timer():
  global gameRunning,time
  if gameRunning:
      now =  datetime.now()
      minutes, seconds = divmod((now - start_time).total_seconds(),60)
      time = f"00:{int(minutes):02}:{round(seconds):02}"
      timer_label['text'] = time
      window.after(1000, update_timer)

def clear_lb(file,limit):
  with open(file,newline='') as f:
    cr = csv.reader(f)
    res = list(cr)
  if len(res)>limit+1:
    res.pop(1)
    with open(file,'w',newline='') as f:
      cw = csv.writer(f)
      cw.writerows(res)

if __name__ == '__main__':
  window = Tk()
  window.geometry(f'{width}x{height}')
  window.title("Minesweeper")
  window.configure(bg='#568a35')
  window.resizable(False, False)
  
  top_frame = Frame(window,
                    bg='#4a752d',
                    width=width,
                    height=height_prct(10))
  top_frame.place(relx=0.5,anchor=N)

  title_label = Label(top_frame,
                      text="MINESWEEPER",
                      bg='#4a752d',
                      fg='white',
                      font=('Arial',28))
  title_label.place(relx=0.5,rely=0.5,anchor=CENTER)

  info_frame = Frame(
    window,
    bg='darkgreen',
    width=width,
    height=height_prct(8))
  info_frame.place(relx=0.5,rely=0.1,anchor=N)

  timer_label = Label(info_frame, font=('verdana', 12), 
  fg='white',text='00:00:00', width=10, bg='darkgreen')
  timer_label.place(relx=0.6,rely=0.5,anchor=CENTER)

  mines_left_label = Label(info_frame,font=('verdana', 12), fg='white',
  bg='darkgreen',text=Cell.mines_left)
  mines_left_label.place(relx=0.3,rely=0.5,anchor=CENTER)

  centre_frame = Frame(window,
                       bg="black",
                       width=width_prct(75),
                       height=height_prct(75))
  centre_frame.place(relx=0.5,rely=0.59,anchor=CENTER)
  
  for x in range(grid_size):
      for y in range(grid_size):
          c = Cell(x,y)
          c.create_btn(centre_frame)
          c.cell_btn_obj.grid(column=x, row=y)
  
  Cell.create_mines()

  gameRunning = True
  start_time = datetime.now()
  timer_label['text'] = '00:00:00'
  window.after(1000,update_timer)
	
  window.mainloop()