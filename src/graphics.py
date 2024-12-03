from core import (
    Blue,
    CleanBoard,
    CollapseBoard,
    CollapsingGame,
    Counter,
    Crash,
    CrashBoard,
    Down,
    Empty,
    Esc,
    Exploding,
    ExplodingGame,
    Game,
    Action,
    Green,
    Init,
    Left,
    Move,
    NextTurn,
    Play,
    End,
    Idle,
    Playing,
    Board,
    Gem,
    Normal,
    PowerGem,
    Color,
    Red,
    Restart,
    Right,
    Rotate,
    GenerateCounterGems,
    Up,
    UpdateCounterGems,
    Yellow,
    Position,
    GemPair,
    update,
)
import pygame
from pygame.surface import Surface
from pygame.font import Font
import sys

keypressed: dict[int, bool] = dict()


def view(surface: Surface, font: Font, game: Game) -> Action:
    match game:
        case Init():
            return Play()

        case Playing():
            action = Idle()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keypressed[event.key] = True
                elif event.type == pygame.KEYUP:
                    keypressed[event.key] = False

                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN
                    and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
                ):
                    action = Esc()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    action = CrashBoard()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    action = CleanBoard()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                    action = UpdateCounterGems()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    action = CollapseBoard()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    action = Restart()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    action = Rotate(Left())
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    action = Rotate(Right())
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    action = NextTurn()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    action = GenerateCounterGems()

            if keypressed.get(pygame.K_UP):
                action = Move(Up())
            elif keypressed.get(pygame.K_RIGHT):
                action = Move(Right())
            elif keypressed.get(pygame.K_DOWN):
                action = Move(Down())
            elif keypressed.get(pygame.K_LEFT):
                action = Move(Left())

            renderPlaying(surface, font, game)

            return action

        case ExplodingGame(playing):
            renderPlaying(surface, font, playing)

            return Idle()

        case CollapsingGame(playing):
            renderPlaying(surface, font, playing)

            return Idle()

        case End(playing):
            action = Idle()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN
                    and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
                ):
                    action = Esc()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    action = Restart()

            renderPlaying(surface, font, playing)
            renderEnd(surface, font)

            return action


SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600


def run(game: Game) -> None:
    pygame.init()

    pygame.display.set_caption("ESC to Quit spf2t")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    clock = pygame.time.Clock()
    time_accumulator = 0

    while True:
        dt = clock.tick(15)

        if isinstance(game, Playing):
            time_accumulator += dt

        screen.fill((0, 0, 0))

        match view(screen, font, game):
            case Esc():
                break

            # Check if 1 second has passed and simulate the down move
            case _ if isinstance(game, Playing) and time_accumulator >= 1000:
                game = update(game, Move(Down()))
                time_accumulator = 0

            case CollapseBoard():
                game = update(game, CollapseBoard())
                time_accumulator = 0

            case action:
                game = update(game, action)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


# utils

GEM_WIDTH, GEM_HEIGHT, GEM_RADIUS = 30, 33, 2
OFFSET_BOARD_X, OFFSET_BOARD_Y, BOARD_GAP, BOARD_BORDER = 40, 50, 1, 3
DEBUG = True


def renderGem(surface: Surface, font: Font, gem: Gem, position: Position) -> None:
    xx, yy = position
    x = OFFSET_BOARD_X + (xx * GEM_WIDTH) + (xx * BOARD_GAP)
    y = OFFSET_BOARD_Y + (yy * GEM_HEIGHT) + (yy * BOARD_GAP)

    match gem:
        case Normal(color):
            pygame.draw.rect(
                surface,
                getColorValue(color),
                pygame.Rect(x, y, GEM_WIDTH, GEM_HEIGHT),
                border_radius=GEM_RADIUS,
            )

        case Crash(color):
            colorValue = getColorValue(color)

            pygame.draw.circle(
                surface,
                colorValue,
                (x + (GEM_WIDTH // 2), y + (GEM_HEIGHT // 2)),
                GEM_WIDTH // 2,
                width=2,
            )
            pygame.draw.circle(
                surface,
                colorValue,
                (x + (GEM_WIDTH // 2), y + (GEM_HEIGHT // 2)),
                GEM_WIDTH // 6,
            )

        case Counter(color, counter):
            colorValue = getColorValue(color)

            pygame.draw.rect(
                surface,
                colorValue,
                pygame.Rect(x, y, GEM_WIDTH, GEM_HEIGHT),
                width=1,
                border_radius=GEM_RADIUS,
            )

            text = font.render(str(counter), True, colorValue)
            textRect = text.get_rect()
            textRect.center = ((x + (GEM_WIDTH // 2)), (y + (GEM_HEIGHT // 2)))

            surface.blit(text, textRect)

        case PowerGem():
            color_top = (255, 182, 193)  # Light pink
            color_bottom = (255, 229, 153)  # Light orange

            cx, cy = ((x + (GEM_WIDTH // 2)), (y + (GEM_HEIGHT // 2)))

            # Key points for the diamond
            mid_top_left = (
                cx - GEM_WIDTH // 4,
                cy - GEM_HEIGHT // 2,
            )  # Top left of the trapezoid
            mid_top_right = (
                cx + GEM_WIDTH // 4,
                cy - GEM_HEIGHT // 2,
            )  # Top right of the trapezoid
            mid_bottom_left = (
                cx - GEM_WIDTH // 2,
                cy - (GEM_HEIGHT // 5),
            )  # Bottom left of the diamond
            mid_bottom_right = (
                cx + GEM_WIDTH // 2,
                cy - (GEM_HEIGHT // 5),
            )  # Bottom right of the diamond
            bottom_point = (cx, cy + GEM_HEIGHT // 2)  # Bottom of the diamond

            # Lower triangle
            lower_triangle = [mid_bottom_left, mid_bottom_right, bottom_point]

            pygame.draw.polygon(surface, color_bottom, lower_triangle)

            pygame.draw.polygon(
                surface,
                color_top,
                [mid_top_left, mid_top_right, mid_bottom_right, mid_bottom_left],
            )

        case Exploding(gem, _chainable, _chainCounter):
            renderGem(surface, font, gem, position)

            # this is for DEBUG purposes

            # font.set_strikethrough(True)
            # text = font.render(str(_chainCounter), True, (255, 255, 255))
            # font.set_strikethrough(False)
            # textRect = text.get_rect()
            # textRect.center = ((x + (GEM_WIDTH // 2)), (y + (GEM_HEIGHT // 2)))

            # surface.blit(text, textRect)


def renderBoard(surface: Surface, font: Font, board: Board) -> None:
    # grid
    for rows, y in zip(board.grid, range(board.height)):
        for gem, x in zip(rows, range(board.width)):
            if not isinstance(gem, Empty):
                renderGem(
                    surface,
                    font,
                    gem,
                    (
                        x,
                        y,
                    ),
                )

    # border
    pygame.draw.rect(
        surface,
        (128, 128, 128),
        pygame.Rect(
            (OFFSET_BOARD_X - BOARD_BORDER - BOARD_GAP),
            (OFFSET_BOARD_Y - BOARD_BORDER - BOARD_GAP),
            (GEM_WIDTH * board.width)
            + (BOARD_GAP * board.width)
            + (BOARD_BORDER * 2)
            + BOARD_GAP,
            (GEM_HEIGHT * board.height)
            + (BOARD_GAP * board.height)
            + (BOARD_BORDER * 2)
            + BOARD_GAP,
        ),
        width=BOARD_BORDER,
        border_radius=GEM_RADIUS,
    )


def renderNext(surface: Surface, font: Font, next: GemPair, boardWidth: int) -> None:
    (pivotGem, rotationGem) = next

    text = font.render("NEXT", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (
        (
            OFFSET_BOARD_X
            + ((boardWidth + 1) * GEM_WIDTH)
            + ((boardWidth + 1) * BOARD_GAP)
            + (GEM_WIDTH // 2)
        ),
        OFFSET_BOARD_Y - (textRect.height // 2) - 4,
    )

    surface.blit(text, textRect)

    renderGem(
        surface,
        font,
        pivotGem,
        (
            boardWidth + 1,
            1,
        ),
    )

    renderGem(
        surface,
        font,
        rotationGem,
        (
            boardWidth + 1,
            0,
        ),
    )


def renderTurn(surface: Surface, font: Font, boardWidth: int, turnNumber: int) -> None:
    # Label text
    text = font.render("TURN", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (
        (
            OFFSET_BOARD_X
            + ((boardWidth + 1) * GEM_WIDTH)
            + ((boardWidth + 1) * BOARD_GAP)
            + (GEM_WIDTH // 2)
        ),
        OFFSET_BOARD_Y
        + ((7) * GEM_WIDTH)
        + ((7) * BOARD_GAP)
        - (textRect.height // 2)
        - 4,
    )

    surface.blit(text, textRect)

    # Number text

    text2 = font.render(str(turnNumber), True, (255, 255, 255))
    textRect2 = text2.get_rect()
    textRect2.center = (
        (
            OFFSET_BOARD_X
            + ((boardWidth + 1) * GEM_WIDTH)
            + ((boardWidth + 1) * BOARD_GAP)
            + (GEM_WIDTH // 2)
        ),
        OFFSET_BOARD_Y
        + ((8) * GEM_WIDTH)
        + ((8) * BOARD_GAP)
        - (textRect2.height // 2)
        - 4,
    )

    surface.blit(text2, textRect2)


def renderIncoming(
    surface: Surface, font: Font, boardWidth: int, incoming: int
) -> None:
    # Label text
    text = font.render("COMING", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (
        (
            OFFSET_BOARD_X
            + ((boardWidth + 1) * GEM_WIDTH)
            + ((boardWidth + 1) * BOARD_GAP)
            + (GEM_WIDTH // 2)
        ),
        OFFSET_BOARD_Y
        + ((4) * GEM_WIDTH)
        + ((4) * BOARD_GAP)
        - (textRect.height // 2)
        - 4,
    )

    surface.blit(text, textRect)

    # Number text

    text2 = font.render(str(incoming), True, (255, 255, 255))
    textRect2 = text2.get_rect()
    textRect2.center = (
        (
            OFFSET_BOARD_X
            + ((boardWidth + 1) * GEM_WIDTH)
            + ((boardWidth + 1) * BOARD_GAP)
            + (GEM_WIDTH // 2)
        ),
        OFFSET_BOARD_Y
        + ((5) * GEM_WIDTH)
        + ((5) * BOARD_GAP)
        - (textRect2.height // 2)
        - 4,
    )

    surface.blit(text2, textRect2)


def renderPlaying(surface: Surface, font: Font, playing: Playing) -> None:
    renderBoard(surface, font, playing.board)
    renderNext(surface, font, playing.next, playing.board.width)
    renderTurn(surface, font, playing.board.width, playing.turnNumber)
    renderIncoming(surface, font, playing.board.width, len(playing.incoming))


def renderEnd(surface: Surface, font: Font) -> None:
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 128))
    surface.blit(overlay, (0, 0))

    text_surface = font.render(
        "Press Esc/q to exit or R to restart", True, (255, 255, 255)
    )
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    surface.blit(text_surface, text_rect)


def getColorValue(color: Color) -> tuple[int, int, int]:
    match color:
        case Red():
            return (255, 0, 0)

        case Green():
            return (0, 255, 0)

        case Blue():
            return (0, 0, 255)

        case Yellow():
            return (255, 255, 0)
