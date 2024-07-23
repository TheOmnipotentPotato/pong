from email.header import Header
import pygame
pygame.init()

HEIGHT, WIDTH = 800, 800
WIN = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("A joystick controling a ball on screen")

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

BLACK = (0, 0 , 0)

    



def main(debug=False, joysticks=joysticks):
    clock = pygame.time.Clock()
    run = True
    my_box = pygame.Rect(50, 50, 50, 50)
    my_box_color = 0
    colors = ((255, 0 ,0), (0, 255, 0), (0, 0, 255))
    my_other_box = pygame.Rect(WIDTH - 100, 50, 50, 50)
    motion = [[0, 0], [0, 0]]
    joysticks = joysticks

    while run:
        WIN.fill(BLACK)
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.JOYBUTTONDOWN:
                print(event)
                if event.button == 1:
                    my_box_color = (my_box_color + 1) % len(colors)
                if event.button == 2:
                    motion = [[0, 0], [0, 0]]
            if event.type == pygame.JOYBUTTONUP:
                print(event)

            
            for joystick in joysticks:
                
                if joystick.get_instance_id() == 0:
                    if abs(joystick.get_axis(0)) > 0.2:
                        motion[0][0] = joystick.get_axis(0)
                        print(joystick.get_axis(0))

                    if abs(joystick.get_axis(1)) > 0.2:
                        motion[0][1] = joystick.get_axis(1)

                if joystick.get_instance_id() == 1:
                    if abs(joystick.get_axis(0)) > 0.2:
                        motion[1][0] = joystick.get_axis(0)
                        print(joystick.get_axis(0))

                    if abs(joystick.get_axis(1)) > 0.2:
                        motion[1][1] = joystick.get_axis(1)

                        
                    


            if event.type == pygame.JOYBALLMOTION:
                print(event)

            if event.type == pygame.JOYHATMOTION:
                print(event)

            if event.type == pygame.JOYDEVICEADDED:
                joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

            if event.type == pygame.JOYDEVICEREMOVED:
                joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        
        pygame.draw.rect(WIN, colors[my_box_color], my_box)
        pygame.draw.rect(WIN, colors[(my_box_color + 1) % len(colors)], my_other_box)
        if abs(motion[0][0]) < 0.5:
            motion[0][0] = 0

        if abs(motion[0][1]) < 0.5:
            motion[0][1] = 0

        if abs(motion[1][0]) < 0.5:
            motion[1][0] = 0

        if abs(motion[1][1]) < 0.5:
            motion[1][1] = 0

        my_box.x += motion[0][0] * 10
        my_box.y += motion[0][1] * 10
        my_other_box.x += motion[1][0] * 10
        my_other_box.y += motion[1][1] * 10

        
        pygame.display.update()
    pygame.quit()

print(len(joysticks))
main()
