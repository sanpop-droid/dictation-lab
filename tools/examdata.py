import json,re,glob,os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','exam','data')
def load(name):
    s=open(f'{D}/{name}.js',encoding='utf-8').read()
    j=s[s.index('=',s.index(']'))+1:].rstrip().rstrip(';')
    return json.loads(j)
