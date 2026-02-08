[Setup]
AppName=Doki-Glass
AppVersion=1.0.0a
AppPublisher=MelodyHSong
AppPublisherURL=https://github.com/MelodyHSong/Doki-Glass
DefaultDirName={autopf}\Doki-Glass
DefaultGroupName=Doki-Glass
UninstallDisplayIcon={app}\Doki-Glass.exe
Compression=lzma
SolidCompression=yes
OutputDir=user_output
OutputBaseFilename=Doki-Glass-Installer
SetupIconFile={#SourcePath}\assets\icon.ico
LicenseFile={#SourcePath}\LICENSE.txt

[Files]
Source: "{#SourcePath}\dist\Doki-Glass.exe"; DestName: "Doki-Glass.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Doki-Glass"; Filename: "{app}\Doki-Glass.exe"
Name: "{group}\Visit Doki-Glass on GitHub"; Filename: "https://github.com/MelodyHSong/Doki-Glass"

[Run]
Filename: "{app}\Doki-Glass.exe"; Description: "Launch Doki-Glass"; Flags: nowait postinstall skipifsilent
Filename: "notepad.exe"; Parameters: "{app}\README.md"; Description: "View the README file"; Flags: postinstall shellexec skipifsilent unchecked