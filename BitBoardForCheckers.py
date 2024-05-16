# uncompyle6 version 3.5.0
# Python bytecode 3.8 (3413)
# Decompiled from: Python 2.7.5 (default, Jun 20 2023, 11:36:40)
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: C:\Users\User\PycharmProjects\pythonProject\BitBoardForCheckers.py
# Size of source mod 2**32: 15470 bytes
import numpy as np
from numpy import uint64 as u
import time, random

class Bitboard:
    black_board = u(0xaa55aa0000000000)
    white_board = u(11163050)
    queenW_board = u(0)
    queenB_board = u(0)
    a = u(0x101010101010101)
    h = u(0x8080808080808080)
    one_piece = u(524288)
    one = u(1)
    kills = np.full((64, 4), None, dtype=tuple)
    line8 = u(0xff00000000000000)
    line1 = u(255)
    noth = ~h
    nota = ~a
    u7 = u(7)
    u9 = u(9)
    u14 = u(14)
    u18 = u(18)
    Available_moves = np.array(24, dtype=u)

    @staticmethod
    def print_board(b):
        arr = np.full(64, 0)
        a = np.array([str(bin(b))[i] for i in range(2, len(str(bin(b))))])
        arr[:len(a)] = a[::-1]
        print(arr.reshape((8, 8))[::-1])
        return arr
    @staticmethod
    def gameVisualizer(white_board, black_board, QueenW_board, QueenB_board):
        Bitboard.print_board(white_board|black_board|QueenW_board|QueenB_board)
    @staticmethod
    def movesWhite(white_board, black_board, QueenW_board, QueenB_board):
        return (
         ((Bitboard.nota & white_board) << Bitboard.u7 | (Bitboard.noth & white_board) << Bitboard.u9) & ~(white_board | QueenW_board | black_board | QueenB_board), white_board, black_board, QueenW_board, QueenB_board)

    @staticmethod
    def movesBlack(white_board, black_board, QueenW_board, QueenB_board):
        return (
         ((Bitboard.noth & black_board) >> Bitboard.u7 | (Bitboard.nota & black_board) >> Bitboard.u9) & ~(white_board | QueenW_board | black_board | QueenB_board), white_board, black_board, QueenW_board, QueenB_board)

    @staticmethod
    def WQueenMoves(white_board, black_board, QueenW_board, QueenB_board):
        return ((Bitboard.noth & QueenW_board) >> Bitboard.u7 | (Bitboard.nota & QueenW_board) >> Bitboard.u9) & ~(black_board | QueenB_board | white_board | QueenW_board) | Bitboard.movesWhite(QueenW_board, black_board, white_board, QueenB_board)

    @staticmethod
    def BQueenMoves(white_board, black_board, QueenW_board, QueenB_board):
        return ((Bitboard.nota & QueenB_board) << Bitboard.u7 | (Bitboard.noth & QueenB_board) << Bitboard.u9) & ~(white_board | QueenW_board | black_board | QueenB_board) | Bitboard.movesBlack(white_board, QueenB_board, QueenW_board, black_board)

    @staticmethod
    def getPLayersPositions (n):  # can only use one board at a time
        list_moves = np.zeros (64, dtype=u)
        count = 0
        i = 0
        while n:
            if n & b.one:
                list_moves[i] = (b.one << u (count))
                i += 1
            count = count + 1
            n = n >> Bitboard.one
        return list_moves
    @staticmethod
    def killswhite(white_board, black_board, QueenW_board, QueenB_board):
        #return np array of the final board for every move
        k = black_board | QueenB_board
        s = ~(black_board | QueenB_board | white_board | QueenW_board)
        b = ((((Bitboard.nota & white_board) << Bitboard.u7) & k) << Bitboard.u7) & s #left eat - only one white can eat left and go to a certain position meaning I know the black eaten
        b1 = ((((Bitboard.noth & white_board) << Bitboard.u9) & k) << Bitboard.u9) & s #right eat
        rightkills = Bitboard.getPLayersPositions(b)
        leftkills = Bitboard.getPLayersPositions(b1)
        last = 0
        for i, position in enumerate(leftkills):
            if position == 0:
                break
            Bitboard.kills[i] = ((white_board & ~(position>>Bitboard.u18)) | position, black_board & ~(position>>Bitboard.u9), QueenW_board, QueenB_board & ~(position>>Bitboard.u9))
            last = i
        for i, position in enumerate(rightkills):
            if position == 0:
                break
            Bitboard.kills[i + last + 1] = ((white_board & ~(position>>Bitboard.u14)) | position, black_board & ~(position>>Bitboard.u7), QueenW_board, QueenB_board & ~(position>>Bitboard.u7))
        #remember to empty the list
        return Bitboard.kills

    @staticmethod
    def killsBlack(black_player, white_board, black_board, QueenW_board, QueenB_board):
        s = ~(black_board | QueenB_board | white_board | QueenW_board)
        k = white_board | QueenW_board
        b = (black_player & Bitboard.noth) >> Bitboard.u7 & k
        b1 = (black_player & Bitboard.nota) >> Bitboard.u9 & k
        black_board = black_board ^ black_player
        s1 = b >> Bitboard.u7 & s
        s2 = b1 >> Bitboard.u9 & s
        if s1 << Bitboard.u7:
            if s2 << Bitboard.u9:
                return (
                 s1 | s2, (white_board ^ s2 << Bitboard.u9) & (white_board ^ s1 << Bitboard.u7), black_board, (queenW_board ^ s2 << Bitboard.u9) & (queenW_board ^ s1 << Bitboard.u7), QueenB_board)
        if s1 >> Bitboard.u7:
            return (
             s1 | s2, white_board ^ s1 << Bitboard.u7, black_board, queenW_board ^ s1 << Bitboard.u7, QueenB_board)
        elif s2 >> Bitboard.u9:
            return (s1 | s2, white_board ^ s2 << Bitboard.u9, black_board, queenW_board ^ s2 << Bitboard.u9, QueenB_board)
        else:
            return (
             black_player, white_board, black_board, queenW_board, queenB_board)

    @staticmethod
    def multkillsW(white_board, black_board, QueenW_board, QueenB_board):
        a, b, c, d = Bitboard.killsWhite(white_board, black_board, QueenW_board, QueenB_board)
        while True:
            if a:
                a, b, c, d = Bitboard.killsWhite(a, b, c, d)

        return a

    @staticmethod
    def multkillsB(white_board, black_board, QueenW_board, QueenB_board):
        a, b, c, d = Bitboard.killsWhite(white_board, black_board, QueenW_board, QueenB_board)
        while True:
            if a:
                a, b, c, d = Bitboard.killsWhite(a, b, c, d)

        return b

    @staticmethod
    def makeAQueen(white_board, black_board, queenW_board, queenB_board):
        if white_board & Bitboard.line8:
            return (queenW_board | white_board, white_board & ~Bitboard.line8)
        if black_board & Bitboard.line1:
            return (queenB_board | black_board, black_board & ~Bitboard.line1)

    @staticmethod
    def Wkills(white_board, black_board, queenW_board, queenB_board):
        s = ~(black_board | queenB_board | white_board | queenW_board)
        k = black_board | queenB_board
        b = queenW_board >> Bitboard.u7 & Bitboard.noth & k
        b1 = queenW_board >> Bitboard.u9 & Bitboard.nota & k
        if b:
            if b1:
                return (
                 white_board, black_board & ~b & black_board & ~b1, (b >> Bitboard.u7 & s | b << Bitboard.u7 ^ queenW_board | b1 >> Bitboard.u9 & s | b1 << Bitboard.u9 ^ queenW_board) ^ queenW_board, queenB_board & ~b & queenB_board & ~b1)
            return b and (
             white_board, black_board & ~b, (b >> Bitboard.u7 & s | b << Bitboard.u7 ^ queenW_board) ^ queenW_board, queenB_board & ~b)
        else:
            return (
             white_board, black_board & ~b1, b1 >> Bitboard.u9 & s | b1 << Bitboard.u9 ^ queenW_board ^ queenW_board, queenB_board & ~b1)

    @staticmethod
    def Bkills(white_board, black_board, QueenW_board, queenB_board):
        k = white_board | QueenW_board
        s = ~(black_board | queenB_board | white_board | QueenW_board)
        b = queenB_board << Bitboard.u7 & Bitboard.nota & k
        b1 = queenB_board << Bitboard.u9 & Bitboard.noth & k
        if b:
            if b1:
                return (
                 white_board & ~b & white_board & ~b1, black_board, QueenW_board & ~b & QueenW_board & ~b1, (b << Bitboard.u7 & s | b >> Bitboard.u7 ^ queenB_board | b1 << Bitboard.u9 & s | b1 >> Bitboard.u9 ^ queenB_board) ^ queenW_board)
            return b and (
             white_board & ~b, black_board, QueenW_board & ~b, b << Bitboard.u7 & s | b >> Bitboard.u7 ^ queenB_board)
        else:
            return (
             white_board & ~b1, black_board, QueenW_board & ~b1, b1 << Bitboard.u9 & s | b1 >> Bitboard.u9 ^ queenB_board ^ queenW_board)

    @staticmethod
    def multkillsWQ(white_board, black_board, QueenW_board, QueenB_board):
        a, b, c, d = (white_board, black_board, QueenW_board, QueenB_board)
        board = Bitboard.u7
        previousBoard = Bitboard.u9
        previousBoard = board ^ previousBoard and board
        Bitboard.print_board(a | b | c | d)
        if Bitboard.killsWhite(c, b, a, d)[0] or Bitboard.Wkills(a, b, c, d)[2]:
            Bitboard.print_board(a | b | c | d)
            while Bitboard.killsWhite(c, b, a, d)[0]:
                if Bitboard.Wkills(a, b, c, d)[2]:
                    board = a | b | c | d
                elif Bitboard.Wkills(a, b, c, d)[2]:
                    a, b, c, d = Bitboard.Wkills(a, b, c, d)
                else:
                    c, b, a, d = Bitboard.killsWhite(c, b, a, d)

            return a | c

    @staticmethod
    def multkillsBQ(white_board, black_board, QueenW_board, QueenB_board):
        a, b, c, d = (white_board, black_board, QueenW_board, QueenB_board)
        while True:
            if Bitboard.killsBlack(a, d, c, b)[1] or Bitboard.Bkills(a, b, c, d)[3]:
                if Bitboard.killsBlack(a, d, c, b)[1]:
                    while Bitboard.Bkills(a, b, c, d)[3]:
                        pera, perb, perc, perd = (
                         a, b, c, d)
                        r = Bitboard.Bkills(pera, perb, perc, perd)
                        k = Bitboard.killsBlack(pera, perd, perc, perb)
                        a = r[0] & k[0]
                        b = r[1] | k[3]
                        c = r[2] & k[2]
                        d = r[3] | k[1]

                if Bitboard.Bkills(a, b, c, d)[3]:
                    a, b, c, d = Bitboard.Bkills(a, b, c, d)
                else:
                    a, d, c, b = Bitboard.killsBlack(a, d, c, b)

        return b | d

    @staticmethod
    def get_all_movesWS(white_board, black_board, QueenW_board, QueenB_board):
        if Bitboard.multkillsW(white_board, black_board, QueenW_board, QueenB_board):
            return Bitboard.multkillsW(white_board, black_board, QueenW_board, QueenB_board)
        else:
            return Bitboard.movesWhite(white_board, black_board, QueenW_board, QueenB_board)

    @staticmethod
    def get_all_movesWQ(white_board, black_board, QueenW_board, QueenB_board):
        if Bitboard.multkillsWQ(white_board, black_board, QueenW_board, QueenB_board):
            return Bitboard.multkillsWQ(white_board, black_board, QueenW_board, QueenB_board)
        else:
            return Bitboard.WQueenMoves(white_board, black_board, QueenW_board, QueenB_board)

    @staticmethod
    def get_all_movesBS(white_board, black_board, QueenW_board, QueenB_board):
        if Bitboard.multkillsB(white_board, black_board, QueenW_board, QueenB_board):
            return Bitboard.multkillsB(white_board, black_board, QueenW_board, QueenB_board)
        else:
            return Bitboard.movesBlack(white_board, black_board, QueenW_board, QueenB_board)

    @staticmethod
    def get_all_movesBQ(white_board, black_board, QueenW_board, QueenB_board):
        if Bitboard.BQueenMoves(white_board, black_board, QueenW_board, QueenB_board):
            return Bitboard.BQueenMoves(white_board, black_board, QueenW_board, QueenB_board)
        else:
            return Bitboard.multkillsBQ(white_board, black_board, QueenW_board, QueenB_board)

    @staticmethod
    def rand_moves(attacksPiece):
        i = 0
        while True:
            if attacksPiece:
                s = ~(attacksPiece - Bitboard.one) & attacksPiece
                Bitboard.rand_moves[i] = s
                i += 1
                attacksPiece ^= s

        return Bitboard.rand_moves[random.randint(0, i - 1)]

    @staticmethod
    def game_over(white_board, black_board, queenw_board, queenb_board):
        if not white_board | queenw_board:
            return 1
        if not black_board | queenb_board:
            return 2



    ''''@staticmethod
    def game(white_board, black_board, queenw_board, queenb_board):
        counter = 0
        allthekills = []
        all = []
        Bitboard.print_board(white_board)
        Bitboard.print_board(black_board)
        while True:
            if counter < 30:
                counter += 1
                if counter % 2 == 0:
                    original_board = white_board
                    index = 0
                    while True:
                        if white_board:
                            previous_board = white_board
                            white_board = white_board & white_board - u(1)
                            player = white_board ^ original_board ^ previous_board ^ original_board
                            if black_board != Bitboard.WhitePlayerKills(player, original_board, black_board, queenw_board, queenb_board)[2]:
                                kills = Bitboard.WhitePlayerKills(player, original_board, black_board, queenw_board, queenb_board)
                                allthekills.append(kills)
                                all.append(kills)
                            else:
                                moves = Bitboard.movesWhite(player, original_board, black_board, queenw_board, queenb_board)
                            if moves[0] | moves[1] != player | original_board:
                                all.append(moves)
                            index += 1

                    white_board = original_board
                    if len(allthekills) != 0:
                        index = random.randint(0, len(allthekills) - 1)
                        player, white_board, black_board, queenw_board, queenb_board = allthekills[index]
                    else:
                        index = random.randint(0, len(all) - 1)
                        print(all)
                        player, white_board, black_board, queenw_board, queenb_board = all[index]
                    white_board = white_board | player
                    Bitboard.print_board(white_board)
                    Bitboard.print_board(black_board)'''
    @staticmethod
    def game(white_board, black_board, queenw_board, queenb_board):
        list = Bitboard.killswhite(white_board, black_board, queenw_board, queenb_board)
        Bitboard.kills = np.full((64, 4), None , dtype=tuple)
        print("Start: ")
        for element in list:
            if (element[0] or element[1] or element[2] or element[3]) is None:
                break
            a,b,c,d = element
            Bitboard.gameVisualizer(a,b,c,d)
    @staticmethod
    def outofbounds(a, b):
        return a>b


b = Bitboard()
time1 = time.time()
black_board = u(0x20000000)
white_board = u(0x55aa55)
queenW_board = u(0)
queenB_board = u(0)
Bitboard.print_board(white_board|black_board|queenW_board|queenB_board)
b.game(white_board, black_board, queenW_board, queenB_board)
time1 = time.time()
for i in range(1000000):
    Bitboard.killswhite (white_board, black_board, queenW_board, queenB_board)
print((time.time() - time1)/1000000)