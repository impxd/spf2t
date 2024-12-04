## Super Puzzle Fighter II Turbo clon

Yet Another [SPF2T](https://en.wikipedia.org/wiki/Super_Puzzle_Fighter_II_Turbo) clon written in Python + Pygame

## Why?

lorem...

## How?

lorem...

### Architecture

https://guide.elm-lang.org/architecture/
lorem...

## Screenshots

<img width="200" alt="Screenshot 2024-12-03 at 9 42 07 p m" src="https://github.com/user-attachments/assets/8e37d7ae-ba20-4845-8fe0-f8c281c86467">

## Gameplay

6-Chain Combo
https://www.youtube.com/watch?v=vonvKEjOsME

[Kapture 2024-12-04 at 11.39.19.webm](https://github.com/user-attachments/assets/8f74ee51-e69d-483c-8a8e-e253ecc5424c)

## Controls

| Key   | Action        |
|-------|---------------|
| Right | Move right    |
| Left  | Move left     |
| Down  | Move down     |
| S     | Rotate left   |
| D     | Rotate right  |
| R     | Restart       |
| Esc/Q | Exit          |

## Requirements

- Python 3.10
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

## Setup

```bash
python3.10 -m virtualenv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
python src/main.py
```

## Testing

```bash
pytest
```

## TODO

- Improve controls
- Improve GFX
- Add SFX
- Add score
- Add block system for grouped gems

## References

- https://en.wikipedia.org/wiki/Super_Puzzle_Fighter_II_Turbo
- https://game.capcom.com/manual/CFC/en/ps4/page/8/1
