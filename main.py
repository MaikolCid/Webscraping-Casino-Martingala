from selenium import webdriver # Abrir e interactuar con Chrome
from selenium.common.exceptions import NoSuchElementException
import time
import config


# conectarse
def login():
    # Coger información de la página web
    website = 'https://play.mansioncasino.es/'
    websiteslingshot = 'https://cachedownload.mansioncasino.es/live/html5/desktop/bundles/23.1.0.52/?lang=es&game=rol&connection=desktop&gamephysicalnetworkId=-1&protocol=Live2&preferredSeat=undefined&preferedmode=real&mode=real&sessionTimer=null&redirect_time=1675881083219&launch_alias=direct_launch_100381&backUrl=https%3A%2F%2Fcachedownload.mansioncasino.es%2Flive%2Fhtml5%2Fdesktop%2F%3Flang%3Des%26game%3Drol%26connection%3Ddesktop%26gametableid%3D100381%26physicalTableId%3D-1%26networkId%3D-1%26protocol%3DLive2%26preferredSeat%3Dundefined%26preferedmode%3Dreal%26mode%3Dreal%26sessionTimer%3Dnull#/'
    time.sleep(.5)
    #driver = webdriver.Chrome('/Users/cidec/Documents/CASINO/chromedriver')

    # Interactuar con la web
    driver.get(website)
    time.sleep(2)

    # localizar un botón
    login1 = driver.find_element_by_class_name("btn_action_login")
    # dar click en un botón
    login1.click()

    # Introducir texto
    usuario = driver.find_element_by_name("userName")
    usuario.send_keys(config.username)
    passoword = driver.find_element_by_name("password")
    passoword.send_keys(config.password)

    # localizar un botón
    login2 = driver.find_element_by_class_name("btn_action_login")
    # dar click en un botón
    login2.click()

    time.sleep(2)

    # localizar un botón
    accept1 = driver.find_element_by_class_name("popup-modal__button")
    # dar click en un botón
    accept1.click()

    # localizar un botón
    #juegosdirecto = driver.find_element_by_class_name("gamesinfo__game-category-Juegos-en-Directo")
    # dar click en un botón
    #juegosdirecto.click()

    driver.get(websiteslingshot)

    time.sleep(8)
    # Historial de las 500 partidas
    otros = driver.find_element_by_xpath('//li[@data-automation-locator="button.extenededHistory"]')
    otros.click()
    return

# genera vector historial y guarda número de repeticiones
def analisis(color, historial, repeticiones, primeraTirada):
    historial.insert(0,color)
    if not primeraTirada:
        if historial[1] == color:
            repeticiones = repeticiones + 1
        elif historial[1] == "verde":
            repeticiones = repeticiones + 1
        else:
            repeticiones = 0
    else:
        repeticiones = 0
    return historial, repeticiones

# realiza la apuesta que corresponda
def apuesta(casColor, moneda1, moneda5, moneda10, moneda25, moneda100, clickMon1, clickMon5, clickMon10, clickMon25, clickMon100):
    if moneda1:
        clickMon1.click()
        for h in range(moneda1):
            casColor.click()
            time.sleep(0.2)
    elif moneda5:
        clickMon5.click()
        print('clickMon5')
        for i in range(moneda5):
            casColor.click()
            time.sleep(0.2)
    elif moneda10:
        clickMon10.click()
        for j in range(moneda10):
            casColor.click()
            time.sleep(0.2)
    elif moneda25:
        clickMon25.click()
        for k in range(moneda25):
            casColor.click()
            time.sleep(0.2)
    elif moneda100:
        clickMon100.click()
        for l in range(moneda100):
            casColor.click()
            time.sleep(0.2)
    return

# Matriz de apuestas : se empieza con un euro, desde 4 colores seguidos hasta los 9 seguidos !
# aplica el método Martingala
matApuesta = [[3,1,0,0,0,0],[4,2,0,0,0,0],[5,4,0,0,0,0],[6,3,1,0,0,0],[7,1,1,1,0,0],[8,2,1,0,1,0],[12,0,0,0,0,0]]

# Casillas y colores
numrojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
numnegros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
numverde = [0]


driver = webdriver.Chrome('/Users/cidec/Documents/CASINO/chromedriver')
login()
primeraTirada = True
historial = []
total = 0
repeticiones = 0
primeraLectura = True

while True:
    # si has sido desconectado => reconéctate
    try: 
        disconnect = driver.find_element_by_xpath('//div[@class="default-modal-html--erlyV"]').text
        if disconnect == 'You have been disconnected from the casino server due to a long period of inactivity.':
            login()
            historial.insert(0,"RESET")
            pass
    except NoSuchElementException:
        pass
    
    try:
        # si sale la ventana pop-up con último resultado
        ventana = driver.find_element_by_class_name("roulette-round-result-position__text")
        while ventana and primeraLectura:
            primeraLectura = False
            time.sleep(1)
            # extrae el último resultado
            resultado = driver.find_element_by_xpath('//div[@data-automation-locator="field.lastHistoryItem"]').text 
            total = total +1
            # actualiza le vector con el historial y la variable con las repeticiones en función del último resultado
            if int(resultado) in numrojos:
                historial, repeticiones= analisis("rojo", historial, repeticiones, primeraTirada)
            elif int(resultado) in numnegros:
                historial, repeticiones= analisis("negro", historial, repeticiones, primeraTirada)
            elif int(resultado) in numverde:
                historial, repeticiones= analisis("verde", historial, repeticiones, primeraTirada)

            print("Resultado: ", resultado, "; Repeticiones: ", repeticiones, "; Historial: ", historial, "; Total: ", total)
            
            # empiezo a apostar tras obtener 7 veces el mismo color y paro si sale 11 veces el mismo color
            # calculo de valor de la apuesta según número de repeticiones
            if repeticiones > 5 and repeticiones < 11:
                n= repeticiones-6
                moneda1 = matApuesta[n][1]
                print(moneda1)
                moneda5= matApuesta[n][2]
                print(moneda5)
                moneda10 = matApuesta[n][3]
                print(moneda10)
                moneda25 = matApuesta[n][4]
                moneda100 = matApuesta[n][5]

                # determinar posición de los distintos elementos para hacer luego el/los click(s)
                clickMon1 = driver.find_element_by_css_selector('#root > div > div.app-container > div.games-slots--KaBtH > div > div.game-node--vmAr9 > div > div > div.game-table > div.game-table__controls-panel > div > div.controls-panel__chip-panel > div > div > div.arrow-slider__container > div > svg:nth-child(2)')
                clickMon5 = driver.find_element_by_css_selector('#root > div > div.app-container > div.games-slots--KaBtH > div > div.game-node--vmAr9 > div > div > div.game-table > div.game-table__controls-panel > div > div.controls-panel__chip-panel > div > div > div.arrow-slider__container > div > svg:nth-child(3)')
                clickMon10 = driver.find_element_by_css_selector('#root > div > div.app-container > div.games-slots--KaBtH > div > div.game-node--vmAr9 > div > div > div.game-table > div.game-table__controls-panel > div > div.controls-panel__chip-panel > div > div > div.arrow-slider__container > div > svg:nth-child(4)')
                clickMon25 = driver.find_element_by_css_selector('#root > div > div.app-container > div.games-slots--KaBtH > div > div.game-node--vmAr9 > div > div > div.game-table > div.game-table__controls-panel > div > div.controls-panel__chip-panel > div > div > div.arrow-slider__container > div > svg:nth-child(5)')
                clickMon100 = driver.find_element_by_css_selector('#root > div > div.app-container > div.games-slots--KaBtH > div > div.game-node--vmAr9 > div > div > div.game-table > div.game-table__controls-panel > div > div.controls-panel__chip-panel > div > div > div.arrow-slider__container > div > svg:nth-child(6)')
                casRojo = driver.find_element_by_css_selector('#root > div > div.app-container > div.games-slots--KaBtH > div > div.game-node--vmAr9 > div > div > div.game-table > div.game-table__game-specific > div > div.roulette-game-area__row > div.roulette-game-area__col.roulette-game-area__col_left > div.roulette-game-area__main-table-wrapper > div > div > svg > g > g.roulette-table-cell.roulette-table-cell_side-red.roulette-table-cell_group-fifty-fifty')
                casNegro = driver.find_element_by_css_selector('#root > div > div.app-container > div.games-slots--KaBtH > div > div.game-node--vmAr9 > div > div > div.game-table > div.game-table__game-specific > div > div.roulette-game-area__row > div.roulette-game-area__col.roulette-game-area__col_left > div.roulette-game-area__main-table-wrapper > div > div > svg > g > g.roulette-table-cell.roulette-table-cell_side-black.roulette-table-cell_group-fifty-fifty')
                
                # apuesto al color que toque y en la cantidad que toque
                if historial[1] != "rojo":
                    apuesta(casRojo, moneda1, moneda5, moneda10, moneda25, moneda100, clickMon1, clickMon5, clickMon10, clickMon25, clickMon100)
                    f= open("ruleta.txt","a")
                    f.write("rojo, ")
                    f.close()
                elif historial[1] != "negro":
                    apuesta(casNegro, moneda1, moneda5, moneda10, moneda25, moneda100, clickMon1, clickMon5, clickMon10, clickMon25, clickMon100)
                    f= open("ruleta.txt","a")
                    f.write("negro, ")
                    f.close()
                # escribir

            primeraTirada = False

            if total == 100:
                primeraTirada = True
                historial = []
                total = 0
                repeticiones = 0
                primeraLectura = True
            break
        
    except NoSuchElementException:
        primeraLectura = True
        time.sleep(0.5)



##################FICHAS##################
#data-automation-locator="chipsPanel.chip50" = 0.5€
#data-automation-locator="chipsPanel.chip100" = 1€
#data-automation-locator="chipsPanel.chip500" = 5€
#data-automation-locator="chipsPanel.chip1000" = 10€
#data-automation-locator="chipsPanel.chip2500" = 25€

## CASILLAS
#data-automation-locator="betPlace.spots50x50-black" = NEGRO
#data-automation-locator="betPlace.spots50x50-red" = ROJO

# Disconnection
#driver.find_element_by_class_name("default-modal-html--erlyV") = 'You have been disconnected from the casino server due to a long period of inactivity.'