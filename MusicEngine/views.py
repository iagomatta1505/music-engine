from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Music, Album
from django.db.models import Q
# Create your views here.


@login_required
def dashboard(request):
    # 1. Preparação inicial e Busca (GET)
    search_term = request.GET.get('search_musics')
    musics_list = Music.objects.filter(user=request.user)
    
    if search_term:
        musics_list = musics_list.filter(Q(title__icontains=search_term) | Q(artist__icontains=search_term))

    context = {
        'musics': musics_list, # Lista filtrada pela busca
        'albums': Album.objects.filter(user=request.user),
        'user': request.user,
        'modo': request.POST.get('action') if request.method == 'POST' else 'ver',
        'search_term': search_term
    }

    # 2. Funções internas (a "cozinha" da view)
    def processar_musica():
        if 'add_music' in request.POST:
            title = request.POST.get('title')
            artist = request.POST.get('artist', '').strip() or "Artista desconhecido"
            url = request.POST.get('soundcloud_url') # Capturando a nova URL
            Music.objects.create(title=title, artist=artist, soundcloud_url=url, user=request.user)
            return redirect('dashboard_index')
        return None

    def processar_album():
        nonlocal context
        action = request.POST.get('action')
        album_id = request.POST.get('album_id')
        
        if action == 'salvar_album':
            name = request.POST.get('album_name')
            musics_ids = request.POST.getlist('musics')
            if len(musics_ids) < 2:
                messages.error(request, 'Selecione pelo menos 2 músicas.')
            else:
                if album_id:
                    album = Album.objects.get(id=album_id, user=request.user)
                    album.name = name
                    album.musics.set(musics_ids)
                    album.save()
                else:
                    album = Album.objects.create(name=name, user=request.user)
                    album.musics.set(musics_ids)
            return redirect('dashboard_index')
        
        elif action == 'remover' and album_id:
            Album.objects.get(id=album_id, user=request.user).delete()
            return redirect('dashboard_index')
        
        elif action == 'ver' and album_id:
            context['modo'] = 'ver_album'
            context['album_visualizado'] = Album.objects.get(id=album_id, user=request.user)
        
        return None

    # 3. Fluxo principal da Dashboard (POST)
    if request.method == 'POST':
        resp_musica = processar_musica()
        if resp_musica: return resp_musica
        
        resp_album = processar_album()
        if resp_album: return resp_album

    # 4. Ajustes finos do contexto
    if context['modo'] == 'editar':
        album_id = request.POST.get('album_id')
        if album_id:
            context['album_editando'] = Album.objects.get(id=album_id, user=request.user)

    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redireciona para o login após criar
        else:
            # Isso vai mostrar o erro no console do terminal
            print(form.errors) 
            # Opcional: adicionar mensagem para o usuário
            messages.error(request, "Erro ao criar conta. Verifique os dados.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_music(request, music_id):

    # Busca a música específica garantindo que pertence ao usuário logado
    music = Music.objects.get(id=music_id, user=request.user)
    
    if request.method == 'POST':
        # Atualiza os dados com o que veio do formulário
        music.title = request.POST.get('title')
        music.artist = request.POST.get('artist')
        music.save() # Salva no banco de dados
        return redirect('dashboard_index')
        
    return render(request, 'edit_music.html', {'music': music})

@login_required
def delete_music(request, music_id):

    music = Music.objects.get(id=music_id, user=request.user)
    music.delete()
    return redirect('dashboard_index')



    album = Album.objects.get(id=album_id, user=request.user)
    musics = Music.objects.filter(user=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        selected_musics = request.POST.getlist('musics')
        
        if len(selected_musics) < 2:
            messages.error(request, 'Um álbum precisa ter pelo menos 2 músicas selecionadas.')
            return render(request, 'album_form.html', {'musics': musics, 'album': album})
            
        if name:
            album.name = name
            album.musics.set(selected_musics) # Atualiza a lista de músicas
            album.save()
            return redirect('dashboard_index')
            
    return render(request, 'album_form.html', {'musics': musics, 'album': album})