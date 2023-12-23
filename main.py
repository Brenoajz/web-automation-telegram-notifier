import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot
from urllib.parse import urlparse
from selenium.common.exceptions import NoSuchElementException
import time

# Substitua SEU_TOKEN_AQUI pelo seu token do Telegram
token = 'SEU_TOKEN_AQUI'
chat_id = -1
bot = Bot(token)

async def enviar_mensagem(bot, chat_id, mensagem):
    try:
        await bot.send_message(chat_id=chat_id, text=mensagem)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def limpar_cache_navegador(driver):
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    driver.execute_script("document.cookie = '';")

async def main():
    while True:
        # Lista de URLs iniciais para cada liga (substitua por URLs genéricas)
        urls_inicio = [
            "SUA_URL_AQUI/liga1",
            "SUA_URL_AQUI/liga2",
            "SUA_URL_AQUI/liga3",
            # ... adicione outras URLs conforme necessário
        ]

        # Configurações do Chrome
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Crie o WebDriver com as opções configuradas
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Antes de finalizar o script, leia os jogos verificados do arquivo
            with open('jogos_verificados.txt', 'r') as arquivo:
                jogos_verificados = arquivo.read().splitlines()

            # Iterar sobre cada URL de início
            for url_inicio in urls_inicio:
                parsed_url = urlparse(url_inicio)
                nome_da_liga = parsed_url.path.split("/")[1]  # Altere o índice conforme a estrutura real da URL
                print(f"Processando jogos da liga: {nome_da_liga}")

                # Navegar para a URL de início
                driver.get(url_inicio)

                # Localizar todos os elementos com a classe "GTM-event-link"
                event_links = driver.find_elements(By.CLASS_NAME, "GTM-event-link")

                # Iterar sobre cada link
                for i in range(len(event_links)):
                    # Localizar novamente o elemento para evitar o StaleElementReferenceException
                    link = driver.find_elements(By.CLASS_NAME, "GTM-event-link")[i]

                    # Obter o href do link
                    href = link.get_attribute("href")

                    # Navegar para a nova URL
                    driver.get(href)

                    try:
                        # Verificar se a string "Especiais de jogadores" está presente
                        if "Especiais de jogadores" in driver.page_source:
                            # Se o jogo não foi verificado anteriormente, processar e adicionar à lista
                            if href not in jogos_verificados:
                                # Tente capturar as strings dos times
                                try:
                                    participante_1_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "participant__name--one")))
                                    participante_1 = participante_1_element.text
                                except NoSuchElementException:
                                    participante_1 = "Time 1 não encontrado"

                                try:
                                    participante_2_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "participant__name--two")))
                                    participante_2 = participante_2_element.text
                                except NoSuchElementException:
                                    participante_2 = "Time 2 não encontrado"

                                # Adicionar o jogo à lista de jogos verificados
                                jogos_verificados.append(href)

                                # Imprimir a mensagem
                                print(f"Jogo entre {participante_1} x {participante_2} está com Especiais de jogadores aberto.")

                                # Enviar mensagem assincronamente
                                mensagem = f"Jogo entre {participante_1} x {participante_2} está com Especiais de jogadores aberto. Na(o) {nome_da_liga}, Segue o link: {href}"
                                await enviar_mensagem(bot, chat_id, mensagem)
                    except Exception as e:
                        print(f"Erro ao processar jogo: {e}")

                    # Voltar para a página inicial
                    driver.get(url_inicio)

            # Antes de finalizar o script, escrever os jogos verificados no arquivo
            with open('jogos_verificados.txt', 'w') as arquivo:
                for jogo in jogos_verificados:
                    arquivo.write(jogo + '\n')

        except Exception as e:
            print(f"Erro geral: {e}")
            print("Reiniciando o script...")
            continue 

        finally:
            # Limpar o cache do navegador e fechar o navegador
            limpar_cache_navegador(driver)
            driver.quit()

if __name__ == "__main__":
    # Executar o código assíncrono no loop de eventos
    asyncio.run(main())
