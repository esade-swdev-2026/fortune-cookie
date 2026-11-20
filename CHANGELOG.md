# Changelog

## v0.7

- Add a categories command that lists every category once
- Reject a fortune that already exists when adding one
- Add a Dockerfile to run the app in a container
- Ignore case when matching categories
- Show the cleaned text when a fortune is added
- Create the data folder only when something is saved
- Show in the README that Docker data survives in a named volume

## v0.6

- Add a Commands section to the README explaining every command
- Add list_categories to return each category once, sorted
- Add a contributing guide with our rules for branches, commits and pull requests

## v0.5

- Move all file reading and writing into file_storage.py
- Make --lucky-number set how many lucky numbers are printed
- Update the README layout and remove the licence placeholders
