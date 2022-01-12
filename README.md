# high-score-get

This tool will pull high scores for tables that are setup in the Pinup Popper DB.

**Instructions**:

1. Confirm correct table name and author within Pinup Popper for every table you want to show high scores. **The table name and author of each table need to match what is in the VPC Discord High Score DB, exactly!**  You will need to make those changes in the Game Manager of "Pinup Popper Setup".

**Setup the batch file to run on Windows startup**

2. Using https://github.com/ericfaris/high-score-get/releases, download the following files to the `c:\pinball\PinupPopper\LAUNCH` folder.
    - ![image](https://user-images.githubusercontent.com/1703672/148884386-6ab53c8e-c254-44a6-af6f-e38ea9a11d14.png)
    
    

3. Open `GetAllHighScores.bat` and edit line3 to conform to you folder structure.
- "Full path of vpc-get-high-scores-image.exe" "Full path to PinUP System folder" "Full path to your media folder for Other2" "max number of rows to display in score list"
- Example: `"C:\Pinball\PinUPSystem\Launch\vpc-get-high-scores-image.exe" "C:\Pinball\PinUPSystem" "C:\Pinball\PinUPSystem\POPMedia\Visual Pinball X\Other2" "10"`
    
5. Create a shortcut to `GetAllHighScores.bat`

6. Copy the shortcut to your Windows startup folder

**Setup scripts to run the vpc-get-high-scores-image.exe**

7. Pinup Popper Setup > Popper Setup Tab > Emulators > Visual Pinball X > Launch Setup Tab
    - Paste the following at the end of the **Launch** and **Close** Scripts:
        - `"[STARTDIR]LAUNCH\vpc-get-high-scores-image.exe" "[GAMENAME]" "[?Author?]" "[MEDIADIR]Other2" 10`
        
8. Save and Close

**Enable Display to Show Other2**

9. Pinup Popper Setup > Popper Setup Tab > GlobalConfig button > Displays tab
    - Set `Other 2` = `Active and Hidden`
    
10. Save

11. Pinup Popper Setup > Popper Setup Tab > Screens / Themes button

12. In Pup Pack Editor
    - Change Mode field of `Other` to `ForcePop`
    
13. Click "Save PuP-Pack" button

**Configure and Place the Other Display**

14. On the same "PuP Editor" screen, click "Configure Display/Locations" button

15. On the "PinUP Player DIsplays" window, click on `Other2` in the "Select Screen" list

16. Adjust this display to your liking.  This will be the display for the high scores.
    - Suggestions:
        - Rotation: `270`
        - Width: `2000`
        - Height: `1800`
        - Default State: `off`
        
17. Click "Save Settings" button

18. Close "PuP Pack Editor" window

**Configure key in PinUP Popper to display Other2 (the high score image)**

19. On "PinUP Popper Setup" window, click "Controller Setup" button

20. Assign key press to `Show Other` entry

21. Click "Close" button

22. On "PinUP Popper Setup" window, click "Exit Setup" button

**Add menu option to PinUP Popper Operator menu to update all high scores on demand**

23. In File Explorer, navigate to `{YOUR ROOT FOLDER}\PinUPSystem` folder

24. Click on `PopperOperatorEdit.exe`

25. In the "CSVBrowserForm" window, right click on the "Show Other" row.

26. Click Insert Row

27. Within the new row, enter as follows (fields not mentioned should be empty):
    - parentMenu: home
    - display: Update High Scores
    - function: launch
    - extra1: GetAllHighScores.bat
    - ingame: 2
    
28. Click Save

29. Close "CVSBrowserForm" window

**Test Getting High Scores**

30. Navigate to the `c:\pinball\PinupPopper\LAUNCH` folder

31. Run `GetAllHighScores.bat`
    - You should see a cmd window start executing and pulling down the images
    - You should also be able to check your `C:\Pinball\PinUPSystem\POPMedia\Visual Pinball X\Other2` to see the high score images being created.

32. Run PinUP Popper

33. Navigate to a table

34. Press button to display `Other2` that you set in step #20.


**High Score Image Explanations**


**Problem:** The message indicates that the table name and/or author name does not exist in Popper.

**Solution:** Modify the table name and author name in Popper to exactly match what is found in the VPC high-scores channel.




**Problem:** The message indicates that the table name and/or author name exists in Popper, but was not found in the VPC high-scores database.

**Solution:** Modify the table name and author name in Popper to exactly match what is found in the VPC high-scores channel.




**Problem:** The message indicates that the table and author was a match, but no high scores were found.

**Solution:** Score needs to be added via Discord.
