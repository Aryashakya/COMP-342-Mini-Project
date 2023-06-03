import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *


# Ball properties
class Ball:
    def __init__(self, radius, position, velocity):
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.color = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]


# Window dimensions
window_width = 800
window_height = 600

# List of balls
balls = [
    Ball(0.1, [-0.3, 0.0], [0.3, 0.5]),
    Ball(0.08, [0.4, 0.3], [-0.2, -0.3]),
    Ball(0.07, [-0.4, -0.4], [0.7, -0.2]),
    Ball(0.09, [-0.8, -0.4], [0.4, -0.2]),
    Ball(0.06, [-0.1, -0.7], [0.4, -0.2]),
    Ball(0.05, [0.5, 0.7], [0.4, 0.2]),
]


def update_ball_position(ball, delta_time):
    # Update ball position based on velocity and time
    ball.position[0] += ball.velocity[0] * delta_time
    ball.position[1] += ball.velocity[1] * delta_time

    # Check collision with window edges
    if ball.position[0] - ball.radius < -1.0 or ball.position[0] + ball.radius > 1.0:
        ball.velocity[0] *= -1.0  # Reverse horizontal velocity
    if ball.position[1] - ball.radius < -1.0 or ball.position[1] + ball.radius > 1.0:
        ball.velocity[1] *= -1.0  # Reverse vertical velocity


def handle_ball_collision(ball1, ball2):
    # Calculate the distance between the centers of the balls
    dx = ball2.position[0] - ball1.position[0]
    dy = ball2.position[1] - ball1.position[1]
    distance = math.sqrt(dx**2 + dy**2)

    # Check if the balls collide
    if distance < ball1.radius + ball2.radius:
        # Calculate the collision normal
        normal_x = dx / distance
        normal_y = dy / distance

        # Calculate the relative velocity
        relative_velocity_x = ball2.velocity[0] - ball1.velocity[0]
        relative_velocity_y = ball2.velocity[1] - ball1.velocity[1]

        # Calculate the dot product of the relative velocity and the collision normal
        dot_product = (relative_velocity_x * normal_x) + (
            relative_velocity_y * normal_y
        )

        # Apply the collision response
        collision_impulse_x = (2.0 * ball2.radius * dot_product * normal_x) / (
            ball1.radius + ball2.radius
        )
        collision_impulse_y = (2.0 * ball2.radius * dot_product * normal_y) / (
            ball1.radius + ball2.radius
        )

        ball1.velocity[0] += collision_impulse_x
        ball1.velocity[1] += collision_impulse_y
        ball2.velocity[0] -= collision_impulse_x
        ball2.velocity[1] -= collision_impulse_y


def update_frame(value):
    delta_time = 0.01  # Time step
    for i in range(len(balls)):
        update_ball_position(balls[i], delta_time)
        # Check collision with other balls
        for j in range(i + 1, len(balls)):
            handle_ball_collision(balls[i], balls[j])
    glutPostRedisplay()
    glutTimerFunc(
        10, update_frame, 0
    )  # Schedule next frame update after 10 milliseconds


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    for ball in balls:
        glPushMatrix()
        glTranslatef(ball.position[0], ball.position[1], 0.0)

        # Render the ball
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(ball.color[0], ball.color[1], ball.color[2])  # Red color
        glVertex2f(0.0, 0.0)  # Center vertex

        num_segments = 100
        for i in range(num_segments + 1):
            angle = 2.0 * math.pi * (i / num_segments)
            x = ball.radius * math.cos(angle)
            y = ball.radius * math.sin(angle)
            glVertex2f(x, y)
        glEnd()

        glPopMatrix()

    glFlush()


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)


# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow("Elastic Collision Mini Project")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(0, update_frame, 0)

    glClearColor(1.0, 1.0, 1.0, 1.0)  # Set clear color to white

    glutMainLoop()


if __name__ == "__main__":
    main()
