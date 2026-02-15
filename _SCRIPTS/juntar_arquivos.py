import os
import sys
from PIL import Image
from PyPDF2 import PdfMerger

def convert_images_to_pdf(image_files, output_folder):
    for image_file in image_files:
        # Obter o caminho completo do arquivo de imagem
        image_path = os.path.join(output_folder, image_file)
        
        # Obter o nome do arquivo sem a extensão e adicionar a extensão .pdf
        pdf_file = os.path.splitext(image_path)[0] + '.pdf'
        
        # Abrir a imagem e salvar como PDF
        img = Image.open(image_path)
        img.save(pdf_file, format='PDF')
        img.close()

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

if __name__ == "__main__":
    # Verifica se o número de argumentos é correto
    if len(sys.argv) != 2:
        print("Uso: python juntar_arquivos.py <caminho_da_pasta>")
        sys.exit(1)
    
    # Obtém o caminho da pasta de trabalho do primeiro argumento
    folder_path = sys.argv[1]
    
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
    
    # Mescla os arquivos PDF com o mesmo prefixo
    merge_pdfs_with_same_prefix(pdf_files, folder_path)
