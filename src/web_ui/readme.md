# web_ui

## Installation

```sh
cd src/web_ui/frontend; npm install
```

## Useful Snippets

<!-- cSpell: ignore uvicorn -->

uvicorn src.web_ui.backend.main:app --reload --port 4059 --reload-dir src --reload-exclude src/web_ui/frontend
### From Linux / WSL
cd src/web_ui/frontend
npm start
### From Windows
cd src\web_ui\frontend
npm run windows-start
<http://127.0.0.1:4059/docs>
<http://localhost:4060/>

$ sqlite3 _data/web_ui/multi_repo_navigator.db
SQLite version 3.37.2 2022-01-06 13:25:41
Enter ".help" for usage hints.
sqlite> .tables
func_def_fav    project_folder
sqlite> select * from project_folder;
sqlite> .quit
