import pygame

def main():
    # Initializing pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint - Practice 10")
    clock = pygame.time.Clock()
    
    # Basic settings and variables
    radius = 15
    current_color = (0, 0, 255) # Default color is Blue
    mode = 'brush' # Available modes: brush, rect, circle, eraser
    
    # List to store all drawn objects to keep them on screen
    # Format: (type, color, position/dimensions, radius/thickness)
    objects = []
    
    drawing = False
    start_pos = None
    
    # Setting up font for UI display
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 18)

    while True:
        # Fill screen with white background each frame
        screen.fill((255, 255, 255))
        
        for event in pygame.event.get():
            # Handle window close
            if event.type == pygame.QUIT:
                return

            # 4. Color selection via keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: current_color = (255, 0, 0) # Red
                elif event.key == pygame.K_g: current_color = (0, 255, 0) # Green
                elif event.key == pygame.K_b: current_color = (0, 0, 255) # Blue
                elif event.key == pygame.K_k: current_color = (0, 0, 0)   # Black
                
                # Switch between tools
                if event.key == pygame.K_1: mode = 'brush'     # Brush tool
                elif event.key == pygame.K_2: mode = 'rect'    # 1. Rectangle tool
                elif event.key == pygame.K_3: mode = 'circle'  # 2. Circle tool
                elif event.key == pygame.K_4: mode = 'eraser'  # 3. Eraser tool

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                # For brush and eraser, start adding points immediately
                if mode == 'brush' or mode == 'eraser':
                    # Eraser is essentially a white brush
                    color_to_use = (255, 255, 255) if mode == 'eraser' else current_color
                    objects.append(('point', color_to_use, event.pos, radius))

            # Handle mouse movement while button is pressed
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == 'brush' or mode == 'eraser':
                        color_to_use = (255, 255, 255) if mode == 'eraser' else current_color
                        objects.append(('point', color_to_use, event.pos, radius))

            # Handle mouse button release to finalize shapes
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_pos = event.pos
                    # 1. Logic for drawing rectangle
                    if mode == 'rect':
                        rect_coords = (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), 
                                       abs(start_pos[0] - end_pos[0]), abs(start_pos[1] - end_pos[1]))
                        objects.append(('rect', current_color, rect_coords))
                    # 2. Logic for drawing circle
                    elif mode == 'circle':
                        # Calculate radius using distance formula
                        r = int(((start_pos[0]-end_pos[0])**2 + (start_pos[1]-end_pos[1])**2)**0.5)
                        objects.append(('circle', current_color, start_pos, r))
                    drawing = False

        # Redraw all saved objects from the list
        for obj in objects:
            obj_type, obj_color = obj[0], obj[1]
            if obj_type == 'point':
                pygame.draw.circle(screen, obj_color, obj[2], obj[3])
            elif obj_type == 'rect':
                pygame.draw.rect(screen, obj_color, obj[2], 2) # Thickness = 2
            elif obj_type == 'circle':
                pygame.draw.circle(screen, obj_color, obj[2], obj[3], 2)

        # Draw a preview of the shape while the user is still dragging the mouse
        if drawing:
            curr_pos = pygame.mouse.get_pos()
            if mode == 'rect':
                temp_rect = (min(start_pos[0], curr_pos[0]), min(start_pos[1], curr_pos[1]), 
                             abs(start_pos[0] - curr_pos[0]), abs(start_pos[1] - curr_pos[1]))
                pygame.draw.rect(screen, current_color, temp_rect, 2)
            elif mode == 'circle':
                temp_r = int(((start_pos[0]-curr_pos[0])**2 + (start_pos[1]-curr_pos[1])**2)**0.5)
                pygame.draw.circle(screen, current_color, start_pos, temp_r, 2)

        # UI Instructions on screen
        instructions = font.render(f"Tool: {mode} | Color: {current_color} | Keys: 1-Brush, 2-Rect, 3-Circle, 4-Eraser", True, (100, 100, 100))
        screen.blit(instructions, (10, 10))

        # Update display and maintain 60 FPS
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
