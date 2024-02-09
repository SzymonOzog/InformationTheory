from manim import *
from entropy import *
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


        encoding = Text("Encoding", font_size=20, color=GREEN).next_to(transmitter.submobjects[0], DOWN)
        encoding_box = SurroundingRectangle(encoding, color=GREEN)
        transmitter.add(encoding)
        decoding = Text("Decoding", font_size=20, color=GREEN).next_to(receiver.submobjects[0], DOWN)
        decoding_box = SurroundingRectangle(decoding, color=GREEN)
        receiver.add(decoding)
        self.play(Create(encoding), Create(decoding),
                  Create(encoding_box), Create(decoding_box))

        for x in [receiver, destination]:
            self.play(x.animate.set_color(GREEN))

def to_binary(i, len):
    return bin(i)[2:].zfill(len)

def create_binary_digits(len):
    return [to_binary(i, len) for i in range(2**len)]


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


class BSC:
    def __init__(self):
        self.input_bit_0 = Circle(radius=0.5, color=BLUE).shift(3*LEFT + 2*UP)
        self.input_bit_1 = Circle(radius=0.5, color=BLUE).shift(3*LEFT + 2*DOWN)

        self.input_0_text = Tex("0").scale(1.5).move_to(self.input_bit_0.get_center())
        self.input_1_text = Tex("1").scale(1.5).move_to(self.input_bit_1.get_center())

        self.output_bit_0 = Circle(radius=0.5, color=BLUE).shift(3*RIGHT + 2*UP)
        self.output_bit_1 = Circle(radius=0.5, color=BLUE).shift(3*RIGHT + 2*DOWN)

        self.output_0_text = Tex("0").scale(1.5).move_to(self.output_bit_0.get_center())
        self.output_1_text = Tex("1").scale(1.5).move_to(self.output_bit_1.get_center())

        self.arrow_00 = Arrow(start=self.input_bit_0.get_right(), end=self.output_bit_0.get_left(), buff=0.25, color=GREEN)
        self.arrow_01 = Arrow(start=self.input_bit_0.get_right(), end=self.output_bit_1.get_left(), buff=0.25, color=RED)

        self.arrow_10 = Arrow(start=self.input_bit_1.get_right(), end=self.output_bit_0.get_left(), buff=0.25, color=RED)
        self.arrow_11 = Arrow(start=self.input_bit_1.get_right(), end=self.output_bit_1.get_left(), buff=0.25, color=GREEN)

        self.p_label0 = Tex("p").scale(1.5).shift(2*RIGHT + 2.5*UP)
        self.one_minus_p_label0 = Tex("1-p").scale(1.5).shift(2*RIGHT + 0.5*DOWN)
        
        self.one_minus_p_label1 = self.one_minus_p_label0.copy().shift(UP)
        self.p_label1 =  self.p_label0.copy().shift(5*DOWN)

        self.q_label = Tex("q").scale(1.5).next_to(self.input_bit_0, LEFT)
        self.one_minus_q_label = Tex("1-q").scale(1.5).next_to(self.input_bit_1, LEFT)

        self.bits = VGroup(self.input_bit_0, self.input_bit_1, self.output_bit_0, self.output_bit_1)
        self.texts = VGroup(self.input_0_text, self.input_1_text, self.output_0_text, self.output_1_text)
        self.arrows = VGroup(self.arrow_00, self.arrow_01, self.arrow_10, self.arrow_11)
        self.labels = VGroup(self.p_label0, self.one_minus_p_label0, self.one_minus_p_label1, self.p_label1)
        self.q_labels = VGroup(self.q_label, self.one_minus_q_label)
        self.full_channel = VGroup(self.bits, self.texts, self.arrows, self.labels, self.q_labels)




class BinarySymmetricChannel(Scene):
    def construct(self):
        title = Tex("Binary Symmetric Channel").scale(1.5)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        bsc = BSC()
        self.play(Create(bsc.bits), Write(bsc.texts))
        self.wait(1)
        
        
        self.play(Create(bsc.arrows[:2]), Write(bsc.labels[:2]))
        self.wait(1)

        self.play(Create(bsc.arrows[2:]), Write(bsc.labels[2:]))
        self.wait(1)

        input_string = "1000101"
        input_text = [Tex(bit).shift((5-0.3*i)*LEFT) for i, bit in enumerate(input_string)]
        
        for t in input_text:
            self.play(Write(t))

        for i,( bit, text) in enumerate(zip(input_string, input_text)):
            source = bsc.input_bit_0.get_center() if bit == "0" else bsc.input_bit_1.get_center()
            prob = np.random.rand()
            FLIP_PROB = 0.1
            if bit == "0":
                target = bsc.output_bit_1.get_center() if prob < FLIP_PROB else bsc.output_bit_0.get_center()  
            else:
                target = bsc.output_bit_0.get_center() if prob < FLIP_PROB else bsc.output_bit_1.get_center()
            resulting_bit = "0" if (target == bsc.output_bit_0.get_center()).all() else "1"

            self.play(FadeOut(text.copy(), target_position=source))

            def animate(arrow): self.play(ShowPassingFlash(arrow.copy().set_color(BLUE)))
            if resulting_bit == "0" and bit == "0":
                animate(bsc.arrow_00)
            elif resulting_bit == "1" and bit == "0":
                animate(bsc.arrow_01)
            elif resulting_bit == "0" and bit == "1":
                animate(bsc.arrow_10)
            else:
                animate(bsc.arrow_11)

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
        balls = [Dot(color=BLUE if i < 7 else RED).move_to((i%columns) * RIGHT + (i//columns)*DOWN + 2*LEFT + 2*UP) for i in range(n_balls)]
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
        self.wait(1)

        self.play(FadeIn(entropy_formula_2.shift(UP)), FadeIn(*balls))
        new_balls = [Dot(color=GREEN).move_to(balls[0].get_center() + 2*DOWN + i * RIGHT) for i in range(5)]
        self.play(FadeIn(*new_balls))
        updated_entropy_formula_2 = Tex("$H(X) =$", "$-\\frac{7}{15} \cdot \log_2(\\frac{7}{15})$", "$- \\frac{3}{15} \cdot \log_2(\\frac{3}{15})$", "$- \\frac{5}{15} \cdot \log_2(\\frac{3}{15})$").scale(0.8).move_to(ball_text.get_center())
        updated_entropy_formula_2[1].set_color(BLUE)
        updated_entropy_formula_2[2].set_color(RED)
        updated_entropy_formula_2[3].set_color(GREEN)
        self.play(Transform(entropy_formula_2,updated_entropy_formula_2),replace_mobject_with_target_in_scene=True)
        self.remove(*balls[:7], updated_entropy_formula_2[1])
        self.play(*[Indicate(x, color=BLUE_A) for x in [*balls[:7], updated_entropy_formula_2[1]]])
        self.add(*balls[:7], updated_entropy_formula_2[1])
        self.remove(*balls[7:], updated_entropy_formula_2[2])
        self.play(*[Indicate(x, color=RED_A) for x in [*balls[7:], updated_entropy_formula_2[2]]])
        self.add(*balls[7:], updated_entropy_formula_2[2])
        self.remove(*new_balls, updated_entropy_formula_2[3])
        self.play(*[Indicate(x, color=GREEN_A) for x in [*new_balls, updated_entropy_formula_2[3]]])
        self.add(*new_balls, updated_entropy_formula_2[3])
        self.wait(1)
        

class EntropyBoxRepresentation:
        def __init__(self, probabilities=None, base_width=2):
            self.scale=1
            self.base_width = base_width 
            self.fill_opacity = 0.9
            joint_entropy_box = Rectangle(width=self.base_width, height=1, fill_opacity=self.fill_opacity).set_fill(GREEN).shift(UP)
            joint_entropy_label = Tex("$H(X,Y)$",color=GREEN).next_to(joint_entropy_box, UP)

            entropy_box_x = Rectangle(width=6, height=1, fill_opacity=self.fill_opacity).set_fill(BLUE).shift(1*LEFT)
            entropy_label_x = Tex("$H(X)$", color=BLUE).next_to(entropy_box_x, LEFT)
            
            entropy_box_y = Rectangle(width=4, height=1, fill_opacity=self.fill_opacity).set_fill(PURPLE).shift(2*RIGHT+DOWN)
            entropy_label_y = Tex("$H(Y)$", color=PURPLE).next_to(entropy_box_y, RIGHT)
            
            cond_entropy_box_x = Rectangle(width=4, height=1, fill_opacity=self.fill_opacity).set_fill(BLUE_A).shift(2*LEFT+DOWN)
            cond_entropy_label_x = Tex("$H(X|Y)$", color=BLUE_A).next_to(cond_entropy_box_x, LEFT)
            
            cond_entropy_box_y = Rectangle(width=2, height=1, fill_opacity=self.fill_opacity).set_fill(PURPLE_A).shift(3*RIGHT)
            cond_entropy_label_y = Tex("$H(Y|X)$", color=PURPLE_A).next_to(cond_entropy_box_y, RIGHT)
            
            mutual_info_box = Rectangle(width=2, height=1, fill_opacity=self.fill_opacity).set_fill(GOLD).shift(2*DOWN+RIGHT)
            mutual_info_label = Tex("I(X; Y)", color=GOLD).next_to(mutual_info_box, DOWN)

            self.boxes = VGroup(joint_entropy_box, entropy_box_x, entropy_box_y, cond_entropy_box_x, cond_entropy_box_y, mutual_info_box)
            self.labels = VGroup(joint_entropy_label, entropy_label_x, entropy_label_y, cond_entropy_label_x, cond_entropy_label_y, mutual_info_label)

            self.whole = VGroup(self.boxes, self.labels)
            # if probabilities != None:
            self.update(None, np.array(probabilities))

        def update(self, scene, probabilities):
            update0 = self.boxes[0].copy().stretch_to_fit_width(self.base_width*self.scale*HXY(probabilities))
            
            update1 = self.boxes[1].copy().stretch_to_fit_width(self.base_width*self.scale*HX(probabilities))
            update1.move_to(update0.get_corner(LEFT+DOWN) , LEFT+UP)
            
            update2 = self.boxes[2].copy().stretch_to_fit_width(self.base_width*self.scale*HY(probabilities))
            update2.move_to(update0.get_corner(RIGHT+DOWN) , RIGHT+UP).shift(self.scale*DOWN)
            
            update3 = self.boxes[3].copy().stretch_to_fit_width(self.base_width*self.scale*HX_g_Y(probabilities))
            update3.move_to(update0.get_corner(LEFT+DOWN) , LEFT+UP).shift(self.scale*DOWN)
            
            update4 = self.boxes[4].copy().stretch_to_fit_width(self.base_width*self.scale*HY_g_X(probabilities))
            update4.move_to(update0.get_corner(RIGHT+DOWN) , RIGHT+UP)
            
            update5 = self.boxes[5].copy().stretch_to_fit_width(self.base_width*self.scale*I(probabilities))
            update5.move_to(update1.get_corner(RIGHT+DOWN) , RIGHT+UP).shift(self.scale*DOWN)

            if scene != None:
                scene.play(Transform(self.boxes[0], update0), self.labels[0].animate.next_to(update0, UP),
                        Transform(self.boxes[1], update1), self.labels[1].animate.next_to(update1, LEFT),
                        Transform(self.boxes[2], update2), self.labels[2].animate.next_to(update2, RIGHT),
                        Transform(self.boxes[3], update3), self.labels[3].animate.next_to(update3, LEFT),
                        Transform(self.boxes[4], update4), self.labels[4].animate.next_to(update4, RIGHT),
                        Transform(self.boxes[5], update5), self.labels[5].animate.next_to(update5, DOWN))
            else: 
                self.labels[0].next_to(update0, UP)
                self.labels[1].next_to(update1, LEFT)
                self.labels[2].next_to(update2, RIGHT)
                self.labels[3].next_to(update3, LEFT)
                self.labels[4].next_to(update4, RIGHT)
                self.labels[5].next_to(update5, DOWN)
            self.boxes[0] = update0
            self.boxes[1] = update1
            self.boxes[2] = update2
            self.boxes[3] = update3
            self.boxes[4] = update4
            self.boxes[5] = update5

        def set_scale(self, new_scale):
            self.scale = new_scale
            self.whole.scale(new_scale)
            return self


class TwoEventEntropy(Scene):
    def construct(self):
        joint_entropy_text = Tex("Joint Entropy")
        joint_entropy_text.shift(UP)
        self.play(Write(joint_entropy_text))
        conditional_entropy_text = Tex("Conditional Entropy")
        self.play(Write(conditional_entropy_text))
        mutual_information_text = Tex("Mutual Information")
        mutual_information_text.shift(DOWN)
        self.play(Write(mutual_information_text))

        self.wait(1)
        self.play(FadeOut(joint_entropy_text), FadeOut(conditional_entropy_text), FadeOut(mutual_information_text))

        colors = [RED, GREEN, RED, BLUE]
        shapes = [Square, Star, Triangle, Circle]
        
        combinations = [[True, True, True, False],
                        [False, True, True, True],
                        [True, False, True, True],
                        [True, True, False, True]]
        def make_table(combinations):
            contents = [[shape(color=color) if condition else Text("") for condition, shape in zip(row, shapes)] for row, color in zip(combinations, colors)]
            t = MobjectTable(contents,
                            row_labels=[Square(color=c, fill_opacity=1) for c in colors], 
                            col_labels=[x(color=WHITE) for x in shapes])
            t.get_vertical_lines()[0].set_color(RED)
            t.get_horizontal_lines()[0].set_color(RED)
            return t
        t = make_table(combinations)
        self.play(Create(t.scale(0.4)))
        self.wait(2)

        self.play(t.animate.become(t.copy().scale(0.4).shift(2*UP+4*RIGHT)))
        self.wait(1)

        joint_entropy_formula = Tex("$H(X,Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2(p(x,y))$")
        entropy_x_formula = Tex("$H(X) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2(\\sum\\limits_{y} p(x,y))$")
        entropy_y_formula = Tex("$H(Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2(\\sum\\limits_{x} p(x,y))$")
        conditional_entropy_formula = Tex("$H(X|Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2\\left(\\frac{p(x,y)}{p(y)}\\right)$")
        mutual_information_formula = Tex("$I(X;Y) = -\\sum\\limits_{x,y} p(x,y) \cdot \\log_2\\left(\\frac{p(x) \\cdot p(y)}{p(x,y)}\\right)$")
        
        formulas = VGroup(entropy_x_formula, entropy_y_formula, joint_entropy_formula, conditional_entropy_formula, mutual_information_formula)
        arranged_formulas = formulas.copy().scale(0.6).shift(3*UP+4*LEFT).arrange(DOWN, center=False, aligned_edge=LEFT)

        formulas[0].shift(UP + 2.5*LEFT)

        self.play(Write(formulas[0]))
        self.wait(1)

        low_frac = 12#$np.sum(combinations)
        final_eq = VGroup(*[
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=RED),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=GREEN),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=RED),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=BLUE)]).arrange(DOWN, center=False, aligned_edge=LEFT)
        
        interm_eq = VGroup(*[
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=RED),
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=RED),
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=RED)]).arrange(DOWN, center=False, aligned_edge=LEFT)
        
        base_eq = Tex(f"$-\\frac{{1}}{{{low_frac}}}$", color=RED).move_to(final_eq[0].get_corner(LEFT), LEFT)
        base_eq2 = Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", color=RED).move_to(final_eq[0].get_corner(LEFT), LEFT)
        base_eq3 = Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{low_frac}}}+\\frac{{1}}{{{low_frac}}}+\\frac{{1}}{{{low_frac}}})$", color=RED).move_to(final_eq[0].get_corner(LEFT), LEFT)
        
        
        self.play(Indicate(t.get_entries((2,2))))
        current = t.get_entries((2,2)).copy()
        self.play(Transform(current, base_eq))
        self.wait(1)
        self.play(Transform(current, base_eq2))
        self.wait(1)
        current = VGroup(*([current] + [t.get_entries(x).copy() for x in [(2,2), (2,3), (2,4)]]))
        self.play(Transform(current, base_eq3))
        self.wait(1)
        self.play(Transform(current, interm_eq[0]))
        i_eq = [current]
        for i in range(2):
            i_eq.append(t.get_entries((2,3+i)).copy())
            self.play(Transform(i_eq[-1], interm_eq[1+i]))
        i_eq = VGroup(*i_eq)
        self.play(Transform(i_eq, final_eq[0]))
        self.wait(1)
        self.play(Transform(i_eq, final_eq))
        self.wait(1)

        old_formula = Tex("$H(X) =$", "$-\\sum\\limits_{x} p(x) \cdot \log_2\\left(p(x)\\right)$").move_to(formulas[0].get_corner(RIGHT), RIGHT)
        formulas[0].save_state()
        self.play(formulas[0].animate.become(old_formula))
        self.wait(1)
        self.play(Restore(formulas[0]))
        self.wait(1)
        self.play(FadeOut(i_eq))
        self.play(Transform(formulas[0], arranged_formulas[0]))
        self.wait(1)


        self.play(Write(formulas[1]))
        self.wait(1)
        old_formula = Tex("$H(Y) =$", "$-\\sum\\limits_{y} p(y) \cdot \log_2\\left(p(y)\\right)$").move_to(formulas[1].get_corner(LEFT), LEFT)
        formulas[1].save_state()
        self.play(formulas[1].animate.become(old_formula))
        self.wait(1)
        self.play(Restore(formulas[1]))
        self.wait(1)
        self.play(Transform(formulas[1], arranged_formulas[1]))
        self.wait(1)

        self.play(Write(formulas[2]))
        self.wait(1)
        self.play(Transform(formulas[2], arranged_formulas[2]))
        self.wait(1)

        formulas[3].shift(0.5*UP + 3*LEFT)
        self.play(Write(formulas[3]))
        new_formula = Tex("$H(X|Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2\\left(p(x|y)\\right)$").move_to(formulas[3].get_corner(LEFT), LEFT)
        self.play(Transform(formulas[3], new_formula))
        self.wait(1)
        
        final_eq = VGroup(*[
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=GREEN),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=BLUE)]).arrange(DOWN, center=False, aligned_edge=LEFT)
        
        interm_eq = VGroup(*[
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED),
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED),
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED)]).arrange(DOWN, center=False, aligned_edge=LEFT)
        
        base_eq = Tex(f"$-\\frac{{1}}{{{low_frac}}}$", color=RED).move_to(final_eq[0].get_corner(LEFT), LEFT)
        base_eq2 = Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", color=RED).move_to(final_eq[0].get_corner(LEFT), LEFT)
        base_eq3 = Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED).move_to(final_eq[0].get_corner(LEFT), LEFT)
        

        self.play(Indicate(t.get_entries((2,2))))
        current = t.get_entries((2,2)).copy()
        self.play(Transform(current, base_eq))
        self.wait(1)
        self.play(Transform(current, base_eq2))
        self.wait(1)
        current = VGroup(*([current] + [t.get_entries(x).copy() for x in [(2,2), (2,3), (2,4)]]))
        self.play(Transform(current, base_eq3))
        self.wait(1)
        self.play(Transform(current, interm_eq[0]))
        i_eq = [current]
        for i in range(2):
            i_eq.append(t.get_entries((2,3+i)).copy())
            self.play(Transform(i_eq[-1], interm_eq[1+i]))
        i_eq = VGroup(*i_eq)
        self.play(Transform(i_eq, final_eq[0]))
        self.wait(1)
        self.play(Transform(i_eq, final_eq))
        self.wait(1)
        self.play(FadeOut(i_eq))
        self.play(Transform(formulas[3], arranged_formulas[3]))
        self.wait(1)
        
        self.play(Write(formulas[4]))
        self.wait(1)
        self.play(Transform(formulas[4], arranged_formulas[4]))
        self.wait(1)       
        def make_probs(combinations):
            num = np.sum(combinations)
            return np.array([[float(x)/num for x in y] for y in combinations])
        ebr = EntropyBoxRepresentation(make_probs(combinations))
        self.play(Create(ebr.set_scale(0.4).whole.shift(DOWN+3*RIGHT)))
        self.wait(1)
        combinations = [[i==j for i in range(4)]for j in range(4)]
        self.play(Transform(t, make_table(combinations).scale(0.4 * 0.4).shift(2*UP+4*RIGHT)))
        self.wait(1)
        ebr.update(self, make_probs(combinations))
        self.wait(1)

        combinations = [[True for i in range(4)] for j in range(4)]
        self.play(Transform(t, make_table(combinations).scale(0.4 * 0.4).shift(2*UP+4*RIGHT)))
        self.wait(1)
        ebr.update(self, make_probs(combinations))
        self.wait(1)
        
        joint_entropy_update = Tex("$H(X,Y) \\leq H(X) + H(Y)$")
        Tex("$H(X,Y) = H(X) + H(Y|X)$")
        Tex("$H(X) + H(Y) \\geq H(X,Y)$")
        Tex("$H(X) \\geq H(X|Y)$")
        Tex("$I(X; Y) = H(Y) - H(Y|X)$")
        Tex("$I(X; Y) = H(Y) + H(X) - H(Y,X)$")
def make_probs(p,q):
    return [[q * p, q * (1-p)],
            [(1-q) * (1-p), (1-q) * p]]

def probs_to_str(pr):
    return [[f"{x:.2f}" for x in y]for y in pr]

class BSCAnalysis(Scene):
    def construct(self):
        bsc = BSC()
        bsc.full_channel.scale(0.5).shift(DOWN+0.5*LEFT)
        self.play(Create(bsc.full_channel[:4]))
        self.wait(1)

        self.play(Create(bsc.q_label))
        self.wait(2)
        self.play(Create(bsc.one_minus_q_label))


        q = 0.5
        p = 0.9
        ebr = EntropyBoxRepresentation(make_probs(p,q))
        ebr.set_scale(0.5).whole.shift(2*UP+2*RIGHT)
        self.play(Create(ebr.boxes), Write(ebr.labels))
        
        self.wait(2)

        q_tr = ValueTracker(q)
        p_tr = ValueTracker(p)


        p_text = Tex("$p=$", f"${p_tr.get_value()}$").add_updater(lambda x: x.become(Tex("$p=$",f"${p_tr.get_value():.2f}$"), match_center=True)).shift(DOWN+5*LEFT)
        q_text = Tex("$q=$", f"${q_tr.get_value()}$").add_updater(lambda x: x.become(Tex("$q=$",f"${q_tr.get_value():.2f}$"), match_center=True)).shift(1.5*DOWN+5*LEFT)
        self.play(Write(p_text), Write(q_text))
        self.wait(1)
        pr = make_probs(p,q)

        def make_prob_table(contents):
            l = Line(0.5*UP+LEFT, 0.5*DOWN+RIGHT)
            x = Tex("X").next_to(l, DOWN+LEFT).shift(0.5*UP+RIGHT)
            y = Tex("Y").next_to(l, UP+RIGHT).shift(0.5*DOWN+LEFT)
            t = Table(contents, 
                           row_labels=[Text("0"), Text("1")], 
                           col_labels=[Text("0"), Text("1")], 
                           v_buff=0.9, h_buff=1.1,
                           top_left_entry=VGroup(l,x,y)).scale(0.4).shift(1.5*UP+3.5*LEFT)
            c = [GREEN, RED, RED, GREEN]
            ent = t.get_entries_without_labels()
            for i in range(len(c)):
                ent[i].set_color(c[i])
            return t

        prob_table = make_prob_table([["",""],["",""]])
        
        str_probs = probs_to_str(pr)
        self.play(Create(prob_table))
        self.wait(1)
        self.play(Transform(prob_table, make_prob_table([["p*q",""],["",""]])))
        self.wait(1)
        self.play(Transform(prob_table, make_prob_table([["p*q","(1-p)*q"],["",""]])))
        self.wait(1)
        self.play(Transform(prob_table, make_prob_table([["p*q","(1-p)*q"],["(1-q)*p",""]])))
        self.wait(1)
        self.play(Transform(prob_table, make_prob_table([["p*q","(1-p)*q"],["(1-q)*p","(1-q)*(1-p)"]])))
        self.wait(1)
        self.play(Transform(prob_table, make_prob_table([[f"{p}*{q}","(1-p)*q"],["(1-q)*p","(1-q)*(1-p)"]])))
        self.wait(1)
        self.play(Transform(prob_table, make_prob_table([[f"{p}*{q}",f"(1-{p})*{q}"],[f"(1-q)*p","(1-q)*(1-p)"]])))
        self.wait(1)
        self.play(Transform(prob_table, make_prob_table([[f"{p}*{q}",f"(1-{p})*{q}"],[f"(1-{q})*{p}","(1-q)*(1-p)"]])))
        self.wait(1)
        self.play(Transform(prob_table, make_prob_table([[f"{p}*{q}",f"(1-{p})*{q}"],[f"(1-{q})*{p}",f"(1-{q})*(1-{p})"]])))
        self.wait(1)
        self.play(Transform(prob_table, make_prob_table([["0.45", "0.05"], ["0.05", "0.45"]])))

        prob_table.add_updater(lambda x: x.become(
            make_prob_table(probs_to_str(make_probs(p_tr.get_value(), q_tr.get_value()))), match_center=True))

        self.play(q_tr.animate.set_value(0.6))
        ebr.update(self, np.array(make_probs(p_tr.get_value(), q_tr.get_value())))
        self.wait(2)

class NoislessChanelTheorem(MovingCameraScene):
    def construct(self):
        title = Text("THE FUNDAMENTAL THEOREM \n     FOR A NOISLESS CHANNEL")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        communication_system = VGroup() 
        source = Square()
        source.add(Text("Information\nSource", font_size=20,))
        source.shift(LEFT*3)
        communication_system.add(source)
        
        transmitter = Square()
        transmitter.add(Text("Transmitter", font_size=20))
        s_to_t = Arrow(source.get_right(), transmitter.get_left(), buff=0, max_stroke_width_to_length_ratio=1)
        communication_system.add(transmitter)
        communication_system.add(s_to_t)

        self.wait(1) 
        group = Group(source, s_to_t, transmitter)
        group.shift(LEFT*3)

        channel = Square()
        channel.add(Text("Channel", font_size=20))
        communication_system.add(Arrow(transmitter.get_right(), channel.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(channel)

        receiver = Square()
        receiver.add(Text("Receiver", font_size=20))
        receiver.shift(RIGHT*3)
        communication_system.add(Arrow(channel.get_right(), receiver.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(receiver)
        self.wait(1)
        
        destination = Square()
        destination.add(Text("Destination", font_size=20))
        destination.shift(RIGHT*6)
        communication_system.add(Arrow(receiver.get_right(), destination.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(destination)
        self.wait(1)

        self.play(Create(communication_system))
        self.wait(1)
        
        self.add(source, channel)
        communication_system.remove(source, channel)
        self.wait(1)
        self.play(FadeOut(communication_system))
        self.play(source.animate.shift(3*RIGHT), channel.animate.shift(3*RIGHT))
        self.wait(1)
        
        entropy = Tex("$H$").next_to(source, DOWN)
        self.play(Write(entropy))
        self.wait(1)

        capacity = Tex("$C =  \\lim_{T \\to \\infty} \\frac{N(T)}{T}$").next_to(channel, DOWN)
        self.play(Write(capacity))
        self.wait(1)

        self.play(FadeOut(source, entropy))
        self.play(capacity.animate.shift(3*LEFT), channel.animate.shift(3*LEFT))
        self.wait(1)

        for i in range(1):
            random_binary = "".join(["0" if random() > 0.5 else "1" for i in range(5)])
            sent_message = Tex(random_binary).next_to(channel, LEFT).shift(LEFT)
            recieved_message = sent_message.copy().next_to(channel, RIGHT).shift(RIGHT)
            self.play(Write(sent_message))
            self.play(FadeOut(sent_message, target_position=channel.get_left()))
            # self.play(ApplyWave(channel, direction=RIGHT, time_width=0.2, amplitude=0.1))
            self.play(FadeIn(recieved_message, target_position=channel.get_right()))
            self.play(FadeOut(recieved_message))
            
        self.play(capacity.animate.shift(3*RIGHT), channel.animate.shift(3*RIGHT))
        self.play(FadeIn(source, entropy), Transform(capacity, Tex("$C$").next_to(channel, DOWN)))
        self.wait(1)

        possible_rate = Tex("$Rate = \\frac{C}{H} - \\epsilon$")
        self.play(Write(possible_rate))
        self.wait(1)

        self.play(Transform(capacity, Tex("$C=2\\frac{bits}{s}$").next_to(channel, DOWN)))
        self.play(self.camera.frame.animate.scale(1.3))
        weather_conditions = VGroup(*[Text(x) for x in ["Sunny", "Rainy","Cloudy","Snowy","Windy","Stormy","Foggy","Drizzle"]])
        weather_conditions.arrange(DOWN, aligned_edge=LEFT).shift(6*LEFT).scale(0.6)

        probabilities = [0.6,0.05,0.2,0.01,0.05,0.01,0.03,0.05]

        self.play(Write(weather_conditions))
        self.wait(1)

        encodings = VGroup(*[Tex(x).scale(0.6).next_to(weather_conditions[i]) for i, x in enumerate(create_binary_digits(3))])
        self.play(Write(encodings))
        self.wait(1)
        
        def update_entropy(current_entropy, additional=None): 
            equality = '=' if current_entropy == 0 else '\\approxeq'
            old = VGroup(entropy)
            if additional != None:
                old.add(additional)
            self.play(Transform(old, Tex(f"$H{equality}{current_entropy:.2f}$").next_to(source, DOWN)))
        current_entropy = 0
        update_entropy(current_entropy)

        written_probs = VGroup(*[Tex(str(x)).scale(0.6).next_to(weather_conditions[i], LEFT)  for i,x in enumerate(probabilities)])
        self.play(Write(written_probs))
        self.wait(1)

        entropy_text = Tex("$H(X)=\\sum\\limits_{x}$","$p(x)$", "$\\cdot \\log_2($", "$\\frac{1}{p(x)}$", "$)$").shift(2*UP)
        self.play(Write(entropy_text))
        self.wait(1)
        
        def transform_entropy(p): 
            self.play(entropy_text.animate.become(Tex("$H(X)=\\sum\\limits_{x}$",f"${p}$", "$\\cdot \\log_2($", f"$\\frac{{1}}{{{p}}}$", "$)$").shift(2*UP)))
        for i,p in enumerate(probabilities):
            self.play(written_probs[i].animate.set_color(GREEN))
            self.play(FadeOut(written_probs[i].copy(), target_position=entropy_text.get_center()))
            transform_entropy(p)

            partial = p*math.log2(1/p)
            current_entropy+=(partial)
            partial_text=Tex(f"$\\approxeq{partial:.2f}$").next_to(entropy_text)
            self.play(Write(partial_text))
            update_entropy(current_entropy, partial_text)
        
        self.play(Transform(possible_rate, Tex(f"$Rate = \\frac{{2}}{{{current_entropy:.2f}}} - \\epsilon$")))
        self.play(Transform(possible_rate, Tex(f"$Rate \\approxeq {(2/current_entropy):.2f}$")))

        huffman_codings = [Tex(c).scale(0.6).next_to(weather_conditions[i]) for i,c in enumerate(["0", "1100", "10", "111000", "1101", "111001", "11101", "1111"])]
        self.play(*[Transform(e,h) for e,h in zip(encodings, huffman_codings)])
        self.wait(1)

        average_length = Tex("$L=$", "$\\sum p(x) \\cdot length(x)$").next_to(possible_rate, 7*DOWN)
        self.play(Write(average_length))
        length_formulas = VGroup()
        lengths = []

        for i, c in enumerate(["0", "1100", "10", "111000", "1101", "111001", "11101", "1111"]):
            length_formulas.add(Tex(f'${probabilities[i]} * {len(c)}{"" if i == 7 else " + "}$'))
            lengths.append(probabilities[i] * len(c))

        length_formulas.arrange_in_grid(2,4).next_to(average_length, DOWN)

        self.wait(1)
        for i in range(len(probabilities)):
            self.play(Transform(VGroup(encodings[i].copy(), written_probs[i].copy()), length_formulas[i]))
        self.wait(1)

        self.play(Transform(VGroup(average_length, length_formulas),Tex("$L=$", f"${sum(lengths)}$").next_to(possible_rate, DOWN) ))
        self.wait(1)
        self.play(Transform(possible_rate, Tex("$R=$", "$\\frac{C}{L}$")))
        self.wait(1)
        self.play(Transform(possible_rate, Tex("$R=$", f"${(2/sum(lengths)):.2f}$")))
        self.wait(1)

class NoisyChannelTheorem(ZoomedScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, zoom_factor=0.05, zoomed_camera_config={'background_opacity': 1, 'default_frame_stroke_width': 0.5}, image_frame_stroke_width=1)

    def construct(self):

        title = Text("THE FUNDAMENTAL THEOREM \n             FOR A NOISY CHANNEL")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        communication_system = VGroup() 
        source = Square()
        source.add(Text("Information\nSource", font_size=20,))
        source.shift(LEFT*3)
        communication_system.add(source)
        
        transmitter = Square()
        transmitter.add(Text("Transmitter", font_size=20))
        s_to_t = Arrow(source.get_right(), transmitter.get_left(), buff=0, max_stroke_width_to_length_ratio=1)
        communication_system.add(transmitter)
        communication_system.add(s_to_t)

        self.wait(1) 
        group = Group(source, s_to_t, transmitter)
        group.shift(LEFT*3)

        channel = Square()
        channel.add(Text("Channel", font_size=20))
        communication_system.add(Arrow(transmitter.get_right(), channel.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(channel)

        receiver = Square()
        receiver.add(Text("Receiver", font_size=20))
        receiver.shift(RIGHT*3)
        communication_system.add(Arrow(channel.get_right(), receiver.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(receiver)
        self.wait(1)
        
        destination = Square()
        destination.add(Text("Destination", font_size=20))
        destination.shift(RIGHT*6)
        communication_system.add(Arrow(receiver.get_right(), destination.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(destination)
        self.wait(1)

        noise = Square(color=RED)
        noise.add(Text("Noise", font_size=20, color=RED))
        noise.shift(DOWN*3)
        communication_system.add(noise)
        communication_system.add(Arrow( noise.get_top(), channel.get_bottom(), buff=0, max_stroke_width_to_length_ratio=1, color=RED))

        self.play(Create(communication_system))
        self.wait(1)

        bsc = BSC()
        bsc.full_channel.scale(0.7)        

        source_arrows = VGroup(Arrow(source.get_right(), bsc.input_bit_0.get_left(), buff=0.25, max_stroke_width_to_length_ratio=1, max_tip_length_to_length_ratio=0.1),
                               Arrow(source.get_right(), bsc.input_bit_1.get_left(), buff=0.25, max_stroke_width_to_length_ratio=1, max_tip_length_to_length_ratio=0.1))
        destination_arrows = VGroup(Arrow(bsc.output_bit_0.get_right(), destination.get_left(), buff=0.25, max_stroke_width_to_length_ratio=1, max_tip_length_to_length_ratio=0.1),
                                    Arrow(bsc.output_bit_1.get_right(), destination.get_left(), buff=0.25, max_stroke_width_to_length_ratio=1, max_tip_length_to_length_ratio=0.1))

        bsc.q_label.next_to(source_arrows[0], 0.1*UP)
        bsc.one_minus_q_label.next_to(source_arrows[1], 0.1*DOWN)
    
        self.add(source, destination)
        communication_system.remove(source, destination)
        self.wait(1)
        self.play(Transform(communication_system, VGroup(bsc.full_channel, source_arrows, destination_arrows)))
        self.wait(1)

        q = 0.7
        p = 0.9
        q_tr = ValueTracker(q)
        p_tr = ValueTracker(p)
        p_text = Tex("$p=$", f"${p_tr.get_value()}$").add_updater(lambda x: x.become(Tex("$p=$",f"${p_tr.get_value():.2f}$"), match_center=True)).next_to(bsc.full_channel, DOWN+RIGHT)
        q_text = Tex("$q=$", f"${q_tr.get_value()}$").add_updater(lambda x: x.become(Tex("$q=$",f"${q_tr.get_value():.2f}$"), match_center=True)).next_to(bsc.full_channel, DOWN+LEFT)
        self.play(Write(p_text), Write(q_text))
        communication_system.add(p_text, q_text, source, destination)
        self.play(communication_system.animate.scale(0.5).shift(2*LEFT+2*UP))

        rate = Tex("$R=$").shift(DOWN)
        self.play(Write(rate))
        self.wait(1)

        self.play(Transform(rate, Tex("$R$", "$=length(transmited) \\cdot p$", f"$=1000 \\cdot {p_tr.get_value()}$", f"$={1000*p_tr.get_value()}$").shift(DOWN)))
        self.play(rate.animate.set_color(RED))
        self.wait(1)

        # rate.add_updater(lambda x: x.become(Tex("$R$", "$=length(transmited) \\cdot p$", f"$=1000 \\cdot {p_tr.get_value():.2f}$", f"$={1000*p_tr.get_value():.2f}$").shift(DOWN).set_color(RED)))
        self.play(p_tr.animate.set_value(0.5))
        self.wait(1)
        self.play(p_tr.animate.set_value(0.0))
        self.wait(1)

        p_tr.set_value(0.9)
    
        ebr = EntropyBoxRepresentation(make_probs(p,q), base_width=3)
        ebr.set_scale(0.5).whole.next_to(communication_system, RIGHT)
        self.play(Create(ebr.whole))
        self.wait(1)

        self.play(Transform(rate, Tex("$R=$", "$H(X) - H(X|Y)$").shift(DOWN).set_color(GREEN)))
        self.wait(1)
        self.play(Transform(rate, Tex("$R=$", "$I(X; Y)$").shift(DOWN).set_color(GREEN)))
        def mutual_inf():  return f"{I(np.array(make_probs(p_tr.get_value(),q_tr.get_value()))):.2f}"
        self.play(Transform(rate, Tex("$R=$", "$I(X; Y)$", f"$={mutual_inf()}$").shift(DOWN).set_color(GREEN)))
        capacity = Tex("$C = Max(R)$")
        self.play(Create(capacity))
        self.wait(1)
        q_tr.set_value(0.5)
        self.play(Transform(rate, Tex("$R=$", "$I(X; Y)$", f"$={mutual_inf()}$").shift(DOWN).set_color(GREEN)))
        self.wait(1)
        self.play(Transform(capacity, Tex("$C = Max(R)$", f"$={mutual_inf()}$")))
        self.wait(1)

        self.play(FadeOut(ebr.whole, communication_system, source, destination, p_text, q_text),
                  Transform(rate, Tex("$R=$", "$I(X; Y)$").shift(DOWN + 3*RIGHT)),
                  Transform(capacity, Tex("$C = Max(R)$").shift(3*RIGHT)))

        self.wait(1)
        
        ax = Axes(x_range=[0,1], y_range=[0,1], x_length=8, y_length=8)
        labels = VGroup(ax.get_x_axis_label(label=Tex("$H(X)$"), edge=DOWN, direction=DOWN).shift(DOWN), ax.get_y_axis_label(label=Tex("$H(X|Y)$"), edge=LEFT, direction=LEFT))
        
        EPS = 1e-2
        graph = ax.plot_line_graph(x_values=[0,0.3,1], y_values=[0,EPS,0.7], add_vertex_dots=False)

        c_label = Tex("C").next_to(ax.c2p(0.3,0), DOWN)

        attainable = Polygon(*graph.get_points_defining_boundary(), ax.c2p(1,1), ax.c2p(0,1), fill_color=GREEN, fill_opacity=0.7, stroke_width=0)
        attainable_text = Tex("$attainable$").move_to(attainable.get_center())
        attainable.add(attainable_text)

        non_attainable = Polygon(ax.c2p(0,0), ax.c2p(0.3,EPS), ax.c2p(1,0.7), ax.c2p(1,0), fill_color=RED, fill_opacity=0.7,stroke_width=0)
        non_attainable_text = Tex("$non-attainable$").move_to(non_attainable.get_center_of_mass())
        non_attainable.add(non_attainable_text)

        ar_plot = VGroup(*[attainable, non_attainable, ax, labels, c_label]).scale(0.6).shift(3*LEFT)
        self.play(Create(ar_plot))
        self.wait(1)

        self.zoomed_camera.frame.move_to(ax.c2p(0.3, EPS))
        self.activate_zooming(True)
        self.wait(1)
        l = DashedLine(ax.c2p(0.3,EPS/3.5),ax.c2p(0.3, EPS), stroke_width=0.3, color=BLUE)
        t = Tex("$\\epsilon$", color=BLUE).scale(0.07).next_to(l, buff=0.01)
        self.play(Create(l), Create(t))
        self.wait(1)

                
        
def combine_positions(a,b,mask): 
    mask = np.array(mask)
    return a*mask + b*(1-mask)

class NoisyChannelTheorem2(Scene):
    def construct(self):
        communication_system = VGroup() 
        source = Square()
        source.add(Text("Information\nSource", font_size=20,))
        source.shift(LEFT*3)
        communication_system.add(source)
        
        transmitter = Square()
        transmitter.add(Text("Transmitter", font_size=20))
        s_to_t = Arrow(source.get_right(), transmitter.get_left(), buff=0, max_stroke_width_to_length_ratio=1)
        communication_system.add(transmitter)
        communication_system.add(s_to_t)

        group = Group(source, s_to_t, transmitter)
        group.shift(LEFT*3)

        channel = Square()
        channel.add(Text("Channel", font_size=20))
        communication_system.add(Arrow(transmitter.get_right(), channel.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(channel)

        receiver = Square()
        receiver.add(Text("Receiver", font_size=20))
        receiver.shift(RIGHT*3)
        communication_system.add(Arrow(channel.get_right(), receiver.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(receiver)
        
        destination = Square()
        destination.add(Text("Destination", font_size=20))
        destination.shift(RIGHT*6)
        communication_system.add(Arrow(receiver.get_right(), destination.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(destination)

        noise_text = Text("Noise", font_size=20, color=RED)
        noise=SurroundingRectangle(noise_text, color=RED)
        noise.add(noise_text)
        noise.next_to(channel.submobjects[0], DOWN)
        communication_system.add(noise)

        encoding = Text("Encoding", font_size=20, color=BLUE).next_to(transmitter.submobjects[0], DOWN)
        encoding_box = SurroundingRectangle(encoding, color=BLUE)
        encoding_box.add(encoding)

        decoding = Text("Decoding", font_size=20, color=BLUE_D).next_to(receiver.submobjects[0], DOWN)
        decoding_box = SurroundingRectangle(decoding, color=BLUE_D)
        decoding_box.add(decoding)
        self.play(Create(communication_system), Create(decoding_box), Create(encoding_box))
        self.wait(1)

        self.remove(encoding_box, decoding_box)
        self.play(Indicate(encoding_box), Indicate(decoding_box))
        self.add(encoding_box, decoding_box)
        self.play(FadeOut(encoding_box), FadeOut(decoding_box))
        self.play(communication_system.animate.shift(3*UP))
        encoding_box.shift(3*UP)
        decoding_box.shift(3*UP)
        
        source_message = VGroup(*[Tex(str(x)).scale(0.6) for x in range(0,4)]).arrange(DOWN)
        source_message.move_to(combine_positions(source.get_center(), source_message.get_center(), [1,0,0]))

        transmitted_message = VGroup(*[Tex(str(x)).scale(0.6) for x in range(0,4)]).arrange(DOWN)
        transmitted_message.move_to(combine_positions(transmitter.get_center(), transmitted_message.get_center(), [1,0,0]))

        noisy_message = VGroup(*[Tex(str(x)).scale(0.6) for x in range(0,5)]).arrange(DOWN)
        noisy_message = noisy_message.move_to(combine_positions(channel.get_center(), noisy_message.get_center(), [1,0,0]))

        destination_message = VGroup(*[Tex(str(x)).scale(0.6) for x in range(0,5)]).arrange(DOWN)
        destination_message = destination_message.move_to(combine_positions(destination.get_center(), destination_message.get_center(), [1,0,0]))

        self.play(Transform(source.copy(), source_message, replace_mobject_with_target_in_scene=True))
        self.play(Transform(transmitter.copy(), transmitted_message, replace_mobject_with_target_in_scene=True))

        s_t_arrows = VGroup(*[Line(s.get_right(), t.get_left(), buff=0.25) for s,t in zip(source_message, transmitted_message)])
        r_d_arrows = VGroup(*[Line(r.get_right(), d.get_left(), buff=0.25) for r,d in zip(noisy_message, destination_message)])
        self.play(Create(s_t_arrows))

        self.wait(1)
        t_r_arrows = []
        for i in range(4):
            src = transmitted_message[i]
            target1 = noisy_message[i]
            target2 = noisy_message[i+1]
            a1 = Line(src.get_right(), target1.get_left(), color=GREEN, buff=0.25)
            a2 = Line(src.get_right(), target2.get_left(), color=RED, buff=0.25) 
            t_r_arrows.extend([a1,a2])
            if i == 0:
                self.play(Create(target1))
            self.play(Create(a1), Create(a2), Create(target2))

        self.play(Transform(destination.copy(), destination_message, replace_mobject_with_target_in_scene=True))
        self.play(Create(r_d_arrows))

        self.play(FadeOut(source_message[1], source_message[3],
                          *t_r_arrows[2:4], *t_r_arrows[6:]))
        self.wait(1)
        self.play(FadeIn(source_message[1], source_message[3],
                          *t_r_arrows[2:4], *t_r_arrows[6:]))
        self.wait(1)

        self.play(FadeOut(*t_r_arrows, *r_d_arrows, noisy_message, destination_message))

        encoded_message = VGroup(*[Tex(str(x)).scale(0.6) for x in range(0,8,2)]).arrange(DOWN).shift(LEFT)
        encoded_message.move_to(combine_positions(transmitter.get_center(), encoded_message.get_center(), [1,0,0]))
        self.play(FadeIn(encoding_box))
        self.play(*[Transform(t, e, replace_mobject_with_target_in_scene=True) for t,e in zip(transmitted_message, encoded_message)])
        self.play(*[a.animate.set_color(encoding_box.color) for a in s_t_arrows])

        self.wait(1)
        noisy_message = VGroup(*[Tex(str(x)).scale(0.6) for x in range(0,8)]).arrange(DOWN)
        noisy_message = noisy_message.move_to(combine_positions(channel.get_center(), noisy_message.get_center(), [1,0,0]))

        noise_arrows = []
        for i in range(0, len(noisy_message), 2):
            src = encoded_message[i//2]
            target1 = noisy_message[i]
            target2 = noisy_message[i+1]
            a1 = Line(src.get_right(), target1.get_left(), color=GREEN, buff=0.25)
            a2 = Line(src.get_right(), target2.get_left(), color=RED, buff=0.25) 
            noise_arrows.extend([a1,a2])
            self.play(Create(a1), Create(a2), Create(target2), Create(target1))

        recieved_message = encoded_message.copy().move_to(combine_positions(receiver.get_center(), encoded_message.get_center(), [1,0,0]))
        decoding_arrows = []
        for i in range(0, len(noisy_message), 2):
            src1 = noisy_message[i]
            src2 = noisy_message[i+1]
            target = recieved_message[i//2]
            a1 = Line(src1.get_right(), target.get_left(), color=GREEN, buff=0.25)
            a2 = Line(src2.get_right(), target.get_left(), color=RED, buff=0.25) 
            decoding_arrows.extend([a1,a2])
            self.play(Create(a1), Create(a2), Create(target))

        decoded_message = VGroup(*[Tex(str(x)).scale(0.6) for x in range(0,4)]).arrange(DOWN).shift(RIGHT)
        self.play(FadeIn(decoding_box))
        decoded_message = decoded_message.move_to(combine_positions(destination.get_center(), decoded_message.get_center(), [1,0,0]))
        r_d_arrows = VGroup(*[Line(r.get_right(), d.get_left(), buff=0.25, color=decoding_box.color) for r,d in zip(recieved_message, decoded_message)])

        for i in range(len(decoded_message)):
            decoder_cpy = decoding_box.copy()
            self.play(FadeOut(recieved_message[i].copy(), target_position=decoder_cpy))
            self.play(Transform(decoder_cpy, r_d_arrows[i], replace_mobject_with_target_in_scene=True), Create(decoded_message[i]))

        self.wait(1)
        self.play(FadeOut(*decoding_arrows, *noise_arrows))
        self.wait(1)

        animations = []
        for grp in [source_message, encoded_message, noisy_message, recieved_message, decoded_message]:
            for i, src in enumerate(grp):
                binary_text = Tex(to_binary(int(src.get_tex_string()), 3)).scale(0.6).move_to(src)
                animations.append(Transform(src, binary_text, replace_mobject_with_target_in_scene=True))
                grp[i] = binary_text
        self.play(*animations)
        self.wait(1)

        def diff(a, b): return sum([0 if a[i]==b[i] else 1 for i in range(len(a))])
        src = encoded_message[0]
        colors = [GREEN, RED_C, RED_B, RED_A]
        transmitting_lines = []
        for r in noisy_message:
            transmitting_lines.append(Line(src.get_right(), r.get_left(), buff=0.25, color=colors[diff(src.get_tex_string(), r.get_tex_string())]))    
        self.play(*[Create(t) for t in transmitting_lines])
        self.wait(1)
        
        src = recieved_message[0]
        decoding_lines = []
        for r in noisy_message:
            decoding_lines.append(Line(r.get_right(), src.get_left(), buff=0.25, color=colors[diff(src.get_tex_string(), r.get_tex_string())]))    
        self.play(*[Create(d) for d in decoding_lines])
        self.wait(1) 

        self.play(*[FadeOut(l) for l in transmitting_lines+decoding_lines if l.color == RED_B or l.color == RED_A])
        self.wait(1) 

        src = recieved_message[3]
        new_code = Tex("111").scale(0.6).move_to(src)
        self.play(Transform(src, new_code, replace_mobject_with_target_in_scene=True)) 
        recieved_message[3] = new_code

        src = encoded_message[3]
        new_code = Tex("111").scale(0.6).move_to(src)
        self.play(Transform(src, new_code, replace_mobject_with_target_in_scene=True)) 
        encoded_message[3] = new_code
        src = encoded_message[3]

        transmitting_lines2 = []
        for r in noisy_message:
            transmitting_lines2.append(Line(src.get_right(), r.get_left(), buff=0.25, color=colors[diff(src.get_tex_string(), r.get_tex_string())]))    
        self.play(*[Create(t) for t in transmitting_lines2])
        self.wait(1)
        
        src = recieved_message[3]
        decoding_lines2 = []
        for r in noisy_message:
            decoding_lines2.append(Line(r.get_right(), src.get_left(), buff=0.25, color=colors[diff(src.get_tex_string(), r.get_tex_string())]))    
        self.play(*[Create(d) for d in decoding_lines2])
        self.wait(1)

        self.play(*[FadeOut(l) for l in transmitting_lines2+decoding_lines2 if l.color == RED_B or l.color == RED_A])
        self.wait(1)

def num_binary_ones(length, num_ones):
    return int(math.factorial(length) / (math.factorial(num_ones) * math.factorial(length - num_ones)))

def possible_outcomes(length, flip_prob):
    probs, counts = [],[]
    for i in range(length + 1):
        counts.append(num_binary_ones(length, i))
        probs.append(pow(flip_prob, i) * pow(1-flip_prob, length-i))
    return counts, probs

class NoisyChannelTheorem3(Scene):
    def construct(self):
        flip_prob=0.1
        rel=0.95
        flip_prob_text = Tex(f"$p = {flip_prob}$").shift(3*UP+6*LEFT)
        stay_prob_text = Tex(f"$q = {1-flip_prob}$").next_to(flip_prob_text)
        message_length = Tex("Message length = 3").next_to(stay_prob_text)
        desired_reliability = Tex(f"Desired reliability= {int(rel*100)}\%").next_to(message_length)
        message = Tex("$000$").shift(3*LEFT)
        digits = create_binary_digits(3)
        digits.sort(key=lambda x: x.count("1"))
        outcomes = VGroup(*[Tex(str(x)) for x in digits]).arrange(DOWN).shift(4*LEFT)

        self.play(Create(flip_prob_text), Create(stay_prob_text), Create(message_length), Create(message), Create(desired_reliability))  
        self.wait(1)
        self.play(Transform(message, outcomes, replace_mobject_with_target_in_scene=True))
        counts, probs = possible_outcomes(3, flip_prob)        
        final_probs = [ p for c,p in zip (counts, probs) for i in range(c)]
        individual_probs = VGroup() 
        for i in range(8):
            components = ["q" if d == '0' else "p" for d in digits[i]]
            x =Tex("$" + "*".join(components) + "$").next_to(outcomes[i]) 
            individual_probs.add(x)
            y = Tex(f"${final_probs[i]:.4f}$").next_to(outcomes[i])
            self.play(Create(x))
            self.play(Transform(x, y))

        current_rel = 0 
        rel_text = Tex(f"Reliability = {int(current_rel*100)}\%").shift(UP+0.5*DOWN)
        for i in range(8):
            current_rel+=final_probs[i]
            self.play(outcomes[i].animate.set_color(GREEN),
                      individual_probs[i].animate.set_color(GREEN))
            self.play(Transform(rel_text, Tex(f"Reliability = {int(current_rel*100)}\%").move_to(rel_text)))
            if(current_rel>=rel):
                break

        used_messages=(i+1)

        used_messages_text = Tex(f"Used messages = {used_messages}").next_to(rel_text, DOWN, aligned_edge=LEFT)
        total_messages = Tex(f"Total messages = 8").next_to(used_messages_text, DOWN, aligned_edge=LEFT)
        self.play(Create(used_messages_text), Create(total_messages))

        reliably_encoded = Tex("Reliably encoded ", "messages = ").next_to(total_messages, DOWN, aligned_edge=LEFT)
        calculated_total=Tex("Reliably encoded ", "messages = ", f"$\\frac{{{8}}}{{{used_messages}}}$").move_to(reliably_encoded, aligned_edge=LEFT)
        self.play(Transform(VGroup(reliably_encoded, used_messages_text.copy(), total_messages.copy()), calculated_total,
                            replace_mobject_with_target_in_scene=True))
        reliably_encoded = calculated_total
        self.play(Transform(reliably_encoded,Tex("Reliably encoded ", "messages = ", f"${8/used_messages}$").move_to(reliably_encoded, LEFT)))
        self.play(Transform(reliably_encoded,Tex("Reliably encoded ", "bits = ", "$\\log_2($", f"${8/used_messages}$",")").move_to(reliably_encoded, LEFT)))
        self.play(Transform(reliably_encoded,Tex("Reliably encoded ", "bits = ", "$\\log_2($", f"${8/used_messages}$",")").move_to(reliably_encoded, LEFT)))
        self.play(Transform(reliably_encoded,Tex("Reliably encoded ", "bits = ", "1").move_to(reliably_encoded, LEFT)))
        reliably_encoded_percent =Tex("Reliably encoded ", "\\% bits = ", f"$100\\% \\cdot \\frac{{\\log_2({8/used_messages})}}{{3}}$").next_to(reliably_encoded, DOWN, aligned_edge=LEFT) 
        self.play(Create(reliably_encoded_percent))
        self.play(Transform(reliably_encoded_percent,Tex("Reliably encoded ", "\\% bits = ", "$33.(3)\\%$").move_to(reliably_encoded_percent, aligned_edge=LEFT)))
        self.wait(1)

        counts, probs = possible_outcomes(4, flip_prob)        
        final_probs = [ p for c,p in zip (counts, probs) for i in range(c)]

        digits = create_binary_digits(4)
        digits.sort(key=lambda x: x.count("1"))
        new_outcomes = VGroup(*[Tex(str(x)) for x in digits]).scale(0.5).arrange(DOWN, 0.15).shift(4*LEFT)
        new_individual_probs = VGroup(*[Tex(f"${final_probs[i]:.4f}$").scale(0.5).next_to(new_outcomes[i]) for i in range(16)])
        self.play(Transform(message_length, Tex("Message length = 4").move_to(message_length)))
        self.play(Transform(outcomes, new_outcomes), Transform(individual_probs, new_individual_probs))
        self.wait(1)
            
        current_rel = 0 
        for i in range(16):
            current_rel+=final_probs[i]
            self.play(outcomes[i].animate.set_color(GREEN),
                      individual_probs[i].animate.set_color(GREEN))
            self.play(Transform(rel_text, Tex(f"Reliability = {int(current_rel*100)}\%").move_to(rel_text)))
            if(current_rel>=rel):
                break

        used_messages=(i+1)
        self.play(Transform(used_messages_text, Tex(f"Used messages = {used_messages}\%").move_to(used_messages_text, aligned_edge=LEFT)),
                  Transform(total_messages, Tex(f"Total messages = 16").move_to(total_messages, aligned_edge=LEFT)),
                  Transform(reliably_encoded, Tex("Reliably encoded ", "bits = ", f"${math.log2(16/used_messages):.2f}$").move_to(reliably_encoded, aligned_edge=LEFT)),
                  Transform(reliably_encoded_percent, Tex("Reliably encoded ", "\\% bits = ", f"${math.log2(16/used_messages)*100/4:.2f}\\%$").move_to(reliably_encoded_percent, aligned_edge=LEFT)))
        self.wait(1)

        bits_used = []
        bits_encoded=[]
        percent_bits_encoded=[]
        for i in [3,4,10,20,32,64]:
            bits_used.append(i)
            counts, probs = possible_outcomes(i,flip_prob)
            current_rel = 0
            used_messages=0
            for c,p in zip(counts, probs):
                if current_rel + c*p >=rel:
                    used_messages = used_messages + math.ceil((rel-current_rel)/p)
                    break
                else:
                    current_rel+=c*p
                    used_messages+=c
            bits_encoded.append(math.log2(2**i/used_messages))
            percent_bits_encoded.append(round(bits_encoded[-1]*100/i, 2))

            print(f"possible bits % = {math.log2(2**i/used_messages)*100/i:.2f} possible bits ={math.log2(2**i/used_messages)}")

        chart = BarChart(
            values = percent_bits_encoded,
            y_range=[0, 100, 10],
            y_length=5,
            bar_names = [str(x) for x in bits_used]
        ).shift(3*RIGHT)
        c_bar_labels=chart.get_bar_labels()

        self.play(Transform(VGroup(message, outcomes, individual_probs, message_length, rel_text, used_messages_text, total_messages, reliably_encoded, reliably_encoded_percent),
                             chart, replace_mobject_with_target_in_scene=True))
        self.play(FadeIn(c_bar_labels))
        self.wait(1)

        rel=0.9999
        bits_used = []
        bits_encoded=[]
        percent_bits_encoded=[]
        for i in [3,4,10,20,32,64]:
            bits_used.append(i)
            counts, probs = possible_outcomes(i,flip_prob)
            current_rel = 0
            used_messages=0
            for c,p in zip(counts, probs):
                if current_rel + c*p >=rel:
                    used_messages = used_messages + math.ceil((rel-current_rel)/p)
                    break
                else:
                    current_rel+=c*p
                    used_messages+=c
            bits_encoded.append(math.log2(2**i/used_messages))
            percent_bits_encoded.append(round(bits_encoded[-1]*100/i, 2))

            print(f"possible bits % = {math.floor(math.log2(2**i/used_messages))/i:.2f} possible bits ={math.floor(math.log2(2**i/used_messages))}")
        self.play(Transform(desired_reliability, Tex(f"Desired reliability = {rel*100:.2f}\%").move_to(desired_reliability)))
        self.play(FadeOut(c_bar_labels))
        self.play(chart.animate.change_bar_values(percent_bits_encoded))
        c_bar_labels = chart.get_bar_labels()
        self.play(FadeIn(c_bar_labels))
        self.wait(1)

class NoisyChannelTheorem4(Scene):
    def construct(self):
        communication_system = VGroup() 
        source = Square()
        source.add(Text("Information\nSource", font_size=20,))
        source.shift(LEFT*3)
        communication_system.add(source)
        
        transmitter = Square()
        transmitter.add(Text("Transmitter", font_size=20))
        s_to_t = Arrow(source.get_right(), transmitter.get_left(), buff=0, max_stroke_width_to_length_ratio=1)
        communication_system.add(transmitter)
        communication_system.add(s_to_t)

        group = Group(source, s_to_t, transmitter)
        group.shift(LEFT*3)

        channel = Square()
        channel.add(Text("Channel", font_size=20))
        communication_system.add(Arrow(transmitter.get_right(), channel.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(channel)

        receiver = Square()
        receiver.add(Text("Receiver", font_size=20))
        receiver.shift(RIGHT*3)
        communication_system.add(Arrow(channel.get_right(), receiver.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(receiver)
        
        destination = Square()
        destination.add(Text("Destination", font_size=20))
        destination.shift(RIGHT*6)
        communication_system.add(Arrow(receiver.get_right(), destination.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(destination)

        noise_text = Text("Noise", font_size=20, color=RED)
        noise=SurroundingRectangle(noise_text, color=RED)
        noise.add(noise_text)
        noise.next_to(channel.submobjects[0], DOWN)
        communication_system.add(noise)

        encoding = Text("Encoding", font_size=20, color=BLUE).next_to(transmitter.submobjects[0], DOWN)
        encoding_box = SurroundingRectangle(encoding, color=BLUE)
        encoding_box.add(encoding)

        decoding = Text("Decoding", font_size=20, color=BLUE_D).next_to(receiver.submobjects[0], DOWN)
        decoding_box = SurroundingRectangle(decoding, color=BLUE_D)
        decoding_box.add(decoding)
        self.play(Create(communication_system), Create(decoding_box), Create(encoding_box))
        self.wait(1)

        self.play(communication_system.animate.shift(3*UP),
                  encoding_box.animate.shift(3*UP),
                  decoding_box.animate.shift(3*UP))

        bsc = BSC()
        bsc.full_channel.scale(0.7).shift(3*UP)        
        bsc.full_channel.remove(bsc.q_label, bsc.one_minus_q_label, bsc.one_minus_p_label0, bsc.p_label0, bsc.one_minus_p_label1, bsc.p_label1)
 
        source_arrows = VGroup(Arrow(source.get_right(), bsc.input_bit_0.get_left(), buff=0.25, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1),
                               Arrow(source.get_right(), bsc.input_bit_1.get_left(), buff=0.25, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1))
        destination_arrows = VGroup(Arrow(bsc.output_bit_0.get_right(), destination.get_left(), buff=0.25, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1),
                                    Arrow(bsc.output_bit_1.get_right(), destination.get_left(), buff=0.25, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1))

        communication_system.add(encoding_box, decoding_box)
        self.wait(1)
        self.play(Transform(communication_system, VGroup(bsc.full_channel, source_arrows, destination_arrows, source.copy(), destination.copy()).shift(LEFT).scale(0.5)))
        self.wait(1)
        
        radius=DEFAULT_SMALL_DOT_RADIUS
        buffer=0.15
        three_dots = VGroup(*[Dot(radius=radius*2/3, color=GREY) for _ in range(3)]).arrange(DOWN,buff=0.1)

        def create_digits(l):
            binary_digits = create_binary_digits(l)
            binary_digits.sort(key=lambda x: x.count("1"))
            tex_digits = [Tex(x).scale(0.7) for x in binary_digits]
            if l < 4:
                return VGroup(*tex_digits).arrange(DOWN, center=False, buff=buffer)
            return VGroup(*(tex_digits[:6] + [three_dots] + tex_digits[-6:])).arrange(DOWN, center=False, buff=buffer)

        self.play(ShowPassingFlash(source_arrows.copy().set_color(BLUE), time_width=0.7))
        x_outcomes = create_digits(1).shift(1.5*UP)
        x_outcomes.move_to(combine_positions(bsc.input_0_text.get_center(), x_outcomes.get_center(), [1, 0, 0]))
        self.play(Transform(VGroup(bsc.input_0_text.copy(), bsc.input_1_text.copy()), x_outcomes, replace_mobject_with_target_in_scene=True))

        self.play(ShowPassingFlash(bsc.arrows.copy().set_color(BLUE), time_width=0.7))
        y_outcomes = x_outcomes.copy()
        y_outcomes.move_to(combine_positions(bsc.output_1_text.get_center(), y_outcomes.get_center(), [1, 0, 0]))
        self.play(Transform(VGroup(bsc.output_0_text.copy(), bsc.output_1_text.copy()), y_outcomes, replace_mobject_with_target_in_scene=True))
        self.wait(1)
        usage = Tex("$T = $", "1").next_to(x_outcomes, LEFT).shift(2*LEFT)
        self.play(Create(usage))

        for l in range(2, 5):
            self.play(Transform(usage, Tex("$T = $", f"{l}").move_to(usage)))
            self.play(ShowPassingFlash(source_arrows.copy().set_color(BLUE), time_width=0.7))
            dir = x_outcomes.get_edge_center(UP)
            x_outcomes = VGroup(x_outcomes, bsc.input_0_text.copy(), bsc.input_1_text.copy())
            self.play(Transform(x_outcomes, create_digits(l).move_to(dir, aligned_edge=UP)))
            self.play(ShowPassingFlash(bsc.arrows.copy().set_color(BLUE), time_width=0.7))
            dir = y_outcomes.get_edge_center(UP)
            y_outcomes = VGroup(y_outcomes, bsc.output_0_text.copy(), bsc.output_1_text.copy())
            self.play(Transform(y_outcomes, create_digits(l).move_to(dir, aligned_edge=UP)))
        self.wait(1)

        binary_digits = create_binary_digits(7)
        binary_digits.sort(key=lambda x: x.count("1"))
        tex_digits = [Tex(x[:3], "...", x[-3:]).scale(0.7) for x in binary_digits]
        long_message = VGroup(*(tex_digits[:6] + [three_dots] + tex_digits[-6:])).arrange(DOWN, center=False, buff=buffer)

        self.play(Transform(usage, Tex("$T \\to \\infty$").move_to(usage)))
        self.play(Transform(x_outcomes, long_message.copy().move_to(x_outcomes, aligned_edge=UP)))
        self.play(Transform(y_outcomes, long_message.copy().move_to(y_outcomes, aligned_edge=UP)))
        self.wait(1)
        
        dot_anims = []
        for i in range(len(x_outcomes)):
            if i != 6:
                dot_anims.append(Transform(x_outcomes[i], Dot(radius=radius).move_to(x_outcomes[i])))
                dot_anims.append(Transform(y_outcomes[i], Dot(radius=radius).move_to(y_outcomes[i])))

        self.play(LaggedStart(*dot_anims))
        self.wait(1)

        probable_messages = Tex("$2^{T}$").next_to(usage, DOWN)
        self.play(Transform(usage.copy(), probable_messages, replace_mobject_with_target_in_scene=True))

        all_arrows = VGroup()
        
        causes_arrows = VGroup()
        for i in range(13):
            causes_arrows.add(Line(x_outcomes[0].get_center(), y_outcomes[i].get_center(), stroke_width=1))

        self.play(LaggedStart(*[Create(c) for c in causes_arrows]))
        all_arrows.add(causes_arrows)
        self.wait(1)

        error_free1 = Tex("$2^{R} = $", "$\\frac{}{}$").shift(2*RIGHT)
        error_free2 = Tex("$2^{R} = $", "$\\frac{output\\ messages}{}$").move_to(error_free1, LEFT)
        error_free3 = Tex("$2^{R} = $", "$\\frac{output\\ messages}{unique\\ messages}$").move_to(error_free2, LEFT)

        self.play(Create(error_free1))
        self.wait(1)
        self.play(Transform(VGroup(error_free1, y_outcomes.copy()), error_free2, replace_mobject_with_target_in_scene=True))
        self.wait(1)
        self.play(Transform(VGroup(error_free2, causes_arrows.copy()), error_free3, replace_mobject_with_target_in_scene=True))
        self.wait(1)

        num_output = probable_messages.copy().next_to(causes_arrows, DOWN)
        num_noised = probable_messages.copy().next_to(y_outcomes, DOWN)
        self.play(Transform(causes_arrows.copy(), num_output, replace_mobject_with_target_in_scene=True))
        self.play(Transform(y_outcomes.copy(), num_noised, replace_mobject_with_target_in_scene=True))

        self.wait(1)
        self.play(Transform(error_free3, Tex("$2^{R} = $", "$\\frac{2^{T}}{2^{T}}$").move_to(error_free3, LEFT)),
                    FadeOut(num_output, num_noised))
        self.wait(1)
        self.play(Transform(error_free3, Tex("$2^{R} = $", "$\\frac{2^{T}}{2^{T}}$", "$ = 2^0$").move_to(error_free3, LEFT)))
        self.wait(1)
        self.play(Transform(error_free3, Tex("$2^{R} = $", "$\\frac{2^{T}}{2^{T}}$", "$ = 2^0$", "$ = 1$").move_to(error_free3, LEFT)))
        self.wait(1)


        uncreation = []
        for i in range(12, 2, -1):
            uncreation.append(Uncreate(causes_arrows[i]))

        self.play(LaggedStart(*uncreation))

        for i in range(12, 2, -1):
            causes_arrows.remove(causes_arrows[i])

        creation = []
        for i in range(1,13):
            if i == 6: continue
            causes_arrows = VGroup()
            for j in range(3):
                idx = i+j if i<=6 else i-j
                causes_arrows.add(Line(x_outcomes[i].get_center(), y_outcomes[idx].get_center(), stroke_width=1))
                if idx == 6: break

            creation.append(LaggedStart(*[Create(c) for c in causes_arrows]))
            all_arrows.add(causes_arrows)
        self.play(LaggedStart(*creation))
        
        uncreation = []
        for i in range(11, 0, -1):
            if i in [0, 3, 8, 11]: continue
            uncreation.append(LaggedStart(*[Uncreate(a) for a in all_arrows[i]]))
        self.play(LaggedStart(*uncreation))

        for i in range(11, 0, -1):
            if i in [0, 3, 8, 11]: continue
            all_arrows.remove(all_arrows[i])
        self.wait(1)

        self.play(Transform(num_output, Tex("$2^{H(Y)T}$").move_to(num_output, LEFT+DOWN)),
                 Transform(error_free3, Tex("$2^{R} = $", "$\\frac{2^{H(Y)T}}{2^{T}}$").move_to(error_free3, LEFT)))
        self.play(Transform(num_noised, Tex("$2^{H(Y|X)T}$").move_to(num_noised, LEFT+DOWN)),
                 Transform(error_free3, Tex("$2^{R} = $", "$\\frac{2^{H(Y)T}}{2^{H(Y|X)T}}$").move_to(error_free3, LEFT)))
        self.wait(1)
        self.play(Transform(error_free3, Tex("$2^{R} = $", "$2^{I(X;Y)T}$").move_to(error_free3, LEFT)))
        self.wait(1)

class Entry:
    def __init__(self, main_tex, subtexts = []):
        self.main = Tex(main_tex)
        self.list = BulletedList(*subtexts)

    def open(self):
        return Transform(self.main.copy(), self.list.next_to(self.main, DOWN, aligned_edge=LEFT), replace_mobject_with_target_in_scene=True)

    def close(self):
        return FadeOut(self.list)

class TableOfContents(Scene):
    def construct(self):

        information_content = Entry("1. Information", ["What is information?", "How do we measure information?"]) 
        entropy = Entry("2. Entropy", ["Uncertainty", "Surprise", "Information"]) 
        two_event_entropy = Entry("3. Entropy with multiple events", ["","Mutual information"])
        communication_system = Entry("4. Communication System", ["General communication system", "Example: Binary Symmetric Channel", "Analysis of a BSC"])
        noiseless_channel = Entry("5. Noiseless Channel Theorem", ["How much data can we send", "How to encode data efficiently"])
        noisy_channel = Entry("6. Noisy Channel Theorem", ["How to send messages reliably in presence of noise", "How much data can we send?"])

        entries = [information_content, entropy, two_event_entropy, communication_system, noiseless_channel, noisy_channel]
        entries[0].main.shift(2*LEFT + 3*UP)
        for i in range(1, len(entries)):
            entries[i].main.next_to(entries[i-1].main, DOWN, aligned_edge=LEFT)
        for e in entries:
            self.play(Create(e.main))
            self.wait(1)
            self.play(e.open())
            self.wait(1)
            self.play(e.close())
            self.wait(1)
        
