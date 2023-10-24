from manim import *


class CommunicationSystem(Scene):
    def construct(self):
        source = Square()
        source.add(Text("Information\nSource", font_size=20,))
        self.play(Create(source))
        self.wait(1)
        self.play(source.animate.shift(LEFT*3))
        
        transmitter = Square()
        transmitter.add(Text("Transmitter", font_size=20))
        s_to_t = Arrow(source.get_right(), transmitter.get_left(), buff=0, max_stroke_width_to_length_ratio=1)
        self.play(Create(transmitter))
        self.play(Create(s_to_t))
        
        group = Group(source, s_to_t, transmitter)
        self.play(group.animate.shift(LEFT*3))

        channel = Square()
        channel.add(Text("Channel", font_size=20))
        self.play(Create(Arrow(transmitter.get_right(), channel.get_left(), buff=0, max_stroke_width_to_length_ratio=1)))
        self.play(Create(channel))

        receiver = Square()
        receiver.add(Text("Receiver", font_size=20))
        receiver.shift(RIGHT*3)
        self.play(Create(Arrow(channel.get_right(), receiver.get_left(), buff=0, max_stroke_width_to_length_ratio=1)))
        self.play(Create(receiver))
        self.wait(1)
        
        destination = Square()
        destination.add(Text("Destination", font_size=20))
        destination.shift(RIGHT*6)
        self.play(Create(Arrow(receiver.get_right(), destination.get_left(), buff=0, max_stroke_width_to_length_ratio=1)))
        self.play(Create(destination))
        self.wait(1)

        for x in self.mobjects:
            # if isinstance(x, Square):          
                self.play(x.animate.set_color(GREEN))

        noise = Square(color=RED)
        noise.add(Text("Noise", font_size=20, color=RED))
        noise.shift(DOWN*3)
        self.play(Create(noise))
        self.play(Create(Arrow( noise.get_top(), channel.get_bottom(), buff=0, max_stroke_width_to_length_ratio=1, color=RED)))

        for x in [channel, receiver, destination]:
            self.play(x.animate.set_color(YELLOW))
        
        self.wait(1)

        # create an observer that sends error correcting data to the reciever
        observer = Square(color=BLUE)
        observer.add(Text("Observer", font_size=20, color=BLUE))
        observer.shift(UP*3)
        self.play(Create(observer))
        self.play(Create(Arrow(channel.get_top(), observer.get_bottom(), buff=0, max_stroke_width_to_length_ratio=1, color=BLUE)))
        print(observer.get_left())
        self.play(Create(Line(observer.get_right(), np.array([receiver.get_top()[0], observer.get_right()[1], 0]), color=BLUE)))
        self.play(Create(Arrow(np.array([receiver.get_top()[0], observer.get_right()[1], 0]), receiver.get_top(), color=BLUE, buff=0, max_stroke_width_to_length_ratio=1)))

        for x in [receiver, destination]:
            self.play(x.animate.set_color(GREEN))

        
    


