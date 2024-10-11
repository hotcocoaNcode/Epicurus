from dataclasses import dataclass
from collections.abc import MutableSequence
from PIL import Image
import numpy as np

@dataclass
class Layer:
    img: Image
    name: str

class InformalCommandInterface:
    def getName(self) -> str:
        pass
    def call(self, tokens: MutableSequence[str]) -> None:
        pass

global layerArray
layerArray: MutableSequence[Layer] = []

def getLayer(name: str) -> Layer:
    for l in layerArray: 
        if (l.name == name): return l

def getIndexOfLayer(name: str) -> int:
    i = 0
    for l in layerArray:
        if (l.name == name): return i
        else: i += 1

class LoadCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "load"
    def call(self, tokens: MutableSequence[str]) -> None:
        layerArray.append(Layer(Image.fromarray(np.array(Image.open(tokens[1]))), tokens[2]))

class ResizeCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "resize"
    def call(self, tokens: MutableSequence[str]) -> None:
        getLayer(tokens[1]).img.thumbnail((int(tokens[2]), int(tokens[3])))

class ExportCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "export"
    def call(self, tokens: MutableSequence[str]) -> None:
        getLayer(tokens[1]).img.save(tokens[2])

class DeleteLayerCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "delete"
    def call(self, tokens: MutableSequence[str]) -> None:
        layerArray.pop(getIndexOfLayer(tokens[1]))

class ShowLayerCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "show"
    def call(self, tokens: MutableSequence[str]) -> None:
        getLayer(tokens[1]).img.show()

class ListLayersCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "list"
    def call(self, tokens: MutableSequence[str]) -> None:
        for l in layerArray:
            print(l.name + " (sized at " + str(l.img.size) + ")")

class QuitCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "quit"
    def call(self, tokens: MutableSequence[str]) -> None:
        exit(0)

global commandArray
commandArray: MutableSequence[InformalCommandInterface] = [
    LoadCommand(),
    ResizeCommand(),
    ExportCommand(),
    DeleteLayerCommand(),
    ShowLayerCommand(),
    ListLayersCommand(),
    QuitCommand()
]

def parseCommand(command: str):
    tokens = command.split(" ")
    for c in commandArray:
        if (tokens[0] == c.getName()):
            c.call(tokens)

print("Epicurus Editor")
while (True):
    parseCommand(input("> "))