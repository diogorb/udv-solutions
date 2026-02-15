import csv

def somar_total_recibo(file_path):
    soma = 0
    # Adicione encoding='utf-8' para lidar com caracteres especiais
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if len(row) >= 8 and "Total do Recibo:" in row[6].strip():  # Verifica se a coluna 7 tem "Total do Recibo:"
                try:
                    valor = float(row[7].strip())  # Converte o valor da coluna 8 para float
                    print(valor)
                    soma += valor
                except ValueError:
                    # Ignora valores não numéricos
                    pass
    return soma

# Defina o caminho do arquivo CSV
file_path = 'set_ate_dia_15.csv'

# Chama a função para calcular a soma
soma_total = somar_total_recibo(file_path)
print(f"Soma total dos recibos: {soma_total}")
