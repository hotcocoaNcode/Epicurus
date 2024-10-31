from dataclasses import dataclass
from collections.abc import MutableSequence
from PIL import Image, ImageFilter
import numpy as np

@dataclass
class ivec2:
    x: int
    y: int

@dataclass
class Layer:
    img: Image
    name: str
    pos: ivec2
    alpha: float

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
        layerArray.append(Layer(Image.fromarray(np.array(Image.open(tokens[1]))).convert("RGBA"), tokens[2], (0, 0), 1.0))

class ResizeCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "resize"
    def call(self, tokens: MutableSequence[str]) -> None:
        getLayer(tokens[1]).img.thumbnail((int(tokens[2]), int(tokens[3])))

class ExportCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "export"
    def call(self, tokens: MutableSequence[str]) -> None:
        image = getLayer(tokens[1]).img.convert("RGB")
        if (len(tokens) == 4): image.save(tokens[2], dpi=(int(tokens[3]), int(tokens[3])))
        else: image.save(tokens[2])

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
        if (len(layerArray) > 0):
            print("Layers:")
            for l in layerArray:
                print("- " + l.name)
                print("  Sized at " + str(l.img.size))
                print("  Located at " + str(l.pos))
                print("  Alpha of " + str(l.alpha))
        else:
            print("No current layers!")

class QuitCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "quit"
    def call(self, tokens: MutableSequence[str]) -> None:
        exit(0)

class AddCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "add"
    def call(self, tokens: MutableSequence[str]) -> None:
        pixels = np.array(getLayer(tokens[1]).img.convert("RGB"))
        pixels+=int(tokens[2])
        clone = np.array(getLayer(tokens[1]).img.convert("RGB"))
        pixels[pixels<clone]=255
        getLayer(tokens[1]).img = Image.fromarray(pixels, 'RGB')

class SubCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "sub"
    def call(self, tokens: MutableSequence[str]) -> None:
        pixels = np.array(getLayer(tokens[1]).img.convert("RGB"))
        pixels = pixels - int(tokens[2])
        clone = np.array(getLayer(tokens[1]).img.convert("RGB"))
        pixels[pixels>clone]=0
        getLayer(tokens[1]).img = Image.fromarray(pixels, 'RGB')

class MulCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "mul"
    def call(self, tokens: MutableSequence[str]) -> None:
        pixels = np.array(getLayer(tokens[1]).img.convert("RGB"))
        pixels = pixels * int(tokens[2])
        clone = np.array(getLayer(tokens[1]).img.convert("RGB"))
        pixels[pixels<clone]=255
        getLayer(tokens[1]).img = Image.fromarray(pixels, 'RGB')

class DivCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "div"
    def call(self, tokens: MutableSequence[str]) -> None:
        pixels = np.array(getLayer(tokens[1]).img.convert("RGB"))
        pixels = pixels / int(tokens[2])
        clone = np.array(getLayer(tokens[1]).img.convert("RGB"))
        pixels[pixels>clone]=0
        getLayer(tokens[1]).img = Image.fromarray(pixels, 'RGB')
        
class MoveCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "move"
    def call(self, tokens: MutableSequence[str]) -> None:
        getLayer(tokens[1]).pos = ivec2(int(tokens[2]), int(tokens[3]))

class AlphaCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "alpha"
    def call(self, tokens: MutableSequence[str]) -> None:
        getLayer(tokens[1]).alpha = float(tokens[2])

class MergeDownCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "merge"
    def call(self, tokens: MutableSequence[str]) -> None:
        for i in range(1, len(layerArray)):
            layerArray[0].img = Image.blend(layerArray[0].img, layerArray[i].img, layerArray[i].alpha)        

class LayerAddCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "ladd"
    def call(self, tokens: MutableSequence[str]) -> None:
        pixels = np.array(getLayer(tokens[1]).img.convert("RGB")) + np.array(getLayer(tokens[2]).img.convert("RGB"))
        clone = np.array(getLayer(tokens[1]).img.convert("RGB"))
        pixels[pixels<clone]=255
        getLayer(tokens[1]).img = Image.fromarray(pixels, 'RGB')

class LayerMulCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "lmul"
    def call(self, tokens: MutableSequence[str]) -> None:
        pixels = np.array(getLayer(tokens[1]).img.convert("RGB")) * np.array(getLayer(tokens[2]).img.convert("RGB"))
        clone = np.array(getLayer(tokens[1]).img.convert("RGB"))
        pixels[pixels<clone]=255
        getLayer(tokens[1]).img = Image.fromarray(pixels, 'RGB')

class GaussianBlurCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "blur"
    def call(self, tokens: MutableSequence[str]) -> None:
        rad = 10
        if (len(tokens) == 3): rad = int(tokens[2])
        getLayer(tokens[1]).img = getLayer(tokens[1]).img.filter(ImageFilter.GaussianBlur(radius=rad))

class SobelCommand(InformalCommandInterface):
    def getName(self) -> str:
        return "edge"
    def call(self, tokens: MutableSequence[str]) -> None:
        getLayer(tokens[1]).img = getLayer(tokens[1]).img.convert("RGB").filter(ImageFilter.Kernel((3, 3), (
            -1, -1, -1,
            -1,  8, -1,
            -1, -1, -1), 
            1, 0))

global commandArray
commandArray: MutableSequence[InformalCommandInterface] = [
    LoadCommand(),
    ResizeCommand(),
    ExportCommand(),
    DeleteLayerCommand(),
    ShowLayerCommand(),
    ListLayersCommand(),
    QuitCommand(),
    AddCommand(),
    SubCommand(),
    MulCommand(),
    DivCommand(),
    MoveCommand(),
    AlphaCommand(),
    MergeDownCommand(),
    GaussianBlurCommand(),
    SobelCommand(),
    LayerAddCommand(),
    LayerMulCommand()
]

def parseCommand(command: str):
    tokens = command.split(" ")
    for c in commandArray:
        if (tokens[0] == c.getName()):
            try:
                c.call(tokens)
            except:
                print("Failed to complete operation.")

print("Epicurus Editor")
while (True):
    parseCommand(input("> "))