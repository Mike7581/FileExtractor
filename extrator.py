import os
import sys
import shutil

def processar_pasta(pasta_origem):
    # Nome da pasta de destino
    nome_pasta_original = os.path.basename(os.path.normpath(pasta_origem))
    pasta_destino = f"Arquivos da pasta {nome_pasta_original}"
    
    # Cria a pasta de destino
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Lista para guardar nomes dos arquivos
    arquivos = []
    contador = 0

    # Varre todas as subpastas
    for raiz, _, files in os.walk(pasta_origem):
        for arquivo in files:
            caminho_completo = os.path.join(raiz, arquivo)
            nome_arquivo = os.path.basename(caminho_completo)
            
            # Copia o arquivo para a pasta destino
            destino_arquivo = os.path.join(pasta_destino, nome_arquivo)
            shutil.copy2(caminho_completo, destino_arquivo)
            arquivos.append(nome_arquivo)
            contador += 1

    # Salva a lista de nomes DENTRO da pasta destino
    caminho_txt = os.path.join(pasta_destino, "lista_arquivos.txt")
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(arquivos))
    
    return contador, pasta_destino

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Arraste uma pasta para o script!")
        sys.exit()

    pasta_alvo = sys.argv[1]
    
    if not os.path.isdir(pasta_alvo):
        print(f"'{pasta_alvo}' não é uma pasta válida!")
        sys.exit()

    total, destino = processar_pasta(pasta_alvo)
    print(f"✅ {total} arquivos copiados para a pasta '{destino}'!")
    print(f"📄 A lista de nomes está em: {os.path.abspath(destino)}/lista_arquivos.txt")