import pygame
import math
import random

pygame.init()

font20 = pygame.font.Font('freesansbold.ttf', 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

WIDTH, HEIGHT = 1000, 1000
BLOCK_WIDTH = WIDTH // 20
BLOCK_HEIGHT = HEIGHT // 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pathfinding')

clock = pygame.time.Clock()


class Grid():
    def __init__(self, has_block):
        self.path_node_list = []

        for x in range(BLOCK_WIDTH):
            for y in range(BLOCK_HEIGHT):
                path_node = PathNode(x, y)
                self.path_node_list.append(path_node)

        if (has_block):
            self.create_block()


    def create_block(self): 
        for _ in range(random.randint(20, 50)):   
            start_point_m = random.randint(0, max(BLOCK_WIDTH, BLOCK_HEIGHT))
            start_point_n = random.randint(0, max(BLOCK_WIDTH, BLOCK_HEIGHT))
            if (random.random() > 0.5):
                for i in range(start_point_n, start_point_n + random.randint(3, 15)):
                    node = self.get_node(start_point_m, i)
                    if (node is not None):
                        self.path_node_list.remove(node)
                for i in range(start_point_n, start_point_n + random.randint(3, 15)):
                    node = self.get_node(i, start_point_m)
                    if (node is not None):
                        self.path_node_list.remove(node)
                

    def display_walkable(self):
        for path_node in self.path_node_list:
            path_node.display(CYAN, True)


    def get_node(self, x, y):
        for path_node in self.path_node_list:
            if x == path_node.x and y == path_node.y:
                return path_node
        return None
    

    def get_min_f_cost_node_in_open_node_list(self, open_node_list):
        min_f_cost_path_node = open_node_list[0]

        for path_node in open_node_list:
            if path_node.f_cost < min_f_cost_path_node.f_cost:
                 min_f_cost_path_node = path_node
        return min_f_cost_path_node
    

    def get_neighbor_node_list(self, current_node):
        neighbor_node_list = []
        for x in range(current_node.x - 1, current_node.x + 2, 1):
            for y in range(current_node.y - 1, current_node.y + 2, 1):
                if (x == current_node.x and y == current_node.y):
                    continue
                if (0 <= x < BLOCK_WIDTH and 0 <= y < BLOCK_HEIGHT):
                    if (self.get_node(x, y) is not None):
                        neighbor_node_list.append(self.get_node(x, y))
        return neighbor_node_list
    

    def get_distance(self, node_A, node_B):
        delta_x = abs(node_A.x - node_B.x)
        delta_y = abs(node_A.y - node_B.y)
        remaining = abs(delta_x - delta_y)
        return min(delta_x, delta_y) * 14 + remaining * 10
    
    
    def way_point_node_list(self, end_node):
        node_list = []
        current_node = end_node

        while current_node is not None:
            node_list.append(current_node)
            current_node = current_node.came_from_path_node
        node_list.reverse()
        return node_list;


    def reset(self):
        for path_node in self.path_node_list:
            path_node.reset()


    def pathfinding(self, start_node, end_node):
        self.reset()  
        open_node_list = []
        closed_node_list = []

        start_node.g_cost = 0
        start_node.h_cost = self.get_distance(start_node, end_node)
        start_node.f_cost = start_node.g_cost + start_node.f_cost
        open_node_list.append(start_node)

        while len(open_node_list) > 0:
            current_node = self.get_min_f_cost_node_in_open_node_list(open_node_list)

            if current_node == end_node:
                return self.way_point_node_list(end_node)

            open_node_list.remove(current_node)
            closed_node_list.append(current_node)

            for neighbor_node in self.get_neighbor_node_list(current_node):
                if neighbor_node in closed_node_list:
                    continue

                tentative_g_cost = current_node.g_cost + self.get_distance(current_node, neighbor_node)

                if tentative_g_cost < neighbor_node.g_cost:
                    neighbor_node.g_cost = tentative_g_cost
                    neighbor_node.h_cost = self.get_distance(neighbor_node, end_node)
                    neighbor_node.f_cost = neighbor_node.g_cost + neighbor_node.h_cost
                    neighbor_node.came_from_path_node = current_node

                    if neighbor_node not in open_node_list:
                        open_node_list.append(neighbor_node)
        return None


class PathNode():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.came_from_path_node = None
        self.g_cost = math.inf
        self.h_cost = 0
        self.f_cost = self.g_cost + self.h_cost

    def display(self, color, is_fill):
        block_rect = pygame.Rect(self.x * 20, self.y * 20, 20, 20)
        if is_fill:
            pygame.draw.rect(screen, color, block_rect)
        else:
            pygame.draw.rect(screen, color, block_rect, 1)

    def display_text(self, txt):
        text = font20.render(txt, True, RED)
        textRect = text.get_rect()
        textRect.center = (self.x * 20 + 10, self.y * 20 + 10)
        screen.blit(text, textRect)

    def reset(self):
        self.came_from_path_node = None
        self.g_cost = math.inf
        self.h_cost = 0
        self.f_cost = self.g_cost + self.h_cost


def main():
    running = True
    FPS = 60

    grid = Grid(has_block=True)
    path = None

    while running:
        screen.fill(BLACK)

        grid.display_walkable()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False              
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_node = None
                end_node = None
                while (start_node == None or end_node == None):
                    start_position = {'x': random.randint(0, BLOCK_WIDTH - 1), 'y' : random.randint(0, BLOCK_HEIGHT - 1)}
                    end_position = {'x': random.randint(0, BLOCK_WIDTH - 1), 'y' : random.randint(0, BLOCK_HEIGHT - 1)}

                    start_node = grid.get_node(start_position['x'], start_position['y'])
                    end_node = grid.get_node(end_position['x'], end_position['y'])

                path = grid.pathfinding(start_node, end_node)       
                
        if path is not None:
            for way_path_node in path:
                way_path_node.display(GREEN, True)

                if (way_path_node == start_node):
                    way_path_node.display_text('S')
                elif (way_path_node == end_node):
                    way_path_node.display_text('F')
                

        for path_node in grid.path_node_list:
            path_node.display(WHITE, False)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
    pygame.quit()