[Setup]
AppName=Doki-Glass
AppVersion=1.0
DefaultDirName={autopf}\Doki-Glass
DefaultGroupName=Doki-Glass
UninstallDisplayIcon={app}\Doki-Glass.exe
Compression=lzma
SolidCompression=yes
OutputDir=..\user_output

[Files]
Source: "..\dist\main.exe"; DestName: "Doki-Glass.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Doki-Glass"; Filename: "{app}\Doki-Glass.exe"

[Run]
Filename: "{app}\Doki-Glass.exe"; Description: "Launch Doki-Glass"; Flags: nowait postinstall skipifsilent