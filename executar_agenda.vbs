Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
WshShell.CurrentDirectory = fso.GetParentFolderName(WScript.ScriptFullName)

' Tentar usar pythonw.exe primeiro (sem janela de console)
On Error Resume Next
WshShell.Run "pythonw.exe editar_agenda_gui.py", 0, False
If Err.Number <> 0 Then
    Err.Clear
    ' Se pythonw não existir, usar python.exe (pode mostrar janela brevemente)
    WshShell.Run "python.exe editar_agenda_gui.py", 0, False
End If
On Error Goto 0

Set WshShell = Nothing
Set fso = Nothing
