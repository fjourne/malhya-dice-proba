import PySimpleGUI as sg

from proba import *

width = 800
height = 500
fight_graph = sg.Graph(
    canvas_size=(width, height),
    graph_bottom_left=(0, 0),
    graph_top_right=(width, height),
    background_color="white",
    key="-GRAPH-"
)

skill_graph = sg.Graph(
    canvas_size=(width, height),
    graph_bottom_left=(0, 0),
    graph_top_right=(width, height),
    background_color="white",
    key="-GRAPH-"
)

fight_layout = [
    [sg.Text("Fight roll"), sg.Button("Skill roll")],
    [
        sg.Image("../resources/icons/damage.png"), sg.Input(default_text="0", key="flat_d", size=4, enable_events=True),
        sg.Image("../resources/icons/shield_reduction.png"),
        sg.Input(default_text="0", key="flat_sr", size=4, enable_events=True),
        sg.Image("../resources/icons/blue_dice_reduction.png"),
        sg.Input(default_text="0", key="flat_blue_dr", size=4, enable_events=True),
        sg.Image("../resources/icons/black_dice_reduction.png"),
        sg.Input(default_text="0", key="flat_black_dr", size=4, enable_events=True)
    ],
    [
        sg.Image("../resources/icons/red_dice.png"), sg.Input(default_text="1", key="dR", size=4, enable_events=True),
        sg.Image("../resources/icons/red_special.png"), sg.Text(":"),
        sg.Image("../resources/icons/damage.png"), sg.Input(default_text="0", key="s_r_d", size=4, enable_events=True),
        sg.Image("../resources/icons/shield_reduction.png"),
        sg.Input(default_text="0", key="s_r_sr", size=4, enable_events=True),
        sg.Image("../resources/icons/blue_dice_reduction.png"),
        sg.Input(default_text="0", key="s_r_blue_dr", size=4, enable_events=True),
        sg.Image("../resources/icons/black_dice_reduction.png"),
        sg.Input(default_text="0", key="s_r_black_dr", size=4, enable_events=True)

    ],
    [
        sg.Image("../resources/icons/yellow_dice.png"),
        sg.Input(default_text="0", key="dJ", size=4, enable_events=True),
        sg.Image("../resources/icons/yellow_special.png"), sg.Text(":"),
        sg.Image("../resources/icons/damage.png"), sg.Input(default_text="0", key="s_y_d", size=4, enable_events=True),
        sg.Image("../resources/icons/shield_reduction.png"),
        sg.Input(default_text="0", key="s_y_sr", size=4, enable_events=True),
        sg.Image("../resources/icons/blue_dice_reduction.png"),
        sg.Input(default_text="0", key="s_y_blue_dr", size=4, enable_events=True),
        sg.Image("../resources/icons/black_dice_reduction.png"),
        sg.Input(default_text="0", key="s_y_black_dr", size=4, enable_events=True)
    ],
    [
        sg.Image("../resources/icons/blue_dice.png"), sg.Input(default_text="0", key="dB", size=4, enable_events=True),
        sg.Image("../resources/icons/blue_special.png"), sg.Text(":"),
        sg.Image("../resources/icons/shield.png"),
        sg.Input(default_text="0", key="s_blue_s", size=4, enable_events=True),
        sg.Image("../resources/icons/cancel.png"), sg.Input(default_text="0", key="s_blue_c", size=4, enable_events=True),
    ],
    [
        sg.Image("../resources/icons/black_dice.png"), sg.Input(default_text="0", key="dN", size=4, enable_events=True),
        sg.Image("../resources/icons/black_special.png"), sg.Text(":"),
        sg.Image("../resources/icons/shield.png"),
        sg.Input(default_text="0", key="s_black_s", size=4, enable_events=True),
        sg.Image("../resources/icons/cancel.png"), sg.Input(default_text="0", key="s_black_c", size=4, enable_events=True),
    ],
    [sg.Checkbox('at least', key="at_least_fight", enable_events=True, default=True)],
    [fight_graph]
]

skill_layout = [
    [sg.Text("Skill roll"), sg.Button("Fight roll")],
    [
        sg.Text("Fail at: "), sg.Input(default_text="2", key="sFA", size=4, enable_events=True),
        sg.Text("Stop at: "), sg.Input(default_text="2", key="sSA", size=4, enable_events=True),
        sg.Text("Margin :"), sg.Input(default_text="0", key="sM", size=4, enable_events=True)
    ],
    [
        sg.Image("../resources/icons/skill_white_dice.png"), sg.Input(default_text="2", key="s_d_w", size=4, enable_events=True),
        sg.Image("../resources/icons/skill_white_special.png"), sg.Text(": "), sg.Image("../resources/icons/skill_success.png"), sg.Input(default_text="0", key="s_s_w", size=4, enable_events=True),
    ],
    [
        sg.Image("../resources/icons/skill_black_dice.png"), sg.Input(default_text="2", key="s_d_b", size=4, enable_events=True),
        sg.Image("../resources/icons/skill_black_special.png"), sg.Text(": "), sg.Image("../resources/icons/skill_failure.png"), sg.Input(default_text="0", key="s_s_b", size=4, enable_events=True),
    ],
    [sg.Checkbox('at least', key="at_least_skill", enable_events=True, default=True)],
    [skill_graph]
]

layout = [[sg.Column(fight_layout, key="fight"), sg.Column(skill_layout, key="skill", visible=False)]]

# Create the window
window = sg.Window("Malhya Dice Stat", layout)


def draw_graph(graph, proba, at_least: bool):
    graph.erase()

    tmp = {}
    cummul = 0
    average = 0
    for value, p in proba.items():
        if p > 0.0001:
            tmp[value] = (1 - cummul) if at_least else p
            cummul += p
            average += value*p
    proba = tmp

    margin_left = 60
    margin_right = 60
    margin_top = 20
    margin_bottom = 20
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom
    nb_bars = len(proba)
    bar_height = chart_height / nb_bars * 0.6
    spacing = chart_height / nb_bars
    # ---------------------------------------------------------
    # Dessin des barres
    # ---------------------------------------------------------
    max_value = max(proba.values())
    graph.draw_text(
        f"Average: {average:.2f}",
        (60, height - margin_top),
        color="black"
    )
    for i, (value, probability) in enumerate(proba.items()):
        # Position verticale
        y = height - margin_top - (i + 0.5) * spacing

        # Longueur de la barre
        bar_width = (
                            probability / max_value
                    ) * chart_width

        # Texte de la valeur
        graph.draw_text(
            str(value),
            (margin_left - 30, y),
            color="black"
        )

        # Barre
        graph.draw_rectangle(
            (margin_left, y - bar_height / 2),
            (margin_left + bar_width, y + bar_height / 2),
            fill_color="#4A90E2",
            line_color="#357ABD"
        )

        # Pourcentage
        graph.draw_text(
            f"{probability * 100:.2f}%",
            (margin_left + bar_width + 30, y),
            color="black"
        )


init = False
is_combat_visible = True
is_skill_visible = False
# Create an event loop
while True:
    event, values = window.read(timeout=0 if not init else None)
    if event == "Skill roll":
        is_skill_visible = True
        is_combat_visible = False
        window["fight"].update(visible=False)
        window["skill"].update(visible=True)
    if event == "Fight roll":
        is_skill_visible = False
        is_combat_visible = True
        window["fight"].update(visible=True)
        window["skill"].update(visible=False)

    init = True
    if is_skill_visible:
        at_least_skill = bool(values["at_least_skill"])
        skill_nb_w = 0 if values["s_d_w"] == '' else int(values["s_d_w"])
        skill_s_w = 0 if values["s_s_w"] == '' else int(values["s_s_w"])
        skill_nb_b = 0 if values["s_d_b"] == '' else int(values["s_d_b"])
        skill_s_b = 0 if values["s_s_b"] == '' else int(values["s_s_b"])
        skill_fail_at = 0 if values["sFA"] == '' else int(values["sFA"])
        skill_stop_at = 0 if values["sSA"] == '' else int(values["sSA"])
        skill_margin = 0 if values["sM"] == '' else int(values["sM"])
        # skill effect success / fail

        skill_max_roll = 25

        skill_roll = roll_skill(skill_nb_w, d_skill_w(skill_s_w),
                                skill_nb_b, d_skill_b(skill_s_b),
                                skill_max_roll,
                                skill_margin,
                                skill_fail_at,
                                skill_stop_at)

        draw_graph(skill_graph, skill_roll, at_least_skill)

    if is_combat_visible:
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
        at_least_fight = bool(values["at_least_fight"])
        # attack effect   (damage, shield remove, blue dice remove, black dice remove)
        fight_flat = (flat_d, flat_sr, flat_blue_dr, flat_black_dr)
        fight_r_spe = (s_r_d, s_r_sr, s_r_blue_dr, s_r_black_dr)
        fight_y_spe = (s_y_d, s_y_sr, s_y_blue_dr, s_y_black_dr)
        # defence effect (shield, cancel)
        fight_blue_spe = (s_blue_s, s_blue_c)
        fight_black_spe = (s_black_s, s_black_c)

        fight_roll = roll_fight(fight_flat,
                                fight_nb_r, d_fight_r(fight_r_spe),
                                fight_nb_y, d_fight_y(fight_y_spe),
                                fight_nb_blue, d_fight_blue(fight_blue_spe),
                                fight_nb_black, d_fight_black(fight_black_spe))

        draw_graph(fight_graph, fight_roll, at_least_fight)

    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break

window.close()
