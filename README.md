# master2main

  Pip or Pip3, you know your machine :x 

# PRÉ Run: 
  pip install -r requirements.txt
  
  cp .env-example .env

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
  pip main.py

# Log:
  Log printed at console and inside a file "logFile.txt"
  
# IF YOU USE SOME "FACILITY" (import .yml to gitlab.yml)
  Change the references from "master" to "main"
