from roll_constant import *


# compétence :
#
# blanc : 4 blanc, 6 succès, 2 spé
# noir : 6 blanc, 4 main, 2 spé
#
#
# combat :
#
# rouge : 2 (1degat), 2 (2 dégats), 2 spé
# jaune : vide,  1degat, 1 (2 dégats), 2 (3 dégats), 1 spé
# bleu : 2 vide , 2 1 shield, 1 2 shield, 1 spé
# noir : 3 vides, 1 2 shield, 1 spé, 1 croix
#
#
# infiltration :
#
# blanc : 3 (1 symbole), 2 (2 symboles), 1 symbole spé, 4 vides
# noir : 3 (1 symbole), 3 (2 symboles), 3 (3 symboles), 1 (symbole spé)

#comp_dice
comp_w = [(0,), (0,), (1,), (1,), (1,), comp_w_spe]
comp_b = [(0,), (0,), (0,), (1,), (1,), comp_b_spe]


# combat effect  (damage, shield remove, blue dice remove, black dice remove)
comb_at_empty = (0, 0, 0, 0)
comb_1d = (1, 0, 0, 0)
comb_2d = (2, 0, 0, 0)
comb_3d = (3, 0, 0, 0)
# deffence effect (shield, cancel)
comb_def_empty = (0, 0)
comb_1s = (1, 0)
comb_2s = (2, 0)
comb_es = (0, 1)


# combat dice
comb_r = [comb_1d, comb_2d, comb_r_spe]
comb_y = [comb_at_empty, comb_1d, comb_2d, comb_3d, comb_3d, comb_y_spe]
comb_blue = [comb_def_empty, comb_def_empty, comb_1s, comb_1s, comb_2s, comb_blue_spe]
comb_black = [comb_def_empty, comb_def_empty, comb_def_empty, comb_2s, comb_es, comb_black_spe]

