from dataclasses import dataclass, field


@dataclass
class Player:
    ID: list[int] = field(default_factory=lambda: [0, 0])
    Token: str = ''
    Name: str = '@BSVSCHANNEL'
    Registered: bool = False
