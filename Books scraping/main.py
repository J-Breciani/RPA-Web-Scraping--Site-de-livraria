from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver.common.by import By
import csv
from time import sleep

class Webdriver:
    def __init__(self, browser: str="chrome", headless: bool=False) -> None:
        self.browser = str(browser).lower()
        self.headless = headless

        self.__validar_browser_utilizado()

    def __validar_browser_utilizado(self):
        """Valida o tipo de navegador utilizado"""
        if self.browser != "firefox" and self.browser != "chrome":
            raise Exception("type browser not supported.")
        
    def __configurar_webdriver_firefox(self):
        """Opções para navegador Firefox
        
        Returns:
            FirefoxOptions: Options for Firefox browser
        """
        opts = FirefoxOptions()
        opts.add_argument('--ignore-certificate-errors')
        opts.add_argument("--disable-infobars")
        opts.add_argument("--window-size=1366,768")
        opts.add_argument("--start-maximized")

        if self.headless:
            opts.add_argument('--headless')
            opts.add_argument('--log-level=3')

        return opts

    def __configurar_webdriver_chrome(self):
        """Opções para navegador Chrome
        
        Returns:
            FirefoxOptions: Options for Firefox browser
        """
        opts = ChromeOptions()
        opts.add_argument("--disable-infobars")
        opts.add_argument("--disable-popup-blocking")
        opts.add_argument("--disable-save-password-bubble")
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_argument("--disable-extensions")
        opts.add_argument("--disable-features=DownloadBubble")
        opts.add_argument("--disable-notifications")
        opts.add_argument('--safe-mode')
        opts.add_argument("--log-level=OFF")
        opts.add_argument("--log-level=3")
        opts.add_argument('ignore-certificate-errors')

        opts.add_experimental_option('detach', True)
        opts.add_experimental_option('prefs', {'credentials_enable_service': False})
        opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])

        if self.headless:
            opts.add_argument('--headless=new')
        
        return opts
    
    def criar_webdriver(self):
        """Inicia o webdriver
        
        Returns:
            WebDriver: WebDriver instance
        """
        try:
            if self.browser == 'chrome':
                self.driver = webdriver.Chrome(options=self.__configurar_webdriver_chrome())

            if self.browser == 'firefox':
                self.driver = webdriver.Firefox(options=self.__configurar_webdriver_firefox())

            return self.driver
        
        except WebDriverException as error:
            raise Exception(f"error started webdriver, error: {str(error)}")

        except Exception as error:
            raise Exception(f"error webdriver, error: {str(error)}")
        

if __name__ == '__main__':
    
    # Instanciando o navegador
    webdriver_instance = Webdriver('chrome', headless=False)
    navegador = webdriver_instance.criar_webdriver()
    navegador.get('https://books.toscrape.com/')
    
    
    
    # Abrindo o arquivo csv
    with open("dados.csv", 'w', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(['Título', 'Preço', 'Disponibilidade', 'Avaliação'])  # cabeçalho
        
        while True:
            livros = navegador.find_elements(By.XPATH, '//article[@class ="product_pod"]')
         # Pegando informação para cada livro:
            for livro in livros:
                titulo = livro.find_element(By.XPATH, './/h3/a').get_attribute('title')  # título completo
                preco = livro.find_element(By.XPATH, './/p[@class="price_color"]').text
                disponibilidade = livro.find_element(By.XPATH, './/p[@class="instock availability"]').text
                avaliacao = livro.find_element(By.XPATH, './/p[contains(@class, "star-rating")]').get_attribute('class')  
                avaliacao = avaliacao.split()[-1] # Pega somente a avaliação
            
                #sleep(1)
                escritor.writerow([titulo, preco, disponibilidade, avaliacao])
                
            try:
                next_button = navegador.find_element(By.XPATH, '//li[@class="next"]/a').click()
                #sleep(2)
            except:
                print("Fim das páginas.")
                break
            
    navegador.close()
            