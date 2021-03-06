from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from pyknp import Juman
from pyknp import KNP
import csv

with open('/home/ubuntu/20201205/sampleform/formapp/Rep_Dic5.csv',encoding='shift_jis') as f_match:
    reader_match  = csv.reader(f_match)
    l_match = [row for row in reader_match]


knp_1 = KNP() 
jumanpp = Juman()
result = jumanpp.analysis("すもももももももものうち")
result_2 = knp_1.parse("下鴨神社の参道は暗かった。")

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

            result_knp =knp_1.parse(raw_sentence)
            knp_temp =''
            for bnst in result_knp.bnst_list(): # 各文節へのアクセス
                knp_temp = knp_temp + ("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%d, 素性:%s" \
            % (bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id, bnst.fstring))
            #post.knp = "aaaa11"
            post.knp = knp_temp
            
            for  i in range(len(l_match)):
                #if raw_sentence.find(l_match[i][0]):
                if l_match[i][0] in raw_sentence:
                   post.answer = l_match[i][1]
                   post.match = l_match[i][0]
                   break
            #post.answer = '答えはここに入れる'
            #post.match = 'マッチ部分はここに入れる'
            #post.match = l_match
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
