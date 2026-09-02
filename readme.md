## Projeto mini-ORM-Fatec

* convenção de uso, nome envolvidos por **colchete** devem ser subistuidos pelos valores reais;

1. para iniciar o projeto crie o ambiente virtual:

```python
python -m venv myvirtual
```
2. ativar ambiente virtual
```bash
source .\myvirtual\Scripts\activate
```
Atualiza o pip para versão mais recente
python.exe -m pip install --upgrade pip

3. para instalar as dependencias
```bash
pip install -r requeriments.txt
```

4. para rodar o projeto execute:
```bash
py server.py
```

caminho das pedras para versionamento via git

1. criar branch para trabalhar na atividade

```bash
git checkout -b [aula-14]
```
ou 
```
git branch [aula-14]
git checkout  [aula-14]
```

2. terminou a atividade
```
git add .
git commit -m "concluido atividade [aula-14]
# git push
git checkout main
git merge [aula-14]
# git push
```
