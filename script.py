import os
from mutagen.id3 import ID3, TYER, TDRC, TPE1, TIT2, TALB, ID3NoHeaderError

def destravar_ano(diretorio):
    for raiz, _, arquivos in os.walk(diretorio):
        for nome_arquivo in arquivos:
            if nome_arquivo.endswith('.mp3'):
                caminho = os.path.join(raiz, nome_arquivo)
                try:
                    try:
                        audio = ID3(caminho)
                    except ID3NoHeaderError:
                        audio = ID3()

                    # 1. Copiamos os dados que você quer manter
                    artista = str(audio.get('TPE1', '')).strip()
                    titulo = str(audio.get('TIT2', '')).strip()
                    album = str(audio.get('TALB', '')).strip()

                    # 2. Deletamos a tag corrompida inteira (A "limpeza" necessária)
                    audio.delete(caminho)

                    # 3. Criamos uma nova estrutura ID3v2.3 limpa
                    novas_tags = ID3()
                    if artista: novas_tags.add(TPE1(encoding=1, text=artista))
                    if titulo: novas_tags.add(TIT2(encoding=1, text=titulo))
                    if album: novas_tags.add(TALB(encoding=1, text=album))
                    
                    # Deixamos o ano explicitamente vazio, mas a tag existirá e estará saudável
                    novas_tags.add(TYER(encoding=1, text='')) 
                    novas_tags.add(TDRC(encoding=1, text=''))

                    # 4. Salvamos no formato que o Windows 11 mais gosta
                    novas_tags.save(caminho, v2_version=3)
                    print(f"Destravado: {nome_arquivo}")

                except Exception as e:
                    print(f"Erro em {nome_arquivo}: {e}")

destravar_ano('.')
