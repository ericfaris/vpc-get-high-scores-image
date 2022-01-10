# high-score-get

This tool will pull high scores for tables that are setup in the Pinup Popper DB.

**Instructions**:

Confirm correct table name and author within Pinup Popper for every table you want to show high scores.

**Setup the batch file to run on Windows startup**
Copy the latest version of vpc-get-high-scores-image into the `c:\pinball\PinupPopper\LAUNCH` folder.

Create a .bat file called `GetAllHighScores.bat` in the `c:\pinball\PinupPopper\LAUNCH` folder.

Edit the `GetAllHighScores.bat` to look like the following:
- vpc-get-high-scores-image.exe "YOUR PINUP SYSTEM FOLDER" "YOUR OTHER2 MEDIA FOLDER" "10" <--- this is max rows for high scores

Create a shortcut to `GetAllHighScores.bat`

Copy the shortcut to your Windows startup folder


**Setup scripts to run the vpc-get-high-scores-image.exe**
Pinup Popper Setup > Popper Setup Tab > Emulators > Visual Pinball X > Launch Setup Tab
    - Paste the following at the end of the Launch and Close Scripts:
        - `"[STARTDIR]LAUNCH\vpc-get-high-scores-image.exe" "[GAMENAME]" "[?Author?]" "[MEDIADIR]Other2" 10`
        
Save and Close

**Enable Display to Show Other2**

Pinup Popper Setup > Popper Setup Tab > GlobalConfig button > Displays tab
    - Set `Other 2` = `Active and Hidden`
    
Save

Pinup Popper Setup > Popper Setup Tab > Screens / Themes button

In Pup Pack Editor

    - Change Mode field of `Other` to `ForcePop`
    
Click "Save PuP-Pack" button

**Configure and Place the Other Display**
On the same "PuP Editor" screen, click "Configure Display/Locations" button
On the "PinUP Player DIsplays" window, click on `Other2` in the "Select Screen" list
Adjust this display to your liking.  This will be the display for the high scores.
    Suggestions:
        - Rotation: `270`
        - Width: `2000`
        - Height: `1800`
        - Default State: `off`
Click "Save Settings" button
Close "PuP Pack Editor" window

**Configre Key in Popper to Display Other2 (the high score image)**
On "PinUP Popper Setup" window, click "Controller Setup" button
Assign key press to `Show Other` entry
Click "Close" button
On "PinUP Popper Setup" window, click "Exit Setup" button

**Add menu option to Pinup Popper Operator menu to update all high scores on demand**
In File Explorer, navigate to `{YOUR ROOT FOLDER}\PinUPSystem` folder
Click on `PopperOperatorEdit.exe`
In the "CSVBrowserForm" window, right click on the "Show Other" row.
Click Insert Row
Within the new row, enter as follows (fields not mentioned should be empty):
    - parentMenu: home
    - display: Update High Scores
    - function: launch
    - extra1: GetAllHighScores.bat
    - ingame: 2
Click Save
Close "CVSBrowserForm" window



