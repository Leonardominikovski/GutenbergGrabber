# GutenbergGrabber

### **Descrição do Projeto**  
Este é um projeto simples e educacional criado para facilitar a construção de bibliotecas pessoais utilizando o vasto acervo de livros gratuitos do [Projeto Gutenberg](https://www.gutenberg.org). Ele automatiza o processo de busca, download e organização de livros, tornando mais acessível o acesso à literatura clássica em formatos como PDF e EPUB.  

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

## **Pré-requisitos**  

### **1. Instale o Python 3.x**  
Para executar o script, é necessário ter o Python instalado.  
- Instale as bibliotecas necessárias:  
  ```bash
  pip install requests beautifulsoup4
  ```  

### **2. Instale o Calibre**  
O *Calibre* é usado para converter arquivos EPUB em PDF. No Linux, você pode instalá-lo com:  
  ```bash
  sudo apt update
  sudo apt install calibre -y
  ```  
Verifique se a instalação foi concluída com sucesso:  
  ```bash
  ebook-convert --version
  ```  

---

## **Como Usar**  

### **1. Clone este Repositório**  
Faça o clone para o seu computador:  
```bash
git clone https://github.com/Leonardominikovski/GutenbergGrabber.git
cd GutenbergGrabber
```  

### **2. Configure o Script**  
Abra o arquivo `gutenberg.py` e configure os seguintes parâmetros no início do código:  
- **`search_url`:** URL de busca para definir o tema dos livros (ex.: "philosophy", "science", etc.).  
- **`download_folder`:** Nome da pasta onde os livros serão armazenados.  

Por exemplo, para buscar livros sobre ciência:  
```python
search_url = "https://www.gutenberg.org/ebooks/search/?query=science&submit_search=Go%21&start_index="
download_folder = "gutenberg_science"
```  

### **3. Execute o Script**  
Execute o script no terminal:  
```bash
python3 gutenberg.py
```  

### **4. Verifique os Resultados**  
- Os livros baixados estarão na pasta especificada.  
- Arquivos EPUB serão automaticamente convertidos para PDF.  

---

## **Explicação do Código**  

Aqui estão alguns detalhes sobre como o script funciona:  

1. **Busca de Livros:**  
   O script acessa o site do Projeto Gutenberg, utilizando a URL base configurada. A função `get_book_links` localiza os links dos livros disponíveis na página e retorna uma lista.  

2. **Download de Livros:**  
   A função `download_book` acessa a página de cada livro, identifica os formatos disponíveis (PDF ou EPUB) e baixa o arquivo para a pasta configurada.  

3. **Conversão de Formatos:**  
   Se o arquivo baixado for um EPUB, a função `convert_epub_to_pdf` usa o comando `ebook-convert` do *Calibre* para convertê-lo em PDF.  

4. **Processamento em Lote:**  
   O script percorre várias páginas de resultados com base no parâmetro `total_books` (configurado para processar até 5000 livros).  

**Exemplo de Trecho do Código:**  

```python
def download_book(book_url):
    """Baixa o livro e converte se necessário."""
    # Acessa a página do livro
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Encontra o link para download
    formats = soup.select("a[type='text/plain'], a[href$='.epub.noimages'], a[href$='.pdf']")
    # Prioriza PDF ou busca por EPUB
    download_link = next((urljoin(base_url, f['href']) for f in formats if '.pdf' in f['href']), None)
    if not download_link:
        download_link = next((urljoin(base_url, f['href']) for f in formats if '.epub' in f['href']), None)
    
    # Realiza o download
    file_name = title + (".pdf" if ".pdf" in download_link else ".epub")
    with open(os.path.join(download_folder, file_name), "wb") as f:
        for chunk in requests.get(download_link, stream=True).iter_content(chunk_size=8192):
            f.write(chunk)
```

Se tiver dúvidas ou sugestões, contribua abrindo issues ou enviando um pull request! 


    
