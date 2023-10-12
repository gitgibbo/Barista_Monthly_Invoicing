DC7_HIRE_CHARGE_MATRIX = {
    (0, 15): 2.25,
    (15, 30): 1.26,
    (30, 50): 0.86,
    (50, 80): 0.62,
    (80, float('inf')): 0.55,
}

EXPRESSO_PLUS_HIRE_CHARGE_MATRIX = {
    (0, 20): 1.26,
    (20, 25): 0.98,
    (25, 30): 0.90,
    (30, 40): 0.86,
    (40, 50): 0.75,
    (50, 60): 0.62,
    (60, 70): 0.60,
    (70, float('inf')): 0.58,
}

wastage_per_month = 30
EP_minimum_hire_charge = 0
DC7_minimum_hire_charge = 347.50

#soul_conditions = (grouped_data['RecipeName'] == 'Splash of milk [S]') | (grouped_data['Canceled'] == 'canceled')
#pro_conditions = (data['local_code_description'].isin(['SPLASH OF MILK', 'ESPRESSO SHOT', 'SYRUP SHOT']))