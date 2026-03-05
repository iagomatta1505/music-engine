from urllib import request
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Music, Album
from django.db.models import Q
from .url_adapters import SoundCloudAdapter
from .factories import ContentFactory
# Create your views here.


@login_required
def dashboard(request):
    #função principal
    search_term = request.GET.get('search_musics')
    musics_list = Music.objects.filter(user=request.user)
    
    if search_term:
        musics_list = musics_list.filter(Q(title__icontains=search_term) | Q(artist__icontains=search_term))

    context = {
        'musics': musics_list,
        'albums': Album.objects.filter(user=request.user),
        'user': request.user,
        'modo': request.POST.get('action') if request.method == 'POST' else 'ver',
        'search_term': search_term
    }

    
    def processar_post(request, context):
        action = request.POST.get('action')
        album_id = request.POST.get('album_id')

        #Adicionar Música
        if 'add_music' in request.POST:
            ContentFactory.create_content('music', request.user, request.POST)
            return redirect('dashboard_index')

        #Ação Criar
        if action == 'criar':
            context['modo'] = 'criar'
            return None

        #Ações do album (Salvar, Editar, Ver, Remover)
        if action == 'salvar_album':
            ContentFactory.create_content('album', request.user, request.POST)
            return redirect('dashboard_index')
            
        elif action == 'remover' and album_id:
            Album.objects.get(id=album_id, user=request.user).delete()
            return redirect('dashboard_index')
            
        elif action == 'ver' and album_id:
            context['modo'] = 'ver_album'
            context['album_visualizado'] = Album.objects.get(id=album_id, user=request.user)
            
        elif action == 'editar' and album_id:
            context['modo'] = 'editar'
            context['album_editando'] = Album.objects.get(id=album_id, user=request.user)
            
        return None

    
    if request.method == 'POST':
        response = processar_post(request, context)
        if response:
            return response

    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') #redireciona para o login apos criar
        else:
            
            print(form.errors)#para mostrar os erros no terminal
            
            messages.error(request, "Erro ao criar conta. Verifique os dados.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_music(request, music_id):

    
    music = Music.objects.get(id=music_id, user=request.user)
    
    if request.method == 'POST':
        
        music.title = request.POST.get('title')
        music.artist = request.POST.get('artist')
        music.save() #salva no banco de dados
        return redirect('dashboard_index')
        
    return render(request, 'edit_music.html', {'music': music})

@login_required
def delete_music(request, music_id):

    music = Music.objects.get(id=music_id, user=request.user)
    music.delete()
    return redirect('dashboard_index')

def MusicLinkAdapter(request):
    adapter = SoundCloudAdapter()
    

    musics = Music.objects.filter(user=request.user)
    for m in musics:
        m.embed_url = adapter.get_embed_url(m.soundcloud_url)
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
            album.musics.set(selected_musics)
            album.save()
            return redirect('dashboard_index')
            
    return render(request, 'album_form.html', {'musics': musics, 'album': album})

def processar_post(request, context):
        action = request.POST.get('action')
        
        album_id = request.POST.get('album_id')

        
        if 'add_music' in request.POST:
            ContentFactory.create_content('music', request.user, request.POST)
            return redirect('dashboard_index')

        
        if action == 'criar':
            context['modo'] = 'criar'
            return None

        
        if not album_id and action in ['editar', 'ver', 'remover']:
            
            return redirect('dashboard_index')

        if action == 'salvar_album':
            ContentFactory.create_content('album', request.user, request.POST)
            return redirect('dashboard_index')
            
        elif action == 'remover':
            Album.objects.get(id=album_id, user=request.user).delete()
            return redirect('dashboard_index')
            
        elif action == 'ver':
            context['modo'] = 'ver_album'
            context['album_visualizado'] = Album.objects.get(id=album_id, user=request.user)
            
        elif action == 'editar':
            context['modo'] = 'editar'
            context['album_editando'] = Album.objects.get(id=album_id, user=request.user)
        elif action == 'ver':
            context['modo'] = 'ver_album'
            context['album_visualizado'] = Album.objects.get(id=album_id, user=request.user)
            
            
        return None