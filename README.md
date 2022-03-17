# vpc-get-high-scores-image

This tool will pull data and create high score images for PinUP Popper.

**Adding VPS Id to table(s) in PinUP Popper**:

1. This tool requires the use of the VPS ID from http://virtual-pinball-spreadsheet.web.app (hereby known as VPS).  The easiest way to add the VPS Id to a table is through the import process via PinUP Popper.

  **1a.** Download an updated version of the puplookup.csv from VPS to the PinUPSystem folder:
    ![image](https://user-images.githubusercontent.com/1703672/158044621-02b8ebba-1be9-4a75-b8a7-4e6cdfb711b9.png)

  **1b.** You will now need to open up the puplookup.csv file and change the last column name in the header row to the field name you want to import the VPS Id into the PinUP Popper DB.
    - Example:  I want to store the VPS ID into the Custom3 field in Game Manager.  I will change the last field to `Custom3`
 
 **1c.** You now need to import the puplookup.csv into PinUP Popper.  This is done by Pinup Popper Setup > Advanced Setup > Import CSV.   When the import completes, the VPS ID will now be imported into the field you renamed in the header, when you hit import in Game Manager.

 **1d.** You now need to re-import data for each table so it picks up the VPS ID into the field you determined in the puplookup.csv header.


**Setup the batch file to run on Windows startup**

2. Using https://github.com/ericfaris/vpc-get-high-scores-image/releases, download the following files to the `C:\Pinball\PinUPSystem\PinupPopper\LAUNCH` folder (**IMPORTANT: BE AWARE THE LAUNCH FOLDER MIGHT BE IN A DIFFERENT LOCATION IF YOU HAVE USE BALLER INSTALLER**).
    - ![image](https://user-images.githubusercontent.com/1703672/158728829-66d670e2-8521-40ed-bdd4-968cdc835c18.png)   
    

3. Open `POPMENU_GetHighScoresForAllTables.bat` and edit line 3 to conform to you folder structure.
    - "Full path of vpc-get-high-scores-image.exe" "Update High Scores For All Tables" "VPS Id" "VPS Id Field Name" "Full path to PinUP System folder" "Full path to your media folder for Other2" "max number of rows to display in score list"
    - Example: `"%_curloc%\vpc-get-high-scores-image.exe" "True" "" "CUSTOM3" "%_ParentFolderName%" "%_ParentFolderName%\POPmedia\Visual Pinball X\Other2" "10"`
        - **You will need change the CUSTOM3 field above to match the field you have chosen to house the VPS Id in Step 1 - 1d**

4. Create a shortcut to `POPMENU_GetHighScoresForAllTables.bat`

5. Copy the shortcut to your Windows startup folder

**Setup scripts to run the vpc-get-high-scores-image.exe on Launch and Close of the table**

6. Pinup Popper Setup > Popper Setup Tab > Emulators > Visual Pinball X > Launch Setup Tab
    - Paste the following at the end of 1. **Launch Script** and 2. **Close Script**:
        - `START /min "" "[STARTDIR]LAUNCH\vpc-get-high-scores-image.exe" "False" "[CUSTOM3]" "CUSTOM3" "C:\Pinball\PinUPSystem" "C:\Pinball\PinUPSystem\POPMedia\Visual Pinball X\Other2" "10"`
            - **You will need change the CUSTOM3 fields above to match the field you have chosen to house the VPS Id in Step 1 - 1d**
        
7. Save and Close

**Enable Display to Show Other2**

8. Pinup Popper Setup > Popper Setup Tab > GlobalConfig button > Displays tab
    - Set `Other 2` = `Active and Hidden`
    
9. Save

10. Pinup Popper Setup > Popper Setup Tab > Screens / Themes button

11. In Pup Pack Editor
    - Change Mode field of `Other` to `ForcePop`
    
12. Click "Save PuP-Pack" button

**Configure and Place the Other Display**

13. On the same "PuP Editor" screen, click "Configure Display/Locations" button

14. On the "PinUP Player DIsplays" window, click on `Other2` in the "Select Screen" list

15. Adjust this display to your liking.  This will be the display for the high scores.
    - Suggestions:
        - Rotation: `270`
        - Width: `2000`
        - Height: `1800`
        - Default State: `off`
        
16. Click "Save Settings" button

17. Close "PuP Pack Editor" window

**Configure key in PinUP Popper to display Other2 (the high score image)**

18. On "PinUP Popper Setup" window, click "Controller Setup" button

19. Assign key press to `Show Other` entry

20. Click "Close" button

21. On "PinUP Popper Setup" window, click "Exit Setup" button

**Test Getting High Scores**

22. Navigate to the C:\Pinball\PinUPSystem\PinupPopper\LAUNCH folder

23. Run GetAllHighScores.bat
    You should see a cmd window start executing and pulling down the images
    You should also be able to check your C:\Pinball\PinUPSystem\POPMedia\Visual Pinball     X\Other2 to see the high score images being created.

24. Run PinUP Popper

25. Navigate to a table

26. Press button to display Other2 that you set in step #19.

**Refreshing All HIgh Scores While in PinUP Popper**

27.  Get to the Operator Menu in PinUP Popper

28.  Scroll to Custom Scripts

29.  Press GetHighScoresForALlTables
