import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import subprocess
import tkinter as tk
from tkinter import simpledialog
import time

def start_download():
    search_query = entry_query.get()  
    total_books = int(entry_books.get()) 
    download_folder = entry_folder.get()  
    
    if not search_query or total_books <= 0 or not download_folder:
        print("Por favor, preencha todos os campos corretamente.")
        return
    
    base_url = "https://www.gutenberg.org"
    search_url = f"https://www.gutenberg.org/ebooks/search/?query={search_query}&submit_search=Go%21&start_index="
    
    os.makedirs(download_folder, exist_ok=True)
    
    def get_book_links(page_url):
        response = requests.get(page_url)
        if response.status_code != 200:
            print(f"Erro ao acessar {page_url}. Código: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        links = [base_url + a['href'] for a in soup.select('.booklink a') if '/ebooks/' in a['href']]
        return links
    
    def download_book(book_url):
        response = requests.get(book_url)
        if response.status_code != 200:
            print(f"Erro ao acessar {book_url}. Código: {response.status_code}")
            return
        soup = BeautifulSoup(response.text, "html.parser")
        
        title = None
        title_tag = soup.find("meta", {"property": "og:title"})
        if title_tag and title_tag.get('content'):
            title = title_tag['content']
        
        if not title:
            title_tag = soup.find("h1", {"class": "header"})
            if title_tag:
                title = title_tag.text.strip()
        
        if not title:
            print(f"Título não encontrado para o livro em {book_url}")
            return
        
        formats = soup.select("a[type='text/plain'], a[href$='.epub.noimages'], a[href$='.pdf']")
        
        download_link = None
        for format_link in formats:
            href = format_link['href']
            if '.pdf' in href:
                download_link = urljoin(base_url, href)
                break
        if not download_link:
            for format_link in formats:
                href = format_link['href']
                if '.epub' in href:
                    download_link = urljoin(base_url, href)
                    break
        
        if not download_link:
            print(f"Nenhum formato PDF ou EPUB disponível para {title}")
            return
        
        file_name = f"{title}.pdf" if '.pdf' in download_link else f"{title}.epub"
        file_path = os.path.join(download_folder, file_name)
        
        with requests.get(download_link, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"Baixado: {file_name}")
        
        if file_name.endswith('.epub'):
            convert_epub_to_pdf(file_path)

     time.sleep(2)
    
    def convert_epub_to_pdf(epub_file_path):
        pdf_file_path = epub_file_path.replace(".epub", ".pdf")
        try:
            subprocess.run(['ebook-convert', epub_file_path, pdf_file_path], check=True)
            print(f"Arquivo convertido com sucesso: {pdf_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Erro na conversão do arquivo {epub_file_path} para PDF: {e}")
    
    books_per_page = 25
    page_links = [f"{search_url}{i}" for i in range(1, total_books + 1, books_per_page)]
    
    for page in page_links:
        print(f"Processando página: {page}")
        book_links = get_book_links(page)
        for book_link in book_links:
            try:
                download_book(book_link)
            except Exception as e:
                print(f"Erro ao baixar {book_link}: {e}")
                
                time.sleep(3)
                
root = tk.Tk()
root.title("GutenbergGrabber")

tk.Label(root, text="Termo de Pesquisa:").pack()
entry_query = tk.Entry(root, width=50)
entry_query.pack()

tk.Label(root, text="Quantidade de páginas (25 livros por página):").pack()
entry_books = tk.Entry(root, width=50)
entry_books.pack()

tk.Label(root, text="Nome da Pasta de Download:").pack()
entry_folder = tk.Entry(root, width=50)
entry_folder.pack()

tk.Button(root, text="Iniciar Download", command=start_download).pack()

root.mainloop()
