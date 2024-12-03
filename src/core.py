from dataclasses import dataclass
import random
# import datetime

random.seed()

"""
data Color
  = Red
  | Green
  | Blue
  | Yellow
"""


@dataclass
class Red:
    pass


@dataclass
class Green:
    pass


@dataclass
class Blue:
    pass


@dataclass
class Yellow:
    pass


Color = Red | Green | Blue | Yellow

"""
data Gem
  = Normal { color: Color }
  | Crash { color: Color }
  | Counter { color: Color, counter: int }
  | PowerGem
  | Exploding { gem: Normal | Crash | Counter | PowerGem, chainable: bool, chainCounter: int }
"""


@dataclass
class Normal:
    color: Color


@dataclass
class Crash:
    color: Color


@dataclass
class Counter:
    color: Color
    counter: int


@dataclass
class PowerGem:
    pass


@dataclass
class Exploding:
    gem: Normal | Crash | Counter | PowerGem
    chainable: bool
    chainCounter: int


Gem = Normal | Crash | Counter | PowerGem | Exploding

"""
data Empty = Empty
"""


@dataclass
class Empty:
    pass


# TODO: rector this so its also IndexError

"""
type BoardValue = Empty | Gem
"""

BoardValue = Empty | Gem

"""
data Board = Board {
  width: int,
  height: int,
  grid: [[BoardValue]]
}
"""


@dataclass
class Board:
    width: int
    height: int
    grid: list[list[BoardValue]]


"""
type XAxis = int
"""

XAxis = int

"""
type YAxis = int
"""

YAxis = int

"""
type Position = (XAxis, YAxis)
"""

Position = tuple[XAxis, YAxis]

"""
type Block = [Position]
"""

Block = list[Position]

"""
type GemPair = (Gem, Gem)
"""

GemPair = tuple[Gem, Gem]

"""
data CDirection
  = Up
  | Right
  | Down
  | Left
"""


@dataclass(frozen=True)
class Up:
    pass


@dataclass(frozen=True)
class Right:
    pass


@dataclass(frozen=True)
class Down:
    pass


@dataclass(frozen=True)
class Left:
    pass


CDirection = Up | Right | Down | Left

"""
data XDirection
  = UpRight
  | DownRight
  | DownLeft
  | UpLeft
"""


@dataclass(frozen=True)
class UpRight:
    pass


@dataclass(frozen=True)
class DownRight:
    pass


@dataclass(frozen=True)
class DownLeft:
    pass


@dataclass(frozen=True)
class UpLeft:
    pass


XDirection = UpRight | DownRight | DownLeft | UpLeft


"""
type Direction = CDirection | XDirection
"""

Direction = CDirection | XDirection


"""
data GameStatus
  = Turn
"""


@dataclass
class Turn:
    pass


GameStatus = Turn

"""
data CollapsingType = RowByRowFast | BlockSlow
"""


@dataclass
class RowByRowFast:
    pass


class BlockSlow:
    pass


CollapsingType = RowByRowFast | BlockSlow

# TODO: add:
# max chain reaction
# max chain combo
# max power gem
# score

"""
data Game
  = Init
  | Playing {
    board: Board,
    current: Block,
    next: GemPair,
    incoming: [(Counter, Position)],
    status: GameStatus
    turnNumber: int
  }
  | ExplodingGame { playing: Playing }
  | CollapsingGame { playing: Playing, collapsingType: CollapsingType }
  | End { playing: Playing }
"""


@dataclass
class Init:
    pass


@dataclass
class Playing:
    board: Board
    current: Block
    next: GemPair
    incoming: list[tuple[Counter, Position]]
    status: GameStatus
    turnNumber: int


@dataclass
class ExplodingGame:
    playing: Playing


@dataclass
class CollapsingGame:
    playing: Playing
    collapsingType: CollapsingType


@dataclass
class End:
    playing: Playing


Game = Init | Playing | ExplodingGame | CollapsingGame | End

# update

"""
data Action
  = Idle
  | Esc
  | Play
  | Move { direction: CDirection }
  | Rotate { direction: Left | Right }
  | EndTurn
  | CrashBoard
  | CleanBoard
  | CollapseBoard
  | Restart
  | NextTurn
  | UpdateCounterGems
  | GenerateCounterGems
  | SendCounterGems
"""


@dataclass
class Idle:
    pass


@dataclass
class Esc:
    pass


@dataclass
class Play:
    pass


@dataclass
class Move:
    direction: CDirection


@dataclass
class Rotate:
    direction: Left | Right


@dataclass
class EndTurn:
    pass


@dataclass
class CrashBoard:
    pass


@dataclass
class CleanBoard:
    pass


@dataclass
class CollapseBoard:
    pass


@dataclass
class Restart:
    pass


@dataclass
class NextTurn:
    pass


@dataclass
class UpdateCounterGems:
    pass


@dataclass
class GenerateCounterGems:
    pass


@dataclass
class SendCounterGems:
    pass


Action = (
    Idle
    | Esc
    | Play
    | Move
    | Rotate
    | EndTurn
    | CrashBoard
    | CleanBoard
    | CollapseBoard
    | Restart
    | NextTurn
    | UpdateCounterGems
    | GenerateCounterGems
    | SendCounterGems
)


def update(game: Game, action: Action) -> Game:
    match game:
        case Init():
            return update(
                Playing(
                    board=emptyBoard(6, 13),
                    current=[],
                    next=randomGemPair(0),
                    incoming=[],
                    status=Turn(),
                    turnNumber=0,
                ),
                NextTurn(),
            )

        case Playing(board, current, next, incoming, status, turnNumber) as playing:
            match action:
                case CrashBoard():
                    board, powerGemCrashedGems = powerGemCrashBoard(board)
                    board, crashedGems = crashBoard(board)

                    if powerGemCrashedGems > 0 or crashedGems > 0:
                        return ExplodingGame(
                            Playing(
                                board,
                                current=current,
                                next=next,
                                incoming=incoming,
                                status=status,
                                turnNumber=turnNumber,
                            )
                        )

                    # before the Next turn we check if we need to generate counter gems
                    return update(playing, SendCounterGems())

                case CleanBoard():
                    return ExplodingGame(playing)

                case CollapseBoard():
                    return CollapsingGame(playing, RowByRowFast())

                case Restart():
                    return Init()

                case Move(direction):
                    pivotGemPosition, rotationGemPosition = current

                    if canMove(board, current, direction):
                        (pivotGemX, pivotGemY) = pivotGemPosition
                        pivotGem = board.grid[pivotGemY][pivotGemX]

                        (rotationGemX, rotationGemY) = rotationGemPosition
                        rotationGem = board.grid[rotationGemY][rotationGemX]

                        ##

                        newPivotGemPosition = getPosition(pivotGemPosition, direction)
                        newRotationGemPosition = getPosition(
                            rotationGemPosition, direction
                        )

                        ##

                        moveBoardItemForced(board, Empty(), pivotGemPosition)
                        moveBoardItemForced(board, Empty(), rotationGemPosition)

                        moveBoardItemForced(board, pivotGem, newPivotGemPosition)
                        moveBoardItemForced(board, rotationGem, newRotationGemPosition)

                        ##

                        pivotGemPosition = newPivotGemPosition
                        rotationGemPosition = newRotationGemPosition

                        return Playing(
                            board,
                            current=[pivotGemPosition, rotationGemPosition],
                            next=next,
                            incoming=incoming,
                            status=status,
                            turnNumber=turnNumber,
                        )

                    elif isinstance(direction, Down):
                        return CollapsingGame(
                            Playing(
                                board=updateCounterGems(board),
                                current=current,
                                next=next,
                                incoming=incoming,
                                status=status,
                                turnNumber=turnNumber,
                            ),
                            RowByRowFast(),
                        )

                    else:
                        return playing

                case Rotate(direction):
                    (pivotGemPosition, rotationGemPosition) = current

                    match (
                        direction,
                        directionFromPivot(pivotGemPosition, rotationGemPosition),
                    ):
                        case Left(), Up():
                            targetDirection = DownLeft()
                            # second attemp is calculated from pivot
                            secondAttempDirection = Right()
                        case Left(), Right():
                            targetDirection = UpLeft()
                            secondAttempDirection = Down()
                        case Left(), Down():
                            targetDirection = UpRight()
                            secondAttempDirection = Left()
                        case Left(), Left():
                            targetDirection = DownRight()
                            secondAttempDirection = Up()
                        case Right(), Up():
                            targetDirection = DownRight()
                            secondAttempDirection = Left()
                        case Right(), Right():
                            targetDirection = DownLeft()
                            secondAttempDirection = Up()
                        case Right(), Down():
                            targetDirection = UpLeft()
                            secondAttempDirection = Right()
                        case Right(), Left():
                            targetDirection = UpRight()
                            secondAttempDirection = Down()

                    if tmpBoard := moveGemBoard(
                        board, rotationGemPosition, targetDirection
                    ):
                        board = tmpBoard
                        rotationGemPosition = getPosition(
                            rotationGemPosition, targetDirection
                        )
                    # second attemp
                    elif isEmptyItem(
                        get(board, pivotGemPosition, secondAttempDirection)
                    ):
                        (pivotGemX, pivotGemY) = pivotGemPosition
                        pivotGem = board.grid[pivotGemY][pivotGemX]

                        (rotationGemX, rotationGemY) = rotationGemPosition
                        rotationGem = board.grid[rotationGemY][rotationGemX]

                        ##

                        newPivotGemPosition = getPosition(
                            pivotGemPosition, secondAttempDirection
                        )
                        newRotationGemPosition = getPosition(
                            getPosition(rotationGemPosition, targetDirection),
                            secondAttempDirection,
                        )

                        ##

                        moveBoardItemForced(board, Empty(), pivotGemPosition)
                        moveBoardItemForced(board, Empty(), rotationGemPosition)

                        moveBoardItemForced(board, pivotGem, newPivotGemPosition)
                        moveBoardItemForced(board, rotationGem, newRotationGemPosition)

                        ##

                        pivotGemPosition = newPivotGemPosition
                        rotationGemPosition = newRotationGemPosition
                    else:
                        # third attemp is a switch between gem positions
                        (pivotGemX, pivotGemY) = pivotGemPosition
                        pivotGem = board.grid[pivotGemY][pivotGemX]

                        (rotationGemX, rotationGemY) = rotationGemPosition
                        rotationGem = board.grid[rotationGemY][rotationGemX]

                        ##

                        newPivotGemPosition = rotationGemPosition
                        newRotationGemPosition = pivotGemPosition

                        ##

                        moveBoardItemForced(board, pivotGem, newPivotGemPosition)
                        moveBoardItemForced(board, rotationGem, newRotationGemPosition)

                        # pivotGemPosition = newPivotGemPosition
                        # rotationGemPosition = newRotationGemPosition

                    return Playing(
                        board,
                        current=[pivotGemPosition, rotationGemPosition],
                        next=next,
                        incoming=incoming,
                        status=status,
                        turnNumber=turnNumber,
                    )

                case NextTurn():
                    currentBlock = [(board.width // 2, 1), (board.width // 2, 0)]

                    # lose condition
                    if not all(
                        [isEmptyItem(get(board, position)) for position in currentBlock]
                    ):
                        return End(playing)

                    turnNumber = turnNumber + 1

                    # each 5 turns generate counter gems
                    if turnNumber % 5 == 0:
                        incoming = incoming + generateCounterGems(board, turnNumber)

                    (pivotGem, rotationGem) = next
                    ((pivotGemX, pivotGemY), (rotationGemX, rotationGemY)) = (
                        currentBlock
                    )

                    board.grid[pivotGemY][pivotGemX] = pivotGem
                    board.grid[rotationGemY][rotationGemX] = rotationGem

                    return Playing(
                        board,
                        current=currentBlock,
                        next=randomGemPair(turnNumber),
                        incoming=incoming,
                        status=status,
                        turnNumber=turnNumber,
                    )

                case UpdateCounterGems():
                    return update(
                        Playing(
                            board=updateCounterGems(board),
                            current=current,
                            next=next,
                            incoming=incoming,
                            status=status,
                            turnNumber=turnNumber,
                        ),
                        CrashBoard(),
                    )

                case SendCounterGems():
                    if len(incoming) > 0:
                        for gem, position in incoming:
                            moveBoardItemForced(board, gem, position)

                        return CollapsingGame(
                            Playing(
                                board,
                                current=current,
                                next=next,
                                incoming=[],
                                status=status,
                                turnNumber=turnNumber,
                            ),
                            BlockSlow(),
                        )

                    return update(playing, NextTurn())

                case Idle():
                    return playing

                case _:
                    raise ValueError(f"Unhandled action: {action}")

        case ExplodingGame(
            Playing(board, current, next, incoming, status, turnNumber) as playing
        ):
            match action:
                case Idle():
                    board, cleanedGems = cleanBoard(board)

                    if cleanedGems > 0:
                        return ExplodingGame(
                            Playing(
                                board,
                                current=current,
                                next=next,
                                incoming=incoming,
                                status=status,
                                turnNumber=turnNumber,
                            ),
                        )
                    else:
                        return CollapsingGame(playing, RowByRowFast())

                case _:
                    raise ValueError(f"Unhandled action: {action}")

        case CollapsingGame(
            Playing(board, current, next, incoming, status, turnNumber) as playing,
            collapsingType,
        ):
            match action:
                case Idle():
                    board, collapsedGems = collapseBoard(board, collapsingType)

                    if collapsedGems > 0:
                        return CollapsingGame(
                            Playing(
                                board,
                                current=current,
                                next=next,
                                incoming=incoming,
                                status=status,
                                turnNumber=turnNumber,
                            ),
                            collapsingType,
                        )
                    else:
                        return update(playing, CrashBoard())

                case _:
                    raise ValueError(f"Unhandled action: {action}")

        case End():
            match action:
                case Restart():
                    return Init()

                case Idle():
                    return game

                case _:
                    raise ValueError(f"Unhandled action: {action}")


# utils


def initGame() -> Game:
    return Init()


def randomGem() -> Gem:
    color = random.choice([Red(), Green(), Blue(), Yellow()])
    gem = random.choice(
        [Normal(color), Crash(color), Counter(color, random.randint(1, 5))]
    )
    return gem


def emptyBoard(width: int, height: int) -> Board:
    return Board(
        width, height, [[Empty() for _ in range(width)] for _ in range(height)]
    )


def randomBoard(width: int, height: int) -> Board:
    return Board(
        width,
        height,
        [
            [Empty(), Empty(), Empty(), Empty(), Empty(), Empty()],
            [Normal(Red()), Empty(), Empty(), Empty(), Empty(), Empty()],
            [Normal(Red()), Empty(), Empty(), Empty(), Empty(), Normal(Red())],
            [Normal(Red()), Empty(), Empty(), Empty(), Empty(), Normal(Red())],
            [
                Normal(Red()),
                Empty(),
                Empty(),
                Normal(Red()),
                Normal(Red()),
                Normal(Red()),
            ],
            [Normal(Red()), Empty(), Empty(), Empty(), Empty(), Normal(Red())],
            [Normal(Red()), Empty(), Empty(), Empty(), Empty(), Normal(Red())],
            [Normal(Red()), Empty(), Empty(), Empty(), Empty(), Normal(Red())],
            [Normal(Red()), Empty(), Empty(), Empty(), Empty(), Normal(Red())],
            [
                Counter(Red(), 2),
                Empty(),
                Empty(),
                Counter(Red(), 2),
                Empty(),
                Counter(Red(), 2),
            ],
            [
                Counter(Red(), 3),
                Empty(),
                Empty(),
                Counter(Red(), 3),
                Empty(),
                Counter(Red(), 3),
            ],
            [
                Counter(Red(), 4),
                Empty(),
                Empty(),
                Counter(Red(), 4),
                Empty(),
                Counter(Red(), 4),
            ],
            [
                Counter(Red(), 5),
                Empty(),
                Counter(Red(), 5),
                Counter(Red(), 5),
                Counter(Red(), 5),
                Counter(Red(), 5),
            ],
        ],
    )

    return Board(
        width, height, [[randomGem() for _ in range(width)] for _ in range(height)]
    )


def randomColor() -> Color:
    return random.choice(
        [Red(), Green(), Blue(), Yellow(), Red(), Green(), Blue(), Yellow()]
    )


def randomGemPair(turnNumber: int) -> GemPair:
    gemPair = (
        random.choice(  # provability of having a Crash gem 1/4
            [
                Crash(randomColor()),
                Normal(randomColor()),
                Normal(randomColor()),
                Normal(randomColor()),
                Normal(randomColor()),
            ]
        ),
        random.choice(  # provability of having a Crash gem 1/5
            [
                Normal(randomColor()),
                Normal(randomColor()),
                Normal(randomColor()),
                Normal(randomColor()),
                Crash(randomColor()),
            ]
        ),
    )

    if turnNumber > 0 and turnNumber % 25 == 0:
        _, rotationGem = gemPair
        return PowerGem(), rotationGem

    return gemPair


def getPosition(position: Position, direction: Direction) -> Position:
    prevX, prevY = position

    match direction:
        case Up():
            x, y = prevX, prevY - 1

        case Right():
            x, y = prevX + 1, prevY

        case Down():
            x, y = prevX, prevY + 1

        case Left():
            x, y = prevX - 1, prevY

        case UpRight():
            x, y = prevX + 1, prevY - 1

        case DownRight():
            x, y = prevX + 1, prevY + 1

        case DownLeft():
            x, y = prevX - 1, prevY + 1

        case UpLeft():
            x, y = prevX - 1, prevY - 1

    return (x, y)


def unboundPosition(board: Board, position: Position) -> bool:
    x, y = position

    if y < 0 or y >= len(board.grid):
        return True

    if x < 0 or x >= len(board.grid[0]):
        return True

    return False


"""
type BoardLookupValue = BoardValue | IndexError
"""

BoardLookupValue = BoardValue | IndexError


# TODO: rename this function
def get(
    board: Board, position: Position, direction: Direction | None = None
) -> BoardLookupValue:
    if direction is None:
        x, y = position
    else:
        x, y = getPosition(position, direction)

    if unboundPosition(board, (x, y)):
        return IndexError()

    return board.grid[y][x]


def crashBoard(
    board: Board, chainCounter: int = 1, crashedGems: int = 0
) -> tuple[Board, int]:
    # check for all crashable gems
    canCrashGems: list[tuple[Crash, Position]] = []

    for rows, y in zip(board.grid, range(board.height)):
        for crashGem, x in zip(rows, range(board.width)):
            if isinstance(crashGem, Crash):
                position = (x, y)
                crashGemColor = crashGem.color
                directions = [Up(), Right(), Down(), Left()]

                for direction in directions:
                    match get(board, position, direction):
                        case Normal(color) if color == crashGemColor:
                            canCrashGems.append((crashGem, position))
                            break

                        case Crash(color) if color == crashGemColor:
                            canCrashGems.append((crashGem, position))
                            break

                        case (
                            Normal()
                            | Crash()
                            | PowerGem()
                            | Counter()
                            | Exploding()
                            | Empty()
                            | IndexError()
                        ):
                            pass

    # set crashable gems to `Exploding`
    for gem, position in canCrashGems:
        board_set(board, position, Exploding(gem, True, chainCounter))

    crashedGems += len(canCrashGems)

    # check for all crashable gems that are part of the chain reaction
    canCrashGems2: list[tuple[Gem, Position]] = []

    for rows, y in zip(board.grid, range(board.height)):
        for explodingGem, x in zip(rows, range(board.width)):
            if (
                isinstance(explodingGem, Exploding)
                # this logic only applies to Normal | Crash | Counter gems because they have a chain reaction
                # Power gem can crash but that's other logic, those gems crash all at once
                and isinstance(explodingGem.gem, Normal | Crash | Counter)
                and explodingGem.chainCounter == chainCounter
                and explodingGem.chainable
            ):
                explodingPosition = (x, y)
                explodingGemColor = explodingGem.gem.color
                directions: list[CDirection] = [Up(), Right(), Down(), Left()]

                for direction in directions:
                    directionPosition = getPosition(explodingPosition, direction)
                    match get(board, directionPosition):
                        case Normal() as gem if gem.color == explodingGemColor:
                            canCrashGems2.append((gem, directionPosition))

                        case Crash() as gem if gem.color == explodingGemColor:
                            canCrashGems2.append((gem, directionPosition))

                        case Counter() as gem:
                            canCrashGems2.append((gem, directionPosition))

                        case (
                            Normal()
                            | Crash()
                            | PowerGem()
                            | Exploding()
                            | Empty()
                            | IndexError()
                        ):
                            pass

    if len(canCrashGems2) == 0:
        return board, crashedGems

    # set crash gems to `Exploding`
    for gem, position in canCrashGems2:
        match gem:
            case Normal() | Crash():
                board_set(board, position, Exploding(gem, True, chainCounter + 1))

            case Counter():
                board_set(board, position, Exploding(gem, False, chainCounter + 1))

            case PowerGem() | Exploding():
                pass

    crashedGems += len(canCrashGems2)

    return crashBoard(board, chainCounter + 1, crashedGems)


def powerGemCrashBoard(
    board: Board, chainCounter: int = 1, crashedGems: int = 0
) -> tuple[Board, int]:
    # check for all power gems
    canCrashGems: list[tuple[PowerGem, Position]] = []

    for rows, y in zip(board.grid, range(board.height)):
        for crashGem, x in zip(rows, range(board.width)):
            if isinstance(crashGem, PowerGem):
                position = (x, y)

                canCrashGems.append((crashGem, position))

    if len(canCrashGems) == 0:
        return board, crashedGems

    # set crashable gems to `Exploding`
    for gem, position in canCrashGems:
        board_set(board, position, Exploding(gem, False, chainCounter))

    crashedGems += len(canCrashGems)

    # check for all crashable gems that are part of the power gem effect
    targetColors = [
        gem.color
        for gem in [
            getSurroundingBoardGems(board, position)[Down()]
            for (_, position) in canCrashGems
        ]
        # gems that the power gem logic can crash
        if isinstance(gem, Normal | Crash | Counter)
    ]

    canCrashGems2: list[tuple[Gem, Position]] = []

    for rows, y in zip(board.grid, range(board.height)):
        for crashGem, x in zip(rows, range(board.width)):
            position = (x, y)

            match crashGem:
                # gems that the power gem logic can crash
                case Normal() | Crash() | Counter() if crashGem.color in targetColors:
                    canCrashGems2.append((crashGem, position))

                case (
                    Normal()
                    | Crash()
                    | Counter()
                    | Empty()
                    | PowerGem()
                    | Exploding()
                ):
                    pass

    if len(canCrashGems2) == 0:
        return board, crashedGems

    # set crash gems to `Exploding`
    for gem, position in canCrashGems2:
        match gem:
            case Normal() | Crash() | Counter():
                board_set(board, position, Exploding(gem, False, chainCounter))

            case PowerGem() | Exploding():
                pass

    crashedGems += len(canCrashGems2)

    return board, crashedGems


def cleanBoard(board: Board) -> tuple[Board, int]:
    cleanedGems = 0

    # check for all removable gems
    for rows, y in zip(board.grid, range(board.height)):
        for gem, x in zip(rows, range(board.width)):
            match gem:
                case Exploding(_, _, 1):
                    board.grid[y][x] = Empty()
                    cleanedGems += 1
                case Exploding(color, chainable, chainCounter):
                    board.grid[y][x] = Exploding(color, chainable, chainCounter - 1)
                case Normal() | Crash() | Counter() | PowerGem() | Empty():
                    pass

    return board, cleanedGems


def collapseBoard(board: Board, type: CollapsingType) -> tuple[Board, int]:
    collapsedGems = 0

    # check for all collapsable gems
    for x in range(board.width):
        spaces = 0
        for yy in range(board.height):
            y = -1 + -yy
            gem = board.grid[y][x]

            match gem:
                case Empty():
                    spaces += 1

                case _ if spaces > 0:
                    board.grid[y][x] = Empty()
                    collapsedGems += 1

                    match type:
                        case RowByRowFast():
                            board.grid[y + spaces][x] = gem
                            break

                        case BlockSlow():
                            board.grid[y + 1][x] = gem

                case _:
                    pass

    return board, collapsedGems


def board_set(board: Board, position: Position, value: BoardValue) -> Board:
    x, y = position
    board.grid[y][x] = value
    return board


def moveGemBoard(
    board: Board,
    currentPosition: Position,
    targetDirection: Direction,
) -> Board | None:
    targetPosition = getPosition(currentPosition, targetDirection)
    currentBoardValue = get(board, currentPosition)
    targetBoardValue = get(board, targetPosition)

    match currentBoardValue, targetBoardValue:
        case ((Normal() | Crash() | Counter() | PowerGem()), Empty()):
            board_set(board, targetPosition, currentBoardValue)
            board_set(board, currentPosition, Empty())
            return board

        case _:
            return None


# TODO: refactor this because is unsafe and mutable
def moveBoardItemForced(
    board: Board,
    currentBoardValue: Position | BoardValue,
    targetPosition: Position,
) -> Board:
    match currentBoardValue:
        case tuple((x, y)):
            newValue = board.grid[y][x]

        case boardValue:
            newValue = boardValue

    board_set(board, targetPosition, newValue)

    return board


"""
type SurroundingBoardGems = dict[Direction, BoardLookupValue]
"""

SurroundingBoardGems = dict[Direction, BoardLookupValue]


def getSurroundingBoardGems(board: Board, pivot: Position) -> SurroundingBoardGems:
    directions: list[Direction] = [
        Up(),
        Right(),
        Down(),
        Left(),
        UpRight(),
        DownRight(),
        DownLeft(),
        UpLeft(),
    ]

    return {direction: get(board, pivot, direction) for direction in directions}


def directionFromPivot(pivot: Position, position: Position) -> CDirection:
    x1, y1 = pivot
    x2, y2 = position

    if y1 == y2:
        if x2 < x1:
            return Left()
        else:
            return Right()
    else:
        if y2 < y1:
            return Up()
        else:
            return Down()


"""
type Edge = list[Position]
"""

Edge = list[Position]


def edge(block: Block, direction: CDirection) -> Edge:
    """
    This function is going to return the edge positions of a block.
    """

    match direction:
        case Up() | Down():
            xAxisYs: dict[XAxis, YAxis] = dict()
            minOrMax = max if isinstance(direction, Down) else min

            for x, y in block:
                if xAxisYs.get(x) is None:
                    xAxisYs[x] = y
                else:
                    xAxisYs[x] = minOrMax(xAxisYs[x], y)

            return list(xAxisYs.items())

        case Right() | Left():
            yAxisXs: dict[YAxis, XAxis] = dict()
            minOrMax = max if isinstance(direction, Right) else min

            for x, y in block:
                if yAxisXs.get(y) is None:
                    yAxisXs[y] = x
                else:
                    yAxisXs[y] = minOrMax(yAxisXs[y], x)

            # reverse the tuple
            return [(x, y) for y, x in yAxisXs.items()]


def isEmptyItem(item: BoardLookupValue) -> bool:
    match item:
        case Empty():
            return True

        # TODO: exahust this
        case _:
            return False


def canMove(
    board: Board,
    block: Block,
    direction: CDirection,
) -> bool:
    edgePositions = edge(block, direction)
    edgeSurroundings = [
        getSurroundingBoardGems(board, position)[direction]
        for position in edgePositions
    ]

    # check if all target position are `Empty`
    return all(map(isEmptyItem, edgeSurroundings))


def equalBlocks(a: Block, b: Block) -> bool:
    return frozenset(a) == frozenset(b)


def updateCounterGems(board: Board) -> Board:
    # check for all Counter gems
    for rows, y in zip(board.grid, range(board.height)):
        for gem, x in zip(rows, range(board.width)):
            match gem:
                case Counter(color, 1):
                    board.grid[y][x] = Normal(color)
                case Counter(color, counter):
                    board.grid[y][x] = Counter(color, counter - 1)
                case Normal() | Crash() | Exploding() | PowerGem() | Empty():
                    pass

    return board


def generateCounterGems(
    board: Board, turnNumber: int
) -> list[tuple[Counter, Position]]:
    """
    TODO: udpate implementation
    """
    # as min the number of gems in a row, each 20 turns we generate counter gems
    numberOfGems = min(board.width, turnNumber // 20)

    return [(Counter(randomColor(), 5), (x, 0)) for x in range(numberOfGems)]
