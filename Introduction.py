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

def create_binary_digits(len):
    return [bin(i)[2:].zfill(len) for i in range(2**len)]

class InformationContent(Scene):
    def construct(self):
        title = Text("Information\nContent")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        log = Tex("$\log_b N$")
        self.play(Write(log))
        self.wait(1)
        self.play(log.animate.shift(2*RIGHT))
        
        binary_digits = [Tex(x) for x in create_binary_digits(2)]
        
        for i,b in enumerate(binary_digits):
            self.play(Write(b))
            self.play(b.animate.shift(2*LEFT + 2*UP + i*DOWN))

        rect = SurroundingRectangle( Group(*binary_digits))
        self.play(Create(rect))
        self.play(Transform(log, Tex("$\log_2 4 = 2$").shift(2*RIGHT)))
        self.wait(1)
        self.play(Transform(rect, SurroundingRectangle(Group(*binary_digits[:2]))))
        self.play(Transform(log, Tex("$\log_2 2 = 1$").shift(2*RIGHT)))

class BinarySymmetricChannel(Scene):
    def construct(self):
        title = Tex("Binary Symmetric Channel").scale(1.5)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        input_bit_0 = Circle(radius=0.5, color=BLUE).shift(3*LEFT + 2*UP)
        input_bit_1 = Circle(radius=0.5, color=BLUE).shift(3*LEFT + 2*DOWN)

        input_0_text = Tex("0").scale(1.5).move_to(input_bit_0.get_center())
        input_1_text = Tex("1").scale(1.5).move_to(input_bit_1.get_center())

        output_bit_0 = Circle(radius=0.5, color=BLUE).shift(3*RIGHT + 2*UP)
        output_bit_1 = Circle(radius=0.5, color=BLUE).shift(3*RIGHT + 2*DOWN)

        output_0_text = Tex("0").scale(1.5).move_to(output_bit_0.get_center())
        output_1_text = Tex("1").scale(1.5).move_to(output_bit_1.get_center())

        self.play(
            Create(input_bit_0), Write(input_0_text),
            Create(input_bit_1), Write(input_1_text),
            Create(output_bit_0), Write(output_0_text),
            Create(output_bit_1), Write(output_1_text),
        )
        self.wait(1)
        
        arrow_00 = Arrow(start=input_bit_0.get_right(), end=output_bit_0.get_left(), buff=0.25, color=GREEN)
        arrow_01 = Arrow(start=input_bit_0.get_right(), end=output_bit_1.get_left(), buff=0.25, color=RED)

        arrow_10 = Arrow(start=input_bit_1.get_right(), end=output_bit_0.get_left(), buff=0.25, color=RED)
        arrow_11 = Arrow(start=input_bit_1.get_right(), end=output_bit_1.get_left(), buff=0.25, color=GREEN)
        
        p_label = Tex("p").scale(1.5).shift(2*RIGHT + 2.5*UP)
        one_minus_p_label = Tex("1-p").scale(1.5).shift(2*RIGHT + 0.5*UP)
        
        self.play(
            Create(arrow_00), Write(one_minus_p_label),
            Create(arrow_01), Write(p_label),
        )
        self.wait(1)

        self.play(
            Create(arrow_10), Write(one_minus_p_label.copy().shift(DOWN)),
            Create(arrow_11), Write(p_label.copy().shift(5*DOWN)),
        )
        self.wait(1)


