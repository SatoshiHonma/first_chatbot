from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from pyknp import Juman
from pyknp import KNP
knp = KNP() 
jumanpp = Juman()
result = jumanpp.analysis("すもももももももものうち")
sentence =''
for mrph in result.mrph_list(): # 各形態素にアクセス
    sentence = sentence + ("\n見出し:%s, \n読み:%s, \n原形:%s, \n品詞:%s, \n品詞細分類:%s, \n活用型:%s, \n活用形:%s, \n意味情報:%s, \n代表表記:%s" \
            % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))

def formfunc(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        
        if form.is_valid():
            juman_temp = ''
            post = form.save(commit=False)
            #rawsentence =jumanpp.analysis(post.memo)
           # for mrph in rawsentence.mrph_list():
            #    juman_temp = juman_temp + ("\n見出し:%s, \n読み:%s, \n原形:%s, \n品詞:%s, \n品詞細分類:%s, \n活用型:%s, \n活用形:%s, \n意味情報:%s, \n代表表記:%s" \
           # % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))
            #form.juman = "すももももももももももも"
            juman_temp = ''
            raw_sentence = ''
            raw_sentence = post.memo

            result_juman =jumanpp.analysis(raw_sentence)
            for mrph in result_juman:
                juman_temp = juman_temp + ("\n見出し:%s, \n読み:%s, \n原形:%s, \n品詞:%s, \n品詞細分類:%s, \n活用型:%s, \n活用形:%s, \n意味情報:%s, \n代表表記:%s"\
            % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))
            post.juman =juman_temp

            knp_temp =''
            post.knp = "aaaa"


            post.save()
            return redirect('list')
    else:
        form = PostForm()
    return render(request, 'form.html', {'form': form})

def listfunc(request):
    posts = Post.objects.all()
    return render(request, 'list.html', {'posts': posts})

def detailfunc(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'detail.html', {'post': post})
