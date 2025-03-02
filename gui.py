import pygame
import configuration as config

pygame.font.init()
font = pygame.font.SysFont(None, 24)


def draw_rounded_rect(surface, color, rect, corner_radius):
    """Draw a rectangle with rounded corners."""
    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(
        circle, [int(min(rect.size) * corner_radius)] * 2
    )

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)


def render_ui(screen):
    toggle_button = {
        "rect": pygame.Rect(10, 10, 140, 35),
        "color": (0, 255, 255),
        "text": "Show Buttons" if not render_ui.show_buttons else "Hide Buttons",
    }

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    draw_rounded_rect(screen, (128, 128, 128), toggle_button["rect"], 0.3)
    draw_rounded_rect(screen, toggle_button["color"], toggle_button["rect"], 0.3)
    text_surface = font.render(toggle_button["text"], True, (0, 0, 0))
    screen.blit(text_surface, (toggle_button["rect"].x + 10, toggle_button["rect"].y + 10))

    if toggle_button["rect"].collidepoint(mouse_pos) and mouse_click[0] and not render_ui.button_pressed:
        toggle_buttons()
        render_ui.button_pressed = True
    elif not mouse_click[0]:
        render_ui.button_pressed = False

    if not render_ui.show_buttons:
        return

    buttons = [
        {
            "rect": pygame.Rect(10, 50, 140, 35),
            "color": (0, 255, 0) if config.RENDER_PREDICTION else (255, 0, 0),
            "config_attr": "RENDER_PREDICTION",
            "text": "Show Future",
        },
        {
            "rect": pygame.Rect(10, 90, 140, 35),
            "color": (0, 255, 0) if config.RENDER_NODES else (255, 0, 0),
            "config_attr": "RENDER_NODES",
            "text": "Show Nodes",
        },
        {
            "rect": pygame.Rect(10, 130, 140, 35),
            "color": (0, 255, 0) if config.RENDER_EDGES else (255, 0, 0),
            "config_attr": "RENDER_EDGES",
            "text": "Show Edges",
        },
        {
            "rect": pygame.Rect(10, 170, 140, 35),
            "color": (0, 255, 0) if config.RENDER_STANDS else (255, 0, 0),
            "config_attr": "RENDER_STANDS",
            "text": "Show Stands",
        },
        {
            "rect": pygame.Rect(10, 210, 140, 35),
            "color": (0, 255, 0) if config.RENDER_DATA else (255, 0, 0),
            "config_attr": "RENDER_DATA",
            "text": "Show Data",
        },
        {
            "rect": pygame.Rect(10, 250, 140, 35),
            "color": (0, 255, 0) if config.NORMAL_SPEED else (255, 0, 0),
            "config_attr": "NORMAL_SPEED",
            "text": "Normal Speed",
        },
    ]

    for button in buttons:
        draw_rounded_rect(screen, (128, 128, 128), button["rect"], 0.3)
        draw_rounded_rect(screen, button["color"], button["rect"], 0.3)
        text_surface = font.render(button["text"], True, (0, 0, 0))
        screen.blit(text_surface, (button["rect"].x + 10, button["rect"].y + 10))

        if button["rect"].collidepoint(mouse_pos) and mouse_click[0] and not render_ui.button_pressed:
            setattr(config, button["config_attr"], not getattr(config, button["config_attr"]))
            render_ui.button_pressed = True
        elif not mouse_click[0]:
            render_ui.button_pressed = False


render_ui.button_pressed = False
render_ui.show_buttons = False


def toggle_buttons():
    render_ui.show_buttons = not render_ui.show_buttons
