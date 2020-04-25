# coding = utf-8
import requests
from bs4 import BeautifulSoup
import time
import re


url = "http://nibs.ac.cn/news.php" # ?cid=4&sid=15&page=2"


def judge_sentence(sen):
    if "实验室" in sen  and "发表" in sen and ("论文" in sen or "文章" in sen):
        return True
    else:
        return False


def del_str(mod):
    if "\n" in mod:
        new_mod = mod.replace("\n", ' ')
        if "\r" in new_mod:
            new_new_mod = new_mod.replace("\r", "")
            return new_new_mod
        else:
            return new_mod
    else:
        return mod


def extrac_jounal(mod_left):
    p = re.compile('.+?《(.+?)》')
    match = re.findall(p, mod_left)
    if match:
        return match[0]
    else:
        mod_left_r = mod_left[mod_left.find("在"):]
        jounal = "".join([x for x in mod_left_r if x.encode().isalpha()])
        return jounal


# sen = "2020年3月6日，北京生命科学研究所/清华大学生物医学交叉研究院罗敏敏实验室在学术期刊Neuron在线发表题为“The Raphe Dopamine System Controls the Expression of Incentive Memory”的研究论文"
# sen1 = ''
def find_jounal_and_title(sen):
    rep_list = []
    p1 = re.compile('.+?“(.+?)”')
    for mod in sen.split("，"):
        mod = del_str(mod)
        print(mod)
        if mod.find("实验室"):
            pos_sys = mod.find("实验室")
            lab = mod[pos_sys-3: pos_sys+3]
        else:
            lab = "No lab"
        if re.findall(p1, mod):
            title = re.findall(p1, mod)[0]
            mod_left = mod[:mod.find(title)]
            jounal = extrac_jounal(mod_left)
            return lab, title, jounal
    return "No lab", "no title", "no jounal"
# print(find_jounal_and_title(sen))


def getLinkfromHTML(url):
    r = requests.get(url)
    print(r.status_code)
    demo = r.text
    soup = BeautifulSoup(demo, 'html.parser')
    # print(soup.prettify())
    text = ""
    for link in soup.find_all('p'):
        #print(link.string)
        text += str(link.string)
    # print(text)
    for sent in text.split("。"):
        if judge_sentence(sent):
            lab, title, jounal = find_jounal_and_title(sent)
            return sent, lab, title, jounal
    return "None sentence","None sentence", "None sentence", "None sentence"

print(getLinkfromHTML("http://nibs.ac.cn/newsshow.php?cid=4&sid=15&id=2150"))


def methods1():
    b = open("reporter.txt", 'w')
    read_list= []
    for i in range(1,10):
        kv = {'cid':'4', 'sid':'15', "page": str(i)}
        r = requests.get(url, params = kv)
        if r.status_code != 200:
            print(i)
            print("Stop")
            break
        else:
            print(r.request.url)
            demo = r.text
            soup = BeautifulSoup(demo, 'html.parser')
            # print(soup.find_all('a'))
            for link in soup.find_all('a'):
                if "实验室" in str(link.parent.string):
                    url_to = "http://nibs.ac.cn/" + link.get('href')
                    if url_to not in read_list:
                        sens, lab, title, jounal = getLinkfromHTML(url_to)
                        wlist = [url_to, sens, lab, title, jounal]
                        b.write("\t".join(wlist)+"\n")
                        time.sleep(3)
                        read_list.append(url_to)

            time.sleep(3)
    b.close()


def main():
    b = open("reporter.txt", 'w')
    for i in range(2286,2267,-1):
        url = "http://nibs.ac.cn/newsshow.php?cid=4&sid=15&id=" + str(i)
        print(url)
        sens, lab, title, jounal = getLinkfromHTML(url)
        wlist = [url, sens, lab, title, jounal]
        b.write("\t".join(wlist)+"\n")
        time.sleep(1)
    b.close()


if __name__ == "__main__":
    methods1()


