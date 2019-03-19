import pygame


# Game conditions(how many items in the game, and moves are allowed in the game)
def main(pile, moves, turn=1):

    class Button:
        def __init__(self, color, x, y, text):
            self.color = color
            self.text = text
            self.my_font = pygame.font.SysFont("Lato", 20)
            self.txt = self.my_font.render(self.text, True, self.color)
            self.rect = self.txt.get_rect()
            self.rect.x = x
            self.rect.y = y

        def contain_pt(self, tup):
            pt_x = tup[0]
            pt_y = tup[1]
            if (pt_x >= self.rect.x and pt_x < self.rect[2]+self.rect.x and
                pt_y >= self.rect.y and pt_y < self.rect[3]+self.rect.y):
                    return True
            return False

        def update(self):
            self.color = (255,255,255)
            self.txt = self.my_font.render(self.text, True, self.color)

    class Stick(pygame.sprite.Sprite):
        def __init__(self, color, width, height, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.flag = False
            self.image = pygame.Surface([width, height])
            self.color = color
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def contain_pt(self, tup):
            pt_x = tup[0]
            pt_y = tup[1]
            if (pt_x >= self.rect.x and pt_x < self.rect[2]+self.rect.x and
                pt_y >= self.rect.y and pt_y < self.rect[3]+self.rect.y):
                    return True
            return False

        def update(self):
            self.color = (255,255,255)
            self.image.fill(self.color)
            self.rect.y -= 20
            self.flag = True

        def release(self):
            self.color = (125, 134, 145)
            self.image.fill(self.color)
            self.rect.y += 20
            self.flag = False

    class ALLSticks(pygame.sprite.Group):
        pass


    def mex(xs):
        without_dups = []
        for i in  sorted(xs):
            if i not in without_dups:
                without_dups.append(i)

        for (i, j) in zip(range(0, max(xs)+1), sorted(without_dups)):
            if i != j:
                return i
        return max(xs)+1

    def SG(amount, mov):

        SG_func = {}
        SG_func[1] = 0  # 1 is a terminal state

        for pile_state in range(2, pile + 1):
            temp_SG_values = []
            for move in mov:
                if move < pile_state:
                    temp_SG_values.append(SG_func[pile_state - move])
            if temp_SG_values == []:
                SG_func[pile_state] = 0
            else:
                move_mex = mex(temp_SG_values)
                SG_func[pile_state] = move_mex
            temp_SG_values = []
        return SG_func


    pygame.init()
    pygame.font.init()
    main_surface = pygame.display.set_mode((640, 380))
    # counter for sprites activity
    c1 = 0
    # Create a group for sticks.
    stick_group = ALLSticks()
    for i in range(pile):
        j = 3*i*(520/(3*pile-2))
        s = Stick((125,134,145), 520/(3*pile-2), 150, 60+j, 100)
        stick_group.add(s)


    button_turn = Button((125,134,145), 160, 300, "TURN")
    button_exit = Button((125,134,145), 310, 300, "QUIT THE GAME")
    button_win = Button((125, 134, 145), 277.5, 177.5, "You won!")
    button_lose = Button((125, 135, 145), 277.5, 177.5, "YOU LOSE!")
    button_again = Button((125,135,145), 160, 300, "Play again?")

    while True:
        # logic for machine
        if turn == 0:
            machineSG = SG(len(stick_group.sprites()), moves)
            for move in moves:
                if turn == 0:
                    if move < len(stick_group.sprites()) and machineSG[len(stick_group.sprites()) - move] == 0:
                        for (sprite, m) in zip(stick_group.sprites(), range(move)):
                            stick_group.remove(sprite)
                        button_turn.update()
                        turn = 1
        # 2. choose move "randomly" if there is no turn with SG value == 0
        for move in moves:
            if turn == 0:
                if move < len(stick_group.sprites()):
                    for (sprite, m) in zip(stick_group.sprites(), range(move)):
                        stick_group.remove(sprite)
                    turn = 1

        # Get the events.
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos_of_click = ev.dict["pos"]
            if button_again.contain_pt(pos_of_click) and len(stick_group.sprites()) == 1:
                main(11, [1,3])

            if button_exit.contain_pt(pos_of_click):
                button_exit.update()
                break
            if button_turn.contain_pt(pos_of_click) and turn == 1 and len(stick_group.sprites()) != 1:
                turn = 0
                for sprite in stick_group.sprites():
                    if sprite.flag == True:
                        stick_group.remove(sprite)
                        c1 -= 1
            for sprite in stick_group.sprites():
                if sprite.contain_pt(pos_of_click) and c1 < max(moves) and sprite.flag == False and turn == 1:
                    c1 += 1
                    sprite.update()

        # Update objects.

        # Draw objects.
        # Draw main screen.
        main_surface.fill((25, 34, 45))
        if len(stick_group.sprites()) == 1:
            if turn  == 0:
                stick_group.draw(main_surface)
                main_surface.blit(button_win.txt, (button_win.rect.x, button_win.rect.y))
                main_surface.blit(button_exit.txt, (button_exit.rect.x, button_exit.rect.y))
                main_surface.blit(button_again.txt, (button_again.rect.x, button_again.rect.y))

            else:
                stick_group.draw(main_surface)
                main_surface.blit(button_lose.txt, (button_lose.rect.x, button_lose.rect.y))
                main_surface.blit(button_exit.txt, (button_exit.rect.x, button_exit.rect.y))
                main_surface.blit(button_again.txt, (button_again.rect.x, button_again.rect.y))
        else:
            # Draw buttons.
            main_surface.blit(button_turn.txt, (button_turn.rect.x, button_turn.rect.y))
            main_surface.blit(button_exit.txt, (button_exit.rect.x, button_exit.rect.y))
            # Draw group of sticks.
            stick_group.draw(main_surface)

        # Turn the display.
        pygame.display.flip()

    pygame.quit()


# if turn == 1 human turns the first, machine turns the firs otherwise
main(11, [1, 3])
