Set WshShell = CreateObject("WScript.Shell")

' 启动 Faster Whisper Server（完全后台）
WshShell.Run "cmd /c """"C:\Users\taosu\AppData\Local\Programs\Python\Python311\python.exe"" -m faster_whisper_server --host 127.0.0.1 --port 8800 medium""", 0, False

' 等待服务就绪
Dim i
For i = 1 To 60
    WScript.Sleep 1000
    On Error Resume Next
    Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "GET", "http://127.0.0.1:8800/health", False
    http.Send
    If http.Status = 200 Then
        Exit For
    End If
    On Error GoTo 0
Next

' 启动 OpenTypeless release 版本
WshShell.Run "D:\Documents\OpenTypeless\src-tauri\target\release\opentypeless.exe", 0, False
