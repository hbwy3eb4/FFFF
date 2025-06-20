from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import FamilyTree
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import copy
import json

# views.py

# Удалить конфликтующие функции
def home_view(request):
    return render(request, 'index.html')

# Удалить лишние функции
# def home(request):
# def login(request):
# def login_view(request):
# def about(request):

# Оставить только актуальные функции
def features_view(request):
    return render(request, 'features.html')

def create_tree_view(request):
    return render(request, 'create_tree.html')

def my_trees_view(request):
    return render(request, 'my_trees.html')

# Оставляю только register_view для регистрации

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})

@login_required
def profile_view(request):
    tree = FamilyTree.objects.filter(owner=request.user).first()
    def count_ancestors(node):
        if not node:
            return 0
        if isinstance(node, list):
            return sum(count_ancestors(branch) for branch in node)
        count = 1
        if node.get('spouse'):
            count += 1
        for child in node.get('children', []):
            count += count_ancestors(child)
        return count
    def count_generations(node, level=1):
        if not node:
            return level - 1
        if isinstance(node, list):
            return max((count_generations(branch, level) for branch in node), default=level-1)
        if not node.get('children'):
            return level
        return max([count_generations(child, level+1) for child in node.get('children', [])])
    def gender_stats(node, stats=None):
        if stats is None:
            stats = {'male': 0, 'female': 0}
        if not node:
            return stats
        if isinstance(node, list):
            for branch in node:
                gender_stats(branch, stats)
            return stats
        if node.get('gender') == 'male':
            stats['male'] += 1
        elif node.get('gender') == 'female':
            stats['female'] += 1
        if node.get('spouse') and node['spouse'].get('gender'):
            if node['spouse']['gender'] == 'male':
                stats['male'] += 1
            elif node['spouse']['gender'] == 'female':
                stats['female'] += 1
        for child in node.get('children', []):
            gender_stats(child, stats)
        return stats
    ancestors = 0
    generations = 0
    gender_data = {'male': 0, 'female': 0}
    if tree and tree.data:
        ancestors = count_ancestors(tree.data)
        generations = count_generations(tree.data)
        gender_data = gender_stats(tree.data)
    return render(request, 'profile.html', {
        'profile': request.user.profile,
        'ancestors': ancestors,
        'generations': generations,
        'gender_data': gender_data,
    })

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})

def generate_random_tree():
    first_names = ["Алексей", "Мария", "Иван", "Ольга"]
    last_names = ["Иванов", "Петров", "Сидоров"]
    professions = ["инженер", "врач", "учитель", "программист"]
    cities = ["Москва", "Санкт-Петербург", "Казань"]
    eye_colors = ["карий", "голубой", "зелёный"]
    blood_types = ["I", "II", "III"]
    bios = ["Очень добрый человек.", "Любил путешествовать."]
    def random_person(prefix=""):
        return {
            "name": f"{prefix}{random.choice(first_names)}",
            "surname": random.choice(last_names),
            "birth": f"{random.randint(1,28):02d}.{random.randint(1,12):02d}.{random.randint(1940,2010)}",
            "profession": random.choice(professions),
            "city": random.choice(cities),
            "height": str(random.randint(150, 200)),
            "eyeColor": random.choice(eye_colors),
            "blood": random.choice(blood_types),
            "bio": random.choice(bios)
        }
    root = random_person()
    children = [
        {**random_person(), "children": [random_person(), random_person()]},
        {**random_person(), "children": [random_person()]},
        random_person()
    ]
    return {**root, "children": children}

@login_required
def family_tree_view(request):
    tree, created = FamilyTree.objects.get_or_create(
        owner=request.user,
        defaults={'name': 'Моё семейное древо'}
    )
    if created or not tree.data:
        tree.data = generate_random_tree()
        tree.save(update_fields=['data'])
    return render(request, 'family_tree.html', {'tree': tree})

@csrf_exempt
@login_required
def edit_family_tree_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Требуется POST-запрос'}, status=400)
    try:
        tree = FamilyTree.objects.get(owner=request.user)
        tree.data = json.loads(request.body)
        tree.save(update_fields=['data'])
        return JsonResponse({'status': 'ok'})
    except FamilyTree.DoesNotExist:
        return JsonResponse({'error': 'Древо не найдено'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный JSON'}, status=400)

@login_required
def family_tree_data(request):
    tree, created = FamilyTree.objects.get_or_create(owner=request.user, defaults={'name': 'Моё семейное древо'})
    return JsonResponse(tree.data, safe=False)