from nltk.tokenize.treebank import TreebankWordDetokenizer
import tqdm
from transformers import BertTokenizer

def preprocess(fin, fout, keep_sep=False, max_len=512):
    fin = open(fin, 'r', encoding='utf-8')
    fout = open(fout, 'w', encoding='utf-8')
    twd = TreebankWordDetokenizer()
    bpe = BertTokenizer.from_pretrained('bert-base-uncased')
    for line in tqdm.tqdm(fin.readlines()):
        line = line.strip().replace('``', '"').replace('\'\'', '"').replace('`', '\'')
        s_list = [twd.detokenize(x.strip().split(
            ' '), convert_parentheses=True) for x in line.split('<S_SEP>')]
        tk_list = [bpe.tokenize(s) for s in s_list]
        output_string_list = [" ".join(s) for s in tk_list]
        if keep_sep:
            output_string = " [X_SEP] ".join(output_string_list)
        else:
            output_string = " ".join(output_string_list)
        output_string = " ".join(output_string.split(' ')[:max_len-1])
        fout.write('{}\n'.format(output_string))
