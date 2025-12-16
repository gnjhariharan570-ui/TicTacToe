import tkinter as tk
from tkinter import messagebox
import math
BG="#1e1e1e"
CARD="#292929"
BTN_BG="#3b3b3b"
BTN_HOVER="#505050"
X_COLOR="#ff5252"
O_COLOR="#61d4ff"
WIN_COLOR="#00ff7f"
root=tk.Tk()
root.title("Tic Tac Toe - vs Computer")
root.geometry("420x520")
root.config(bg=BG)
root.resizable(False,False)
board=[[""for _ in range(3)]for _ in range(3)]
buttons=[[None]*3 for _ in range(3)]
player="X"
computer="O"
title=tk.Label(root,text="TIC • TAC • TOE",font=("Helvetica",28,"bold"),bg=BG,fg="white")
title.pack(pady=15)
status=tk.Label(root,text="Your Turn (X)",font=("Helvetica",16),bg=BG,fg="#bbbbbb")
status.pack()
board_frame=tk.Frame(root,bg=CARD)
board_frame.pack(pady=20)
def on_enter(e):
    if e.widget["text"]=="":
        e.widget.config(bg=BTN_HOVER)
def on_leave(e):
    if e.widget["text"]=="":
        e.widget.config(bg=BTN_BG)
def check_winner(b):
    for r in range(3):
        if b[r][0]==b[r][1]==b[r][2]!="" :
            return b[r][0],[(r,0),(r,1),(r,2)]
    for c in range(3):
        if b[0][c]==b[1][c]==b[2][c]!="" :
            return b[0][c],[(0,c),(1,c),(2,c)]
    if b[0][0]==b[1][1]==b[2][2]!="" :
        return b[0][0],[(0,0),(1,1),(2,2)]
    if b[0][2]==b[1][1]==b[2][0]!="" :
        return b[0][2],[(0,2),(1,1),(2,0)]
    return None,None
def minimax(b,depth,is_max):
    winner,_=check_winner(b)
    if winner==computer:
        return 1
    if winner==player:
        return -1
    if all(b[r][c]!="" for r in range(3) for c in range(3)):
        return 0
    if is_max:
        best=-math.inf
        for r in range(3):
            for c in range(3):
                if b[r][c]=="":
                    b[r][c]=computer
                    score=minimax(b,depth+1,False)
                    b[r][c]=""
                    best=max(best,score)
        return best
    else:
        best=math.inf
        for r in range(3):
            for c in range(3):
                if b[r][c]=="":
                    b[r][c]=player
                    score=minimax(b,depth+1,True)
                    b[r][c]=""
                    best=min(best,score)
        return best
def computer_move():
    best_score=-math.inf
    best_move=None
    for r in range(3):
        for c in range(3):
            if board[r][c]=="":
                board[r][c]=computer
                score=minimax(board,0,False)
                board[r][c]=""
                if score>best_score:
                    best_score=score
                    best_move=(r,c)
    r,c=best_move
    buttons[r][c]["text"]=computer
    buttons[r][c]["fg"]=O_COLOR
    board[r][c]=computer
    winner,line=check_winner(board)
    if winner:
        for wr,wc in line:
            buttons[wr][wc].config(bg=WIN_COLOR)
        messagebox.showinfo("Game Over","Computer Wins!")
        reset_game()
        return
    if all(board[r][c]!="" for r in range(3) for c in range(3)):
        messagebox.showinfo("Game Over","It's a Draw!")
        reset_game()
        return
    status.config(text="Your Turn (X)")
def on_click(r,c):
    if board[r][c]!="":
        return
    buttons[r][c]["text"]=player
    buttons[r][c]["fg"]=X_COLOR
    board[r][c]=player
    winner,line=check_winner(board)
    if winner:
        for wr,wc in line:
            buttons[wr][wc].config(bg=WIN_COLOR)
        messagebox.showinfo("Game Over","You Win!")
        reset_game()
        return
    if all(board[r][c]!="" for r in range(3) for c in range(3)):
        messagebox.showinfo("Game Over","It's a Draw!")
        reset_game()
        return
    status.config(text="Computer Thinking...")
    root.after(500,computer_move)
def reset_game():
    global board
    board=[[""for _ in range(3)]for _ in range(3)]
    status.config(text="Your Turn (X)")
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="",bg=BTN_BG)
for r in range(3):
    for c in range(3):
        btn=tk.Label(board_frame,text="",font=("Helvetica",36,"bold"),width=3,height=1,bg=BTN_BG,fg="white")
        btn.grid(row=r,column=c,padx=10,pady=10)
        btn.bind("<Button-1>",lambda e,r=r,c=c:on_click(r,c))
        btn.bind("<Enter>",on_enter)
        btn.bind("<Leave>",on_leave)
        buttons[r][c]=btn
restart_btn=tk.Button(root,text="Restart Game",font=("Helvetica",14,"bold"),command=reset_game,bg=BTN_BG,fg="white",activebackground=BTN_HOVER)
restart_btn.pack(pady=10)
root.mainloop()
