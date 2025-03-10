import os
import sys
import shutil
import traceback

def processar_arquivo(origem, pasta_destino):
    nome, ext = os.path.splitext(os.path.basename(origem))
    contador = 1
    while True:
        novo_nome = f"{nome} ({contador}){ext}" if contador > 1 else f"{nome}{ext}"
        destino = os.path.join(pasta_destino, novo_nome)
        if not os.path.exists(destino):
            return destino
        contador += 1

def main(pasta_origem):
    try:
        nome_base = os.path.basename(os.path.normpath(pasta_origem))
        pasta_destino = f"Arquivos da pasta {nome_base}"
        os.makedirs(pasta_destino, exist_ok=True)

        total_arquivos = sum(len(files) for _, _, files in os.walk(pasta_origem))
        contador = 0
        erros = []

        with open(os.path.join(pasta_destino, "lista_arquivos.txt"), 'w', encoding='utf-8') as log_file:
            for raiz, _, arquivos in os.walk(pasta_origem):
                for arquivo in arquivos:
                    origem = os.path.join(raiz, arquivo)
                    try:
                        destino = processar_arquivo(origem, pasta_destino)
                        shutil.copy2(origem, destino)
                        log_file.write(f"{os.path.basename(destino)}\n")
                        contador += 1
                        
                        # Atualiza progresso a cada 100 arquivos
                        if contador % 100 == 0:
                            porcentagem = (contador / total_arquivos) * 100
                            print(f"Progresso: {porcentagem:.2f}% ({contador}/{total_arquivos})")
                    except Exception as e:
                        erros.append(f"ERRO: {origem} -> {str(e)}")
                        continue

        print(f"\n✅ Concluído! {contador} arquivos processados.")
        if erros:
            print(f"⚠️ {len(erros)} arquivos com erro. Verifique:")
            for erro in erros[:5]:
                print(f"• {erro}")
            
            with open(os.path.join(pasta_destino, "erros.log"), 'w') as f:
                f.write("\n".join(erros))

    except Exception as e:
        print("\n🔥 ERRO FATAL:")
        traceback.print_exc()
    finally:
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: extrator.py <pasta_origem>")
        sys.exit(1)
    main(sys.argv[1])