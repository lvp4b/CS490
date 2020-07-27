class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
    def onLoad(self):
        self.tts = ALProxy("ALTextToSpeech")
        pass
    def onUnload(self):
        pass
    def setVoice(self, pitch, voice, level, shift):
        self.tts.setParameter("pitchShift", pitch)
        self.tts.setParameter("doubleVoice", voice)
        self.tts.setParameter("doubleVoiceLevel", level)
        self.tts.setParameter("doubleVoiceTimeShift", shift)
    def QuinceSay(self, message):
        self.setVoice(1.1, 1, 0.5, 0.1)
        self.tts.say(message)
    def BottomSay(self, message):
        self.setVoice(0.7, 0.5, 0.5, 0)
        self.tts.say(message)
    def FluteSay(self, message):
        self.setVoice(0.9, 0.5, 0.2, 0.07)
        self.tts.say(message)
    def SnoutSay(self, message):
        self.setVoice(1.4, 0.75, 0.9, 0.05)
        self.tts.say(message)
    def onInput_onStart(self):
        self.tts.say("Hi CS490 IoT")
        self.tts.say("My name is NAO")
        self.QuinceSay("""Is all our company here?""")
        self.BottomSay("""You were best to call them generally, man by man, according to the scrip.""")
        self.QuinceSay("""Here is the scroll of every man's name, which is thought fit through
all Athens, to play in our interlude before the Duke and Duchess, on
his wedding-day at night.""")
        self.BottomSay("""First, good Peter Quince, say what the play treats on; then read the
names of the actors; and so grow to a point.""")
        self.QuinceSay("""Marry, our play is _The most lamentable comedy and most cruel death of
Pyramus and Thisbe_.""")
        self.BottomSay("""A very good piece of work, I assure you, and a merry. Now, good Peter
Quince, call forth your actors by the scroll. Masters, spread
yourselves.""")
        self.QuinceSay("""Answer, as I call you. Nick Bottom, the weaver.""")
        self.BottomSay("""Ready. Name what part I am for, and proceed.""")
        self.QuinceSay("""You, Nick Bottom, are set down for Pyramus.""")
        self.BottomSay("""What is Pyramus—a lover, or a tyrant?""")
        self.QuinceSay("""A lover, that kills himself most gallantly for love.""")
        self.BottomSay("""That will ask some tears in the true performing of it. If I do it, let
the audience look to their eyes. I will move storms; I will condole in
some measure. To the rest—yet my chief humour is for a tyrant. I could
play Ercles rarely, or a part to tear a cat in, to make all split.
    The raging rocks
    And shivering shocks
    Shall break the locks
           Of prison gates,
    And Phibbus' car
    Shall shine from far,
    And make and mar
           The foolish Fates.
This was lofty. Now name the rest of the players. This is Ercles' vein,
a tyrant's vein; a lover is more condoling.""")
        self.QuinceSay("""Francis Flute, the bellows-mender.""")
        self.FluteSay("""Here, Peter Quince.""")
        self.QuinceSay("""Flute, you must take Thisbe on you.""")
        self.FluteSay("""What is Thisbe? A wandering knight?""")
        self.QuinceSay("""It is the lady that Pyramus must love.""")
        self.FluteSay("""Nay, faith, let not me play a woman. I have a beard coming.""")
        self.QuinceSay("""That's all one. You shall play it in a mask, and you may speak as small
as you will.""")
        self.BottomSay("""And I may hide my face, let me play Thisbe too. I'll speak in a
monstrous little voice; 'Thisne, Thisne!'—'Ah, Pyramus, my lover dear!
thy Thisbe dear! and lady dear!'""")
        self.QuinceSay("""No, no, you must play Pyramus; and, Flute, you Thisbe.""")
        self.BottomSay("""Well, proceed.""")
        self.QuinceSay("""Robin Starveling, the tailor.""")
        self.QuinceSay("""Robin Starveling, you must play Thisbe's mother.
Tom Snout, the tinker.""")
        self.SnoutSay("""Here, Peter Quince.""")
        self.QuinceSay("""You, Pyramus' father; myself, Thisbe's father;
Snug, the joiner, you, the lion's part. And, I hope here is a play
fitted.""")
        self.QuinceSay("""You may do it extempore, for it is nothing but roaring.""")
        self.BottomSay("""Let me play the lion too. I will roar that I will do any man's heart
good to hear me. I will roar that I will make the Duke say 'Let him
roar again, let him roar again.'""")
        self.QuinceSay("""If you should do it too terribly, you would fright the Duchess and the
ladies, that they would shriek; and that were enough to hang us all.""")
        self.BottomSay("""I grant you, friends, if you should fright the ladies out of their
wits, they would have no more discretion but to hang us. But I will
aggravate my voice so, that I will roar you as gently as any sucking
dove; I will roar you an 'twere any nightingale.""")
        self.QuinceSay("""You can play no part but Pyramus, for Pyramus is a sweet-faced man; a
proper man as one shall see in a summer's day; a most lovely
gentleman-like man. Therefore you must needs play Pyramus.""")
        self.BottomSay("""Well, I will undertake it. What beard were I best to play it in?""")
        self.QuinceSay("""Why, what you will.""")
        self.BottomSay("""I will discharge it in either your straw-colour beard, your
orange-tawny beard, your purple-in-grain beard, or your
French-crown-colour beard, your perfect yellow.""")
        self.QuinceSay("""Some of your French crowns have no hair at all, and then you will play
bare-faced. But, masters, here are your parts, and I am to entreat you,
request you, and desire you, to con them by tomorrow night; and meet me
in the palace wood, a mile without the town, by moonlight; there will
we rehearse, for if we meet in the city, we shall be dogg'd with
company, and our devices known. In the meantime I will draw a bill of
properties, such as our play wants. I pray you fail me not.""")
        self.BottomSay("""We will meet, and there we may rehearse most obscenely and
courageously. Take pains, be perfect; adieu.""")
        self.QuinceSay("""At the Duke's oak we meet.""")
        self.BottomSay("""Enough. Hold, or cut bow-strings.""")
        self.onStopped()
    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()
