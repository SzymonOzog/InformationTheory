from manim import * #NOQA
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from entropy import * #NOQA
from random import random 


class CommunicationSystem(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            # RecorderService()
            GTTSService(transcription_model='base')
        )
        toc = TOC(3)

        with self.voiceover(
            """Hello and welcome to episode 4 in our series on Information Theory
            In this episode we will talk about <bookmark mark='1'/> a communication system
            and more specifically <bookmark mark='2'/>
            We will create a blueprint for our communication system, we will show an example of a 
            binary symmetric channel and analyze it 
            """
                            ) as trk:
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("1")
            self.play(*[Unwrite(e.main) for e in toc.entries[4:]])
            self.wait_until_bookmark("2")
            self.play(toc.entries[3].open())
        source = Square()
        source.add(Text("Information\nSource", font_size=20,))
        
        transmitter = Square()
        transmitter.add(Text("Transmitter", font_size=20))
        

        channel = Square()
        channel.add(Text("Channel", font_size=20))

        receiver = Square()
        receiver.add(Text("Receiver", font_size=20))
        receiver.shift(RIGHT*3)
        self.wait(1)
        
        destination = Square()
        destination.add(Text("Destination", font_size=20))
        destination.shift(RIGHT*6)
        self.wait(1)

        noise = Square(color=RED)
        noise.add(Text("Noise", font_size=20, color=RED))
        noise.shift(DOWN*3)

        
        self.wait(1)



        with self.voiceover("""
        Our blueprint for a communication system <bookmark mark='1'/>starts with a source, it produces information,
        and passes it to the <bookmark mark='2'/> transmitter, whose job is to send it via <bookmark mark='3'/>a channel
        to <bookmark mark='4'/> the receiver that further passes the information <bookmark mark='5'/> to the destination
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(toc.get_open(3), source,replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("2")
            self.play(source.animate.shift(LEFT*3))
            self.play(Create(transmitter))
            s_to_t = Arrow(source.get_right(), transmitter.get_left(), buff=0, max_stroke_width_to_length_ratio=1)
            self.play(Create(s_to_t))
            self.wait_until_bookmark("3")
            group = Group(source, s_to_t, transmitter)
            self.play(group.animate.shift(LEFT*3))
            t_to_c = Arrow(transmitter.get_right(), channel.get_left(), buff=0, max_stroke_width_to_length_ratio=1)
            self.play(Create(t_to_c))
            self.play(Create(channel))
            self.wait_until_bookmark("4")
            c_to_r = Arrow(channel.get_right(), receiver.get_left(), buff=0, max_stroke_width_to_length_ratio=1)
            self.play(Create(c_to_r))
            self.play(Create(receiver))
            self.wait_until_bookmark("5")
            r_to_d = Arrow(receiver.get_right(), destination.get_left(), buff=0, max_stroke_width_to_length_ratio=1)
            self.play(Create(r_to_d))
            self.play(Create(destination))


        with self.voiceover("""
        This is a case known as a noiseless channel,<bookmark mark='1'/>where there message is unchanged across all of the
        steps along it's way
            """) as trk:
            self.wait_until_bookmark("1")
            for x in self.mobjects:
                self.play(x.animate.set_color(GREEN))

        encoding = Text("Encoding", font_size=20, color=GREEN).next_to(transmitter.submobjects[0], DOWN)
        encoding_box = SurroundingRectangle(encoding, color=GREEN)
        decoding = Text("Decoding", font_size=20, color=GREEN).next_to(receiver.submobjects[0], DOWN)
        decoding_box = SurroundingRectangle(decoding, color=GREEN)

        with self.voiceover("""We will end with
        But most often our channel is not perfect and there is <bookmark mark='1'/> noise acting on it,
        that partially corrupts our message. The job of the transmitter and the receiver <bookmark mark='2'/>is to encode and decode
        said information in a way <bookmark mark='3'/>that reduces the amount of corruption introduced by the noise
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Create(noise))
            n_to_c = Arrow( noise.get_top(), channel.get_bottom(), buff=0, max_stroke_width_to_length_ratio=1, color=RED)
            self.play(Create(n_to_c))
            for x in [channel, receiver, destination]:
                self.play(x.animate.set_color(YELLOW))
            self.wait_until_bookmark("2")
            self.play(Create(encoding), Create(decoding),
                    Create(encoding_box), Create(decoding_box))
            self.wait_until_bookmark("3")
            for x in [receiver, destination]:
                self.play(x.animate.set_color(GREEN))
        # self.play(FadeOut(*[o for o in self.mobjects]))
        self.wait(1)

        title = Tex("Binary Symmetric Channel").scale(1.5).shift(3.2*UP)
        with self.voiceover("""
        Let' go over an example and introduce <bookmark mark='1'/> the Binary Symmetric Channel
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(title))

        bsc = BSC()
        with self.voiceover("""
        Our transmitter will be sending <bookmark mark='1'/> binary digits, that will be passed down to <bookmark mark='2'/>the receiver 
        and our channel will send our bit with a <bookmark mark='3'/>probability of p and flip it with a probability of 1 minus p
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(VGroup(transmitter, t_to_c, s_to_t, encoding, encoding_box), VGroup(*bsc.bits[:2], *bsc.texts[:2]), replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("2")
            self.play(Transform(VGroup(receiver, c_to_r, r_to_d, decoding, decoding_box), VGroup(*bsc.bits[2:], *bsc.texts[2:]), replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("3")
            self.play(Transform(VGroup(channel, noise, n_to_c), VGroup(*bsc.arrows, *bsc.labels), replace_mobject_with_target_in_scene=True))

        input_string = "001000101"
        flips = [False] * len(input_string)
        flips[0] = True
        flips[1] = True
        flips[2] = True
        flips[3] = True
        flips[8] = True

        input_text = [Tex(bit).next_to(source, DOWN, aligned_edge=RIGHT).scale(0.7).shift((0.2*i)*LEFT) for i, bit in enumerate(reversed(input_string))]
        
        with self.voiceover("""
        Let's say that we want to transmit this <bookmark mark='1'/> sequence of bits through our channel
            """) as trk:
            self.wait_until_bookmark("1")
            for t in reversed(input_text):
                self.play(Write(t))
        
        
        results = []
        with self.voiceover("""
        We just go over every bit in the input sequence and pass it into our channel, it then it flips some of the bits with a certain probability
        and sends some of the bits unchanged
            """) as trk:
            for i,(bit, text, flip) in enumerate(zip(input_string, input_text, flips)):
                src = bsc.input_bit_0.get_center() if bit == "0" else bsc.input_bit_1.get_center()
                if bit == "0":
                    target = bsc.output_bit_1.get_center() if flip else bsc.output_bit_0.get_center()  
                else:
                    target = bsc.output_bit_0.get_center() if flip else bsc.output_bit_1.get_center()
                resulting_bit = "0" if (target == bsc.output_bit_0.get_center()).all() else "1"

                self.play(FadeOut(text.copy(), target_position=src))

                def animate(arrow): self.play(ShowPassingFlash(arrow.copy().set_color(BLUE), time_width=0.2))
                if resulting_bit == "0" and bit == "0":
                    animate(bsc.arrow_00)
                elif resulting_bit == "1" and bit == "0":
                    animate(bsc.arrow_01)
                elif resulting_bit == "0" and bit == "1":
                    animate(bsc.arrow_10)
                else:
                    animate(bsc.arrow_11)

                result = Tex(resulting_bit, color=GREEN if resulting_bit == bit else RED).scale(0.7).next_to(destination, DOWN, aligned_edge=LEFT).shift((0.2*i)*RIGHT)
                self.play(FadeIn(result, target_position=target))
                results.append(result)
        source_arrows = VGroup(Arrow(source.get_right(), bsc.input_bit_0.get_left(), buff=0.25, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1),
                            Arrow(source.get_right(), bsc.input_bit_1.get_left(), buff=0.25, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1))
        with self.voiceover("""
        We can now perform an analysis of that channel,  imagine that instead of a predetermined<bookmark mark='1'/> message, we send bits 0 
        with a certain probablility q and we send 1 otherwise
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(VGroup(*input_text), VGroup(source_arrows, bsc.q_label, bsc.one_minus_q_label), replace_mobject_with_target_in_scene=True))


        q = 0.5
        p = 0.9
        pr = make_probs(p,q)
        joint_entropy_formula = Tex("$H(X,Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2(p(x,y))$")
        entropy_x_formula = Tex("$H(X) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2(\\sum\\limits_{y} p(x,y))$")
        entropy_y_formula = Tex("$H(Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2(\\sum\\limits_{x} p(x,y))$")
        conditional_entropy_formula = Tex("$H(X|Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2\\left(\\frac{p(x,y)}{p(y)}\\right)$")
        conditional_entropy_formula2 = Tex("$H(Y|X) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2\\left(\\frac{p(x,y)}{p(x)}\\right)$")
        mutual_information_formula = Tex("$I(X;Y) = $", "$-\\sum\\limits_{x,y} p(x,y) \cdot \\log_2\\left(\\frac{p(x) \\cdot p(y)}{p(x,y)}\\right)$")
        
        formulas = VGroup(entropy_x_formula, entropy_y_formula, joint_entropy_formula, conditional_entropy_formula, conditional_entropy_formula2, mutual_information_formula)

        bsc_and_source = VGroup(bsc.full_channel, source, source_arrows)
        q_tr = ValueTracker(q)
        p_tr = ValueTracker(p)

        def make_prob_table(contents):
            l = Line(0.5*UP+LEFT, 0.5*DOWN+RIGHT)
            x = Tex("X").next_to(l, DOWN+LEFT).shift(0.5*UP+RIGHT)
            y = Tex("Y").next_to(l, UP+RIGHT).shift(0.5*DOWN+LEFT)
            t = Table(contents, 
                           row_labels=[Text("0"), Text("1")], 
                           col_labels=[Text("0"), Text("1")], 
                           v_buff=0.9, h_buff=1.1,
                           top_left_entry=VGroup(l,x,y)).scale(0.4).next_to(q_text, UP)
            c = [GREEN, RED, RED, GREEN]
            ent = t.get_entries_without_labels()
            for i in range(len(c)):
                ent[i].set_color(c[i])
            return t

        pr = make_probs(p,q)


        p_text = Tex("$p=$", f"${p_tr.get_value()}$").add_updater(lambda x: x.become(Tex("$p=$",f"${p_tr.get_value():.2f}$"), match_center=True))
        q_text = Tex("$q=$", f"${q_tr.get_value()}$").add_updater(lambda x: x.become(Tex("$q=$",f"${q_tr.get_value():.2f}$"), match_center=True))
        with self.voiceover("""
        Let's start by giving values <bookmark mark='1'/> to our probabilities for generating and flipping bits.
        When we have them we can create a table <bookmark mark='2'/> that contains information about all possible combinations
        of sent and recieved bits
            """) as trk:
            self.play(FadeOut(title, destination,*results))
            self.play(bsc_and_source.animate.scale(0.5).shift(2*DOWN+3.5*RIGHT))
            formulas.scale(0.5).next_to(bsc_and_source, LEFT, aligned_edge=UP).shift(1.2*UP+0.5*LEFT).arrange(DOWN, center=False, aligned_edge=LEFT)
            self.wait_until_bookmark("1")
            p_text.next_to(bsc.full_channel, UP)
            q_text.next_to(p_text, UP)
            self.play(Write(p_text), Write(q_text))
            self.wait_until_bookmark("2")
            prob_table = make_prob_table([["",""],["",""]])
            self.play(Create(prob_table))
        self.wait(1)

        with self.voiceover("""
        The probability of sending and recieving a value of 0 will be <bookmark mark='1'/>the probability of generating 0
        multiplied by the probability of not flipping that bit. Similarly the probability of sending 0 and receiving 1
        <bookmark mark='2'/>is the probability of generating 0 times the probability of flipping a bit
        and the same<bookmark mark='3'/> applies when we send 1 
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(prob_table, make_prob_table([["p*q",""],["",""]])))
            self.wait_until_bookmark("2")
            self.play(Transform(prob_table, make_prob_table([["p*q","(1-p)*q"],["",""]])))
            self.wait_until_bookmark("3")
            self.play(Transform(prob_table, make_prob_table([["p*q","(1-p)*q"],["(1-q)*p",""]])))
            self.play(Transform(prob_table, make_prob_table([["p*q","(1-p)*q"],["(1-q)*p","(1-q)*(1-p)"]])))

        self.wait(1)
        with self.voiceover("""
        we can now plug in the values for p and q to get the final probabilities
            """) as trk:
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

            
        joint_entropy_formula_update = MathTex("H(X,Y) =", *[f"-{x:.2f}\cdot log_2({x:.2f})" + ('\\\\' if i == 1 and j == 0 else '') for j, row in enumerate(pr) for i, x in enumerate(row)])
        joint_entropy_formula_update.scale(0.5).move_to(joint_entropy_formula, aligned_edge=LEFT)
        for i,c in enumerate([GREEN, RED, RED, GREEN]):
            joint_entropy_formula_update[1+i].set_color(c)
        with self.voiceover("""
        Let's write out our entropy formulas<bookmark mark='1'/>, we can now place<bookmark mark='2'/> our values in the equations
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(formulas))
            self.wait_until_bookmark("2")
            self.play(Transform(joint_entropy_formula[0], joint_entropy_formula_update[0],replace_mobject_with_target_in_scene=True))
            self.play(Transform(VGroup(joint_entropy_formula[1], prob_table.get_entries((2,2)).copy()), joint_entropy_formula_update[1],replace_mobject_with_target_in_scene=True))
            self.wait(1)
            self.play(Transform(VGroup(prob_table.get_entries((2,3)).copy()), joint_entropy_formula_update[2],replace_mobject_with_target_in_scene=True))
            self.wait(1)
            self.play(Transform(VGroup(prob_table.get_entries((3,2)).copy()), joint_entropy_formula_update[3],replace_mobject_with_target_in_scene=True))
            self.wait(1)
            self.play(Transform(VGroup(prob_table.get_entries((3,3)).copy()), joint_entropy_formula_update[4],replace_mobject_with_target_in_scene=True))
        
        ebr = EntropyBoxRepresentation(make_probs(p,q))
        ebr.set_scale(0.5).whole.next_to(formulas,UP)
        joint_entropy_formula = joint_entropy_formula_update

        with self.voiceover("""
        I won't write out all of the equations by hand to save you some time, but I encourage everyone watching to do this yourself
        for practice purposes, here are the values <bookmark mark='1'/>that come out 
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(joint_entropy_formula.animate.become(Tex("$H(X,Y) =$", f"{HXY(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(joint_entropy_formula, aligned_edge=LEFT)))
            self.play(entropy_x_formula.animate.become(Tex("$H(X) =$", f"{HX(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(entropy_x_formula, aligned_edge=LEFT)))
            self.play(entropy_y_formula.animate.become(Tex("$H(Y) =$", f"{HY(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(entropy_y_formula, aligned_edge=LEFT)))
            self.play(conditional_entropy_formula.animate.become(Tex("$H(X|Y) =$", f"{HX_g_Y(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(conditional_entropy_formula, aligned_edge=LEFT)))
            self.play(conditional_entropy_formula2.animate.become(Tex("$H(Y|X) =$", f"{HY_g_X(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(conditional_entropy_formula2, aligned_edge=LEFT)))
            self.play(mutual_information_formula.animate.become(Tex("$I(X;Y) =$", f"{I(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(mutual_information_formula, aligned_edge=LEFT)))


        with self.voiceover("""
        Let's also bring out our nice visual representation
            """) as trk:
            self.play(Create(ebr.whole))

        self.wait(1)

        with self.voiceover("""
        I will now tweak the values for both p and q, but before this happens, please pause the video and think for yourself
        how will that affect all of the entropies? Do you know what to change to maximize mutual information?
            """) as trk:
            pass
        
        joint_entropy_formula.add_updater(lambda x: x.become(
            Tex("$H(X,Y) =$", f"{HXY(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(joint_entropy_formula, aligned_edge=LEFT)
        ))
        entropy_x_formula.add_updater(lambda x: x.become(
            Tex("$H(X) =$", f"{HX(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(entropy_x_formula, aligned_edge=LEFT)
        ))
        entropy_y_formula.add_updater(lambda x: x.become(
            Tex("$H(Y) =$", f"{HY(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(entropy_y_formula, aligned_edge=LEFT)
        ))
        conditional_entropy_formula.add_updater(lambda x: x.become(
            Tex("$H(X|Y) =$", f"{HX_g_Y(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(conditional_entropy_formula, aligned_edge=LEFT)
        ))
        conditional_entropy_formula2.add_updater(lambda x: x.become(
            Tex("$H(Y|X) =$", f"{HY_g_X(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(conditional_entropy_formula2, aligned_edge=LEFT)
        ))
        mutual_information_formula.add_updater(lambda x: x.become(
            Tex("$I(X;Y) =$", f"{I(make_probs(p_tr.get_value(), q_tr.get_value())):.2f}").scale(0.5).move_to(mutual_information_formula, aligned_edge=LEFT)
        ))
        with self.voiceover("""
        First let's see what happens when we change the value for p, <bookmark mark='1'/> if we start biasing toward some value in our inputs, the entropy starts decreasing
        just as expected, <bookmark mark='2'/>, if we go all the way and just send only 0's the entropy of the input goes to 0, but there is still a bit of 
        uncertainty about the output since the bit can get flipped. Note how the entropy of the input given that we know the output is also 0 since no matter if the bit is flipped or not
        we can be certain that it was generated by sending a 0.
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(q_tr.animate.set_value(0.7))
            ebr.update(self, np.array(make_probs(p_tr.get_value(), q_tr.get_value())))
            self.wait_until_bookmark("2")
            self.play(q_tr.animate.set_value(1))
            ebr.update(self, np.array(make_probs(p_tr.get_value(), q_tr.get_value())))

        self.wait(1)
        self.play(q_tr.animate.set_value(0.5))
        ebr.update(self, np.array(make_probs(p_tr.get_value(), q_tr.get_value())))
        self.wait(1)

        with self.voiceover("""
        When we increase the flip probability,<bookmark mark='1'/> the uncertainty of the input given that we know the output is decreasing, 
        if we start flipping<bookmark mark='2'/> with a probability of 0.5, we maximize uncertainty, and get to the state where there is no mutual information
        this is because we end up sending random outcomes that do not depend on our input
        Similarly, when we reduce our flip probability<bookmark mark='3'/> to 0, we are absolutely certain about the input when we receive our bit
        and mutual information is maximized
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(p_tr.animate.set_value(0.7))
            ebr.update(self, np.array(make_probs(p_tr.get_value(), q_tr.get_value())))
            self.wait_until_bookmark("2")
            self.play(p_tr.animate.set_value(0.5))
            ebr.update(self, np.array(make_probs(p_tr.get_value(), q_tr.get_value())))
            self.wait_until_bookmark("3")
            self.play(p_tr.animate.set_value(1))
            ebr.update(self, np.array(make_probs(p_tr.get_value(), q_tr.get_value())))

        
        self.play(*[FadeOut(x) for x in self.mobjects])

        toc = TOC(3)
        with self.voiceover("""
        Here is where we will end this<bookmark mark='1'/> episode, right now we have all 
        the tools <bookmark mark='2'/> needed to get to the most exciting parts of information theory
        so make sure that you understand all of them and stay tuned for the next episode.
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("2")
            self.play(toc.entries[3].main.animate.set_color(GREEN))
        self.wait(2)
        self.play(FadeOut(toc.header, *[e.main for e in toc.entries]))
        self.wait(2)

def to_binary(i, len):
    return bin(i)[2:].zfill(len)

def create_binary_digits(len):
    return [to_binary(i, len) for i in range(2**len)]

from manim_voiceover.services.gtts import GTTSService

class InformationContent(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            RecorderService(trim_buffer_start=500, trim_buffer_end=500)
            # GTTSService(transcription_model='base')
        )
        toc = TOC()

        with self.voiceover(
            """Hello and welcome to episode 1 in the series on Information Theory
            In this episode we will cover a topic that might be familiar to most people
            with a bit of experience in computer science. And the subject of todays episode is <bookmark mark='1'/>
            Information, and more specifically <bookmark mark='2'/> how do we describe, and measure it"""
                            ) as trk:
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("1")
            self.play(*[Unwrite(e.main) for e in toc.entries[1:]])
            self.wait_until_bookmark("2")
            self.play(toc.entries[0].open())

        self.play(FadeOut(toc.header, toc.entries[0].list, toc.entries[0].main))
        hard_drive = Square()
        hard_drive.add(Text("Hard Drive", font_size=20))
        byte = VGroup(*[Circle(radius=0.5, fill_color = BLUE, color = BLUE, fill_opacity = 1) for _ in range(8)]).arrange(RIGHT).scale(0.2).shift(DOWN)
        hard_drive.add(byte)

        with self.voiceover(
            """Imagine <bookmark mark='1'/> that you bought a very expensive 
            hard drive that can store<bookmark mark='2'/> 8 binary digits, and you are the person
            that needs to decide on what the measure for it's information capacity will be?   
            """
                            ) as trk:
            self.wait_until_bookmark("1")
            self.play(Create(hard_drive))
            self.wait_until_bookmark("2")
            while trk.get_remaining_duration () > 0:
                anims = []
                for b in byte:
                    anims.append(b.animate.set_color(BLUE if random() > 0.5 else RED))
                self.play(*anims, run_time=0.3)

        self.play(*[b.animate.set_color(BLUE) for b in byte])
        with self.voiceover(
            """One way that you could go about creating such a metric   
            You could decide that the total amount of patterns<bookmark mark='b'/> that we can store should be 
            the amount of information. 
            """
                            ) as trk:

            self.wait_until_bookmark("b")
            num_messages = Tex("$Patterns = $", "$2$", "$^8$").next_to(hard_drive, DOWN)
            self.play(Write(num_messages))

        with self.voiceover(
            """To test how your measure behaves you imagine that you somehow managed to save some money
            and get another hard drive<bookmark mark='1'/>
            that can store an additional 8 binary digits of information there are now <bookmark mark='2'/>
            two to the power of 16 distinct patterns that you can store
            """
                            ) as trk:
            self.play(hard_drive.animate.shift(2*UP + 3*LEFT),
                    num_messages.animate.shift(2*UP + 3*LEFT))
            l1 = Line(10*LEFT, 10*RIGHT).shift(DOWN)
            l2 = Line(10*UP, l1.get_center())
            self.play(Create(l1), Create(l2))
            hard_drive2 = hard_drive.copy().shift(5.5*RIGHT)
            hard_drive3 = hard_drive.copy().next_to(hard_drive2)
            r_drives = VGroup(hard_drive2, hard_drive3)
            self.wait_until_bookmark("1")
            self.play(Transform(hard_drive.copy(), r_drives, replace_mobject_with_target_in_scene=True))

            self.wait_until_bookmark("2")
            num_messages2 = Tex("$Patterns = $", "$2$", "$^{16}$").next_to(VGroup(hard_drive2, hard_drive3), DOWN)
            self.play(Write(num_messages2))

        message_difference = Tex("message difference").shift(2*DOWN+2*LEFT)
        diff_1 = Tex("$\\frac{2^{16}}{2^8} = 2^8$").next_to(message_difference, DOWN)
        bit_difference = Tex("bit difference").shift(2*DOWN+2*RIGHT)
        diff_2 = MathTex("{16","\\over", "8}", "=", "2").set_color_by_tex("8", GREEN).set_color_by_tex("16", BLUE).next_to(bit_difference, DOWN)

        self.wait(1)
             
        with self.voiceover("""
            if you compare those two situations, the difference in possible messages you could store <bookmark mark='x'/>is  
            2 to the power of 8 and it kind of does not feel like that should be the case, increasing our storage should not
            increase our information exponentially, what we want instead is for our information content to double when we double 
            our storage
            """
                            ) as trk:
            self.wait_until_bookmark("x")
            self.play(Write(message_difference))
            self.play(Transform(VGroup(num_messages.copy(), num_messages2.copy()), diff_1, replace_mobject_with_target_in_scene=True))
        

        with self.voiceover("""
            If you are perceptive, you might have noticed that dividing the number of binary digits that one of our drives can store<bookmark mark='1'/>
            by the amount of digits that the second one<bookmark mark='2'/> can store gives us exactly<bookmark mark='3'/> the result we are looking for
            but we want our equation for information in a nice compact form so let's write it out and transform it
            """) as trk:

            self.wait_until_bookmark("1")
            bits_1 = num_messages.get_part_by_tex("^8") 
            self.play(bits_1.animate.set_color(GREEN))

            self.wait_until_bookmark("2")
            bits_2 = num_messages2.get_part_by_tex("^{16}")
            self.play(bits_2.animate.set_color(BLUE))
            
            self.wait_until_bookmark("3")
            self.play(Transform(VGroup(bits_1.copy(), bits_2.copy()), diff_2, replace_mobject_with_target_in_scene=True))
        
        self.play(FadeOut(message_difference, diff_1, diff_2))
        extraction_1 = Tex("$M$", "$ = $", "$2^I$").shift(2*DOWN)
        extraction_2 = Tex("$log$", "$_2$", "$M$", "$ = $", "$log_2{2^I}$").shift(2*DOWN)
        extraction_3 = Tex("$log$", "$_2$", "$M$", "$ = $", "$I$").shift(2*DOWN)
        with self.voiceover("""
            Our number of messages is<bookmark mark='1'/> M, and there are<bookmark mark='2'/> 2 to the power of information messages that we can store
            To extract our information<bookmark mark='3'/> we can take the logarithm of both sides, and that gives us<bookmark mark='4'/> the equation for information
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(extraction_1.get_part_by_tex("M")))
            self.wait_until_bookmark("2")
            self.play(Write(extraction_1.get_part_by_tex("=")))
            self.play(Write(extraction_1.get_part_by_tex("2^I")))
            self.wait_until_bookmark("3")
            self.play(Transform(extraction_1, extraction_2, replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("4")
            self.play(Transform(extraction_2, extraction_3, replace_mobject_with_target_in_scene=True))

        with self.voiceover("""
        , but there is <bookmark mark='1'/>one final tweak that we have to make,
        so far we have been only working with binary digits, so our logarithm had a base of two, let's just change it <bookmark mark='2'/> to an arbitrary one,
                            so that it can be used for any base of information.
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(FadeOut(hard_drive, r_drives, l1, l2, num_messages, num_messages2))
            self.play(Transform(extraction_3, Tex("$log$", "$_2$", "$M$", "$ = $", "$I$", font_size=85)))
            self.wait_until_bookmark("2")
            log = Tex("$\log$", "$_b$", "$M$", "$ = $", "$I$", font_size=85)
            self.play(Transform(extraction_3, log, replace_mobject_with_target_in_scene=True))

        with self.voiceover("""
            Let's go over a quick example to demonstrate how the base works, and verify our equation once again
            """) as trk:
            pass

        self.play(Transform(log, Tex("$\log$", "$_b$", "$M$").set_color_by_tex("_b", BLUE).set_color_by_tex("$M$", ORANGE).shift(2*RIGHT)))

        source = Square()
        source.add(Text("Information\nSource", font_size=20))
        source.shift(LEFT*3)

        decimal_digits = VGroup()
        radius=DEFAULT_SMALL_DOT_RADIUS
        three_dots = VGroup(*[Dot(radius=radius*2/3, color=WHITE) for _ in range(3)]).arrange(DOWN,buff=0.1)
        for i in range(10):
            if i == 3: 
                decimal_digits.add(three_dots.copy().scale(1.5))
            elif i < 3 or i > 6:
                dig = Circle(radius=0.5, color=BLUE)
                dig.add(Tex(str(i)).scale(1.5).move_to(dig.center()))
                decimal_digits.add(dig)
        decimal_digits.arrange(DOWN).scale(0.3).next_to(source, RIGHT, aligned_edge=RIGHT)
        
        with self.voiceover(
            """Imagine some kind<bookmark mark='1'/> of information source 
            that we use to<bookmark mark='2'/> send digits from 1 to 10  
            after<bookmark mark='3'/> using it once, we will<bookmark mark='4'/> have 10 possible states
            and our unit of information<bookmark mark='5'/> will be decimal digits
            which leaves<bookmark mark='6'/> us with one decimal digit of information after performing the math
            using it again<bookmark mark='7'/> we increase our possible<bookmark mark='8'/> states to a 100 giving us
            2 decimal digits of information
            """
                            ) as trk:
            self.wait_until_bookmark("1")
            self.play(Create(source))
            self.play(Create(decimal_digits))
            self.wait_until_bookmark("2")
            messages = VGroup(*[Tex(str(x), color=ORANGE) for x in range(10)]).arrange(DOWN)
            self.wait_until_bookmark("3")
            self.play(Transform(decimal_digits.copy(), messages, replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("4")
            self.play(Transform(log, Tex("$\log$", "$_{b}$", "$10$").set_color_by_tex("_{b}", BLUE).set_color_by_tex("$10$", ORANGE).shift(2*RIGHT)))
            self.wait_until_bookmark("5")
            self.play(Transform(log, Tex("$\log$", "$_{10}$", "$10$").set_color_by_tex("_{10}", BLUE).set_color_by_tex("$10$", ORANGE).shift(2*RIGHT)))
            self.wait_until_bookmark("6")
            self.play(Transform(log, Tex("$\log$", "$_{10}$", "$10$", "$=$", "$1$").set_color_by_tex("_{10}", BLUE).set_color_by_tex("$10$", ORANGE).shift(2*RIGHT)))
            self.wait(1)
            
            new_messages = VGroup(*[Tex(x, color=ORANGE) for x in ["00", "01", "02", "03"]], three_dots, *[Tex(x, color=ORANGE) for x in ["96", "97", "98", "99"]]).arrange(DOWN)
            self.wait_until_bookmark("7")
            self.play(Transform(VGroup(decimal_digits.copy(), messages), new_messages, replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("8")
            self.play(Transform(log, Tex("$\log$", "$_{10}$", "$100$", "$=$", "$2$").set_color_by_tex("_{10}", BLUE).set_color_by_tex("$100$", ORANGE).shift(2*RIGHT)))
            self.wait(1)
        
        
        bit_0 = Circle(radius=0.5, color=BLUE).next_to(source, RIGHT+UP, aligned_edge=RIGHT+UP)
        bit_0.add(Tex("0").scale(1.5).move_to(bit_0.get_center()))
        bit_0.scale(0.5)
        bit_1 = Circle(radius=0.5, color=BLUE).next_to(source, RIGHT+DOWN, aligned_edge=RIGHT+DOWN)
        bit_1.add(Tex("1").scale(1.5).move_to(bit_1.get_center()))
        bit_1.scale(0.5)
        bits = VGroup(bit_0, bit_1)

        with self.voiceover(
            """And the same scenario works when our source<bookmark mark='1'/> is sending binary digits instead 
            after using it<bookmark mark='2'/> once we get one binary digit of information 
            commonly referred to as one bit of information<bookmark mark='3'/>
            two bits after using it twice <bookmark mark='4'/> and three after a third usage
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(decimal_digits, bits, replace_mobject_with_target_in_scene=True),FadeOut(new_messages))

            binary_digits = VGroup(*[Tex(x, color=ORANGE) for x in create_binary_digits(1)]).arrange(DOWN)
            self.wait_until_bookmark("2")
            self.play(Transform(bits.copy(), binary_digits, replace_mobject_with_target_in_scene=True))
            self.play(Transform(log, Tex("$\log$", "$_2$", "$2$", "$=$", "$1$").set_color_by_tex("_2", BLUE).set_color_by_tex("$2$", ORANGE).shift(2*RIGHT)))
            self.wait(1)

            self.wait_until_bookmark("3")
            binary_digits_2 = VGroup(*[Tex(x, color=ORANGE) for x in create_binary_digits(2)]).arrange(DOWN)
            self.play(Transform(VGroup(bits.copy(), binary_digits), binary_digits_2, replace_mobject_with_target_in_scene=True))
            self.play(Transform(log, Tex("$\log$", "$_2$", "$4$", "$=$", "$2$").set_color_by_tex("_2", BLUE).set_color_by_tex("$4$", ORANGE).shift(2*RIGHT)))
            self.wait(1)
            
            self.wait_until_bookmark("4")
            binary_digits_3 = VGroup(*[Tex(*[c for c in x], color=ORANGE) for x in create_binary_digits(3)]).arrange(DOWN)
            self.play(Transform(VGroup(bits.copy(), binary_digits_2), binary_digits_3, replace_mobject_with_target_in_scene=True))
            self.play(Transform(log, Tex("$\log$", "$_2$", "$8$", "$=$", "$3$").set_color_by_tex("_2", BLUE).set_color_by_tex("$8$", ORANGE).shift(2*RIGHT)))
            self.wait(1)


        with self.voiceover("""
        So far we have only looked at how much information is contained inside a group of messages
        but we also need to be able to measure how much information we gain when we become aware of 
        some outcome
        <bookmark mark='1'/>
        By intuition, if someone told us that the 
        <bookmark mark='2'/>hightest bit is 0
        our space of possible<bookmark mark='3'/> messages is cut down in half.
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(FadeOut(source,bits,log))
            self.wait_until_bookmark("2")
            self.play(*[x.submobjects[0].animate.set_color(GREEN) for x in binary_digits_3[:4]])
            self.wait_until_bookmark("3")
            self.play(*[x.animate.set_color(GREY) for x in binary_digits_3[4:]])

        with self.voiceover("""
        Again, when we get the knowledge that the
        <bookmark mark='2'/>next bit is also 0
        our space of possible<bookmark mark='3'/> messages is cut down in half one more time.
            """) as trk:
            self.wait_until_bookmark("2")
            self.play(*[x.submobjects[1].animate.set_color(GREEN) for x in binary_digits_3[:2]])
            self.wait_until_bookmark("3")
            self.play(*[x.animate.set_color(GREY) for x in binary_digits_3[2:4]])
        
        extraction_1 = MathTex("p", " = ", "(", "{1", "\\over", "2}", ")", "^I").scale(2)
        extraction_base = MathTex("p", " = ", "(", "{1", "\\over", "b}", ")", "^I").scale(2)
        extraction_2 = MathTex("p", " = ", "(", "{1^I", "\\over", "2^I}", ")").scale(2)
        extraction_3 = MathTex("p", " = ", "(", "{1", "\\over", "2^I}", ")").scale(2)
        extraction_4 = MathTex("2^I", " = ", "(", "{1", "\\over", "p}", ")").scale(2)
        extraction_5 = MathTex("log", "_2", "2^I", " = ", "log_2", "(", "{1", "\\over", "p}", ")").scale(2)
        extraction_6 = MathTex("I", " = ", "log_2", "(", "{1", "\\over", "p}", ")").scale(2)
        
        with self.voiceover("""
            And this is exactly how we formulate the information content of a single observation,
            <bookmark mark='1'/>, getting one bit of information reduces our probability by a half
            or if you want a more general case, getting one unit of information 
            <bookmark mark='2'/>
            reduces the possible space of messages by a factor of that unit
            """) as trk:
            self.play(FadeOut(binary_digits_3))
            self.wait_until_bookmark("1")
            self.play(Write(extraction_1))
            self.wait_until_bookmark("2")
            self.play(Transform(extraction_1, extraction_base, replace_mobject_with_target_in_scene=True))

        with self.voiceover("""
            In this series the base unit of information will be<bookmark mark='1'/> binary digits, because
            it's the most commonly used and all information can be stored in binary digits
            To extract the information from that equation we perform a similar logarithm trick as before
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(extraction_base, extraction_1, replace_mobject_with_target_in_scene=True))
        self.play(Transform(extraction_1, extraction_2, replace_mobject_with_target_in_scene=True))
        self.play(Transform(extraction_2, extraction_3, replace_mobject_with_target_in_scene=True))
        self.play(Transform(extraction_3, extraction_4, replace_mobject_with_target_in_scene=True))
        self.play(TransformMatchingTex(extraction_4, extraction_5, replace_mobject_with_target_in_scene=True))
        self.play(TransformMatchingTex(extraction_5, extraction_6, replace_mobject_with_target_in_scene=True))
        
        old_eq = Tex("$I$", "$ = $", "$log$", "$_2$", "$M$").scale(2).next_to(extraction_6, DOWN,aligned_edge=LEFT)
        with self.voiceover("""
        this leaves us with our final equation, for information content it will be very important
        so make sure that you understand it and all of it's implications. As an exercise
        try to explain to yourself why this equation,<bookmark mark='1'/> and the equation for information content of 
        a group of messages are essentially the same equation
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(extraction_6.copy(), old_eq, replace_mobject_with_target_in_scene=True))
                
        self.wait(3)
        self.play(FadeOut(extraction_6, old_eq))
# 
        toc = TOC()
        with self.voiceover("""
        And with this, <bookmark mark='1'/>we come to the end of the first episode
        <bookmark mark='2'/> and our knowledge on Information deepens.
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("2")
            self.play(toc.entries[0].main.animate.set_color(GREEN))
        self.wait(2)
        self.play(FadeOut(toc.header, *[e.main for e in toc.entries]))
        self.wait(2)



class BSC():
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


class Entropy(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            RecorderService(trim_buffer_start=500, trim_buffer_end=500)
            # GTTSService(transcription_model='base')
        )
        toc = TOC(1)

        with self.voiceover(
            """Helo and welcome to episode 2 in our series on Information Theory
            In this episode we will introduce the most fundamental formula
            in information theory, which is <bookmark mark='1'/>
            Entropy, we will explain what it means  
            and how do we use <bookmark mark='2'/>it to describe the level of uncertainty, surprise and information
            of a random variable"""
                            ) as trk:
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("1")
            self.play(*[Unwrite(e.main) for e in toc.entries[2:]])
            self.wait_until_bookmark("2")
            self.play(toc.entries[1].open())
            
        general_entropy_formula = Tex("$H(X) =$", "$\sum$", "$p(x)$", "$\cdot$", "$\log_2$", "$($", "$\\frac{1}{p(x)}$", "$)$")
        general_entropy_formula2 = Tex("$H(X) =$", "$\\mathbb{E}[I(X)]$").next_to(general_entropy_formula, DOWN, aligned_edge=LEFT)
        with self.voiceover(""" 
        And this is the formula that was established by Claude Shannon as the measure of entropy 
        of a set of possible events, and for those that are familiar with statistics, this equation is equivalent 
        to <bookmark mark='1'/> an expected value for the information content of our random variable 
            """) as trk:
            self.play(Transform(VGroup(toc.entries[1].list, toc.entries[0].main, toc.entries[1].main, toc.header), general_entropy_formula, replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("1")
            self.play(Transform(general_entropy_formula.copy(), general_entropy_formula2, replace_mobject_with_target_in_scene=True))

        with self.voiceover(""" 
        You might also see the entropy written out like this, were we negate the sum instead of inverting the probability in the logarithm
        As an exercise you are encouraged to prove that both are exactly the same
            """) as trk:
            self.play(Transform(general_entropy_formula, Tex("$H(X) =$", "$-\sum$", "$p(x)$", "$\cdot$", "$\log_2$", "$($", "$p(x)$", "$)$")))
           
        with self.voiceover(""" 
        Let's go over a few examples
            """) as trk:
           self.play(FadeOut(general_entropy_formula2)) 

        self.play(general_entropy_formula.animate.shift(3*UP))

        with self.voiceover(""" 
        The classical example of a random variable is<bookmark mark='1'/> flipping a coin, there are 2 states<bookmark mark='2'/> 
        heads and<bookmark mark='3'/> tails and they are both equally probable
            """) as trk:
            self.wait_until_bookmark("1")
            coin_flipping_text = Text("Flip a fair coin: Equally likely probabilities").shift(2*DOWN)
            self.play(Write(coin_flipping_text))

            self.wait_until_bookmark("2")
            coin = Circle(radius=1, color=BLUE).shift(1.5*LEFT)
            heads = Text("H", color=BLUE).scale(1.5).move_to(coin.get_center())
            self.play(FadeIn(coin), Write(heads))
            
            self.wait_until_bookmark("3")
            coin2 = Circle(radius=1, color=RED).shift(1.5*RIGHT)
            tails = Text("T", color=RED).scale(1.5).move_to(coin2.get_center())
            self.play(FadeIn(coin2), Write(tails))
            entropy_formula_1 = Tex("$H(X) =$", "$-0.5 \cdot \log_2(0.5)$", "$- 0.5 \cdot \log_2(0.5)$", "$ = 1$").scale(0.8).next_to(coin_flipping_text, DOWN)
            entropy_formula_1[1].set_color(BLUE)
            entropy_formula_1[2].set_color(RED)

        with self.voiceover(""" 
        We can plug in the values <bookmark mark='1'/>into our entropy equation. What it tells us is that there is exactly one 
        bit of uncertainty about the outcome, and it makes absolute sense, there are two states - so they can be represented by one bit
        and they are both equally probable so we cannot make any accurate predictions about the outcome of a coin flip  
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(general_entropy_formula.copy(), entropy_formula_1[0], replace_mobject_with_target_in_scene=True),
                      Transform(VGroup(coin, heads).copy(), entropy_formula_1[1], replace_mobject_with_target_in_scene=True),
                      Transform(VGroup(coin2, tails).copy(), entropy_formula_1[2], replace_mobject_with_target_in_scene=True))
            self.play(Write(entropy_formula_1[3]))


        # fade away all objects

        def en(probs): return f"{sum([-x*math.log2(x) for x in probs]):.2f}"

        with self.voiceover(""" 
        Another example that we can look at <bookmark mark='1'/>is picking a ball, imagine that someone throws <bookmark mark='2'/>a few balls of different colors
        into a bag and picks one out at random, you know that there are more blue balls than red ones so the outcome 
        should not be as surprising as when we flipped a fair coin 
            """) as trk:
        # Non equally likely probabilities
            self.play(FadeOut(entropy_formula_1), FadeOut(coin), FadeOut(heads), FadeOut(coin_flipping_text), FadeOut(coin2), FadeOut(tails))
            ball_text = Text("Pick a ball: Non equally likely probabilities").shift(2*DOWN)
            self.wait_until_bookmark("1")
            self.play(Write(ball_text))
            self.wait(1)

            columns = 5
            n_balls = 10

            balls = [Dot(color=BLUE if i < 7 else RED).move_to((i%columns) * RIGHT + (i//columns)*DOWN + 2*LEFT + 2*UP) for i in range(n_balls)]
            self.wait_until_bookmark("2")
            self.play(*[Create(b) for b in balls])

        with self.voiceover(""" 
        And after doing<bookmark mark='1'/> the math we can see that the outcome is smaller, the event is still random
        but we are not as uncertain of the outcome since we know that the probability for picking a blue ball is much higher.
            """) as trk:

            entropy_formula_2 = Tex("$H(X) =$", "$-\\frac{7}{10} \cdot \log_2(\\frac{7}{10})$",
                                     "$- \\frac{3}{10} \cdot \log_2(\\frac{3}{10})$", f"$= {en([0.7, 0.3])}$").scale(0.8).next_to(ball_text, DOWN)
            entropy_formula_2[1].set_color(BLUE)
            entropy_formula_2[2].set_color(RED)
            self.wait_until_bookmark("1")

            self.play(Transform(general_entropy_formula.copy(), entropy_formula_2[0], replace_mobject_with_target_in_scene=True),
                      Transform(VGroup(*balls[:7]).copy(), entropy_formula_2[1], replace_mobject_with_target_in_scene=True),
                      Transform(VGroup(*balls[7:]).copy(), entropy_formula_2[2], replace_mobject_with_target_in_scene=True))
            self.play(Write(entropy_formula_2[3]))
        # fade away all objects

        with self.voiceover(""" 
        The entropy of a two event random variable <bookmark mark='1'/>that we have been looking at so far is called a Binary entropy,
        and since the probabilities need to add up to 1 <bookmark mark='2'/>we can describe it using only one value p as an unknown 
        variable 
                    """) as trk:
            self.play(FadeOut(entropy_formula_2), FadeOut(*balls), FadeOut(ball_text))
            self.wait_until_bookmark("1")
            binary_entropy_formula = Tex("$H_b(p) =$", "$-p \cdot \log_2(p_1)$", "$- (p_2) \cdot \log_2(p_2)$").shift(2*DOWN)
            self.play(Transform(general_entropy_formula, binary_entropy_formula, replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("2")
            self.play(Transform(binary_entropy_formula, Tex("$H_b(p) =$", "$-p \cdot \log_2(p)$", "$- (1-p) \cdot \log_2(1-p)$").shift(2*DOWN)))

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
        def bin_ent(p): 
            try:
                 return f"{(-p*math.log2(p)-(1-p)*math.log2(1-p)):.2f}"
            except:
                return 0


        # Creating curve for y = -plog2(p) - (1-p)log2(1-p)
        graph = axes.plot(
            func,
            color=WHITE,
            x_range=[0,1]
        )
        labels = axes.get_axis_labels("p", "H(p)")

        with self.voiceover(""" 
        When we graph <bookmark mark='1'/> a function for binary entropy we can see more clearly what it means, and how it relates to all of the properties
        mentioned before, <bookmark mark='2'/>it is at it's peak when the probabilities for both events are equal, 
        and intuitively it goes <bookmark mark='3'/>to 0 when we become certain of the<bookmark mark='4'/> outcome  
                             - meaning that there is no uncertainty about the event,
                            there is no surprise of the outcome, and it provides us with no information 
                    """) as trk:
            self.wait_until_bookmark("1")
            self.play(
                Create(axes), 
                Create(graph), 
                Write(labels)
            )
            self.play(Create(dot))
            self.wait_until_bookmark("2")
            binary_entropy_formula.add_updater(lambda x: x.become(
                Tex(f"$H_b({t.get_value():.2f}) =$", f"$-{t.get_value():.2f} \cdot \log_2({t.get_value():.2f})$", 
                    f"$- ({(1-t.get_value()):.2f} \cdot \log_2({(1-t.get_value()):.2f})$", f"$={bin_ent(t.get_value())}$").shift(2*DOWN)))
            self.play(t.animate.set_value(0.5))
            self.play(Indicate(binary_entropy_formula[3]))
            # self.play(Transform(binary_entropy_formula, Tex("$H_b(0.5) =$", "$-0.5 \cdot \log_2(0.5)$", "$- (1-0.5) \cdot \log_2(1-0.5)$", "$=1$").shift(2*DOWN)))
            self.wait_until_bookmark("3")
            self.play(t.animate.set_value(0))
            self.play(Indicate(binary_entropy_formula[3]))
            # self.play(Transform(binary_entropy_formula, Tex("$H_b(0) =$", "$-0 \cdot \log_2(0)$", "$- (1-0) \cdot \log_2(1-0)$", "$=0$").shift(2*DOWN)))
            self.wait_until_bookmark("4")
            self.play(t.animate.set_value(1))
            self.play(Indicate(binary_entropy_formula[3]))
            # self.play(Transform(binary_entropy_formula, Tex("$H_b(1) =$", "$-1 \cdot \log_2(1)$", "$- (1-1) \cdot \log_2(1-1)$", "$=0$").shift(2*DOWN)))

        #fade out everything
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(labels), FadeOut(dot), FadeOut(binary_entropy_formula))

        with self.voiceover(""" 
        Let's get back to our ball<bookmark mark='1'/> example and see what happens with our entropy
        when we <bookmark mark='2'/>throw a few more balls into our bag. As you might have expected, <bookmark mark='3'/>there are now
        more possible events so our uncertainty of the outcome increases. This is another property of the entropy function
        - adding another event that has a probability greater than 0, increases entropy
                    """) as trk:
            self.wait_until_bookmark("1")
            self.play(FadeIn(entropy_formula_2.shift(UP)), FadeIn(*balls))
            new_balls = [Dot(color=GREEN).move_to(balls[0].get_center() + 2*DOWN + i * RIGHT) for i in range(5)]
            self.wait_until_bookmark("2")
            self.play(*[Create(b) for b in new_balls])
            updated_entropy_formula_2 = Tex("$H(X) =$", "$-\\frac{7}{15} \cdot \log_2(\\frac{7}{15})$", 
                                            "$- \\frac{3}{15} \cdot \log_2(\\frac{3}{15})$", 
                                            "$- \\frac{5}{15} \cdot \log_2(\\frac{5}{15})$", f"$ = {en([7/15, 3/15, 5/15])}$").scale(0.8).move_to(ball_text.get_center())
            updated_entropy_formula_2[1].set_color(BLUE)
            updated_entropy_formula_2[2].set_color(RED)
            updated_entropy_formula_2[3].set_color(GREEN)
            self.wait_until_bookmark("3")
            self.play(Transform(entropy_formula_2,updated_entropy_formula_2),replace_mobject_with_target_in_scene=True)


        self.wait(1)
        self.play(*[FadeOut(x) for x in self.mobjects])
        self.wait(1)

        toc = TOC(1)
        toc.entries[0].main.animate.set_color(GREEN)
        with self.voiceover("""
        And this is where we will end the second episode  <bookmark mark='1'/>
        hopefully you now have an intuitive understanding <bookmark mark='2'/> of Entropy
        If there are still things that aren't clear please rewind the video as the next one will 
        be building up on everything that we have learned in this episode 
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("2")
            self.play(toc.entries[1].main.animate.set_color(GREEN))
        self.wait(2)
        self.play(FadeOut(toc.header, *[e.main for e in toc.entries]))
        self.wait(2)

        

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


class TwoEventEntropy(VoiceoverScene):
    def construct(self):

        self.set_speech_service(
            RecorderService(trim_buffer_start=500, trim_buffer_end=500)
            # GTTSService(transcription_model='base')
        )
        toc = TOC(2)

        with self.voiceover(
            """Hello and welcome to episode 3 in our series on Information Theory
            Today we will extend the subject of the previous episode <bookmark mark='1'/>
            to a case where there are multiple random events happening
            and we will introduce new properties <bookmark mark='2'/>
            joint entropy, conditional entropy and mutual information
            """
                            ) as trk:
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("1")
            self.play(*[Unwrite(e.main) for e in toc.entries[3:]])
            self.wait_until_bookmark("2")
            self.play(toc.entries[2].open())
        colors = [RED, GREEN, YELLOW, BLUE]
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

        with self.voiceover("""
        Remember our example with picking a ball from a set of balls of different colors that we introduced in the previous episode?
        We can expand on it, <bookmark mark='1'/> where now instead of just balls there are different shapes.
        You can think of an outcome of picking from our bag as two events, one <bookmark mark='2'/> is picking a specific color, 
        and the other one is <bookmark mark='3'/>picking a specific shape
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(toc.get_open(2), t.scale(0.4), replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("2")
            self.play(Indicate(t.get_row_labels()))
            self.wait_until_bookmark("3")
            self.play(Indicate(t.get_col_labels()))



        joint_entropy_formula = Tex("$H(X,Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2(p(x,y))$")
        entropy_x_formula = Tex("$H(X) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2(\\sum\\limits_{y} p(x,y))$")
        entropy_y_formula = Tex("$H(Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2(\\sum\\limits_{x} p(x,y))$")
        conditional_entropy_formula = Tex("$H(X|Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2\\left(\\frac{p(x,y)}{p(y)}\\right)$")
        mutual_information_formula = Tex("$I(X;Y) = $", "$-\\sum\\limits_{x,y} p(x,y) \cdot \\log_2\\left(\\frac{p(x) \\cdot p(y)}{p(x,y)}\\right)$")
        
        formulas = VGroup(entropy_x_formula, entropy_y_formula, joint_entropy_formula, conditional_entropy_formula, mutual_information_formula)
        arranged_formulas = formulas.copy().scale(0.6).shift(3*UP+4*LEFT).arrange(DOWN, center=False, aligned_edge=LEFT)

        formulas[0].shift(UP + 2.5*LEFT)

        self.wait(1)

        low_frac = 12#$np.sum(combinations)
        final_eq = VGroup(*[
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=RED),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=GREEN),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=YELLOW),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=BLUE)]).arrange(DOWN, center=False, aligned_edge=LEFT)
        
        interm_eq = VGroup(*[
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=RED),
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=RED),
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{3}}{{{low_frac}}})$", color=RED)]).arrange(DOWN, center=False, aligned_edge=LEFT)
        
        base_eq = Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{low_frac}}}+\\frac{{1}}{{{low_frac}}}+\\frac{{1}}{{{low_frac}}})$", color=RED).move_to(final_eq[0].get_corner(LEFT), LEFT)
        

        with self.voiceover("""
        Firstly, let's take a look at what happens to our equation for entropy <bookmark mark='1'/> now that there are two events in play 
        it might look complex at first but let's write it out and see what we come to
            """) as trk:
            self.play(t.animate.become(t.copy().scale(0.4).shift(2*UP+4*RIGHT)))
            self.wait_until_bookmark("1")
            self.play(Write(formulas[0]))

        with self.voiceover("""
        We take the probability of a single event, let's say it's picking a<bookmark mark='1'/> red square
         and we multiply it<bookmark mark='2'/> by the logarithm
       <bookmark mark='3'/> of the sum of all probabilities of picking a red shape

            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Indicate(t.get_entries((2,2))))
            current = t.get_entries((2,2)).copy()
            self.play(Transform(current, base_eq[0],replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("2")
            self.play(Write(base_eq[1]))
            self.wait_until_bookmark("3")
            current = VGroup(*[t.get_entries(x).copy() for x in [(2,2), (2,3), (2,4)]])
            self.play(Transform(current, base_eq[2],replace_mobject_with_target_in_scene=True))

        self.play(Transform(base_eq, interm_eq[0], replace_mobject_with_target_in_scene=True))
        with self.voiceover("""
            We then do it for the rest of the red shapes and we sum the results
            """) as trk:
            for i in range(2):
                self.play(Transform(t.get_entries((2,3+i)).copy(), interm_eq[1+i], replace_mobject_with_target_in_scene=True))
            self.play(Transform(interm_eq, final_eq[0], replace_mobject_with_target_in_scene=True))

        with self.voiceover("""
        And we continue doing this for the<bookmark mark='1'/> green
        <bookmark mark='2'/> yellow 
        <bookmark mark='3'/> and blue shapes
            """) as trk:
            self.wait_until_bookmark("1")
            current = VGroup(*[t.get_entries(x).copy() for x in [(3,3), (3,4), (3,5)]])
            self.play(Transform(current, final_eq[1],replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("2")
            current = VGroup(*[t.get_entries(x).copy() for x in [(4,2), (4,4), (4,5)]])
            self.play(Transform(current, final_eq[2],replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("3")
            current = VGroup(*[t.get_entries(x).copy() for x in [(5,2), (5,3), (5,5)]])
            self.play(Transform(current, final_eq[3],replace_mobject_with_target_in_scene=True))

        old_formula = Tex("$H(X) =$", "$-\\sum\\limits_{x} p(x) \cdot \log_2\\left(p(x)\\right)$").move_to(formulas[0].get_corner(RIGHT), RIGHT)
        formulas[0].save_state()

        with self.voiceover("""
        I've purposely did all of the calculations by color, so that the more alert viewers might notice that this is  
        <bookmark mark='1'/> exactly the same formula as when we did it for one event only, <bookmark mark='2'/> except now we just
        note that there are two possible events
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(formulas[0].animate.become(old_formula))
            self.wait_until_bookmark("2")
            self.play(Restore(formulas[0]))
            self.wait(1)
            self.play(FadeOut(final_eq))
            self.play(Transform(formulas[0], arranged_formulas[0]))
            self.wait(1)


        with self.voiceover("""
        We can do the same thing <bookmark mark='1'/>if we want to calculate the entropy of picking a specific shape
        <bookmark mark='2'/>
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(formulas[1]))
            old_formula = Tex("$H(Y) =$", "$-\\sum\\limits_{y} p(y) \cdot \log_2\\left(p(y)\\right)$").move_to(formulas[1].get_corner(LEFT), LEFT)
            formulas[1].save_state()
            self.wait_until_bookmark("2")
            self.play(formulas[1].animate.become(old_formula))
            self.wait(3)
            self.play(Restore(formulas[1]))
            self.wait(2)
            self.play(Transform(formulas[1], arranged_formulas[1]))


        with self.voiceover("""
        Let's now introduce the concept of<bookmark mark='1'/> a joint entropy
        what it measures is just the entropy<bookmark mark='2'/> of all of the possible outcomes for both
        of our events, think about it as treating all of the events as a one independent event, and calculating it`s entropy
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(formulas[2][0]))
            self.wait_until_bookmark("2")
            self.play(Write(formulas[2][1:]))
            self.wait(1)
            self.play(Transform(formulas[2], arranged_formulas[2]))
            self.wait(1)

        formulas[3].shift(0.5*UP + 3*LEFT)

        with self.voiceover("""
        Another new concept is that of a conditional entropy, it calculates the uncertainty of <bookmark mark='1'/> one of our events,
        given that<bookmark mark='2'/> we know the outcome of the other one 
            """) as trk:
            self.play(Write(formulas[3][0]))
            self.wait_until_bookmark("1")
            self.play(Write(formulas[3][1:]))
            self.wait_until_bookmark("2")
            new_formula = Tex("$H(X|Y) =$", "$-\\sum\\limits_{x,y} p(x,y) \cdot \log_2\\left(p(x|y)\\right)$").move_to(formulas[3].get_corner(LEFT), LEFT)
            self.play(Transform(formulas[3], new_formula))
        self.wait(1)
        
        final_eq = VGroup(*[
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=GREEN),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=YELLOW),
                    Tex(f"$-\\frac{{3}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=BLUE)]).arrange(DOWN, center=False, aligned_edge=LEFT)
        
        interm_eq = VGroup(*[
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED),
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED),
                    Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED)]).arrange(DOWN, center=False, aligned_edge=LEFT)
        
        base_eq = Tex(f"$-\\frac{{1}}{{{low_frac}}}$", "$\log_2($", f"$\\frac{{1}}{{{3}}})$", color=RED).move_to(final_eq[0].get_corner(LEFT), LEFT)
        
        with self.voiceover("""
        Let's say we want to calculate the uncertainty of a color, when we know what shape an object is
            """) as trk:
            pass
        with self.voiceover("""
        To do that, we take the probability of an outcome being a specific color and shape,<bookmark mark='1'/>
        and we multiply it <bookmark mark='2'/> by a logarithm of the probability <bookmark mark='3'/>of it being a certain color 
        when we know it's shape
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Indicate(t.get_entries((2,2))))
            current = t.get_entries((2,2)).copy()
            self.play(Transform(current, base_eq[0],replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("2")
            self.play(Write(base_eq[1]))
            self.wait_until_bookmark("3")
            current = VGroup(*[t.get_entries(x).copy() for x in [(2,2), (2,3), (2,4)]])
            self.play(Transform(current, base_eq[2],replace_mobject_with_target_in_scene=True))
        self.wait(1)
        with self.voiceover("""
        And we do that for all of the possible shapes<bookmark mark='1'/> of that color
        And for all of<bookmark mark='2'/> the possible colors
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(base_eq, interm_eq[0], replace_mobject_with_target_in_scene=True))
            for i in range(2):
                self.play(Transform(t.get_entries((2,3+i)).copy(), interm_eq[1+i], replace_mobject_with_target_in_scene=True))
            self.play(Transform(interm_eq, final_eq[0], replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("2")
            self.play(Transform(interm_eq, final_eq[0], replace_mobject_with_target_in_scene=True))
            current = VGroup(*[t.get_entries(x).copy() for x in [(3,3), (3,4), (3,5)]])
            self.play(Transform(current, final_eq[1],replace_mobject_with_target_in_scene=True))
            current = VGroup(*[t.get_entries(x).copy() for x in [(4,2), (4,4), (4,5)]])
            self.play(Transform(current, final_eq[2],replace_mobject_with_target_in_scene=True))
            current = VGroup(*[t.get_entries(x).copy() for x in [(5,2), (5,3), (5,5)]])
            self.play(Transform(current, final_eq[3],replace_mobject_with_target_in_scene=True))
        self.wait(1)
        self.play(FadeOut(final_eq))
        self.play(Transform(formulas[3], arranged_formulas[3]))
        self.wait(1)
        with self.voiceover("""
        The last new concept that we will introduce today is that<bookmark mark='1'/>
        of mutual information, what it tells us<bookmark mark='2'/> is how much information is shared 
        between both of our events.
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(formulas[4][0]))
            self.wait_until_bookmark("2")
            self.play(Write(formulas[4][1]))
        with self.voiceover("""
        You can think about it this way, just as one bit of information cuts down the space of possible events in half
        one bit of mutual information, means that knowing the outcome of one event
        eliminates cuts down the space of possible events for the other one in half
            """) as trk:
            pass
        self.play(Transform(formulas[4], arranged_formulas[4]))
        self.wait(1)       
        dependencies =VGroup(
        Tex("$H(X,Y) \\leq H(X) + H(Y)$"),
        Tex("$H(X,Y) = H(X) + H(Y|X)$"),
        Tex("$H(X) \\geq H(X|Y)$"),
        Tex("$I(X; Y) = H(Y) - H(Y|X)$"),
        Tex("$I(X; Y) = H(Y) + H(X) - H(Y,X)$")
        ).scale(0.6).arrange(DOWN, center=False, aligned_edge=LEFT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER*2.1)\
            .next_to(arranged_formulas, RIGHT, aligned_edge=UP).shift(2*RIGHT)
        
        with self.voiceover("""
        there are also a few very important dependencies between the formulas for entropy
            """) as trk:
            self.play(t.animate.next_to(arranged_formulas, DOWN))
        
        with self.voiceover("""
        Joint entropy <bookmark mark='1'/> is always lesser or equal to the sum of individual entropies for both events
        It is also equal <bookmark mark='2'/>to the uncertainty of one event, increased by the uncertainty of the second one given that we know the first
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(dependencies[0]))
            self.wait_until_bookmark("2")
            self.play(Write(dependencies[1]))

        with self.voiceover("""
        Entropy of one of the events is always greater than or equal to the entropy of that event given that we know the other one
            """) as trk:
            self.play(Write(dependencies[2]))

        with self.voiceover("""
        Mutual information <bookmark mark='1'/> is how much our uncertainty of an event decreases when we find out the outcome of the other one
        It is also equal <bookmark mark='2'/> to the cumulative uncertainty of both events individually reduced by the joint entropy
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(dependencies[3]))
            self.wait_until_bookmark("2")
            self.play(Write(dependencies[4]))
        def make_probs(combinations):
            num = np.sum(combinations)
            return np.array([[float(x)/num for x in y] for y in combinations])
        ebr = EntropyBoxRepresentation(make_probs(combinations))
        
        with self.voiceover("""
        This also has a nice visual representation that might help you get an intuitive feeling
        for the relation between entropies
            """) as trk:
            self.play(Create(ebr.set_scale(0.4).whole.next_to(t, RIGHT, aligned_edge=UP).shift(3*RIGHT)))
        self.wait(1)

        with self.voiceover("""
        Right now I'm going to show you two special cases to further improve your intuition, but before that 
        I encourage you to pause the video, and think about when will<bookmark mark='1'/> Joint entropy be exactly equal to the sum of individual entropies,
        and when will Entropy of one of the events<bookmark mark='2'/> be exactly equal to the conditional entropy of that event given the second one
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Indicate(dependencies[0]))
            self.wait_until_bookmark("2")
            self.play(Indicate(dependencies[2]))

        with self.voiceover("""
        the first special case is when both events have a deterministic relationship<bookmark mark='1'/>
        meaning that knowing one event tells us everything about the other <bookmark mark='2'/>
            """) as trk:
            combinations = [[i==j for i in range(4)]for j in range(4)]
            self.wait_until_bookmark("1")
            self.play(Transform(t, make_table(combinations).scale(0.4 * 0.4).move_to(t)))
            self.wait_until_bookmark("2")
            ebr.update(self, make_probs(combinations))

        with self.voiceover("""
        In this case, conditional entropy is equal to 0 because there is no uncertainty about the event if we know
        the outcome of the second one. Mutual information is equal to the entropies of the other variables, since knowing
        one event tells us everything about the other one
            """) as trk:
            pass
        with self.voiceover("""
        The second special case is when both events are independent<bookmark mark='1'/>
        meaning that knowing one event tells us nothing about the other <bookmark mark='2'/>
            """) as trk:
            combinations = [[True for i in range(4)] for j in range(4)]
            self.wait_until_bookmark("1")
            self.play(Transform(t, make_table(combinations).scale(0.4 * 0.4).move_to(t).shift(1.3*LEFT+0.4*DOWN)))
            self.wait_until_bookmark("2")
            ebr.update(self, make_probs(combinations))
        with self.voiceover("""
        This is exactly the case that I encouraged you to think about earlier, there is no mutual information since knowing the color
        does not reduce the probabilities of shapes, conditional entropy is equal to the entropy of an event since 
        knowing one event is not reducing our uncertainty. And Joint entropy is equal to the sum of individual entropies.
            """) as trk:
            pass
            
        self.play(FadeOut(t, formulas, dependencies, ebr.whole))
        toc = TOC(2)
        with self.voiceover("""
        We have come to the end of the second episode  <bookmark mark='1'/>
        This was a lot of information to parse but hopefully you now have an intuitive feeling
        <bookmark mark='2'/> of multiple event entropy
        If you want to test yourself event further I encourage you to think about - or perhaps
        event write out on paper the exact outcomes of all the entropies for our two special cases
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("2")
            self.play(toc.entries[2].main.animate.set_color(GREEN))
        self.wait(2)
        self.play(FadeOut(toc.header, *[e.main for e in toc.entries]))
        self.wait(2)
        
def make_probs(p,q):
    return [[q * p, q * (1-p)],
            [(1-q) * (1-p), (1-q) * p]]

def probs_to_str(pr):
    return [[f"{x:.2f}" for x in y]for y in pr]


class NoiselessChannelTheorem(VoiceoverScene, MovingCameraScene):
    def construct(self):

        self.set_speech_service(
            # RecorderService()
            GTTSService(transcription_model='base')
        )
        toc = TOC(3)

        with self.voiceover(
            """Hello and welcome to the fifth episode in our series on Information Theory
            Today we will talk about the fundamental theorem <bookmark mark='1'/> for a noiseless channel, also known 
            as the source coding theorem
            and we will introduce <bookmark mark='2'/> a concept of a channel capacity, as well as describe
            the ways of efficiently encoding information sent through our channel
            """
                            ) as trk:
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("1")
            self.play(*[Unwrite(e.main) for e in toc.entries[5:]])
            self.wait_until_bookmark("2")
            self.play(toc.entries[4].open())

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
        
        destination = Square()
        destination.add(Text("Destination", font_size=20))
        destination.shift(RIGHT*6)
        communication_system.add(Arrow(receiver.get_right(), destination.get_left(), buff=0, max_stroke_width_to_length_ratio=1))
        communication_system.add(destination)

        with self.voiceover("""
        Let's get back to our <bookmark mark='1'/>communication system, and focus on the source<bookmark mark='2'/>
        and the channel.
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(toc.get_open(4), communication_system, replace_mobject_with_target_in_scene=True))
            self.add(source, channel)
            communication_system.remove(source, channel)
            self.wait_until_bookmark("2")
            self.play(FadeOut(communication_system))
            self.play(source.animate.shift(3*RIGHT), channel.animate.shift(3*RIGHT))
        
        self.wait(1)

        with self.voiceover("""
        As you might remember from our previous episodes, our source<bookmark mark='1'/>
        can be described by it's entropy - this tells us how much information it produces
            """) as trk:
            self.wait_until_bookmark("1")
            entropy = Tex("$H$").next_to(source, DOWN)
            self.play(Write(entropy))


        with self.voiceover("""
        The way that we can describe our channel, is by it's capacity<bookmark mark='1'/> C which tells us how <bookmark mark='2'/>many
        bits we can send each second. It's given by this formula<bookmark mark='3'/> in which T is the
        duration of our signals and N is the number of allowed signals of duration T
            """) as trk:
            capacity = Tex("$C$").next_to(channel, DOWN)
            self.wait_until_bookmark("1")
            self.play(Write(capacity))
            self.wait_until_bookmark("2")
            self.play(Transform(capacity, Tex("$C$", "$=\\frac{bits}{second}$").next_to(channel, DOWN)))
            self.wait_until_bookmark("3")
            self.play(Transform(capacity, Tex("$C$", "$\\displaystyle{=\\lim_{T \\to \\infty} \\frac{\\log N(T)}{T}}$").next_to(channel, DOWN)))
            self.wait(1)

        with self.voiceover("""
            This essentially means, that we<bookmark mark='1'/> calculate it by sending messages through our channel, over and over again for a long time, then 
            we  <bookmark mark='2'/> take the information content that we sent and divide it by the time it took, giving us information per second of our channel
            """) as trk:
            self.play(FadeOut(source, entropy))
            self.play(capacity.animate.shift(3*LEFT), channel.animate.shift(3*LEFT))

            self.wait_until_bookmark("1")
            run_time = 0.5
            while trk.time_until_bookmark("2") > 0:
                random_binary = "".join(["0" if random() > 0.5 else "1" for i in range(5)])
                sent_message = Tex(random_binary).next_to(channel, LEFT).shift(LEFT)
                recieved_message = sent_message.copy().next_to(channel, RIGHT).shift(RIGHT)
                self.play(Write(sent_message, run_time=run_time))
                self.play(FadeOut(sent_message, target_position=channel.get_left(), run_time=run_time))
                self.play(FadeIn(recieved_message, target_position=channel.get_right(), run_time=run_time))
                self.play(FadeOut(recieved_message, run_time=run_time))
                run_time*=0.9
            
        self.play(capacity.animate.shift(3*RIGHT), channel.animate.shift(3*RIGHT))
        self.play(FadeIn(source, entropy), Transform(capacity, Tex("$C$").next_to(channel, DOWN)))
        self.wait(1)

        with self.voiceover("""
        What the fundamental theorem for a noiseless channel tells us is that we can
        send messages through our channel<bookmark mark='1'/> with a rate that's very close
        to the capacity of our channel divided by the entropy of our source. Epsilon here is just 
        a very small number that indicates that the outcome is a little bit smaller than our fraction.
            """) as trk:
            possible_rate = MathTex("Rate = \\frac{C}{H}", "- \\epsilon")
            self.wait_until_bookmark("1")
            self.play(Write(possible_rate))
            self.wait(1)

        with self.voiceover("""
        Take a moment to think how beautiful and logical this outcome is. Remember that, the capacity<bookmark mark='1'/> is how much information we can send in a second
        and the entropy tells us how much information we expect<bookmark mark='2'/> from one symbol produced by our source. Divide them and that gives<bookmark mark='3'/> us the 
        number of symbols that we can send in a second
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(possible_rate, MathTex("Rate = \\frac{C}{H} - \\epsilon", "\\\\", "=\\frac{\\frac{bits}{s}}{H}").move_to(possible_rate, aligned_edge=LEFT)))
            self.wait_until_bookmark("2")
            self.play(Transform(possible_rate, MathTex("Rate = \\frac{C}{H} - \\epsilon", "\\\\", "=\\frac{\\frac{bits}{s}}{\\frac{bits}{symbol}}").move_to(possible_rate, aligned_edge=LEFT)))
            self.wait_until_bookmark("3")
            self.play(Transform(possible_rate, MathTex("Rate = \\frac{C}{H} - \\epsilon", "\\\\", "=\\frac{symbol}{s}").move_to(possible_rate, aligned_edge=LEFT)))

        weather_conditions = VGroup(*[Text(x) for x in ["Sunny", "Rainy","Cloudy","Snowy","Windy","Stormy","Foggy","Drizzle"]])
        weather_conditions.arrange(DOWN, aligned_edge=LEFT).shift(6*LEFT).scale(0.6)
        probabilities = [0.6,0.05,0.2,0.01,0.05,0.01,0.03,0.05]

        with self.voiceover("""
        To show you how important this theorem is, imagine this scenario. You are resting in a tavern and a man runs in
        saying that they have a high paying job at a local weather station. They have a channel <bookmark mark='1'/>that can send 2 bits a second
        and they need someone to help them transmit weather data from one station to another.
            """) as trk:
            self.play(Unwrite(possible_rate[2]))
            self.wait_until_bookmark("1")
            self.play(Transform(capacity, Tex("$C=2\\frac{bits}{s}$").next_to(channel, DOWN)))
        
        with self.voiceover("""
        You can hear everyone around you saying easy and getting up to take the job. But the weather man tells you the catch.
        <bookmark mark='1'/> there are 8 possible weather conditions. And we need to send 10000 states in 10000 seconds. 
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(self.camera.frame.animate.scale(1.3))
            self.play(Write(weather_conditions))

        with self.voiceover("""
        Everyone quickly does the math in their heads and screams that it's not possible. One <bookmark mark='1'/>symbol requires 
        3 bits to encode and the channel capacity is only 2 bits. But you know better.
            """) as trk:
            self.wait_until_bookmark("1")
            encodings = VGroup(*[Tex(x).scale(0.6).next_to(weather_conditions[i]) for i, x in enumerate(create_binary_digits(3))])
            self.play(Write(encodings))
        
        def update_entropy(current_entropy, additional=None): 
            equality = '=' if current_entropy == 0 else '\\approxeq'
            old = VGroup(entropy)
            if additional != None:
                old.add(additional)
            self.play(Transform(old, Tex(f"$H{equality}{current_entropy:.2f}$").next_to(source, DOWN)))
        current_entropy = 0
        entropy_text = Tex("$H(X)=\\sum\\limits_{x}$","$p(x)$", "$\\cdot \\log_2($", "$\\frac{1}{p(x)}$", "$)$").shift(2*UP)

        with self.voiceover("""
        You approach the man and tell him that it might be possible to send that data, but first
        you have too take a quick look at it and calculate<bookmark mark='1'/> it's entropy
            """) as trk:
            self.wait_until_bookmark("1")
            update_entropy(current_entropy)
            self.play(Write(entropy_text))

        written_probs = VGroup(*[Tex(str(x)).scale(0.6).next_to(weather_conditions[i], LEFT)  for i,x in enumerate(probabilities)])
        with self.voiceover("""
        Going into the weather station, you notice that indeed, just as you expected - there are weather states <bookmark mark='1'/>that are much more probable
        than <bookmark mark='2'/>the other ones, so you quickly go over all of them and calculate the entropy to check how much information there really is in
        the set of possible weather conditions. 
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(written_probs))
            self.wait_until_bookmark("2")
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
        
        with self.voiceover("""
        You then use you outcome to calculate the possible rate <bookmark mark='1'/>at which you can send that information
        and it turns out that it's <bookmark mark='2'/> greater than one so you can send more than one symbol per second and 
        get the payment for that job. The only question now is - how do you do this?
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(possible_rate, Tex(f"$Rate = \\frac{{2}}{{{current_entropy:.2f}}} - \\epsilon$")))
            self.wait_until_bookmark("2")
            self.play(Transform(possible_rate, Tex(f"$Rate \\approxeq {(2/current_entropy):.2f}$")))

        huffman_codings = [Tex(c).scale(0.6).next_to(weather_conditions[i]) for i,c in enumerate(["0", "1100", "10", "111000", "1101", "111001", "11101", "1111"])]

        with self.voiceover("""
        And the answer is - encoding. Let's say that instead of the current encodings for our states, you change them to this<bookmark mark='1'/>
        ones, that have 2 properties, firstly they make more probable messages have shorter lengths and less probable ones longer, and secondly
        no message is a prefix of another one so there is only one way to decode the sequence of messages.
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(*[Transform(e,h) for e,h in zip(encodings, huffman_codings)])

        with self.voiceover("""
        The codes are called huffman codes, I won't go into much detail on how to generate them because there is already a magnificent
        video by Reducible on the subject that I will link in the description for those interested
            """) as trk:
            pass

        with self.voiceover("""
        The expected length of our message will the sum over all possible states, that multiplies the probability of <bookmark mark='1'/> sending that state
        multiplied by the length of the message required to send it. <bookmark mark='2'/> We go over all of the states and calculate what is the average
        length of our message after changing  the encoding
            """) as trk:
            average_length = Tex("$L=$", "$\\sum p(x) \\cdot length(x)$").next_to(possible_rate, 7*DOWN)
            self.play(Write(average_length))
            length_formulas = VGroup()
            lengths = []
            for i, c in enumerate(["0", "1100", "10", "111000", "1101", "111001", "11101", "1111"]):
                length_formulas.add(Tex(f'${probabilities[i]} * {len(c)}{"" if i == 7 else "+"}$'))
                lengths.append(probabilities[i] * len(c))
            length_formulas.arrange_in_grid(2,4,buff=0.1).next_to(average_length, DOWN)
            for i in range(len(probabilities)):
                self.play(Transform(VGroup(encodings[i].copy(), written_probs[i].copy()), length_formulas[i], replace_mobject_with_target_in_scene=True))

        with self.voiceover("""
        And it turns out, that our average length is now 1.87, which is very close to our entropy that described the amount of information - meaning
        that we are very close to perfect compression. To calculate the rate at which we can send our data now <bookmark mark='1'/>we divide the capacity by our new message length
        giving us a rate <bookmark mark='2'/>greater than one message per second. 
            """) as trk:
            self.play(Transform(VGroup(average_length, length_formulas),Tex("$L=$", f"${sum(lengths)}$").next_to(possible_rate, DOWN) ))
            self.wait_until_bookmark("1")
            current_rate = Tex("$R=$", "$\\frac{C}{L}$").next_to(possible_rate, UP)
            self.play(Create(current_rate))
            self.wait_until_bookmark("2")
            self.play(Transform(current_rate, Tex("$R=$", f"${(2/sum(lengths)):.2f}$").move_to(current_rate, aligned_edge=LEFT)))

        with self.voiceover("""
        And just like that, you managed to solve the problem that a lot of people would claim to be impossible
            """) as trk:
            pass

        self.play(*[FadeOut(x) for x in self.mobjects])

        toc = TOC(4)
        with self.voiceover("""
        With that we come to an end <bookmark mark='1'/>of another episode. 
        Hopefully you now see how useful information theory can be and you appreciate
        the beauty <bookmark mark='2'/> of the fundamental theorem for the noiseless channel.
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("2")
            self.play(toc.entries[4].main.animate.set_color(GREEN))
        self.wait(2)
        self.play(FadeOut(toc.header, *[e.main for e in toc.entries]))
        self.wait(2)

class NoisyChannelTheorem(VoiceoverScene, ZoomedScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, zoom_factor=0.05, zoomed_camera_config={'background_opacity': 1, 'default_frame_stroke_width': 0.5}, image_frame_stroke_width=1)

    def construct(self):

        self.set_speech_service(
            # RecorderService()
            GTTSService(transcription_model='base')
        )
        toc = TOC(5)

        with self.voiceover(
            """Hello and welcome to the sixth, and final episode in our series on Information Theory
            Today we will talk about the fundamental theorem <bookmark mark='1'/> for a noisy channel, also known 
            as Noisy channel coding theorem, that was first described by Claude Shannon
            and we will introduce a concept of a channel capacity in presence of noise, 
            as well as provide a rate at which we can send symbols through the noisy channel - and describe how to do so reliably
                       """
                            ) as trk:
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])
            self.wait_until_bookmark("1")
            self.play(toc.entries[5].open())

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

        with self.voiceover("""
        Given our blueprint<bookmark mark='1'/> for a communication system and using the <bookmark mark='2'/> binary symmetric channel as our 
        means of communication, we need a way to calculate the<bookmark mark='3'/> rate at which we are able to send information through that channel
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(toc.get_open(5), communication_system, replace_mobject_with_target_in_scene=True))

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
            self.wait_until_bookmark("2")
            self.play(Transform(communication_system, VGroup(bsc.full_channel, source_arrows, destination_arrows)))
            self.wait(1)
            q = 0.7
            p = 0.9
            q_tr = ValueTracker(q)
            p_tr = ValueTracker(p)
            p_text = Tex("$p=\\:$", f"${p_tr.get_value()}$").add_updater(lambda x: x.become(Tex("$p=\\:$",f"${p_tr.get_value():.2f}$"), match_center=True)).next_to(bsc.full_channel, DOWN+RIGHT)
            q_text = Tex("$q=\\:$", f"${q_tr.get_value()}$").add_updater(lambda x: x.become(Tex("$q=\\:$",f"${q_tr.get_value():.2f}$"), match_center=True)).next_to(bsc.full_channel, DOWN+LEFT)
            self.play(Write(p_text), Write(q_text))
            communication_system.add(p_text, q_text, source, destination)
            self.play(communication_system.animate.scale(0.5).shift(2*UP))
            self.wait_until_bookmark("3")
            rate = Tex("$R$", "$\\:=p$", f"$\\:={p_tr.get_value():.2f}$").shift(DOWN)
            self.play(Write(rate[0]))
        self.wait(1)

        with self.voiceover("""
        I believe that you already have the tools and intuition necessary to get to the correct answer, but shannon claims
        that the first impulse might be to just<bookmark mark='1'/> take the amount of bits that we sent that didn't get flipped
        For example if we sent with a 90 percent flip probability, <bookmark mark='2'/> 0.9 bits
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Write(rate[1]))
            self.wait_until_bookmark("2")
            self.play(Write(rate[2]))


        rate.add_updater(lambda x: x.become(Tex("$R$", "$\\:=p$", f"$\\:={p_tr.get_value():.2f}$").shift(DOWN).set_color(RED)))
        
        with self.voiceover("""
        This might seem correct at first,<bookmark mark='1'/> and the idea is right but the formulation is not
        let's see what happens as we increase the probability of a bit flip to 0.5
        <bookmark mark='2'/>, by our current definition we are still sending bits with a rate of 0.5, but there is actually no information
        being transmitted since what the destination gets is just random outcomes
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(rate.animate.set_color(RED))
            self.wait_until_bookmark("2")
            self.play(p_tr.animate.set_value(0.5))

        with self.voiceover("""
        Likewise, if we set the probability of a flip to 100%, this formula gives us a rate of 0 bits
        while we can just flip the bit again on the receiving side to get the correct answer with no information loss
            """) as trk:
            self.play(p_tr.animate.set_value(0.0))

        p_tr.set_value(0.9)
    
        with self.voiceover("""
        Evidently the proper correction to apply to the amount of transmitted information is the amount of missing information
        in the received signal, or in other terms, the uncertainty about what was actually send in the received signal
        could you formulate that in terms of entropy? 
            """) as trk:
            pass

        rate.clear_updaters()
        with self.voiceover("""
        The answer is the following - our rate is <bookmark mark='1'/>equal to the entropy of the input, reduced by the entropy of the input 
        given the output. Or in other words, it's how much information there was in the original signal reduced by how uncertain we are of 
        what got sent when we receive the signal
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(rate, Tex("$R=\\:$", "$H(X) - H(X|Y)$").shift(DOWN).set_color(GREEN)))
        self.wait(1)

        with self.voiceover("""
        And as some of you might remember, this is exactly what was formulated as
        mutual information between the input and the output
            """) as trk:
            self.play(Transform(rate, Tex("$R=\\:$", "$I(X; Y)$").shift(DOWN).set_color(GREEN)))
        def mutual_inf():  return f"{abs(I(np.array(make_probs(p_tr.get_value(),q_tr.get_value())))):.2f}"

        with self.voiceover("""
        And we can check if our previous examples made sense, 
        for equal flip probability <bookmark mark='1'/>where we send random data,
        the rate is indeed 0 and for an inverted case <bookmark mark='2'/> the rate
        is equal to the expected information in the input
            """) as trk:
            self.play(Transform(rate, Tex("$R=\\:$", "$I(X; Y)$", f"$=\\:{mutual_inf()}$").shift(DOWN).set_color(GREEN)))
            self.wait_until_bookmark("1")
            rate.add_updater(lambda x : x.become(Tex("$R=\\:$", "$I(X; Y)$", f"$\\:={mutual_inf()}$").shift(DOWN).set_color(GREEN)))
            self.play(p_tr.animate.set_value(0.5))
            self.wait_until_bookmark("2")
            self.play(p_tr.animate.set_value(0.0))
        
        self.play(p_tr.animate.set_value(0.9))

        with self.voiceover("""
        The capacity for the noisy channel, should be <bookmark mark='1'/> the maximum possible rate of transmission
        and since we can only manipulate the entropy of our source, it would be <bookmark mark='2'/> when the expected
        information of the sent message is maximal, so when we maximize our input's entropy
            """) as trk:
            self.wait_until_bookmark("1")
            capacity = Tex("$C = Max(R)$")
            self.play(Write(capacity))
            self.wait_until_bookmark("2")
            self.play(q_tr.animate.set_value(0.5))
            self.wait(1)
            self.play(Transform(capacity, Tex("$C = Max(R)$", f"$\\:={mutual_inf()}$")))

        with self.voiceover("""
        The notion of a capacity of a noisy channel may seem uncomfortable at first, why would we define such a metric since the 
        output is never fully certain? However it should be clear that we can reduce the uncertainty of the message by adding redundancy to it.
            """) as trk:
            pass
        with self.voiceover("""
        For example imagine that we sent the same message 1000 times, statistically we would be able to recover the 
        original message, with a very low probability of error, but our rate of transmission would drop by a factor of a 1000
            """) as trk:
            pass

        rate.clear_updaters()
        capacity.clear_updaters()
        self.play(FadeOut(communication_system, source, destination, p_text, q_text),
                  Transform(rate, Tex("$R=\\:$", "$I(X; Y)$").shift(DOWN + 3*RIGHT)),
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
        with self.voiceover("""
        Here is where the beauty of the noisy channel theorem comes at play, <bookmark mark='1'/>it shows what are the attainable 
        <bookmark mark='2'/>uncertainties of the input given the output when we send data through a source<bookmark mark='3'/> with
        a certain entropy
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Create(ax))
            self.wait_until_bookmark("2")
            self.play(Create(labels[1]))
            self.wait_until_bookmark("3")
            self.play(Create(labels[0]))


        with self.voiceover("""
        And it revolutionized the modern world by showing that if we transmit data with rates up to 
        our channel's capacity<bookmark mark='1'/> the error rate can be made arbitrarily small
            """) as trk:
            self.play(Create(attainable), Create(non_attainable), Create(c_label))
            self.zoomed_camera.frame.move_to(ax.c2p(0.3, EPS))
            self.activate_zooming(True)
            self.wait_until_bookmark("1")
            l = DashedLine(ax.c2p(0.3,EPS/3.5),ax.c2p(0.3, EPS), stroke_width=0.3, color=BLUE)
            t = Tex("$\\epsilon$", color=BLUE).scale(0.07).next_to(l, buff=0.01)
            self.play(Create(l), Create(t))

        self.wait(3)
        self.play(*[FadeOut(x) for x in self.mobjects])

                
        
def combine_positions(a,b,mask): 
    mask = np.array(mask)
    return a*mask + b*(1-mask)

class NoisyChannelTheorem2(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            # RecorderService()
            GTTSService(transcription_model='base')
        )
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

        with self.voiceover("""
        But before we get into the intuition behind the noisy channel, let's see how can we send messages reliably, 
        because obviously repetition is not going to take us very far.
            """) as trk:
            self.play(Create(communication_system))

        with self.voiceover("""
        I already hinted this before but we are going to use encoding and decoding
        to add redundancy to our message that reduces the error rate introduced by the noise.
            """) as trk:
            self.play(Create(decoding_box), Create(encoding_box))

        with self.voiceover("""
        Let's see and example, where we don't perform any encoding
            """) as trk:
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


        with self.voiceover("""
        Imagine that our source sends digits from 0 to 3, since there is no encoding our transmitter just blindly
        <bookmark mark='1'/> copies the message and sends it over our channel
            """) as trk:
            self.play(Transform(source.copy(), source_message, replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("1")
            self.play(Transform(transmitter.copy(), transmitted_message, replace_mobject_with_target_in_scene=True))
            s_t_arrows = VGroup(*[Line(s.get_right(), t.get_left(), buff=0.25) for s,t in zip(source_message, transmitted_message)])
            r_d_arrows = VGroup(*[Line(r.get_right(), d.get_left(), buff=0.25) for r,d in zip(noisy_message, destination_message)])
            self.play(Create(s_t_arrows))

        with self.voiceover("""
        There, it is disrupted by noise that randomly increments the number in our message.
            """) as trk:
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

        with self.voiceover("""
        And again, there is no decoding so we can completely skip the receiver 
            """) as trk:
            self.play(Transform(destination.copy(), destination_message, replace_mobject_with_target_in_scene=True))
            self.play(Create(r_d_arrows))


        with self.voiceover("""
        Currently there is no way to unambiguously map the message that was received at the destination
        to the message that was sent, but there are messages outputs are non confusable, <bookmark mark='1'/>
        let's say we just send 0 and 2, now there is no ambiguity about the message on the receiving side
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(FadeOut(source_message[1], source_message[3],
                            *t_r_arrows[2:4], *t_r_arrows[6:]))

        self.play(FadeIn(source_message[1], source_message[3],
                        *t_r_arrows[2:4], *t_r_arrows[6:]))
        self.wait(1)

        self.play(FadeOut(*t_r_arrows, *r_d_arrows, noisy_message, destination_message))

        encoded_message = VGroup(*[Tex(str(x)).scale(0.6) for x in range(0,8,2)]).arrange(DOWN).shift(LEFT)
        encoded_message.move_to(combine_positions(transmitter.get_center(), encoded_message.get_center(), [1,0,0]))

        with self.voiceover("""
        So for this case, we can just use encoding<bookmark mark='1'/> and map all of our messages, so that they are a multiple of 2
            """) as trk:
            self.play(FadeIn(encoding_box))
            self.play(*[Transform(t, e, replace_mobject_with_target_in_scene=True) for t,e in zip(transmitted_message, encoded_message)])
            self.play(*[a.animate.set_color(encoding_box.color) for a in s_t_arrows])

        self.wait(1)
        noisy_message = VGroup(*[Tex(str(x)).scale(0.6) for x in range(0,8)]).arrange(DOWN)
        noisy_message = noisy_message.move_to(combine_positions(channel.get_center(), noisy_message.get_center(), [1,0,0]))

        with self.voiceover("""
        And now even if our noise increments the message, it is still not overlapping with any other message in our subset of messages
            """) as trk:
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
        decoded_message = decoded_message.move_to(combine_positions(destination.get_center(), decoded_message.get_center(), [1,0,0]))
        r_d_arrows = VGroup(*[Line(r.get_right(), d.get_left(), buff=0.25, color=decoding_box.color) for r,d in zip(recieved_message, decoded_message)])

        with self.voiceover("""
        All that is now left is to use the decoder to map our encoded messages, back to their original
        form and voila - we achieved reliable transmission in presence of noise
            """) as trk:
            self.play(FadeIn(decoding_box))
            for i in range(len(decoded_message)):
                decoder_cpy = decoding_box.copy()
                self.play(FadeOut(recieved_message[i].copy(), target_position=decoder_cpy))
                self.play(Transform(decoder_cpy, r_d_arrows[i], replace_mobject_with_target_in_scene=True), Create(decoded_message[i]))

        self.wait(1)

        with self.voiceover("""
        But that is not exactly fair, since real world data and noise do not really look like this
        and is usually <bookmark mark='1'/>in some sort of binary form
            """) as trk:
            self.play(FadeOut(*decoding_arrows, *noise_arrows))
            self.wait_until_bookmark("1")
            animations = []
            for grp in [source_message, encoded_message, noisy_message, recieved_message, decoded_message]:
                for i, src in enumerate(grp):
                    binary_text = Tex(to_binary(int(src.get_tex_string()), 3)).scale(0.6).move_to(src)
                    animations.append(Transform(src, binary_text, replace_mobject_with_target_in_scene=True))
                    grp[i] = binary_text
            self.play(*animations)

        def diff(a, b): 
            return sum([0 if a[i]==b[i] else 1 for i in range(len(a))])
        src = encoded_message[0]
        colors = [GREEN, RED_C, RED_B, RED_A]
        transmitting_lines = []
        for r in noisy_message:
            transmitting_lines.append(Line(src.get_right(), r.get_left(), buff=0.25, color=colors[diff(src.get_tex_string(), r.get_tex_string())]))    
        with self.voiceover("""
        And the noise just changes each bit with some probability. The important thing to note is that if we are not flipping our bits at random
        there will be some outcomes of noise that are more probable than others, this is denoted by different colors here. 
            """) as trk:
            self.play(*[Create(t) for t in transmitting_lines])
        self.wait(1)
        
        with self.voiceover("""
        And the same goes for the receiving part
            """) as trk:
            src = recieved_message[0]
            decoding_lines = []
            for r in noisy_message:
                decoding_lines.append(Line(r.get_right(), src.get_left(), buff=0.25, color=colors[diff(src.get_tex_string(), r.get_tex_string())]))    
            self.play(*[Create(d) for d in decoding_lines])
            self.wait(1) 


        with self.voiceover("""
        To combat noise, we can just assume that some of those pattens of perturbation by noise are so improbable that they will never happen
            """) as trk:
            self.play(*[FadeOut(l) for l in transmitting_lines+decoding_lines if str(l.color).upper() == RED_B or str(l.color).upper() == RED_A])

        with self.voiceover("""
        Right now we can use this encoding to send a second message through our channel.
        <bookmark mark='1'/>
        Since their subset of probable outcomes of noise does not overlap 
            """) as trk:
            src = recieved_message[3]
            new_code = Tex("111").scale(0.6).move_to(src)
            self.play(Transform(src, new_code, replace_mobject_with_target_in_scene=True)) 
            recieved_message[3] = new_code

            src = encoded_message[3]
            new_code = Tex("111").scale(0.6).move_to(src)
            self.play(Transform(src, new_code, replace_mobject_with_target_in_scene=True)) 
            encoded_message[3] = new_code
            src = encoded_message[3]

            self.wait_until_bookmark("1")
            transmitting_lines2 = []
            for r in noisy_message:
                transmitting_lines2.append(Line(src.get_right(), r.get_left(), buff=0.25, color=colors[diff(src.get_tex_string(), r.get_tex_string())]))    
            self.play(*[Create(t) for t in transmitting_lines2])
            
            src = recieved_message[3]
            decoding_lines2 = []
            for r in noisy_message:
                decoding_lines2.append(Line(r.get_right(), src.get_left(), buff=0.25, color=colors[diff(src.get_tex_string(), r.get_tex_string())]))    
            self.play(*[Create(d) for d in decoding_lines2])

            self.play(*[FadeOut(l) for l in transmitting_lines2+decoding_lines2 if str(l.color).upper() == RED_B or str(l.color).upper() == RED_A])
        self.wait(3)


        bsc = BSC()
        bsc.full_channel.scale(0.7).shift(3*UP)        
        bsc.full_channel.remove(bsc.q_label, bsc.one_minus_q_label, bsc.one_minus_p_label0, bsc.p_label0, bsc.one_minus_p_label1, bsc.p_label1)
 
        source_arrows = VGroup(Arrow(source.get_right(), bsc.input_bit_0.get_left(), buff=0.25, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1),
                               Arrow(source.get_right(), bsc.input_bit_1.get_left(), buff=0.25, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1))
        destination_arrows = VGroup(Arrow(bsc.output_bit_0.get_right(), destination.get_left(), buff=0.25, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1),
                                    Arrow(bsc.output_bit_1.get_right(), destination.get_left(), buff=0.25, max_stroke_width_to_length_ratio=2, max_tip_length_to_length_ratio=0.1))

        with self.voiceover("""
        With that in mind, it is now time to get an intuition behind the noisy channel theorem 
        <bookmark mark='1'/>
        again we will be using our binary symmetric channel as an example
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(*[FadeOut(x) for x in self.mobjects if x not in [communication_system]])
            self.play(Transform(communication_system, VGroup(bsc.full_channel, source_arrows, destination_arrows, source.copy(), destination.copy()).shift(LEFT).scale(0.5)))
        
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

        with self.voiceover("""
        So far we were only using encoding and decoding with a single message. But it is much more efficient
        when we use something called an extended channel.
            """) as trk:
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

        with self.voiceover("""
        The idea of an extended channel is that we use our channel to send multiple messages, and encode and then decode
        a block made out of them. Here the number of symbols that form that block is denoted by capital T.
            """) as trk:
            for l in range(2, 5):
                self.play(ShowPassingFlash(source_arrows.copy().set_color(BLUE), time_width=0.7))
                dir = x_outcomes.get_edge_center(UP)
                x_outcomes = VGroup(x_outcomes, bsc.input_0_text.copy(), bsc.input_1_text.copy())
                self.play(Transform(x_outcomes, create_digits(l).move_to(dir, aligned_edge=UP)))
                self.play(Transform(usage, Tex("$T = $", f"{l}").move_to(usage)))
                self.play(ShowPassingFlash(bsc.arrows.copy().set_color(BLUE), time_width=0.7))
                dir = y_outcomes.get_edge_center(UP)
                y_outcomes = VGroup(y_outcomes, bsc.output_0_text.copy(), bsc.output_1_text.copy())
                self.play(Transform(y_outcomes, create_digits(l).move_to(dir, aligned_edge=UP)))
        self.wait(1)

        binary_digits = create_binary_digits(7)
        binary_digits.sort(key=lambda x: x.count("1"))
        tex_digits = [Tex(x[:3], "...", x[-3:]).scale(0.7) for x in binary_digits]
        long_message = VGroup(*(tex_digits[:6] + [three_dots] + tex_digits[-6:])).arrange(DOWN, center=False, buff=buffer)

        with self.voiceover("""
        To give an intuitive understanding of the noisy channel theorem <bookmark mark='1'/>
        we are going to work with large blocks, so just imagine for now that we encode an infinitely 
        long sequence of messages
            """) as trk:
            self.wait_until_bookmark("1")
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

        with self.voiceover("""
        In this scenarios there will be two to the power or T
        possible messages we can send
            """) as trk:
            probable_messages = Tex("$2^{T}$").next_to(x_outcomes, LEFT)
            self.play(Transform(usage.copy(), probable_messages, replace_mobject_with_target_in_scene=True))

        all_arrows = VGroup()
        
        causes_arrows = VGroup()
        for i in range(13):
            causes_arrows.add(Line(x_outcomes[0].get_center(), y_outcomes[i].get_center(), stroke_width=1))

        with self.voiceover("""
        And each message can be obfuscated by noise, into every other output message with varying probabilities
            """) as trk:
            self.play(LaggedStart(*[Create(c) for c in causes_arrows]))
            all_arrows.add(causes_arrows)
            self.wait(1)

        error_free1 = Tex("$2^{RT} = $", "$\\frac{}{}$").shift(2*RIGHT)
        error_free2 = Tex("$2^{RT} = $", "$\\frac{output\\ messages}{}$").move_to(error_free1, LEFT)
        error_free3 = Tex("$2^{RT} = $", "$\\frac{output\\ messages}{unique\\ messages}$").move_to(error_free2, LEFT)

        with self.voiceover("""
        Our rate is essentially the amount <bookmark mark='1'/>of bits that we can send reliably through our channel
        each cycle
        To calculate it, we need to take the amout of messages <bookmark mark='2'/>that we can send
        and <bookmark mark='3'/> divide them by the amount of messages that can be uniquely encoded
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Create(error_free2[0]))
            self.wait_until_bookmark("2")
            self.play(Transform(y_outcomes.copy(), error_free2[1], replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("3")
            self.play(Transform(VGroup(error_free2, causes_arrows.copy()), error_free3, replace_mobject_with_target_in_scene=True))

        num_noised = probable_messages.copy().next_to(causes_arrows, DOWN)
        num_output = probable_messages.copy().next_to(y_outcomes, RIGHT)
        with self.voiceover("""
        With our current assumptions, the amount of output messages<bookmark mark='1'/> and the amount of unique messages
        <bookmark mark='2'/> will be the same as the amount of input messages
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(y_outcomes.copy(), num_output, replace_mobject_with_target_in_scene=True))
            self.wait_until_bookmark("2")
            self.play(Transform(causes_arrows.copy(), num_noised, replace_mobject_with_target_in_scene=True))

        error_free4=Tex("$2^{RT} = $", "$\\frac{2^{T}}{2^{T}}$", "$ = 2^0$", "$ = 1$").move_to(error_free3, LEFT)
        with self.voiceover("""
        If we do the math this essentially boils down to just a rate of 1. And it is true, if we want a completely error free
        communication we can only send one message no matter how long our block is.
            """) as trk:
            self.play(Transform(error_free3, error_free4[:2]))
            self.wait(1)
            self.play(Write(error_free4[2]))
            self.wait(1)
            self.play(Write(error_free4[3]))
        self.play(Transform(error_free3, error_free4))
        self.remove(error_free4[2])
        self.remove(error_free4[3])


        uncreation = []
        for i in range(12, 2, -1):
            uncreation.append(Uncreate(causes_arrows[i]))

        with self.voiceover("""
        And as you might have already guessed, we are going to do the same trick as before <bookmark mark='1'/>
        we pick a very small error rate that we are satisfied with, and we prune out the connections between the messages
        that have such low probability that they will almost certainly never happen
            """) as trk:
            self.wait_until_bookmark("1")
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

        
        with self.voiceover("""
        Then we just use the input messages that map to unique output messages
            """) as trk:
            for i in range(11, 0, -1):
                if i in [0, 3, 8, 11]: continue
                all_arrows.remove(all_arrows[i])

        self.wait(1)

        with self.voiceover("""
        But to be fair, we also need to consider that there will be some inputs and outputs that will also be improbable
        <bookmark mark='1'/> so that leaves us with 2 to the power of entropy of our input times the amount of messages that we sent
        of probable input messages, <bookmark mark='2'/> and similarly for the output
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(Transform(probable_messages, Tex("$2^{H(X)T}$").move_to(probable_messages, RIGHT)))
            self.wait_until_bookmark("2")
            self.play(Transform(num_output, Tex("$2^{H(Y)T}$").move_to(num_output, LEFT+DOWN)),
                    Transform(error_free3, Tex("$2^{RT} = $", "$\\frac{2^{H(Y)T}}{2^{T}}$").move_to(error_free3, LEFT)))
        
        with self.voiceover("""
        And the reasonable effects for each message that we sent is equal <bookmark mark='1'/>to the amount of information that our input
        gives as about the output, again multiplied by the amount of messages that we sent
            """) as trk:
            self.play(Transform(num_noised, Tex("$2^{H(Y|X)T}$").move_to(num_noised, LEFT+DOWN)),
                    Transform(error_free3, Tex("$2^{RT} = $", "$\\frac{2^{H(Y)T}}{2^{H(Y|X)T}}$").move_to(error_free3, LEFT)))

        with self.voiceover("""
        And this essentially simplifies to our rate being equal to mutual information between the input and the output
        - this is exactly the outcome, that Shannon came to in his work.
            """) as trk:
            self.play(Transform(error_free3, Tex("$2^{RT} = $", "$2^{I(X;Y)T}$").move_to(error_free3, LEFT)))
            self.wait(2)
            self.play(Transform(error_free3, Tex("$R$", "$I(X;Y)$").move_to(error_free3, LEFT)))
        
        with self.voiceover("""
        The interesting part about the noisy channel theorem is that it does not tell you how to find the codes,
        it just proves that they exist - and up to this day there is still a huge amount of work being put into finding the 
        best codes for<bookmark mark='1'/> some types of channels.
            """) as trk:
            self.wait_until_bookmark("1")
            self.play(FadeOut(*[o for o in self.mobjects]))


        toc = TOC(5)
        with self.voiceover("""
        This is where I leave you, the series has been a long and great journey for me
        I learned a lot through making this, and I hope that you learned as much by watching it.
            """) as trk:
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
            self.play(*[Write(e.main) for e in toc.entries])

        self.play(toc.entries[5].main.animate.set_color(GREEN))
        self.wait(2)
        self.play(FadeOut(toc.header, *[e.main for e in toc.entries]))
        self.wait(2)

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


class Entry:
    def __init__(self, main_tex, subtexts = []):
        self.main = Tex(main_tex)
        self.list = BulletedList(*subtexts)

    def open(self):
        return Transform(self.main.copy(), self.list.next_to(self.main, DOWN, aligned_edge=LEFT), replace_mobject_with_target_in_scene=True)

    def close(self):
        return Unwrite(self.list)


class TOC:
    def __init__(self, episode = 0):
        self.header = Tex("Information Theory", font_size=85)

        information_content = Entry("1. Information", ["What is information?", "How do we measure information?"]) 
        entropy = Entry("2. Entropy", ["Uncertainty", "Surprise", "Information"]) 
        two_event_entropy = Entry("3. Entropy with multiple events", ["Joint entropy", "Conditional entropy", "Mutual information"])
        communication_system = Entry("4. Communication System", ["General communication system", "Example: Binary Symmetric Channel", "Analysis of a BSC"])
        noiseless_channel = Entry("5. Noiseless Channel Theorem", ["Capacity", "Efficient encoding"])
        noisy_channel = Entry("6. Noisy Channel Theorem", ["Capacity", "Rate", "Reliable communication"])

        self.entries = [information_content, entropy, two_event_entropy, communication_system, noiseless_channel, noisy_channel]
        self.entries[0].main.shift(2*LEFT + 2*UP)

        for i in range(1, len(self.entries)):
            self.entries[i].main.next_to(self.entries[i-1].main, DOWN, aligned_edge=LEFT)
        for i in range(episode):
            self.entries[i].main.set_color(GREEN)

    def get_open(self, episode):
        return VGroup(self.header, *[self.entries[i].main for i in range(episode+1)], self.entries[episode].list)



class TableOfContents(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            RecorderService()
        )
        toc = TOC()
        contents = BulletedList("What it is", "Why should you care", "What this series will be ", "What this series won't be")

        with self.voiceover("Header") as trk:
            self.play(Write(toc.header.next_to(toc.entries[0].main, UP, aligned_edge=LEFT)))
        rendered = []
        for i, e in enumerate(contents):
            print(e.get_tex_string())
            self.wait(1)
            with self.voiceover(e.get_tex_string()) as trk:
                self.play(Write(e))
                rendered.append(e)
            if i == 1:
                self.wait(1)
                with self.voiceover(e.get_tex_string()+"2") as trk:
                    pass

        with self.voiceover("Mid") as trk:
            self.wait(8)
            self.play(*[Unwrite(e) for e in rendered])
        
        for e in toc.entries:
            with self.voiceover(e.main.tex_string) as trk:
                self.play(Write(e.main))
            self.wait(1)
            with self.voiceover(e.main.tex_string + "opening") as trk:
                self.play(e.open())
            self.wait(1)
            self.play(e.close())
            self.wait(1)
        self.wait(3)
        self.play(FadeOut(*[o for o in self.mobjects]))