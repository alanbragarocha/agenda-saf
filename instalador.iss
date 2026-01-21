; Script de Instalação Inno Setup para Editor de Agenda SAFs
; Para compilar, instale Inno Setup: https://jrsoftware.org/isinfo.php

#define MyAppName "Editor de Agenda SAFs"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Federação de SAFs"
#define MyAppURL ""
#define MyAppExeName "EditorAgendaSAF.exe"

[Setup]
; Informações básicas
AppId={{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=
OutputDir=dist
OutputBaseFilename=InstaladorAgendaSAFs
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

; Idioma
[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

; Arquivos a serem instalados
[Files]
Source: "editar_agenda_gui.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "gerar_agenda.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "gerar_com_fotos.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "extrair_fotos.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "agenda_data.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "fotos\*"; DestDir: "{app}\fotos"; Flags: ignoreversion recursesubdirs createallsubdirs
; Se você já tiver um executável compilado:
; Source: "dist\EditorAgendaSAF.exe"; DestDir: "{app}"; Flags: ignoreversion

; Atalhos
[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

; Executáveis
[Run]
Filename: "python"; Parameters: "-m pip install -r ""{app}\requirements.txt"""; StatusMsg: "Instalando dependências..."; Flags: runhidden
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

; Código de inicialização
[Code]
procedure InitializeWizard;
begin
  // Verificar se Python está instalado
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.11\InstallPath', '', PythonPath) then
  begin
    if not RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.10\InstallPath', '', PythonPath) then
    begin
      if not RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.9\InstallPath', '', PythonPath) then
      begin
        MsgBox('Python não encontrado! Por favor, instale Python 3.8+ primeiro.', mbError, MB_OK);
        Abort;
      end;
    end;
  end;
end;
