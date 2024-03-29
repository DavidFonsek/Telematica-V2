import pygame
import random
import socket
import threading
import time


WIDTH, HEIGHT = 1200, 600
ballVel = 0.1
new_paddle_b_y = HEIGHT // 2 - 40



def receive_messages(client_socket):
    global new_paddle_b_y
    global bola_x
    global bola_y
    global punt_a 
    global punt_b 


    while True:


        data = client_socket.recv(50).decode("utf-8")
        # Analizar el mensaje para obtener la posición de la paleta derecha

        dat = data.split("|")[0].split()
        print(f"{data}")
        

        if data.startswith("SUBIO ") or data.startswith("BAJO "):        
                action = dat[0]
                value = dat[1]
                if action == "SUBIO":
                    new_paddle_b_y = float(value)
                elif action == "BAJO":
                    new_paddle_b_y = float(value)
        elif data.startswith("BOLA ") and int(aux) % 2 != 0 and len(dat) == 3:
                print(dat)  
                bola_x = (WIDTH - 20) - float(dat[1])
                bola_y = float(dat[2])
        elif data.startswith("PUNTAJE ") and int(aux) % 2 != 0 and len(dat) == 3:
                print(dat)
                punt_a = int(dat[1])
                punt_b = int(dat[2])


def main():
    global new_paddle_b_y
    global prueba
    global bola_x
    global bola_y
    global aux

    #host = "54.89.162.182"
    host = "54.89.162.182"
    host = "127.0.0.1"
    port = 8080
    

    name = input("Ingrese su nombre: ") 



    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(name.encode())
    aux = int(client_socket.recv(1).decode("utf-8")) +1 
    print(aux)
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    # Inicializar Pygame
    pygame.init()

    # Configuración de la pantalla
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")

    # Colores
    WHITE = (255, 255, 255)

    # Inicialización de las posiciones y velocidades de las paletas y la pelota
    ball_x = WIDTH - 10 // 2
    ball_y = HEIGHT - 10 // 2
    ball_speed_x = ballVel #* random.choice((1, -1))
    ball_speed_y = ballVel #* random.choice((1, -1))

    paddle_a_x = 10
    paddle_a_y = HEIGHT // 2 - 40 
    paddle_b_x = WIDTH - 20
    if 0 <= new_paddle_b_y <= HEIGHT - 80:
        paddle_b_y = new_paddle_b_y
    paddle_speed = .3

    # Puntuación
    if int(aux) % 2 == 0:
        score_a = -1
    else:
        score_a = 0

    score_b = 0

    font = pygame.font.Font(None, 36)

    # Bucle principal del juego
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()

                # Actualizar la posición de la pelota
        if int(aux) % 2 == 0:
            ball_x += ball_speed_x
            ball_y += ball_speed_y   

            posBall = "BOLA " + str(ball_x) + " " + str(ball_y) + "|" 
            #print(posBall)
            client_socket.send(posBall.encode())
        else:
            ball_x = bola_x
            ball_y = bola_y

        pos = ''
        if keys[pygame.K_w] and paddle_a_y > 0:
            paddle_a_y -= paddle_speed
            pos = "SUBIO " + str(paddle_a_y) + "|"
            client_socket.send(pos.encode())
    

        if keys[pygame.K_s] and paddle_a_y < HEIGHT - 80:
            paddle_a_y += paddle_speed
            pos = "BAJO " + str(paddle_a_y) + "|"
            client_socket.send(pos.encode())

        # Actualizar la posición de la paleta derecha con la posición global
        paddle_b_y = new_paddle_b_y

        if int(aux) % 2 == 0:
            puntaje = "PUNTAJE " + str(score_a) + " " + str(score_b) + "|" 
            client_socket.send(puntaje.encode())
        else:
            score_a = punt_a
            score_b = punt_b



        # Colisiones de la pelota con las paredes
        if ball_y <= 0 or ball_y >= HEIGHT - 20:
            ball_speed_y *= -1

        # Colisiones de la pelota con las paletas
        if (
            ball_x <= paddle_a_x + 10
            and paddle_a_y < ball_y < paddle_a_y + 80
        ) or (
            ball_x >= paddle_b_x - 10
            and paddle_b_y < ball_y < paddle_b_y + 80
        ):
            ball_speed_x *= -1

        # Punto para el jugador A
        if ball_x >= WIDTH - 20:
            score_a += 1

            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = ballVel * random.choice((1, -1))
            ball_speed_y = ballVel * random.choice((1, -1))

        # Punto para el jugador B
        if ball_x <= 0:
            score_b += 1

            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = ballVel * random.choice((1, -1))
            ball_speed_y = ballVel * random.choice((1, -1))

        # Verificar si uno de los jugadores llegó a 7 puntos para terminar el juego
        
        if score_a == 2:
        
            print("Gano jugador1")
            running = False
        elif score_b == 2:
            print("Gano jugador2")
            running = False
            

        # Limpiar la pantalla
        screen.fill((0, 0, 0))

        # Dibujar las paletas y la pelota
        pygame.draw.rect(screen, WHITE, (paddle_a_x, paddle_a_y, 10, 80))
        pygame.draw.rect(screen, WHITE, (paddle_b_x, paddle_b_y, 10, 80))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, 20, 20))

        # Mostrar la puntuación en la pantalla
        score_display = font.render(f"{score_a}  {score_b}", True, WHITE)
        screen.blit(score_display, (WIDTH // 2 - 19, 10))

        # Linea del centro
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

        # Actualizar la pantalla
        pygame.display.update()

    # Salir de Pygame
    pygame.quit()

if __name__ == "__main__":
    main()