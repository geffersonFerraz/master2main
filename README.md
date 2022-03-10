# master2main (PT-BR)

  Pip or Pip3, geralmente é só pip, mas o pip3 deve funcionar também :x

# Pré requisitos: 
  pip install -r requirements.txt
  
  cp .env.example .env

# Configure o .env:
  PRIVATE_TOKEN= crie um token para seu usuário em https://gitlab.xpto.com/-/profile/personal_access_tokens com as seguintes permissões: api, read_user, read_api, read_repository, write_repository

  GITLAB_URL=https://gitlab.xpto.com/api/v4

  GITLAB_GROUP= ID do seu grupo, 108 é o nosso ID, conforme: https://gitlab.xpto.com/xpto/squad-xpto
  ![image](https://user-images.githubusercontent.com/13826728/157687274-773f3466-79cb-41f8-ad9d-89a11e9c2adf.png)


  VERIFY_ARCHIVED_PROJECTS= TRUE => Verificar até projetos arquivados / FALSE => Verificar apenas projetos ativos

  REMOVE_OLD_MAIN= TRUE => Remove uma branch "main" antiga que já exista no repositório / FALSE => faz nada.

  REMOVE_MASTER= TRUE => Remove a branch "master" após a conclusão da criação da "main" / FALSE => do nothing.

  PROTECT_MASTER= TRUE => Se não removida, protege a "master" contra "pushs". / FALSE => do nothing.

  SIMULATE= TRUE => Apenas faz analise e printa os logs, tipo uma simulação.. / FALSE => (DANGER) Analisa e aplica as alterações.

  JUST_TRY_WITH=0 => Aplica a analise apenas neste projeto - ID.

  JUST_TRY_ONE= TRUE => Aplica a analise e alteração apenas no primeiro projeto encontrado. / FALSE = Aplica a análise e alteração em todos os projetos do seu grupo.


# Run: 
  python3 main.py

# Log:
  Arquivo de log: "logFile.txt"
  
# Se seu time utiliza algum "FACILITY" (import .yml do gitlab.yml)
  Lembre-se de alterar nos .yml de "master" para "main"



# master2main (EN)

  Pip or Pip3, you know your machine :x 

# PRÉ Run: 
  pip install -r requirements.txt
  
  cp .env.example .env

# Change .env:
  PRIVATE_TOKEN= Generate a personal token at https://gitlab.xpto.com/-/profile/personal_access_tokens with that permissions: api, read_user, read_api, read_repository, write_repository

  GITLAB_URL=https://gitlab.xpto.com/api/v4 

  GITLAB_GROUP= Group id of your team, Group ID: 108 is our id https://gitlab.xpto.com/xpto/squad-xpto

  VERIFY_ARCHIVED_PROJECTS= TRUE => Will analyze including the archived projects / FALSE => ONLY will analyze the active projects

  REMOVE_OLD_MAIN= TRUE => WIll delete (DANGER) the branch "main" if already exists / FALSE => do nothing.

  REMOVE_MASTER= TRUE => Will delete the old "master" branch. / FALSE => do nothing.

  PROTECT_MASTER= TRUE => Will protect the old branch "master". / FALSE => do nothing.

  SIMULATE= TRUE => Just will analyze and print logs, wont do changes. / FALSE => (DANGER) Will apply changes at projects (logging with your name) ;) 

  JUST_TRY_WITH=0 => Used to just apply analyze with a single defined project.

  JUST_TRY_ONE= TRUE => Used to just apply analyze with a first listed project. / FALSE = Analyze everything respecting all other rules.


# Run: 
  python3 main.py

# Log:
  Log printed at console and inside a file "logFile.txt"
  
# IF YOU USE SOME "FACILITY" (import .yml to gitlab.yml)
  Change the references from "master" to "main"
