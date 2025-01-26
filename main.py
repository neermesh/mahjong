import pygame
import random
from collections import defaultdict

# Initialize Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mahjong Solitaire")
clock = pygame.time.Clock()

# Tile settings
tile_width = 64
tile_height = 32

class Tile:
    def __init__(self, layer, x, tile_type):
        self.layer = layer
        self.x = x
        self.tile_type = tile_type
        self.removed = False
        self.left = None
        self.right = None
        self.covering_tiles = []

    def is_free(self):
        if any(not t.removed for t in self.covering_tiles):
            return False
        left_ok = self.left is None or self.left.removed
        right_ok = self.right is None or self.right.removed
        return left_ok or right_ok

# Create layers and tiles
layers = []
layer0 = [Tile(0, x, None) for x in range(4)]  # Layer 0: 4 tiles
layer1 = [Tile(1, x, None) for x in range(2)]  # Layer 1: 2 tiles
layers.extend([layer0, layer1])

# Assign covering tiles and neighbors
for tile in layer0[:2]:
    tile.covering_tiles.append(layer1[0])
for tile in layer0[2:]:
    tile.covering_tiles.append(layer1[1])

layer0[0].right = layer0[1]
layer0[1].left, layer0[1].right = layer0[0], layer0[2]
layer0[2].left, layer0[2].right = layer0[1], layer0[3]
layer0[3].left = layer0[2]

layer1[0].right = layer1[1]
layer1[1].left = layer1[0]

# Assign tile types
all_tiles = [tile for layer in layers for tile in layer]
tile_types = ['A', 'A', 'B', 'B', 'C', 'C']
random.shuffle(tile_types)
for i, tile in enumerate(all_tiles):
    tile.tile_type = tile_types[i]

# Colors
colors = {'A': (255,0,0), 'B': (0,255,0), 'C': (0,0,255)}
selected_color = (255, 165, 0)

def get_position(tile):
    layer_width = len(layers[tile.layer]) * tile_width
    start_x = (screen_width - layer_width) // 2
    return (start_x + tile.x * tile_width, 100 + tile.layer * tile_height * 2)

selected_tiles = []
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_tile = None
            for layer in reversed(layers):
                for tile in layer:
                    if not tile.removed and tile.is_free():
                        x, y = get_position(tile)
                        if pygame.Rect(x, y, tile_width, tile_height).collidepoint(mouse_pos):
                            clicked_tile = tile
                            break
                if clicked_tile: break
            if clicked_tile:
                if clicked_tile in selected_tiles:
                    selected_tiles.remove(clicked_tile)
                else:
                    selected_tiles.append(clicked_tile)
                    if len(selected_tiles) == 2:
                        t1, t2 = selected_tiles
                        if t1.tile_type == t2.tile_type:
                            t1.removed = t2.removed = True
                        selected_tiles = []

    # Win/Lose conditions
    if all(t.removed for t in all_tiles):
        print("You win!")
        running = False
    free_tiles = [t for t in all_tiles if not t.removed and t.is_free()]
    type_counts = defaultdict(int)
    for t in free_tiles: type_counts[t.tile_type] += 1
    if not any(c >=2 for c in type_counts.values()) and not all(t.removed for t in all_tiles):
        print("You lose!")
        running = False

    # Draw
    screen.fill((0,0,0))
    for layer in layers:
        for tile in layer:
            if not tile.removed:
                x, y = get_position(tile)
                color = colors.get(tile.tile_type, (255,255,255))
                pygame.draw.rect(screen, color, (x, y, tile_width, tile_height))
                if tile in selected_tiles:
                    pygame.draw.rect(screen, selected_color, (x, y, tile_width, tile_height), 3)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()