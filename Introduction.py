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
        self.wait(3)

        self.play(FadeIn(entropy_formula_2.shift(UP)), FadeIn(*balls))
        new_balls = [Dot(color=GREEN).move_to(balls[0].get_center() + 2*DOWN + i * RIGHT) for i in range(5)]
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
        

class EntropyBoxRepresentation:
        def __init__(self):
            self.scale=1
            self.base_width = 6
            joint_entropy_box = Rectangle(width=self.base_width, height=1, fill_opacity=0.5).set_fill(GREEN).shift(UP)
            joint_entropy_label = Tex("$H(X,Y)$",color=GREEN).next_to(joint_entropy_box, UP)

            entropy_box_x = Rectangle(width=6, height=1, fill_opacity=0.5).set_fill(TEAL).shift(1*LEFT)
            entropy_label_x = Tex("$H(X)$", color=TEAL).next_to(entropy_box_x, LEFT)
            
            entropy_box_y = Rectangle(width=4, height=1, fill_opacity=0.5).set_fill(YELLOW).shift(2*RIGHT+DOWN)
            entropy_label_y = Tex("$H(Y)$", color=YELLOW).next_to(entropy_box_y, RIGHT)
            
            cond_entropy_box_x = Rectangle(width=4, height=1, fill_opacity=0.5).set_fill(TEAL_A).shift(2*LEFT+DOWN)
            cond_entropy_label_x = Tex("$H(X|Y)$", color=TEAL_A).next_to(cond_entropy_box_x, LEFT)
            
            cond_entropy_box_y = Rectangle(width=2, height=1, fill_opacity=0.5).set_fill(YELLOW_A).shift(3*RIGHT)
            cond_entropy_label_y = Tex("$H(Y|X)$", color=YELLOW_A).next_to(cond_entropy_box_y, RIGHT)
            
            mutual_info_box = Rectangle(width=2, height=1, fill_opacity=0.5).set_fill(GOLD).shift(2*DOWN+RIGHT)
            mutual_info_label = Tex("I(X; Y)", color=GOLD).next_to(mutual_info_box, DOWN)

            self.boxes = VGroup(joint_entropy_box, entropy_box_x, entropy_box_y, cond_entropy_box_x, cond_entropy_box_y, mutual_info_box)
            self.labels = VGroup(joint_entropy_label, entropy_label_x, entropy_label_y, cond_entropy_label_x, cond_entropy_label_y, mutual_info_label)

            self.whole = VGroup(self.boxes, self.labels)

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

            scene.play(Transform(self.boxes[0], update0), self.labels[0].animate.next_to(update0, UP),
                       Transform(self.boxes[1], update1), self.labels[1].animate.next_to(update1, LEFT),
                       Transform(self.boxes[2], update2), self.labels[2].animate.next_to(update2, RIGHT),
                       Transform(self.boxes[3], update3), self.labels[3].animate.next_to(update3, LEFT),
                       Transform(self.boxes[4], update4), self.labels[4].animate.next_to(update4, RIGHT),
                       Transform(self.boxes[5], update5), self.labels[5].animate.next_to(update5, DOWN))
            
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
        self.wait(3)

        self.play(Create(bsc.q_label))
        self.wait(2)
        self.play(Create(bsc.one_minus_q_label))


        ebr = EntropyBoxRepresentation()
        ebr.set_scale(0.5).whole.shift(2*UP+2*RIGHT)
        self.play(Create(ebr.boxes), Write(ebr.labels))
        
        self.wait(2)
        q = 0.5
        p = 0.9

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

