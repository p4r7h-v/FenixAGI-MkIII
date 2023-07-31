class FenixState:
    def __init__(self,
                 conversation=[],
                 instructions="",
                 display_response=False,
                 mode="auto",
                 approved_functions=None,
                 voice_mode=None):
        self.conversation = conversation
        self.instructions = instructions
        self.display_response = display_response
        self.mode = mode
        self.approved_functions = approved_functions or []
        self.voice_mode = voice_mode
