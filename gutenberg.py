import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import subprocess

# Configurações
base_url = "https://www.gutenberg.org"
search_url = "https://www.gutenberg.org/ebooks/search/?query=philosophy&submit_search=Go%21&start_index="  # Link base para busca de livros
download_folder = "gutenberg_philosophypdf"

# Criar pasta para os downloads
os.makedirs(download_folder, exist_ok=True)

def get_book_links(page_url):
    """Obtém os links dos livros na página de livros."""
    print(f"Acessando {page_url}...")
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Erro ao acessar {page_url}. Código: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    # Links para as páginas de livros
    links = [base_url + a['href'] for a in soup.select('.booklink a') if '/ebooks/' in a['href']]
    return links

def convert_epub_to_pdf(epub_file_path):
    """Converte um arquivo EPUB para PDF usando Calibre."""
    pdf_file_path = epub_file_path.replace(".epub", ".pdf")
    try:
        # Chamar o Calibre ebook-convert
        subprocess.run(['ebook-convert', epub_file_path, pdf_file_path], check=True)
        print(f"Arquivo convertido com sucesso: {pdf_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erro na conversão do arquivo {epub_file_path} para PDF: {e}")
        return None
    return pdf_file_path

def download_book(book_url):
    """Acessa a página de um livro e baixa o arquivo em um formato disponível."""
    print(f"Acessando {book_url}...")
    response = requests.get(book_url)
    if response.status_code != 200:
        print(f"Erro ao acessar {book_url}. Código: {response.status_code}")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Tentar encontrar o título na meta tag og:title
    title = None
    title_tag = soup.find("meta", {"property": "og:title"})
    
    if title_tag and title_tag.get('content'):
        title = title_tag['content']
    
    if not title:
        # Tentativa alternativa caso o título não seja encontrado
        title_tag = soup.find("h1", {"class": "header"})
        if title_tag:
            title = title_tag.text.strip()
    
    if not title:
        print(f"Título não encontrado para o livro em {book_url}")
        return

    # Procurar links de download nos formatos PDF e EPUB
    formats = soup.select("a[type='text/plain'], a[href$='.epub.noimages'], a[href$='.pdf']")
    
    # PDF e depois EPUB
    download_link = None
    for format_link in formats:
        href = format_link['href']
        if '.pdf' in href:
            download_link = urljoin(base_url, href)
            break  # Se encontrar PDF, priorizar e sair do loop
    if not download_link:
        for format_link in formats:
            href = format_link['href']
            if '.epub' in href:
                download_link = urljoin(base_url, href)
                break  # Se encontrar EPUB, baixar e sair do loop

    if not download_link:
        print(f"Nenhum formato PDF ou EPUB disponível para {title}")
        return

    # Renomear para cada titulo
    file_name = f"{title}.pdf" if '.pdf' in download_link else f"{title}.epub"
    file_path = os.path.join(download_folder, file_name)

    print(f"Baixando: {title} de {download_link}...")
    # Baixar 
    with requests.get(download_link, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Baixado com sucesso: {file_name}")

    # EPUB para PDF
    if file_name.endswith('.epub'):
        convert_epub_to_pdf(file_path)

# start_index de 1 até 5000
total_books = 5000
books_per_page = 25
page_links = [f"{search_url}{i}" for i in range(1, total_books + 1, books_per_page)]

# scraping e download
for page in page_links:
    print(f"Processando página: {page}")
    book_links = get_book_links(page)
    for book_link in book_links:
        try:
            download_book(book_link)
        except Exception as e:
            print(f"Erro ao baixar {book_link}: {e}")
