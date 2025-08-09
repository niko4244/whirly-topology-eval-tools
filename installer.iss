; Inno Setup script for WHIRLY one-click installer
[Setup]
AppName=WHIRLY
AppVersion=1.0
DefaultDirName={pf}\WHIRLY
DefaultGroupName=WHIRLY
UninstallDisplayIcon={app}\WHIRLY.exe
OutputBaseFilename=WHIRLYSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\WHIRLY.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\logo_whirlpool_50s.png"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\WHIRLY"; Filename: "{app}\WHIRLY.exe"; IconFilename: "{app}\logo_whirlpool_50s.png"
Name: "{userdesktop}\WHIRLY"; Filename: "{app}\WHIRLY.exe"; IconFilename: "{app}\logo_whirlpool_50s.png"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\WHIRLY.exe"; Description: "Launch WHIRLY"; Flags: nowait postinstall skipifsilent