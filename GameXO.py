from tkinter import *
from tkinter import messagebox
import random

root = Tk()
root.title('Game Caro 6x6 Minimax')
clicked = True
count = 0
player_vs_computer = False  
player1_score = 0
player2_score = 0
player_turn = True  
def disableButtons():
    for button in buttons:
        button.config(state=DISABLED)

def updateStatus():
    if player_vs_computer:
        status_text.set("Lượt người chơi" if player_turn else "Đến lượt máy")  
    else:
        status_text.set("Người chơi 1" if clicked else "Người chơi 2")

def checkWinner():
    global win, player1_score, player2_score
    win = False
    for pattern in winning_patterns:
        if all(button["text"] == "X" for button in pattern):
            for button in pattern:
                button.config(bg="#80ffaa")
            win = True
            player1_score += 1
            updateScore()
            messagebox.showinfo("OX Game", "X WINNER!!")
            disableButtons()
            return
        elif all(button["text"] == "O" for button in pattern):
            for button in pattern:
                button.config(bg="#80ffaa")
            win = True
            player2_score += 1
            updateScore()
            messagebox.showinfo("OX Game", "O WINNER!!")  
            disableButtons()
            return

def checkDraw():
    global count, win
    if count == 36 and not win:
        messagebox.showerror("OX Game", "Hoà!!")
        resetBoard()

def buttonClicked(button):
    global clicked, count, player_vs_computer, player_turn
    if button["text"] == " " and player_turn:  
        if not player_vs_computer:  
            if count % 2 == 0:
                button["text"] = "X"
                status_text.set("O")  
            else:
                button["text"] = "O"
                status_text.set("X")
            count += 1
            checkWinner()
            checkDraw()
        else:  
            button["text"] = "X"
            count += 1
            checkWinner()
            checkDraw()
            updateStatus()
            if not win:
                player_turn = False
                root.after(500, computerMove)  
    elif button["text"] != " ":
        messagebox.showerror("OX Game", "Lỗi")

def findBestMove():
  
    for symbol in ["O", "X"]:
        for button in buttons:
            if button["text"] == " ":
                button["text"] = symbol
                if checkPotentialWin(symbol):
                    button["text"] = " "  
                    return button
                button["text"] = " "  
    center = buttons[17]
    if center["text"] == " ":
        return center
    return random.choice([button for button in buttons if button["text"] == " "])

def checkPotentialWin(symbol):
    for pattern in winning_patterns:
        if all(button["text"] == symbol for button in pattern):
            return True
    return False

def computerMove():
    global count, player_turn
    move = findBestMove()
    move["text"] = "O"
    count += 1
    checkWinner()
    checkDraw()
    updateStatus()
    player_turn = True  
def updateScore():
    score_text.set(f"X: {player1_score} | O: {player2_score}")  

def resetBoard():
    global count, clicked, win, player_turn
    clicked = True
    count = 0
    win = False
    player_turn = True
    for button in buttons:
        button.config(text=" ", bg="SystemButtonFace", state=NORMAL)
    updateStatus()

def resetGame():
    global player1_score, player2_score
    player1_score = 0
    player2_score = 0
    updateScore()
    resetBoard()

def start(mode="two_player"):
    global clicked, count, player_vs_computer, buttons, winning_patterns, player_turn
    clicked = True
    count = 0
    player_vs_computer = (mode == "single_player")
    player_turn = True 
    for widget in root.winfo_children():
        widget.destroy()

    global status_text, score_text
    status_text = StringVar()
    score_text = StringVar()
    updateScore()
    updateStatus()
    Label(root, textvariable=status_text, font=("Helvetica", 14)).grid(row=0, column=0, columnspan=6, pady=10)
    Label(root, textvariable=score_text, font=("Helvetica", 14)).grid(row=1, column=0, columnspan=6, pady=5)

    buttons = []
    for i in range(36):
        button = Button(root, text=" ", font=("Helvetica", 20), height=3, width=7, bg="SystemButtonFace")
        button.config(command=lambda b=button: buttonClicked(b)) 
        buttons.append(button)
    for i, button in enumerate(buttons):
        row, col = divmod(i, 6)
        button.grid(row=row + 2, column=col)

    winning_patterns = []

    for row in range(6):
        for col in range(2):
            winning_patterns.append([buttons[row * 6 + col + i] for i in range(5)])
  
    for col in range(6):
        for row in range(2):
            winning_patterns.append([buttons[row * 6 + col + i * 6] for i in range(5)])
    for row in range(2):
        for col in range(2):
            winning_patterns.append([buttons[(row + i) * 6 + col + i] for i in range(5)])

    for row in range(2):
        for col in range(4, 6):
            winning_patterns.append([buttons[(row + i) * 6 + col - i] for i in range(5)])

    Button(root, text="Chơi lại", font=("Helvetica", 14), command=resetBoard).grid(row=8, column=1, columnspan=2, pady=10)
    Button(root, text="Reset điểm", font=("Helvetica", 14), command=resetGame).grid(row=8, column=3, columnspan=2, pady=10)

def showModeSelection():
    
    for widget in root.winfo_children():
        widget.destroy()
    Label(root, text="Chọn chế độ", font=("Helvetica", 16)).pack(pady=10)
    Button(root, text="Chơi với máy", font=("Helvetica", 14), command=lambda: start("single_player")).pack(pady=5)
    Button(root, text="Chơi 2 người", font=("Helvetica", 14), command=lambda: start("two_player")).pack(pady=5)

showModeSelection()
root.mainloop()
