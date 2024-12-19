import tkinter as tk
import numpy as np
import copy

root = tk.Tk()
root.geometry('480x450+150+100')
root.title('Tic-Tac-Toe Game')
root.resizable(False, False)
# Set the title label
photo = tk.PhotoImage(file="E:\python代码\jingziqi_\jingziqi.gif") 
Lab = tk.Label(root, text='Tic-Tac-Toe Game', compound='center', font=('微软雅黑', 30), image=photo)
Lab.pack()  # Set main window

def main_window():
    main_window = tk.Toplevel(root)
    main_window.geometry('650x450+150+100')
    text1 = '''
    The rules of Tic-Tac-Toe are that two players, A and B,
take turns to place either 'O' or 'X' on a 3x3 grid.
If one player's pieces form a line, horizontally, vertically, or diagonally, that player wins. 
Players cannot place their pieces on already occupied positions.
The game is called Tic-Tac-Toe because it is played on a grid that forms a "tic-tac" pattern.
'''
    #photo1 = tk.PhotoImage(file="E:\python代码\jingziqi_\jingziqi.gif")
    lab1 = tk.Label(main_window, text=text1, width=30,               # Set the label width: 30
			height=10,              # Set the label height: 10
			justify='left',         # Set text alignment: left
			anchor='nw',            # Set text position: northwest
			font=('微软雅黑', 20),   # Set font: 微软雅黑, font size: 20
			fg='black',             # Set foreground color: black
            background='grey',
            #image=photo1,  
			#compound='center',      # Set text and image combination method
			padx=10,                # Set x-direction padding: 20
			pady=10)                # Set y-direction padding: 10
    lab1.pack()

but = tk.Button(root, text='Game Rules', bg='lightgreen', command=main_window) # Open game rules window
but.pack()

# Main game window
def game_over(B1, B2, B3):
    global B
    for i in range(3):
        for j in range(3):
            B[i][j]['state'] = 'disabled'  # Disable the button
            B[i][j]['cursor'] = 'arrow'  # Change cursor style
    if B1['text'] == 'X':
        window1 = tk.Tk()
        window1.geometry('250x100')
        text = tk.Label(window1, text="Congratulations, Player Wins!!!", bg="yellow", fg="red", font=('黑体', 15, 'bold italic underline'))
        text.pack()
    elif B1['text'] == 'O' or B2['text'] == 'O':
        window2 = tk.Tk()
        window2.geometry('250x100')
        text = tk.Label(window2, text="Unfortunately, the computer wins.", bg="yellow", fg="red", font=('黑体', 15, 'bold italic underline'))
        text.pack()
    else:
        global b2
        window3 = tk.Tk()
        window3.geometry('250x100')
        text = tk.Label(window3, text="It's a draw.", bg="yellow", fg="red", font=('黑体', 15, 'bold italic underline'))
        text.pack()

# Key points for AI strategy
def Key_points(M, t):
    x = []
    s_r = M.sum(axis=1)  # Sum of rows
    s_c = M.sum(axis=0)  # Sum of columns
    m_d = M[0, 0] + M[1, 1] + M[2, 2]  # Main diagonal
    b_d = M[0, 2] + M[1, 1] + M[2, 0]  # Anti-diagonal
    for i in range(3):
        for j in range(3):
            if M[i][j] == 0:  # Empty space
                c = 0  # Count of lines (row, column, or diagonal) that sum to 1
                if i == j and m_d == t: c += 1  # If it is on the diagonal or anti-diagonal
                if i + j == 2 and b_d == t: c += 1
                if s_r[i] == t: c += 1
                if s_c[j] == t: c += 1
                if c >= 2:
                    x.append([i, j])  # Can win, make a move
    return x

# AI makes a move + check win
def aiplay():
    global B, b1, b2, b3
    mark = []  # Mark to store the board
    t = 0  # Count of empty spaces
    for i in range(3):
        mark.append([])
        for j in range(3):
            if B[i][j]['text'] == 'O':
                mark[i].append(1)
            elif B[i][j]['text'] == 'X':
                mark[i].append(-1)
            else:
                mark[i].append(0)
                t += 1
        if sum(mark[i]) == -3:  # If any row has three 'X's, player wins
            game_over(B[i][0], B[i][1], B[i][2])
            return
    if not t:  # No empty space, it's a draw
        game_over(b1, b2, b3)
    mark = np.array(mark)
    sum_row = mark.sum(axis=1)  # Sum of rows
    sum_column = mark.sum(axis=0)  # Sum of columns
    main_diagonal = mark[0, 0] + mark[1, 1] + mark[2, 2]  # Main diagonal
    back_diagonal = mark[0, 2] + mark[1, 1] + mark[2, 0]  # Anti-diagonal
    for j in range(3):
        if sum_column[j] == -3:  # If any column has three 'X's, player wins
            game_over(B[0][j], B[1][j], B[2][j])
            return
    if main_diagonal == -3:  # Check main diagonal
        game_over(B[0][0], B[1][1], B[2][2])
        return
    if back_diagonal == -3:  # Check anti-diagonal
        game_over(B[0][2], B[1][1], B[2][0])
        return
    # AI win check ============================================
    for i in range(3):  # If there are two 'O's in a row, AI wins
        if sum_row[i] == 2:
            game_over(B[i][0], B[i][1], B[i][2])
            return
        if sum_column[i] == 2:
            game_over(B[0][i], B[1][i], B[2][i])
            return
    if main_diagonal == 2:  # Check main diagonal
        game_over(B[0][0], B[1][1], B[2][2])
        return
    if back_diagonal == 2:  # Check anti-diagonal
        game_over(B[0][2], B[1][1], B[2][0])
        return
    # Can't win directly, check if there are places to block AI ===================================
    for i in range(3):  # If there are two 'X's in a row, block
        if sum_row[i] == -2:
            aiplace(B[i][0]), aiplace(B[i][1]), aiplace(B[i][2])
            return
        if sum_column[i] == -2:
            aiplace(B[0][i]), aiplace(B[1][i]), aiplace(B[2][i])
            return
    if main_diagonal == -2:  # Check main diagonal
        aiplace(B[0][0]), aiplace(B[1][1]), aiplace(B[2][2])
        return
    if back_diagonal == -2:  # Check anti-diagonal
        aiplace(B[0][2]), aiplace(B[1][1]), aiplace(B[2][0])
        return
    # Look ahead, check if there are any key points where AI can win ===========================================
    K = Key_points(mark, 1)
    for i in K:
        aiplace(B[i[0]][i[1]])  # Can win, make a move
        return
    # Block opponent from winning ========================================
    K = Key_points(mark, -1)
    for i in K:
        aiplace(B[i[0]][i[1]])  # Block winning move
        return
    # No direct move, place in any empty spot
    for i in range(3):
        for j in range(3):
            if mark[i][j] == 0:  # Empty space
                aiplace(B[i][j])  # Make the move
                return
    # No space left, draw
    game_over(b1, b2, b3)

# AI places a piece
def aiplace(Bu):
    if not Bu['text'] == 'X':
        Bu['text'] = 'O'  # Place 'O'
        Bu['background'] = 'linen'
        Bu['state'] = 'disabled'  # Disable the button
        Bu['cursor'] = 'arrow'  # Change cursor style

# Player places a piece
def place(Bu):
    Bu['text'] = 'X'  # Place 'X'
    Bu['background'] = 'mistyrose'
    Bu['state'] = 'disabled'  # Disable the button
    Bu['cursor'] = 'arrow'  # Change cursor style
    aiplay()

# Restart the game
def restart():
    global B
    for i in range(3):
        for j in range(3):
            B[i][j]['text'] = ''
            B[i][j]['background'] = 'white'
            B[i][j]['state'] = 'normal'  # Reset all buttons to normal
    b1 = B[0][0]  # Player starts
    b2 = B[0][1]
    b3 = B[0][2]

# Button initialization
def new_game():
    global B, b1, b2, b3
    B = []
    for i in range(3):
        B.append([])
        for j in range(3):
            b = tk.Button(root, width=6, height=2, font=('微软雅黑', 20, 'bold'), relief="solid", command=lambda i=i, j=j: place(B[i][j]))
            b.grid(row=i + 1, column=j)  # Set grid positions
            B[i].append(b)
    b1 = B[0][0]  # First button as player
    b2 = B[0][1]
    b3 = B[0][2]
    b1.bind("<Enter>", lambda event, b=b1: b.config(background='lightblue'))  # Hover effect
    b1.bind("<Leave>", lambda event, b=b1: b.config(background='white'))  # Reset hover effect
    b2.bind("<Enter>", lambda event, b=b2: b.config(background='lightblue'))  # Hover effect
    b2.bind("<Leave>", lambda event, b=b2: b.config(background='white'))  # Reset hover effect
    b3.bind("<Enter>", lambda event, b=b3: b.config(background='lightblue'))  # Hover effect
    b3.bind("<Leave>", lambda event, b=b3: b.config(background='white'))  # Reset hover effect

new_game()
root.mainloop()
