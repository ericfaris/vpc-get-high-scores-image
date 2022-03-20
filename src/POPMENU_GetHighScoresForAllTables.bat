CD /d %~dp0
set _curloc=%~dp0
for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set _ParentFolderName=%%~dpnxJ
echo %_ParentFolderName%
echo %_curloc%

start playsound UpdateHighScoreStart.mp3

"%_curloc%\vpc-get-high-scores-image.exe" "True" "" "CUSTOM3" "%_ParentFolderName%" "%_ParentFolderName%\POPmedia\Visual Pinball X\Other2" "10" ""

start playsound UpdateHighScoreStop.mp3
