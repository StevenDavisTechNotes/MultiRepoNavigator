# Roadmap

## Project Picker

- Debounce the project picker so that it waits for 25 ms before querying the backend

## Display Source File

- In the navigator replace the current <ul> with an indented series of SourceFile components
- Each SourceFile component displays the file name and the module name (URL)
- There is an open checkbox to open the SourceFile
- If open, there are 0 or more Function displayed below the SourceFile

## Display Function

- Each Function component displays the function name and import statement
  - Includes a copy-to-clipboard button
- Below the Function display an indented series of related FunctionHead components
- There is are buttons:
  - A Sync button to apply changes to all related function implementations
  - A Refresh button 

## Display Function Head

- Each FunctionHead component displays the function name and arguments
  - Includes a copy-to-clipboard button
- Below the Function Head display an indented series of related FunctionImpl components
- There is are buttons:
  - A Sync button to apply changes to all related function implementations
  - A Refresh button 

## Display FunctionImpl

- Each FunctionImpl component displays the function name and import statement
  - Includes a copy-to-clipboard button
- The following actions have buttons
  - Display opens a modal with the function source code
  - Transform opens a modal with transformed function source code
  - Untransform opens a modal with function source code transformation reversed

## Source Code Editor

- Displays the function name and arguments
  - Includes a copy-to-clipboard button
- The FunctionImpl opened the SourceCodeEditor component in a modal.
- The SourceCodeEditor displays the source code of the function
- The SourceCodeEditor has buttons:
  - A Save button to save the source code
  - A Cancel button to cancel the source code
  - A Close button to close the modal
  - A Format button to format the source code
- The FunctionHead component and its children are updated when the modal closes

## Source Code Search

- When Navigator opens, query the backend for the source code tree using the default search of "".

## Add the ability to add, edit, or remove a project folder

- Add an edit button to the Navigator to the right of the ProjectPicker
- Clicking on this button opens a new ProjectFolder page within the project_folder area
- There is a list of known project folders
- This page has a form to add or edit project folders
  - Clicking a known project folder populates the form
- There is a button to save the project folder
- There is a button to delete the project folder
- Upen save/delete the project folder list is requeried
- There is a button to close the page and return to the Navigator
- Add error handling in the Navigator if all project folders have been deleted
- When ready, remove the remove_file_if_exists of the DATABASE_FILE_PATH

## Add a file watcher to the project folders (Hold off for now)

- Rather than walk the source code tree with each request, add a file watcher to the project folders
- Hold the file tree in the sqlite database source_code_cache
  - Truncate and load on startup
  - Update it when a file is added, removed, or changed
- Change the backend implementations to the source_code_cache
- Add a button to the ProjectFolder page to truncate and refresh the source_code_cache

