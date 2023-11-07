from manim import *
from random import random 


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
            self.play(b.animate.shift(2*LEFT + 2*UP + i*0.5*DOWN))

        rect = SurroundingRectangle( Group(*binary_digits))
        self.play(Create(rect))
        self.play(Transform(log, Tex("$\log$", "$_2$", "$4$", "$=$", "$2$").set_color_by_tex("_2", RED).shift(2*RIGHT)))
        self.wait(1)
        self.play(Transform(rect, SurroundingRectangle(Group(*binary_digits[:2]))))
        self.play(Transform(log, Tex("$\log$", "$_2$", "$2$", "$=$", "$1$").set_color_by_tex("_2", RED).shift(2*RIGHT)))
        
        anims = []
        for i,b in enumerate(create_binary_digits(3)):
            if len(binary_digits)>i:
                x = Tex(b).shift(2*LEFT + 2*UP + i*0.5*DOWN)
                anims.append(Transform(binary_digits[i],x))
                binary_digits[i] = x
            else:
                x = Tex(b).shift(2*LEFT + 2*UP + i*0.5*DOWN)
                binary_digits.append(x)
                anims.append(Write(x))
        anims.append(Transform(rect, SurroundingRectangle(Group(*binary_digits[:2]))))
        self.play(*anims)

        self.wait(1)


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

        input_string = "1000101"
        input_text = [Tex(bit).shift((5-0.3*i)*LEFT) for i, bit in enumerate(input_string)]
        
        for t in input_text:
            self.play(Write(t))

        for i,( bit, text) in enumerate(zip(input_string, input_text)):
            source = input_bit_0.get_center() if bit == "0" else input_bit_1.get_center()
            prob = np.random.rand()
            FLIP_PROB = 0.1
            if bit == "0":
                target = output_bit_1.get_center() if prob < FLIP_PROB else output_bit_0.get_center()  
            else:
                target = output_bit_0.get_center() if prob < FLIP_PROB else output_bit_1.get_center()
            resulting_bit = "0" if (target == output_bit_0.get_center()).all() else "1"

            self.play(FadeOut(text.copy(), target_position=source))

            def animate(arrow): self.play(ShowPassingFlash(arrow.copy().set_color(BLUE)))
            if resulting_bit == "0" and bit == "0":
                animate(arrow_00)
            elif resulting_bit == "1" and bit == "0":
                animate(arrow_01)
            elif resulting_bit == "0" and bit == "1":
                animate(arrow_10)
            else:
                animate(arrow_11)

            result = Tex(resulting_bit, color=GREEN if resulting_bit == bit else RED).move_to((4+0.3*i)*RIGHT)
            self.play(FadeIn(result, target_position=target))


class Entropy(Scene):
    def construct(self):
        coin = Circle(radius=1, color=BLUE).shift(1.5*LEFT)
        heads = Text("H", color=BLUE).scale(1.5).move_to(coin.get_center())
        
        coin2 = Circle(radius=1, color=RED).shift(1.5*RIGHT)
        tails = Text("T", color=RED).scale(1.5).move_to(coin2.get_center())

        self.play(FadeIn(coin), Write(heads))
        self.play(FadeIn(coin2), Write(tails))
        coin_flipping_text = Text("Flip a fair coin: Equally likely probabilities").shift(2*DOWN)
        self.play(Write(coin_flipping_text))
        self.wait(1)

        entropy_formula_1 = Tex("$H(X) =$", "$-0.5 \cdot \log_2(0.5)$", "$- 0.5 \cdot \log_2(0.5)$").scale(0.8).next_to(coin_flipping_text, DOWN)
        entropy_formula_1[1].set_color(BLUE)
        entropy_formula_1[2].set_color(RED)

        self.play(Write(entropy_formula_1))
        self.wait(2)

        self.play(*[Indicate(x, color=BLUE_A) for x in [*coin, *heads, entropy_formula_1[1]]])
        self.play(*[Indicate(x, color=RED_A) for x in [*coin2, *tails, entropy_formula_1[2]]])
        self.wait(2)
        
        # fade away all objects
        self.play(FadeOut(entropy_formula_1), FadeOut(coin), FadeOut(heads), FadeOut(coin_flipping_text), FadeOut(coin2), FadeOut(tails))


        # Non equally likely probabilities
        columns = 5
        n_balls = 10
        balls = [Dot(color=BLUE if i < 7 else RED).move_to((i%columns) * RIGHT + (i//columns)*DOWN + 2*LEFT + UP) for i in range(n_balls)]
        self.play(FadeIn(*balls))

        ball_text = Text("Pick a ball: Non equally likely probabilities").shift(2*DOWN)
        self.play(Write(ball_text))
        self.wait(1)

        entropy_formula_2 = Tex("$H(X) =$", "$-\\frac{7}{10} \cdot \log_2(\\frac{7}{10})$", "$- \\frac{3}{10} \cdot \log_2(\\frac{3}{10})$").scale(0.8).next_to(ball_text, DOWN)
        entropy_formula_2[1].set_color(BLUE)
        entropy_formula_2[2].set_color(RED)

        self.play(Write(entropy_formula_2))
        self.wait(2)

        self.play(*[Indicate(x, color=BLUE_A) for x in [*balls[:7], entropy_formula_2[1]]])
        self.play(*[Indicate(x, color=RED_A) for x in [*balls[7:], entropy_formula_2[2]]])
        self.wait(2)
        # fade away all objects
        self.play(FadeOut(entropy_formula_2), FadeOut(*balls), FadeOut(ball_text))

        # Binary Entropy Formula
        binary_entropy_formula = Tex("$H_b(p) =$", "$-p \cdot \log_2(p)$", "$- (1-p) \cdot \log_2(1-p)$").shift(2*DOWN)
        self.play(Write(binary_entropy_formula))
        self.wait(2)

        # H(p) Chart
        axes = Axes(
            x_range=[0, 1.2, 0.1],
            y_range=[0, 1.2, 0.1],
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": [0, 0.5, 1]},
            y_axis_config={"numbers_to_include": [0, 1]},
            x_length=7,
            y_length=4
        ).shift(UP)

        t = ValueTracker(0)
        func = lambda x: -x * np.log2(x) - (1-x) * np.log2(1-x) if 0 < x < 1 else 0
        initial_point = [axes.coords_to_point(t.get_value(), func(t.get_value()))]
        dot = Dot(point=initial_point)

        dot.add_updater(lambda x: x.move_to(axes.c2p(t.get_value(), func(t.get_value()))))

        # Creating curve for y = -plog2(p) - (1-p)log2(1-p)
        graph = axes.plot(
            func,
            color=WHITE,
            x_range=[0,1]
        )
        labels = axes.get_axis_labels("p", "H(p)")
        self.play(
            Create(axes), 
            Create(graph), 
            Write(labels)
        )
        self.wait(2)

        self.play(Create(dot))

        self.play(t.animate.set_value(0.5))
        self.play(Transform(binary_entropy_formula, Tex("$H_b(0.5) =$", "$-0.5 \cdot \log_2(0.5)$", "$- (1-0.5) \cdot \log_2(1-0.5)$", "$=1$").shift(2*DOWN)))

        self.wait(2)

        self.play(t.animate.set_value(0))
        self.play(Transform(binary_entropy_formula, Tex("$H_b(0) =$", "$-0 \cdot \log_2(0)$", "$- (1-0) \cdot \log_2(1-0)$", "$=0$").shift(2*DOWN)))

        self.wait(2)
    
        self.play(t.animate.set_value(1))
        self.play(Transform(binary_entropy_formula, Tex("$H_b(1) =$", "$-1 \cdot \log_2(1)$", "$- (1-1) \cdot \log_2(1-1)$", "$=0$").shift(2*DOWN)))

        self.wait(2)

        #fade out everything
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(labels), FadeOut(dot), FadeOut(binary_entropy_formula))

        # General Entropy Formula
        general_entropy_formula = Tex("$H(X) =$", "$\sum p(x) \cdot \log_2\\left(\\frac{1}{p(x)}\\right)$").scale(0.9).next_to(ball_text, UP)
        self.play(Write(general_entropy_formula))
        self.wait(3)

        self.play(FadeIn(entropy_formula_2.shift(UP)), FadeIn(*balls))
        new_balls = [Dot(color=GREEN).move_to(balls[0].get_center() + UP + i * RIGHT) for i in range(5)]
        self.play(FadeIn(*new_balls))
        updated_entropy_formula_2 = Tex("$H(X) =$", "$-\\frac{7}{15} \cdot \log_2(\\frac{7}{15})$", "$- \\frac{3}{15} \cdot \log_2(\\frac{3}{15})$", "$- \\frac{5}{15} \cdot \log_2(\\frac{3}{15})$").scale(0.8).move_to(ball_text.get_center())
        updated_entropy_formula_2[1].set_color(BLUE)
        updated_entropy_formula_2[2].set_color(RED)
        updated_entropy_formula_2[3].set_color(GREEN)
        self.play(Transform(entropy_formula_2,updated_entropy_formula_2))
        self.play(*[Indicate(x, color=BLUE_A) for x in [*balls[:7], updated_entropy_formula_2[1]]])
        self.play(*[Indicate(x, color=RED_A) for x in [*balls[7:], updated_entropy_formula_2[2]]])
        self.play(*[Indicate(x, color=GREEN_A) for x in [*new_balls, updated_entropy_formula_2[3]]])
        

        self.wait(3)
        

class EntropyBoxRepresentation(Scene):
    def construct(self):
        joint_entropy_box = Rectangle(width=8, height=1, color=WHITE).shift(UP)
        joint_entropy_label = Tex("$H(X,Y)$").move_to(joint_entropy_box.get_center())

        entropy_box_x = Rectangle(width=6, height=1, color=WHITE).shift(1*LEFT)
        entropy_label_x = Tex("$H(X)$").move_to(entropy_box_x.get_center())
        
        entropy_box_y = Rectangle(width=4, height=1, color=WHITE).shift(2*RIGHT+DOWN)
        entropy_label_y = Tex("$H(Y)$").move_to(entropy_box_y.get_center())
        
        cond_entropy_box_x = Rectangle(width=4, height=1, color=WHITE).shift(2*LEFT+DOWN)
        cond_entropy_label_x = Tex("$H(X|Y)$").move_to(cond_entropy_box_x.get_center())
        
        cond_entropy_box_y = Rectangle(width=2, height=1, color=WHITE).shift(3*RIGHT)
        cond_entropy_label_y = Tex("$H(Y|X)$").move_to(cond_entropy_box_y.get_center())
        
        mutual_info_box = Rectangle(width=2, height=1, color=WHITE).shift(2*DOWN+RIGHT)
        mutual_info_label = Tex("I(X; Y)").move_to(mutual_info_box.get_center())

        boxes = VGroup(joint_entropy_box, entropy_box_x, entropy_box_y, cond_entropy_box_x, cond_entropy_box_y, mutual_info_box)
        labels = VGroup(joint_entropy_label, entropy_label_x, entropy_label_y, cond_entropy_label_x, cond_entropy_label_y, mutual_info_label)

        self.play(*[Create(box) for box in boxes], *[Write(label) for label in labels])
        self.wait(3)
