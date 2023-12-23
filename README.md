## Descrição do Projeto

Desenvolvi um script em Python para automação web utilizando a biblioteca Selenium. Este script verifica periodicamente páginas da web específicas. Quando identifica a abertura de uma condição específica em um determinado link, o script envia uma mensagem via Telegram para notificar sobre essa condição.

### Tecnologias Utilizadas

- **Python**
- **Selenium** (para automação de navegação web)
- **Asyncio** (para operações assíncronas)
- **Telegram API** (para envio de mensagens)
- **Chrome WebDriver** (para interação com o navegador Chrome)

### Funcionalidades Principais

1. **Navegação Automática:** O script acessa URLs específicas.
   
2. **Verificação de Condições Específicas:** Examina o conteúdo das páginas em busca da presença de uma string.
   
3. **Notificação via Telegram:** Quando encontra um jogo com as condições desejadas, o script envia uma mensagem Telegram informando sobre.

## Desenvolvimento

Durante o desenvolvimento deste projeto, enfrentei alguns desafios notáveis, dos quais destaco:

### Dificuldades com o Looping

A principal dificuldade encontrada foi manter o looping de forma eficiente. O script requer um loop contínuo para verificar periodicamente as condições nas páginas da web. Para resolver esse problema, utilizei a biblioteca `asyncio` para operações assíncronas, garantindo que o script pudesse executar tarefas em segundo plano enquanto aguardava a resposta das páginas.

A estrutura de repetição `while True` foi escolhida para manter o script em execução de forma contínua. Além disso, ao lidar com exceções, implementei um bloco `try...except` para capturar erros, reiniciar o script e continuar a execução.

### Lições Aprendidas

Este projeto proporcionou uma oportunidade valiosa para aprimorar minhas habilidades em automação web, lidar com operações assíncronas em Python e desenvolver soluções robustas para execução contínua. A abordagem iterativa para resolver os desafios de looping foi crucial para alcançar a funcionalidade desejada.
