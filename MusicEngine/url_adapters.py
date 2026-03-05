#padrão de projeto Adapter Pattern

class MusicPlayerAdapter:
    def get_embed_url(self, original_url):
        """Transforma a URL original em uma URL de embed para o player"""
        raise NotImplementedError

class SoundCloudAdapter(MusicPlayerAdapter):
    def get_embed_url(self, original_url):
        # Transforma o link em formato de player
        return f"https://w.soundcloud.com/player/?url={original_url}&auto_play=true"
    

#Para quê serve o Adapter Pattern?

#Para padronização, minha dashboard não precisa saber que é do soundcloud
#E para flexibilidade, se um dia eu quiser adicionar o youtube, 
# basta criar um YouTubeAdapter que seguindo o mesmo padrão da interface.