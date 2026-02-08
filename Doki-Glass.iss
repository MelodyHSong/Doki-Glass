; ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
; ☆ Author: ☆ MelodyHSong ☆
; ☆ Program: Doki-Glass v1.2.0a 
; ☆ Language: Delphi (Inno Setup)
; ☆ License: MIT
; ☆ Date: 2026-02-08
; ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

[Setup]
AppName=Doki-Glass
AppVersion=1.2.0a
AppPublisher=MelodyHSong
AppPublisherURL=https://github.com/MelodyHSong/Doki-Glass
DefaultDirName={autopf}\Doki-Glass
DefaultGroupName=Doki-Glass
UninstallDisplayIcon={app}\Doki-Glass.exe
Compression=lzma
SolidCompression=yes
OutputDir=user_output
OutputBaseFilename=Doki-Glass-Installer
; Ensure these paths match your local repository structure
SetupIconFile={#SourcePath}\assets\icon.ico
LicenseFile={#SourcePath}\docs\LICENSE.txt
; Force administrative privileges to match the executable's manifest
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
UsedUserAreasWarning=no

[Registry]
; Ensures the "Run at Startup" entry is removed when the user uninstalls
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "Doki-Glass"; ValueData: """{app}\Doki-Glass.exe"""; Flags: uninsdeletevalue

[Files]
Source: "{#SourcePath}\dist\Doki-Glass.exe"; DestName: "Doki-Glass.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Doki-Glass"; Filename: "{app}\Doki-Glass.exe"
Name: "{group}\Visit Doki-Glass on GitHub"; Filename: "https://github.com/MelodyHSong/Doki-Glass"
; Optional desktop shortcut
Name: "{autodesktop}\Doki-Glass"; Filename: "{app}\Doki-Glass.exe"; IconFilename: "{app}\Doki-Glass.exe"

[Run]
; 'shellexec' is critical here to allow the Windows Shell to handle the UAC elevation
Filename: "{app}\Doki-Glass.exe"; Description: "Launch Doki-Glass"; Flags: nowait postinstall skipifsilent shellexec