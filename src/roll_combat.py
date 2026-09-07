from proba import Proba

proba = Proba()

# FIGHT
fight_flat = (0, 0, 0, 0)
fight_nb_r = 5
fight_nb_y = 0
fight_nb_blue = 1
fight_nb_black = 1
# attack effect   (damage, shield remove, blue dice remove, black dice remove)
fight_r_spe = (1, 0, 0, 0)
fight_y_spe = (4, 0, 0, 0)
# defence effect (shield, cancel)
fight_blue_spe = (0, 0)
fight_black_spe = (0, 0)

fight_roll = proba.roll_fight(fight_flat,
                              fight_nb_r, proba.d_fight_r(fight_r_spe),
                              fight_nb_y, proba.d_fight_y(fight_y_spe),
                              fight_nb_blue, proba.d_fight_blue(fight_blue_spe),
                              fight_nb_black, proba.d_fight_black(fight_black_spe))

print("Fight average : {}".format(proba.compute_average(fight_roll)))
print(proba.display_at_least(fight_roll))
print(proba.display_proba(fight_roll))
