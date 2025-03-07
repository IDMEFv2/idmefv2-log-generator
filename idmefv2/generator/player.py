import abc

class Player(abc.ABC):
    @abc.abstractmethod
    def play(self, rendered: str):
        raise NotImplementedError

class PrintPlayer(Player):
    def play(self, rendered: str):
        print(rendered)

class RecordPlayer(Player, list):
    def play(self, rendered: str):
        self.append(rendered)
