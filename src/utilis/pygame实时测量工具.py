import pygame

def coordinate_finder():
    """实时显示鼠标坐标的工具"""
    pygame.init()
    window = pygame.display.set_mode((400,400))

    background = pygame.image.load("../../../../../新建文件夹/GitHub/pet-game/assets/images/backgrounds/room_background.png")
    background = pygame.transform.scale(background,(400,400))

    font = pygame.font.Font(None,24)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                print(f"点击位置:({x},{y})")

        window.blit(background,(0,0))

        mouse_x,mouse_y = pygame.mouse.get_pos()
        coord_text = font.render(f"坐标:({mouse_x},{mouse_y})",
                                 True,(255,255,255))
        window.blit(coord_text,(10,10))

        pygame.display.flip()
    pygame.quit()

coordinate_finder()