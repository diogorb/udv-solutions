from pypdf import PdfReader, PdfWriter
import os

def split_pdf_by_pages_reversed_numbered(input_pdf_path, output_directory="output_pdfs_inverted_numbered"):
    """
    Divide um arquivo PDF em PDFs individuais, um para cada página,
    começando da última página para a primeira, e nomeando os arquivos
    na ordem de geração (arquivo_1, arquivo_2, etc.).

    Args:
        input_pdf_path (str): O caminho para o arquivo PDF de entrada.
        output_directory (str): O diretório onde os PDFs de saída serão salvos.
                                Padrão para "output_pdfs_inverted_numbered".
    """
    if not os.path.exists(input_pdf_path):
        print(f"Erro: O arquivo de entrada '{input_pdf_path}' não foi encontrado.")
        return

    # Garante que o diretório de saída exista
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Diretório de saída '{output_directory}' criado.")

    try:
        reader = PdfReader(input_pdf_path)
        num_pages = len(reader.pages)
        print(f"Processando '{input_pdf_path}' com {num_pages} páginas...")
        print("Gerando PDFs da última página para a primeira, numerando na ordem de criação...")

        generated_file_count = 1 # <--- NOVO: Contador para a ordem de geração

        # Percorre as páginas de trás para frente: de (num_pages - 1) até 0
        for i in range(num_pages - 1, -1, -1):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])

            # O nome do arquivo agora usa o contador de geração
            # Também incluímos o número da página original entre parênteses para referência
            base_file_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
            output_pdf_name = f"{generated_file_count}.pdf" # <--- MUDANÇA AQUI
            output_pdf_path = os.path.join(output_directory, output_pdf_name)

            with open(output_pdf_path, "wb") as output_file:
                writer.write(output_file)
            print(f"Página Original {i + 1} salva como '{output_pdf_name}' (arquivo gerado {generated_file_count} de {num_pages})")

            generated_file_count += 1 # <--- Incrementa o contador a cada arquivo gerado

        print(f"\nDivisão concluída! {num_pages} PDFs foram gerados no diretório '{output_directory}'.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    # --- CONFIGURAÇÃO ---
    # Coloque o caminho para o seu arquivo PDF aqui
    # Exemplo: meu_arquivo.pdf (se estiver na mesma pasta do script)
    # Exemplo: /caminho/completo/para/meu_documento.pdf (para um caminho absoluto)
    input_pdf_file = "comprovantes.pdf"  # <--- ALtere este para o seu arquivo PDF

    # Nome do diretório onde os PDFs individuais serão salvos
    output_folder = "Output" # <--- Opcional: Altere o nome da pasta de saída
    # --- FIM DA CONFIGURAÇÃO ---

    split_pdf_by_pages_reversed_numbered(input_pdf_file, output_folder)