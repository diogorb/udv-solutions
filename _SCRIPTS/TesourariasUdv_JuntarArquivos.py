import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfMerger

def convert_images_to_pdf(image_files, output_folder):
    for image_file in image_files:
        # Obter o caminho completo do arquivo de imagem
        image_path = os.path.join(output_folder, image_file)
        
        # Obter o nome do arquivo sem a extensão e adicionar a extensão .pdf
        pdf_file = os.path.splitext(image_path)[0] + '.pdf'
        
        # Criar um novo arquivo PDF
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.drawImage(image_path, 0, 0, width=letter[0], height=letter[1])
        c.showPage()
        c.save()

def merge_pdfs_with_same_prefix(pdf_files, output_folder):
    prefix_map = {}
    for pdf_file in pdf_files:
        # Extrair o prefixo do nome do arquivo PDF
        prefix = os.path.splitext(os.path.basename(pdf_file))[0][:2]
        prefix_map.setdefault(prefix, []).append(pdf_file)

    # Juntar PDFs com o mesmo prefixo
    for prefix, pdf_files_in_group in prefix_map.items():
        output_pdf_file = os.path.join(output_folder, 'output', f'{prefix}.pdf')
        merger = PdfMerger()
        for pdf_file in pdf_files_in_group:
            merger.append(os.path.join(output_folder, pdf_file))
        merger.write(output_pdf_file)
        merger.close()

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Define o caminho da pasta de saída
        output_folder = os.path.join(folder_path, 'output')

        # Cria a pasta 'output' se ela não existir
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Lista de extensões de arquivo de imagem
        image_extensions = ('.jpg', '.jpeg', '.png')

        # Lista de arquivos de imagem
        image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(image_extensions)]

        # Converter imagens para PDF
        convert_images_to_pdf(image_files, folder_path)

        # Lista de arquivos PDF
        pdf_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.pdf')]
        
        try:
            # Mescla os arquivos PDF com o mesmo prefixo
            merge_pdfs_with_same_prefix(pdf_files, folder_path)
            messagebox.showinfo("Concluído", "Os arquivos foram mesclados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a mesclagem dos arquivos: {str(e)}")

# Cria a janela principal
root = tk.Tk()
root.title("Juntar Arquivos")

# Define a geometria da janela (largura x altura + posição X + posição Y)
root.geometry("400x200")  # Por exemplo, define a largura para 400 pixels e a altura para 200 pixels

# Cria um botão para selecionar a pasta
btn_select_folder = tk.Button(root, text="Selecionar Pasta", command=select_folder)
btn_select_folder.pack(pady=20)

# Inicia o loop principal da GUI
root.mainloop()