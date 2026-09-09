import PySimpleGUI as sg

from proba import Proba

version = "0.3-SNAPSHOT"


class MainWindow:

    p_comput = Proba()
    init = False
    is_combat_visible = True
    is_skill_visible = False
    default_graph_width = 800
    default_graph_heigth = 500
    background_color = "#404040"
    background_color_graph = "#C0C0C0"
    graph_bar_color = "#1660AA"

    graph = sg.Graph(
        canvas_size=(default_graph_width, default_graph_heigth),
        graph_bottom_left=(0, 0),
        graph_top_right=(default_graph_width, default_graph_heigth),
        expand_x=True,
        expand_y=True,
        background_color=background_color_graph,
        key="-GRAPH-"
    )

    fight_layout = [
        [sg.Text("Fight roll", background_color=background_color), sg.Button("Skill roll")],
        [
            sg.Image("../resources/icons/damage.png", background_color=background_color),
            sg.Input(default_text="0", key="flat_d", size=4, enable_events=True),
            sg.Image("../resources/icons/shield_reduction.png", background_color=background_color),
            sg.Input(default_text="0", key="flat_sr", size=4, enable_events=True),
            sg.Image("../resources/icons/blue_dice_reduction.png", background_color=background_color),
            sg.Input(default_text="0", key="flat_blue_dr", size=4, enable_events=True),
            sg.Image("../resources/icons/black_dice_reduction.png", background_color=background_color),
            sg.Input(default_text="0", key="flat_black_dr", size=4, enable_events=True)
        ],
        [
            sg.Image("../resources/icons/red_dice.png", background_color=background_color),
            sg.Input(default_text="1", key="dR", size=4, enable_events=True),
            sg.Image("../resources/icons/red_special.png"), sg.Text(":", background_color=background_color),
            sg.Image("../resources/icons/damage.png", background_color=background_color),
            sg.Input(default_text="0", key="s_r_d", size=4, enable_events=True),
            sg.Image("../resources/icons/shield_reduction.png", background_color=background_color),
            sg.Input(default_text="0", key="s_r_sr", size=4, enable_events=True),
            sg.Image("../resources/icons/blue_dice_reduction.png", background_color=background_color),
            sg.Input(default_text="0", key="s_r_blue_dr", size=4, enable_events=True),
            sg.Image("../resources/icons/black_dice_reduction.png", background_color=background_color),
            sg.Input(default_text="0", key="s_r_black_dr", size=4, enable_events=True)

        ],
        [
            sg.Image("../resources/icons/yellow_dice.png", background_color=background_color),
            sg.Input(default_text="0", key="dJ", size=4, enable_events=True),
            sg.Image("../resources/icons/yellow_special.png"), sg.Text(":", background_color=background_color),
            sg.Image("../resources/icons/damage.png", background_color=background_color),
            sg.Input(default_text="0", key="s_y_d", size=4, enable_events=True),
            sg.Image("../resources/icons/shield_reduction.png", background_color=background_color),
            sg.Input(default_text="0", key="s_y_sr", size=4, enable_events=True),
            sg.Image("../resources/icons/blue_dice_reduction.png", background_color=background_color),
            sg.Input(default_text="0", key="s_y_blue_dr", size=4, enable_events=True),
            sg.Image("../resources/icons/black_dice_reduction.png", background_color=background_color),
            sg.Input(default_text="0", key="s_y_black_dr", size=4, enable_events=True)
        ],
        [
            sg.Image("../resources/icons/blue_dice.png", background_color=background_color),
            sg.Input(default_text="0", key="dB", size=4, enable_events=True),
            sg.Image("../resources/icons/blue_special.png"), sg.Text(":", background_color=background_color),
            sg.Image("../resources/icons/shield.png", background_color=background_color),
            sg.Input(default_text="0", key="s_blue_s", size=4, enable_events=True),
            sg.Image("../resources/icons/cancel.png", background_color=background_color),
            sg.Input(default_text="0", key="s_blue_c", size=4, enable_events=True),
        ],
        [
            sg.Image("../resources/icons/black_dice.png", background_color=background_color),
            sg.Input(default_text="0", key="dN", size=4, enable_events=True),
            sg.Image("../resources/icons/black_special.png"), sg.Text(":", background_color=background_color),
            sg.Image("../resources/icons/shield.png", background_color=background_color),
            sg.Input(default_text="0", key="s_black_s", size=4, enable_events=True),
            sg.Image("../resources/icons/cancel.png", background_color=background_color),
            sg.Input(default_text="0", key="s_black_c", size=4, enable_events=True),
        ],
    ]

    skill_layout = [
        [sg.Text("Skill roll", background_color=background_color), sg.Button("Fight roll")],
        [
            sg.Text("Fail at:", background_color=background_color), sg.Input(default_text="2", key="sFA", size=4, enable_events=True),sg.Image("../resources/icons/skill_failure.png", background_color=background_color),
        ],
        [
            sg.Text("Continue under:", background_color=background_color),sg.Input(default_text="1", key="sCU", size=4, enable_events=True),sg.Image("../resources/icons/skill_success.png", background_color=background_color),
            sg.Text("  Stop at:", background_color=background_color), sg.Input(default_text="2", key="sSA", size=4, enable_events=True),sg.Image("../resources/icons/skill_success.png", background_color=background_color),
            sg.Text("  Margin :", background_color=background_color), sg.Input(default_text="1", key="sM", size=4, enable_events=True), sg.Image("../resources/icons/skill_failure.png", background_color=background_color)
        ],
        [
            sg.Image("../resources/icons/skill_white_dice.png", background_color=background_color),
            sg.Input(default_text="2", key="s_d_w", size=4, enable_events=True),
            sg.Image("../resources/icons/skill_white_special.png", background_color=background_color), sg.Text(": ", background_color=background_color),
            sg.Image("../resources/icons/skill_success.png", background_color=background_color),
            sg.Input(default_text="0", key="s_s_w", size=4, enable_events=True),
        ],
        [
            sg.Image("../resources/icons/skill_black_dice.png", background_color=background_color),
            sg.Input(default_text="2", key="s_d_b", size=4, enable_events=True),
            sg.Image("../resources/icons/skill_black_special.png", background_color=background_color), sg.Text(": ", background_color=background_color),
            sg.Image("../resources/icons/skill_failure.png", background_color=background_color),
            sg.Input(default_text="0", key="s_s_b", size=4, enable_events=True),
        ],
    ]

    layout = [
        [sg.Column(fight_layout, key="fight", background_color=background_color), sg.Column(skill_layout, key="skill", visible=False, background_color=background_color)],
        [sg.Checkbox('at least', key="at_least", enable_events=True, default=True, background_color=background_color)],
        [graph]
    ]

    # Create the window
    window = sg.Window(f"Malhya Dice Stat  v{version}", layout,
                       icon='../resources/icons/aura.ico',
                       resizable=True,
                       background_color=background_color,
                       button_color="#292929",
                       finalize=True
                       )
    sg.theme_background_color("#6a6a6a")
    window.bind('<Configure>', "window")

    def draw_graph(self, proba, at_least: bool):
        self.graph.erase()

        tmp = {}
        cummul = 0
        average = 0
        for value, p in proba.items():
            if p > 0.0001:
                tmp[value] = (1 - cummul) if at_least else p
                cummul += p
                average += value * p
        proba = tmp

        g_width, g_height = self.graph.get_size()
        drift = g_height - 500

        margin_left = 60
        margin_right = 60
        margin_top = 60
        margin_bottom = 20
        chart_g_width = g_width - margin_left - margin_right
        chart_g_height = g_height - margin_top - margin_bottom
        nb_bars = max(len(proba), 8)
        bar_g_height = chart_g_height / nb_bars * 0.6
        spacing = chart_g_height / nb_bars
        # ---------------------------------------------------------
        # Dessin des barres
        # ---------------------------------------------------------
        max_value = max(proba.values())
        self.graph.draw_text(
            f"Average: {average:.2f}",
            (60, g_height - 20 - drift),
            color="black"
        )

        for i, (value, probability) in enumerate(proba.items()):
            # Position verticale
            y = g_height - margin_top - (i + 0.5) * spacing - drift

            # Longueur de la barre
            bar_g_width = (probability / max_value) * chart_g_width

            # Texte de la valeur
            self.graph.draw_text(
                str(value),
                (margin_left - 30, y),
                color="black"
            )

            # Barre
            self.graph.draw_rectangle(
                (margin_left, y - bar_g_height / 2),
                (margin_left + bar_g_width, y + bar_g_height / 2),
                fill_color=self.graph_bar_color,
                line_color="black"
            )

            # Pourcentage
            self.graph.draw_text(
                f"{probability * 100:.2f}%",
                (margin_left + bar_g_width + 30, y),
                color="black"
            )

    def compute_skill_roll(self, val: dict) -> dict[int, float]:
        skill_nb_w = 0 if val["s_d_w"] == '' else int(val["s_d_w"])
        skill_s_w = 0 if val["s_s_w"] == '' else int(val["s_s_w"])
        skill_nb_b = 0 if val["s_d_b"] == '' else int(val["s_d_b"])
        skill_s_b = 0 if val["s_s_b"] == '' else int(val["s_s_b"])
        skill_fail_at = 0 if val["sFA"] == '' else int(val["sFA"])
        skill_continue_under = 0 if val["sCU"] == '' else int(val["sCU"])
        skill_stop_at = 0 if val["sSA"] == '' else int(val["sSA"])
        skill_margin = 0 if val["sM"] == '' else int(val["sM"])
        # skill effect success / fail
        skill_max_roll = 25
        return self.p_comput.roll_skill(skill_nb_w, self.p_comput.d_skill_w(skill_s_w),
                                        skill_nb_b, self.p_comput.d_skill_b(skill_s_b),
                                        skill_max_roll,
                                        skill_margin,
                                        skill_fail_at,
                                        skill_continue_under,
                                        skill_stop_at)

    def compute_fight_roll(self, values: dict) -> dict[int, float]:
        flat_d = 0 if values["flat_d"] == '' else int(values["flat_d"])
        flat_sr = 0 if values["flat_sr"] == '' else int(values["flat_sr"])
        flat_blue_dr = 0 if values["flat_blue_dr"] == '' else int(values["flat_blue_dr"])
        flat_black_dr = 0 if values["flat_black_dr"] == '' else int(values["flat_black_dr"])
        fight_nb_r = 0 if values["dR"] == '' else int(values["dR"])
        fight_nb_y = 0 if values["dJ"] == '' else int(values["dJ"])
        fight_nb_blue = 0 if values["dB"] == '' else int(values["dB"])
        fight_nb_black = 0 if values["dN"] == '' else int(values["dN"])

        s_r_d = 0 if values["s_r_d"] == '' else int(values["s_r_d"])
        s_r_sr = 0 if values["s_r_sr"] == '' else int(values["s_r_sr"])
        s_r_blue_dr = 0 if values["s_r_blue_dr"] == '' else int(values["s_r_blue_dr"])
        s_r_black_dr = 0 if values["s_r_black_dr"] == '' else int(values["s_r_black_dr"])
        s_y_d = 0 if values["s_y_d"] == '' else int(values["s_y_d"])
        s_y_sr = 0 if values["s_y_sr"] == '' else int(values["s_y_sr"])
        s_y_blue_dr = 0 if values["s_y_blue_dr"] == '' else int(values["s_y_blue_dr"])
        s_y_black_dr = 0 if values["s_y_black_dr"] == '' else int(values["s_y_black_dr"])

        s_blue_s = 0 if values["s_blue_s"] == '' else int(values["s_blue_s"])
        s_blue_c = 0 if values["s_blue_c"] == '' else int(values["s_blue_c"])

        s_black_s = 0 if values["s_black_s"] == '' else int(values["s_black_s"])
        s_black_c = 0 if values["s_black_c"] == '' else int(values["s_black_c"])

        # FIGHT

        # attack effect   (damage, shield remove, blue dice remove, black dice remove)
        fight_flat = (flat_d, flat_sr, flat_blue_dr, flat_black_dr)
        fight_r_spe = (s_r_d, s_r_sr, s_r_blue_dr, s_r_black_dr)
        fight_y_spe = (s_y_d, s_y_sr, s_y_blue_dr, s_y_black_dr)
        # defence effect (shield, cancel)
        fight_blue_spe = (s_blue_s, s_blue_c)
        fight_black_spe = (s_black_s, s_black_c)

        return self.p_comput.roll_fight(fight_flat,
                                        fight_nb_r, self.p_comput.d_fight_r(fight_r_spe),
                                        fight_nb_y, self.p_comput.d_fight_y(fight_y_spe),
                                        fight_nb_blue, self.p_comput.d_fight_blue(fight_blue_spe),
                                        fight_nb_black, self.p_comput.d_fight_black(fight_black_spe))

    def start(self):
        while True:
            event, values = self.window.read(timeout=0 if not self.init else None)
            if not self.init:
                self.init = True

            if event == sg.WIN_CLOSED:
                break
            if event == "Skill roll":
                self.is_skill_visible = True
                self.is_combat_visible = False
                self.window["fight"].update(visible=False)
                self.window["skill"].update(visible=True)
            if event == "Fight roll":
                self.is_skill_visible = False
                self.is_combat_visible = True
                self.window["fight"].update(visible=True)
                self.window["skill"].update(visible=False)

            if self.is_skill_visible:
                at_least_skill = bool(values["at_least"])
                skill_roll = self.compute_skill_roll(values)
                self.draw_graph(skill_roll, at_least_skill)

            if self.is_combat_visible:
                fight_roll = self.compute_fight_roll(values)
                at_least_fight = bool(values["at_least"])
                self.draw_graph(fight_roll, at_least_fight)
        self.window.close()


window = MainWindow()
window.start()
