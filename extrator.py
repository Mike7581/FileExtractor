import os
import sys
import shutil
import traceback
import zipfile

def processar_arquivo(origem, pasta_destino):
    nome, ext = os.path.splitext(os.path.basename(origem))
    contador = 1
    while True:
        novo_nome = f"{nome} ({contador}){ext}" if contador > 1 else f"{nome}{ext}"
        destino = os.path.join(pasta_destino, novo_nome)
        if not os.path.exists(destino):
            return destino
        contador += 1

def decompilar_jar(origem, pasta_destino):
    # Usa o zipfile para extrair o .jar (jar é basicamente um zip)
    nome, _ = os.path.splitext(os.path.basename(origem))
    pasta_decompilado = os.path.join(pasta_destino, f"{nome}_decompilado")
    os.makedirs(pasta_decompilado, exist_ok=True)
    try:
        with zipfile.ZipFile(origem, 'r') as jar:
            jar.extractall(pasta_decompilado)
    except Exception as e:
        raise RuntimeError(f"Falha ao extrair {origem}: {e}")
    return pasta_decompilado

def log_erros(erros, pasta_destino):
    if erros:
        print(f"⚠️ {len(erros)} arquivos com erro. Códigos de erro:")
        for erro in erros[:5]:
            if "FALTA DECOMPILER" in erro:
                print(f"• [ERRO 404] {erro.split('->')[-1].strip()}")
            elif "NA DECOMPILAÇÃO" in erro:
                print(f"• [ERRO 500] {erro.split('->')[-1].strip()}")
            else:
                print(f"• [ERRO GERAL] {erro}")
        with open(os.path.join(pasta_destino, "erros.log"), 'w') as f:
            f.write("\n".join(erros))

def main(pasta_origem, decompilar=False):
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
                        if decompilar and arquivo.lower().endswith('.jar'):
                            try:
                                destino = decompilar_jar(origem, pasta_destino)
                            except Exception as e:
                                erros.append(f"ERRO (NA DECOMPILAÇÃO): {origem} -> {str(e)}")
                                continue
                        else:
                            destino = processar_arquivo(origem, pasta_destino)
                            shutil.copy2(origem, destino)
                        log_file.write(f"{os.path.basename(destino)}\n")
                        contador += 1

                        if contador % 100 == 0:
                            porcentagem = (contador / total_arquivos) * 100
                            print(f"Progresso: {porcentagem:.2f}% ({contador}/{total_arquivos})")
                    except Exception as e:
                        erros.append(f"ERRO GERAL: {origem} -> {str(e)}")
                        continue

        print(f"\n✅ Concluído! {contador} arquivos processados.")
        log_erros(erros, pasta_destino)

    except Exception as e:
        print("\n🔥 ERRO FATAL:")
        traceback.print_exc()
    finally:
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: extrator.py <pasta_origem> [--decompile]")
        sys.exit(1)
    pasta_origem = sys.argv[1]
    decompilar_flag = "--decompile" in sys.argv[2:]
    main(pasta_origem, decompilar_flag)
