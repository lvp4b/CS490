class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
    def onLoad(self):
        self.tts = ALProxy("ALTextToSpeech")
        pass
    def onUnload(self):
        pass
    def sing(self, letters, notes):
        for (letter, note) in zip(letters, notes):
            self.tts.setParameter("pitchShift", 2 ** ("CDEFGAB".index(note) / 12))
            self.tts.say(letter)
    def onInput_onStart(self):
        self.tts.setParameter("doubleVoice", 1)
        self.tts.setParameter("doubleVoiceLevel", 0.5)
        self.tts.setParameter("doubleVoiceTimeShift", 0)
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXY"
        notes = "CCGGAAGFFEEDDDDCGGFEEDGGF"
        self.sing(alpha, notes)
        alpha = ["and", "Z", "Now", "I", "know", "my", "A", "B", "C's"]
        notes = "EDCCGGAAG"
        self.sing(alpha, notes)
        alpha = ["Next", "time", "won't", "you", "sing", "with", "me."]
        notes = "FFEEDDC"
        self.sing(alpha, notes)
        self.onStopped()
    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()
