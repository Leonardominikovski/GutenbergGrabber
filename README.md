# GutenbergGrabber

![GutenbergGrabber Logo](assets/logo.png)

### **Descrição do Projeto**  
Este é um projeto simples e educacional criado para facilitar a construção de bibliotecas pessoais utilizando o vasto acervo de livros gratuitos do [Projeto Gutenberg](https://www.gutenberg.org). O objetivo principal foi criar uma solução prática e funcional para meu uso pessoal, agora arquivada aqui como referência e aprendizado.

O objetivo do script é educativo e pretende mostrar como combinar ferramentas de *web scraping*, manipulação de arquivos e conversão de formatos para resolver problemas reais de forma prática.  

Este projeto foi desenvolvido com a ajuda do ChatGPT, que auxiliou na codificação.  

---

## **Recursos do Projeto**  
- **Simplicidade:** O código é fácil de entender e modificar, mesmo para iniciantes.  
- **Busca automatizada:** Permite pesquisar livros no Gutenberg com base em palavras-chave.  
- **Download de livros:** Dá prioridade a arquivos PDF, mas também suporta EPUB.  
- **Conversão de formatos:** Converte automaticamente arquivos EPUB para PDF usando a ferramenta *Calibre*.  
- **Organização:** Todos os livros baixados são salvos em uma pasta dedicada, pronta para ser utilizada.  

---

Requisitos para Executar o Projeto

Antes de rodar o script, você precisará instalar algumas dependências. Aqui estão os requisitos:
1. Python 3.x

Este projeto é desenvolvido em Python. Você pode verificar se o Python está instalado rodando o comando:

python3 --version

Se não tiver o Python instalado, pode baixá-lo [aqui](https://www.python.org/downloads/).
2. Instalar Bibliotecas do Python

O script depende de algumas bibliotecas externas que precisam ser instaladas. Utilize o pip para instalá-las:

pip install requests beautifulsoup4

Essas bibliotecas são responsáveis pela execução de requisições HTTP (requests) e pelo processamento do HTML das páginas do Projeto Gutenberg (beautifulsoup4).
3. Instalar o Calibre para Conversão de EPUB para PDF

O script utiliza o Calibre para converter arquivos EPUB para PDF. Você pode instalar o Calibre com o comando:

sudo apt update
sudo apt install calibre -y

O Calibre deve estar acessível no terminal como ebook-convert. Para verificar se a instalação foi bem-sucedida, execute:

ebook-convert --version

Se o Calibre não estiver instalado ou configurado corretamente, a conversão de EPUB para PDF não funcionará.
Como Usar o Script

Este script inclui uma interface gráfica simples, usando a biblioteca Tkinter, para facilitar o uso. Aqui está o passo a passo de como utilizá-lo:
1. Clone o Repositório

Primeiro, clone o repositório para sua máquina:

git clone https://github.com/Leonardominikovski/GutenbergGrabber.git
cd GutenbergGrabber
cd code

2. Configure o Script

O script não requer configurações complicadas. Basta definir o termo de pesquisa, quantidade de livros a serem baixados e nome da pasta onde os livros serão salvos diretamente na interface gráfica.
3. Executando o Script

Abra um terminal na pasta onde o repositório foi clonado e execute o script:

python3 gutenberg.py

Isso abrirá a interface gráfica, onde você poderá inserir:

    Termo de pesquisa (ex: "philosophy", "shakespeare").
    Quantidade de livros que deseja baixar.
    Nome da pasta onde os livros serão salvos.

Depois de preencher as informações, clique no botão "Iniciar Download". O script irá:

    Realizar a busca no Projeto Gutenberg com o termo inserido.
    Baixar os livros em formatos PDF ou EPUB.
    Converter os arquivos EPUB para PDF (se necessário).
    Salvar os arquivos na pasta indicada.

4. Resultados

Os livros serão baixados e salvos na pasta que você definiu. Se algum livro for no formato EPUB, ele será convertido automaticamente para PDF e armazenado na mesma pasta.
Explicação Detalhada do Código

Agora que você sabe como usar o script, vamos explicar em detalhes como ele funciona.
1. Importações e Inicializações

No início do código, importamos as bibliotecas necessárias para rodar o script:

    requests: Usada para enviar requisições HTTP e acessar as páginas de livros do Projeto Gutenberg.
    BeautifulSoup: Usada para processar o HTML das páginas e extrair os links de download dos livros.
    subprocess: Usada para executar o comando ebook-convert do Calibre, convertendo arquivos EPUB para PDF.
    tkinter: Usada para criar a interface gráfica onde o usuário pode interagir com o script.

2. Função start_download()

Essa função é chamada quando o usuário clica no botão da interface gráfica. Ela coleta os dados inseridos pelo usuário (termo de pesquisa, quantidade de livros, nome da pasta) e inicia o processo de download.
3. Função get_book_links(page_url)

Essa função faz uma requisição para cada página de resultados no Projeto Gutenberg e extrai os links dos livros. Ela usa o BeautifulSoup para processar o HTML e encontrar os links corretos.
4. Função download_book(book_url)

Depois de coletar os links dos livros, essa função acessa cada um dos links, encontra os formatos de download (PDF ou EPUB) e baixa os arquivos para a pasta definida. Se o livro for um EPUB, ele será convertido para PDF.
5. Função convert_epub_to_pdf()

Se o livro for um arquivo EPUB, ele será convertido para PDF usando o comando ebook-convert do Calibre.
6. Interface Gráfica (Tkinter)

A interface gráfica permite ao usuário inserir o termo de pesquisa, quantidade de livros e nome da pasta de forma intuitiva. Ela usa o Tkinter para coletar as entradas do usuário e iniciar o processo de download.
7. Navegação por Páginas

O script gera uma lista de links de páginas de resultados do Projeto Gutenberg. Ele usa o parâmetro start_index para navegar pelas páginas e buscar os livros em diferentes páginas de resultados.

 se você tiver sugestões ou melhorias, sinta-se à vontade para contribuir. Abra issues ou envie pull requests com suas alterações!
