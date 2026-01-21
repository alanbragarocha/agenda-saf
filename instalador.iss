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
; SetupIconFile=agenda_icon.ico  ; Descomente se tiver o arquivo agenda_icon.ico
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
Source: "extrair_fotos.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "agenda_data.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "agenda_data_exemplo.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "executar_agenda.vbs"; DestDir: "{app}"; Flags: ignoreversion
Source: "agenda_icon.ico"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists(ExpandConstant('{src}\agenda_icon.ico'))
Source: "agenda_icon.png"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists(ExpandConstant('{src}\agenda_icon.png'))
; Se você já tiver um executável compilado, descomente a linha abaixo e comente as linhas dos arquivos .py acima:
; Source: "dist\EditorAgendaSAF.exe"; DestDir: "{app}"; Flags: ignoreversion

; Atalhos
[Icons]
Name: "{group}\{#MyAppName}"; Filename: "wscript.exe"; Parameters: """{app}\executar_agenda.vbs"""; WorkingDir: "{app}"; IconFilename: "{code:GetIconPath}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "wscript.exe"; Parameters: """{app}\executar_agenda.vbs"""; WorkingDir: "{app}"; Tasks: desktopicon; IconFilename: "{code:GetIconPath}"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

; Executáveis
[Run]
Filename: "python.exe"; Parameters: "-m pip install -r ""{app}\requirements.txt"""; StatusMsg: "Instalando dependências..."; Flags: runhidden waituntilterminated
; Opcional: Executar o programa após instalação (descomente se desejar)
; Filename: "python.exe"; Parameters: """{app}\editar_agenda_gui.py"""; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent; WorkingDir: "{app}"

; Código de inicialização
[Code]
var
  PythonFound: Boolean;

function CheckPythonInstalled(): Boolean;
var
  Version: String;
  Versions: TArrayOfString;
  I: Integer;
  PythonPath: String;
begin
  Result := False;
  PythonPath := '';

  // Lista de versões para verificar
  SetArrayLength(Versions, 5);
  Versions[0] := '3.12';
  Versions[1] := '3.11';
  Versions[2] := '3.10';
  Versions[3] := '3.9';
  Versions[4] := '3.8';

  // Verificar em HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore
  for I := 0 to GetArrayLength(Versions) - 1 do
  begin
    Version := Versions[I];
    if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\' + Version + '\InstallPath', '', PythonPath) then
    begin
      Result := True;
      Exit;
    end;
  end;

  // Verificar em HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Python\PythonCore (32-bit em 64-bit)
  for I := 0 to GetArrayLength(Versions) - 1 do
  begin
    Version := Versions[I];
    if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\WOW6432Node\Python\PythonCore\' + Version + '\InstallPath', '', PythonPath) then
    begin
      Result := True;
      Exit;
    end;
  end;

  // Verificar em HKEY_CURRENT_USER (instalação do usuário)
  for I := 0 to GetArrayLength(Versions) - 1 do
  begin
    Version := Versions[I];
    if RegQueryStringValue(HKEY_CURRENT_USER, 'SOFTWARE\Python\PythonCore\' + Version + '\InstallPath', '', PythonPath) then
    begin
      Result := True;
      Exit;
    end;
  end;
end;

procedure InitializeWizard;
var
  ResultCode: Integer;
begin
  PythonFound := CheckPythonInstalled();

  if not PythonFound then
  begin
    if MsgBox('Python não encontrado automaticamente!' + #13#10 + #13#10 +
              'Você tem Python 3.8 ou superior instalado?' + #13#10 + #13#10 +
              'Clique em SIM para continuar mesmo assim (você precisará ter Python instalado).' + #13#10 +
              'Clique em NÃO para cancelar e instalar Python primeiro.',
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      ShellExec('open', 'https://www.python.org/downloads/', '', '', SW_SHOWNORMAL, ewNoWait, ResultCode);
      Abort;
    end;
  end;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
end;

function GetIconPath(Param: String): String;
begin
  if FileExists(ExpandConstant('{app}\agenda_icon.ico')) then
    Result := ExpandConstant('{app}\agenda_icon.ico')
  else if FileExists(ExpandConstant('{app}\agenda_icon.png')) then
    Result := ExpandConstant('{app}\agenda_icon.png')
  else
    Result := ExpandConstant('{sys}\shell32.dll,23');
end;
