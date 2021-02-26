import matplotlib.pyplot as plt
import time
""" predictions about active covid cases, based on reproduction number
    CONTENT:
        1) USER INPUT
        2) GLOBAL VALUES
        3) PROGRAM CORE
        4) RUN PROGRAM
        5) MATPLOTLIB SETTINGS
        """

print(f"ACTIVE COVID CASES PREDICTION\n-----------------------------")
default_r_number = 0.95
default_population = 100

# 1) USER INPUT
def take_reproduction_number():
    """ here we will take user input, set default values and avoid to error """

    global r_number
    r_number = input("Reproduction number: ")
    
    if r_number == "":
        r_number = default_r_number     # if user will fill anything, we will use default value
        print(f"You did not choose R number. Default value is set to: R = {r_number}.\n")

    try:
        r_number = float(r_number)
    except ValueError:
        r_number = default_r_number
        print(f"\t - Error: you did not set a number")
        print(f"\t - R number has been set to: {r_number}\n")
    
    #r_number = float(r_number)
    if r_number > 8:
        r_number = 8
        print(f"\t - Max allowed R number is: {r_number}")
        print(f"\t - R number has been set to: {r_number}\n")

    elif r_number <= 0:
        r_number = default_r_number
        print(f"\t - R number cannot be negative or zero")
        print(f"\t - R number has been set to: {r_number}\n")
take_reproduction_number()

def set_dtp (r_number):
    """ We will take r_number and acording to this number
    we will set days to predict(dtp). Bigger r_num requires lower dtp """

    global dtp
    if r_number <= 1.6:
        dtp = 20
    elif r_number <= 1.9:
        dtp = 15
    elif r_number <= 2.8:
        dtp = 10
    elif r_number <= 8:
        dtp = 5   
set_dtp(r_number)

def take_active_cases_number():
    """here we will take from user active cases and avoid errors
        if user put anything, we will set default vaule """

    global population
    global number_label
    number_label = "thousands"    
    population = input("Active cases (number in thousands): ")
    if population == "":
        population = default_population
        print(f"You did not choose Active cases. Default value is set to: Active cases = {population} {number_label}.\n")

    try:
        population = float(population)
    except ValueError:
        population = default_population
        print(f"\t - Error: you did not set a number")
        print(f"\t - Active cases number has been set to: {population} {number_label}\n")

    if population <= 0:
        population = default_population
        population = int(population)
        print(f"\t - Active cases number cannot be negative or zero")
        print(f"\t - Active cases number has been set to: {population} {number_label}\n")
    
    elif population > 0 and population < 100:
        print(f"\t - Active cases number has been transformed without {number_label}\n")
        if population < 0.001:
            population = 0.001
            print(f"\t - Active cases number cannot be less than 0.001 {number_label}")
            print(f"\t - Active cases number has been set to: 0.001 {number_label} = 1\n")
        population = population * 1_000
        number_label = ""

    elif population >= 100_000:
        population = population / 1_000
        number_label = "milions"
        print(f"\t - Active cases number has been transformed to {number_label}\n")

    population = int(population)
    if population > 150_000:
        population = 150_000
        print(f"\t - Max allowed Active cases number is {population} {number_label} (150 billions)")
        print(f"\t - Active cases number has been set to: {population} {number_label}\n")
take_active_cases_number()

# 2) GLOBAL VALUES
#dtp = 20    # days to predict / prediction horizont
print(f"NEXT {dtp} DAYS:\n")
dtp_label = dtp
ttr = 5     # time to reproduction: how many days will take reproduction 
dtp = dtp / ttr   # Reproduction in covid is based on 5 days of ifectivity; ttr = 5
dtp = int(dtp)
zone_up = +0.1; zone_down = -0.1    #numbers for alternative predictions and zones
       
# 2) PROGRAM CORE
prognosis = [population, ]
prognosis_low = []; r_low = r_number + zone_down
prognosis_high = []; r_high = r_number + zone_up

def count_reproduction (r_number, population):
    """this function makes prognosis to dtp days
    just input R number and active cases"""
    
    for n in range (0, dtp):
        population = r_number * population
        population = round(population)
        prognosis.append(population)
        #print(population)
        
      # p = prognosis[-2] + ((prognosis[-1] - prognosis[-2]) /2 )
      # p = round(p)
      # prognosis.insert(-1, p)

def alter_count():
    """ here we will count alternative scenario
    lower and higher prognosis """
    for n in range (dtp):
        x = prognosis_low[-1] * r_low
        y = prognosis_high[-1] * r_high
        x = round(x); y = round(y)
        prognosis_low.append(x)
        prognosis_high.append(y)

      # p_h = prognosis_high[-2] + ((prognosis_high[-1] - prognosis_high[-2]) /2 )
      # p_h = round(p_h)
      # prognosis_high.insert(-1, p_h)
      # p_l = prognosis_low[-2] + ((prognosis_low[-1] - prognosis_low[-2]) /2 )
      # p_l = round(p_l)
      # prognosis_low.insert(-1, p_l)

def set_key_days(dtp_label):
    """ this function will set key days for the plot """

    for x in range(0, dtp_label + 1, 5):
        days.append(x)
        #if x > 0:
            #z = days[-2] + ((days[-1] - days[-2]) /2 )
            #days.insert(-1, z)

# 3) RUN PROGRAM
today_date = time.strftime("%d/%m/%Y")
count_reproduction(r_number, population) 
prognosis_low.append(prognosis[0])
prognosis_high.append(prognosis[0])
alter_count()
days = []
set_key_days(dtp_label)
print(f"KEY DAYS: {days}")
print(f"LOWER PROGNOSIS: {prognosis_low}")
print(f"MAIN PROGNOSIS: {prognosis} --- {number_label.upper()}")
print(f"HIGHER PROGNOSIS: {prognosis_high}")
print(f"\nTODAY: {today_date}")
print(f" - Today date is set to 0 (zero) in the plot")

# 4) MATPLOTLIB SETTINGS
#days = list(range(0, dtp_label + 1, 5)) # list of the days
plt.style.use("seaborn") # style of the plot
fig, ax = plt.subplots()
ax.plot(days, prognosis, linewidth = 5, label = (f"R {r_number} (mid)")) #1st line
plt.plot(days, prognosis_low, linestyle = "dashed", label = (f"R {r_low} (lower)")) #2nd line
plt.plot(days, prognosis_high,linestyle = "dashed", label = (f"R {r_high} (higher)")) #3rd line
ax.set_title(f"{dtp_label} DAYS PREDICTION from {today_date}\nR number: {r_number}; Today Active cases: {prognosis[0]} {number_label}", fontsize = 15)
ax.set_xlabel(f"{dtp_label} Days", fontsize = 15)
ax.set_ylabel("Active Cases", fontsize = 15)

ax.tick_params(axis="both", labelsize = 15)

plt.legend() #show legend on the plot
plt.show() #display plot

