#!/usr/bin/env python3

##########################################
#
#    Recoded by Eugene Cormier
#     July 2015
#
##########################################


### IMPORTS ###
import curses
import os
import ast


### FUNCTIONS ###

def initialize(myscreen):
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)
  myscreen.keypad(True)
  curses.start_color()
  curses.use_default_colors()
  ### COLOR PAIRS ###
  # -1 means transparent
  curses.init_pair(1, curses.COLOR_YELLOW, -1)
  curses.init_pair(2, curses.COLOR_WHITE, -1)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

def drawscreen(myscreen,rows,tasks,var,temp):
  # var: 0=no enum, 1=enumerated categories, 2=enumerated items
  # start up curses window with borders and headers/footers
  myscreen.clear()
  #  ║═
  myscreen.border(0,0,0,0,0,0,0,0)
  myscreen.addstr(0, 1, " ectodo v2 ", curses.color_pair(1) | curses.A_BOLD)
  myscreen.addstr(int(rows)-1, 1, " options: nc=new category, dc=delete category, ni=new item, di=delete item, q=quit ", curses.color_pair(1) | curses.A_BOLD)
  # draw categories/items with categories numbered
  sortedkeys = sorted(tasks.keys())
  line = 2
  startpos = 5
  if var == 1 or var == 2:
    enum = 1
  for i in sortedkeys:
    line = line + 1
    if line == int(rows) - 3:
      line = 3
      startpos = 90
    if var == 1:
      myscreen.addstr(line, startpos - 2, str(enum), curses.color_pair(2))
      enum = enum + 1
    myscreen.addstr(line, startpos, "┌", curses.color_pair(2))
    myscreen.addstr(line, startpos + 2, i, curses.color_pair(2) | curses.A_BOLD )
    myscreen.refresh()
    for j in sorted(tasks[i]):
      line = line + 1
      if line == int(rows) - 3:
        line = 3
        startpos = 90
      if j != sorted(tasks[i])[-1]:
        myscreen.addstr(line, startpos, "├─", curses.color_pair(2))
        myscreen.addstr(line, startpos + 3, j)
        if var == 2:
          if i == sortedkeys[int(temp)-1]:
            myscreen.addstr(line, startpos - 2, str(enum), curses.color_pair(2))
            enum = enum + 1
      else:
        myscreen.addstr(line, startpos, "└─", curses.color_pair(2))
        myscreen.addstr(line, startpos + 3, j)
        if var == 2:
          if i == sortedkeys[int(temp)-1]:
            myscreen.addstr(line, startpos - 2, str(enum), curses.color_pair(2))
            enum = enum + 1
    line = line + 1
    if line == int(rows) - 3:
      line = 2
      startpos = 90
  myscreen.refresh()

def killscreen(myscreen):
  curses.nocbreak()
  myscreen.keypad(False)
  curses.echo()
  curses.endwin()

def menu(myscreen,res,tasks,rows,taskfile):
  loop = True
  while loop == True:
    drawscreen(myscreen,rows,tasks,0,0)
    res = myscreen.getch()
    # New
    if res == 110:
      myscreen.addstr(int(rows)-2, 1, " NEW: ", curses.color_pair(2))
      myscreen.refresh()
      resb = myscreen.getch()
      # New Category
      if resb == 99:
        createcategory(tasks,myscreen,rows,taskfile)
        continue
      # New Item
      elif resb == 105:
        createitem(tasks,myscreen,rows,taskfile)
        continue
    # Delete
    elif res == 100:
      myscreen.addstr(int(rows)-2, 1, " DEL: ", curses.color_pair(2))
      myscreen.refresh()
      resb = myscreen.getch()
      # Delete Category
      if resb == 99:
        delcategory(tasks,myscreen,rows,taskfile)
        continue
      # Delete item
      if resb == 105:
        delitem(tasks,myscreen,rows,taskfile)
        continue
    # Quit
    elif res == 113:
      break

def readtasks(taskfile):
  f = open(taskfile, 'r')
  return f.readline()
  f.close()

def writetasks(taskfile,tasks):
  f = open(taskfile, 'w')
  f.write(str(tasks))
  f.close()

def createcategory(tasks,myscreen,rows,taskfile):
  myscreen.addstr(int(rows)-2, 1, " NEW CATEGORY: ", curses.color_pair(2))
  myscreen.refresh()
  curses.echo()
  curses.curs_set(1)
  catname = myscreen.getstr(int(rows)-2, 16)
  curses.noecho()
  curses.curs_set(0)
  cattemp = str(catname)
  tasks[cattemp[2:-1]] = [ ]
  writetasks(taskfile,tasks)

def delcategory(tasks,myscreen,rows,taskfile):
  # 1 makes categories enumerated
  drawscreen(myscreen,rows,tasks,1,0)
  myscreen.addstr(int(rows)-2, 1, " DEL CATEGORY: ", curses.color_pair(2))
  myscreen.refresh()
  sortedkeys = sorted(tasks.keys())
  curses.echo()
  curses.curs_set(1)
  delcatnum = myscreen.getstr(int(rows)-2, 16)
  curses.noecho()
  curses.curs_set(0)
  delcatnumtemp = str(delcatnum)
  temp = delcatnumtemp[2:-1]
  del tasks[sortedkeys[int(temp)-1]]
  writetasks(taskfile,tasks)

def createitem(tasks,myscreen,rows,taskfile):
  # 1 makes categories enumerated
  drawscreen(myscreen,rows,tasks,1,0)
  myscreen.addstr(int(rows)-2, 1, " NEW ITEM: Create new item in which category? ", curses.color_pair(2))
  myscreen.refresh()
  sortedkeys = sorted(tasks.keys())
  curses.echo()
  curses.curs_set(1)
  catnum = myscreen.getstr(int(rows)-2, 47)
  catnumtemp = str(catnum)
  temp = int(catnumtemp[2:-1])
  myscreen.addstr(int(rows)-2, 1, " NEW ITEM:                                        ", curses.color_pair(2))
  myscreen.refresh()
  itemname = myscreen.getstr(int(rows)-2, 12)
  curses.noecho()
  curses.curs_set(0)
  itemnametemp = str(itemname)
  tempb = itemnametemp[2:-1]
  templist = tasks[sortedkeys[int(temp)-1] ]
  templist.append(tempb)
  tasks[ sortedkeys[ int(temp)-1 ] ] = sorted(templist)
  writetasks(taskfile,tasks)

def delitem(tasks,myscreen,rows,taskfile):
  # 1 makes categories enumerated
  drawscreen(myscreen,rows,tasks,1,0)
  myscreen.addstr(int(rows)-2, 1, " DEL ITEM: Delete an item in which category? ", curses.color_pair(2))
  myscreen.refresh()
  sortedkeys = sorted(tasks.keys())
  curses.echo()
  curses.curs_set(1)
  delcatnum = myscreen.getstr(int(rows)-2, 46)
  curses.noecho()
  curses.curs_set(0)
  delcatnumtemp = str(delcatnum)
  temp = delcatnumtemp[2:-1]
  drawscreen(myscreen,rows,tasks,2,temp)
  myscreen.addstr(int(rows)-2, 1, " NEW ITEM: Delete which item ", curses.color_pair(2))
  curses.echo()
  curses.curs_set(1)
  delitemnum = myscreen.getstr(int(rows)-2, 30)
  curses.noecho()
  curses.curs_set(0)
  delitemnumtemp = str(delitemnum)
  tempb = delitemnumtemp[2:-1]
  itemslist = [ ]
  for i in tasks[sortedkeys[int(temp)-1]]:
    itemslist.append(i)
  itemslist.remove(itemslist[int(tempb)-1])
  tasks[ sortedkeys[ int(temp)-1 ] ] = itemslist
  writetasks(taskfile,tasks)

#####################
### MAIN FUNCTION ###
#####################

def main():
  # open save file for r/w
  taskfile = os.path.expanduser('~/.todo.td')
  # load file into 'task' dictionary
  tasks = ast.literal_eval(readtasks(taskfile))
  # read 'rows' and 'columns' from term
  rows, columns = os.popen('stty size', 'r').read().split()
  # initiate curses screen
  myscreen = curses.initscr()
  initialize(myscreen)
  res = drawscreen(myscreen,rows,tasks,0,0)
  # run main menu loop
  menu(myscreen,res,tasks,rows,taskfile)
  # quit program
  killscreen(myscreen)

main()
