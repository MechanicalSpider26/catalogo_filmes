# Sistema de Gerenciamento de Acervo de Cinema

**Aluno:** Guilherme Ferreira Prates Amaral 
**Matrícula:** 202603181057
**Domínio Escolhido:** Gerenciamento de Filmes e Diretores de Cinema  

---

## Como Rodar a Aplicação do Zero

Siga os passos abaixo no terminal para configurar o ambiente e executar o projeto:

### 1. Clonar o repositório (caso aplicável) e navegar até a pasta
```bash
cd seu_projeto
```

### 2. Criar e ativar o ambiente virtual (.venv)

```bash
- Linux / macOS:
    python3 -m venv .venv
```
```bash
- Windows (PowerShell):
    python -m venv .venv
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```


### 4. Popular o banco de dados inicial
Execute o script de inicialização para criar as tabelas e inserir os dados iniciais do acervo:

```bash
python dados_iniciais.py
```

### 5. Executar a aplicação Flask

```bash
python app.py
```

Acesse a aplicação no navegador através do endereço: http://127.0.0.1:5000


### Lista de Rotas

Método,Rota,Descrição
GET,/,Página inicial com listagem geral dos filmes
GET,/diretores,Lista todos os diretores cadastrados e total de filmes vinculados
"GET, POST",/cadastrar_filme (ou /novo),Formulário e ação de cadastro de um novo filme
"GET, POST",/cadastrar_diretor,Formulário e ação de cadastro de um novo diretor
GET,/filme/<id>,Detalhes do filme selecionado e dados do seu diretor
GET,/diretores/<id>,Perfil do diretor e lista de filmes por ele dirigidos
GET,/buscar,"Busca de filmes por título, gênero ou nome do diretor"
"GET, POST",/filme/<id>/editar,Form e atualização dos dados de um filme existente
"GET, POST",/diretores/<id>/editar,Form e atualização dos dados de um diretor
POST,/filme/<id>/excluir,Remoção de um filme do banco de dados
POST,/diretores/<id>/deletar,Remoção de um diretor e atualização/deleção em cascata
POST,/filme/<id>/sinopse,Atualização rápida da sinopse na página de detalhes

### Regras de Validação Implementadas
#### Entidade Diretor

    Nome Válido: Deve conter no mínimo 2 caracteres e não pode ser vazio.

    Nacionalidade: Deve conter no mínimo 2 caracteres.

    Data de Nascimento: Campo de preenchimento obrigatório.

    Unicidade no Banco: Consulta via SELECT impede a inserção de diretores com o mesmo nome já cadastrado.


#### Entidade Filme

    Campos Textuais Mínimos: Título, Gênero e Estúdio exigem no mínimo 2 caracteres.

    Ano de Lançamento: Deve ser um valor numérico inteiro compreendido entre 1888 (surgimento do cinema) e 2026.

    Nota de Avaliação: Deve ser um número decimal entre 0.0 e 10.0.

    Seleção de Diretor: Obrigatoriedade de vínculo a um diretor válido existente ou recém-criado.

    Unicidade no Banco: Validação direta via SELECT que impede o cadastro de filmes com títulos duplicados.

Nenhum requisito obrigatório ficou pendente. Todas as funcionalidades de CRUD (Listar, Detalhar, Cadastrar, Editar, Excluir e Buscar), tratamento de erro 404, retenção de formulário, validação de banco de dados, isolamento da arquitetura e script de dados iniciais foram implementadas e testadas com sucesso.