import requests

commandUrl = "http://localhost:9000/command"


class Interface():
    def __init__(self) -> None:
        self.buffer: list[str] = []

    def __del__(self):
        self.sendCommands()

    def runCommand(self, command: str, limit: int = 50):
        """**Run a Minecraft command in the world**."""
        self.buffer.append(command)
        if len(self.buffer) >= limit:
            self.sendCommands()
        else:
            return "0"

    def runCommands(self, commands: list[str], limit: int = 50):
        """**Run Minecraft commands in the world**."""
        self.buffer += commands
        if len(self.buffer) >= limit:
            return self.sendCommands()
        else:
            return "0"

    def sendCommands(self, retries=5):
        """**Send buffered commands in the world**."""
        if self.buffer == []:
            return "0"

        def removePrefix(command: str):
            if command[0] == '/':
                command = command[1:]
            return command

        self.buffer = map(removePrefix, self.buffer)
        try:
            response = requests.post(commandUrl, bytes(
                "\n".join(self.buffer), "utf-8"))
        except ConnectionError:
            if retries > 0:
                return self.sendCommands(retries-1)
            return "connection error"
        self.buffer = []
        return response.text
