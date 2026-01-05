# MoaM Sans

My custom display font

![SIL Open Font License](https://openfontlicense.org/images/OFLLogoRectColor.png)

## build instructions

### illustrator -> svgs

- open moamfont.ai with adobe illustrator
- File -> Export -> Export for Screens
- export all artboards as svgs to a directory (doesnt matter where, just remember)
  - turn off include bleed
  - turn off create sub-folders
  - make sure svg has no suffix
  - any artboard that is named "Artboard sfdhjoiudf" isn't necessary, just part of the design process. deselect or delete 
  if you WANT but the script ignores them so who cares

### svgs -> fontforge

- open main.py script
- on line 7 (at time of writing) change the directory in `dir = ` to your svg directory
  - make sure it doesn't end with a \ or python will shart
- open fontforge, hit new
- file > execute script
- make sure it's on Python mode, paste the entire contents of main.py in, hit ok
- save as sfd if you want

### fontforge -> font file

- in fontforge, file -> generate fonts