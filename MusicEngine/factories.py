#Factory Pattern para criação de conteúdo.

from .models import Music, Album

class ContentFactory:
    @staticmethod
    def create_content(content_type, user, data):
        """Método de Fábrica para centralizar a criação e edição de conteúdo"""
        if content_type == 'music':
            return Music.objects.create(
                title=data.get('title'),
                artist=data.get('artist', 'Artista desconhecido') or "Artista desconhecido",
                soundcloud_url=data.get('soundcloud_url'),
                user=user
            )
            
        elif content_type == 'album':
            album_name = data.get('album_name')
            if not album_name:
                raise ValueError("O nome do álbum não pode ser vazio.")
            
            # Tenta recuperar o ID do álbum enviado pelo Modal de Edição
            album_id = data.get('album_id')
            
            if album_id:
                # MODO EDIÇÃO: Busca o álbum existente
                album = Album.objects.get(id=album_id, user=user)
                album.name = album_name
                album.save()
            else:
                # MODO CRIAÇÃO: Cria um novo
                album = Album.objects.create(name=album_name, user=user)
            
            # Atualiza a lista de músicas (funciona para ambos os casos)
            musics_ids = data.getlist('musics')
            album.musics.set(musics_ids)
                
            return album
        
        raise ValueError(f"Tipo de conteúdo desconhecido: {content_type}")
    
    