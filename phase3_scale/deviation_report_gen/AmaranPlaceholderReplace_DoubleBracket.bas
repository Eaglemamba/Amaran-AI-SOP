Option Explicit

'================================================================
' Amaran Placeholder Replacement Macro (Copilot version)
' [[double bracket]] format
'================================================================

'===============================
' Main Entry (Interactive Menu)
'===============================
Sub ReplaceTokens_UI()
    Dim choice As VbMsgBoxResult
    Dim jsonText As String
    
    choice = MsgBox( _
        "Select input method:" & vbCrLf & vbCrLf & _
        "Yes  = Paste JSON string" & vbCrLf & _
        "No   = Load from JSON file" & vbCrLf & _
        "Cancel = Abort", _
        vbYesNoCancel + vbQuestion, "Amaran [[Placeholder]] Replace")
    
    If choice = vbYes Then
        jsonText = InputBox( _
            "Paste flat JSON:" & vbCrLf & vbCrLf & _
            "Example: {""batch_number"":""90001"",""product"":""AX251 Placebo""}" & vbCrLf & vbCrLf & _
            "Limit ~1024 chars. For large JSON use file import.", _
            "Paste JSON")
        If Trim$(jsonText) = "" Then Exit Sub
        Call ReplaceTokens_Core(jsonText)
        
    ElseIf choice = vbNo Then
        Dim path As String
        path = PickJsonFilePath()
        If Len(path) = 0 Then Exit Sub
        
        jsonText = ReadTextAutoEncoding(path)
        If Len(Trim$(jsonText)) = 0 Then
            MsgBox "File is empty or unreadable.", vbExclamation
            Exit Sub
        End If
        Call ReplaceTokens_Core(jsonText)
        
    Else
        Exit Sub
    End If
End Sub

'===============================
' Core: Parse JSON + Replace
'===============================
Private Sub ReplaceTokens_Core(ByVal json As String)
    Dim dict As Object
    Dim k As Variant
    Dim totalReplaced As Long
    Dim undoScope As Word.UndoRecord
    
    Set dict = ParseFlatJsonToDict(json)
    If dict Is Nothing Or dict.Count = 0 Then
        MsgBox "No key/value pairs found." & vbCrLf & _
               "Expected flat JSON: {""key"":""value""}", vbExclamation
        Exit Sub
    End If
    
    Set undoScope = Application.UndoRecord
    undoScope.StartCustomRecord "ReplaceTokensFromJson"
    
    Application.ScreenUpdating = False
    Application.Options.ReplaceSelection = True
    
    totalReplaced = 0
    For Each k In dict.Keys
        '=== KEY CHANGE: [[double brackets]] ===
        totalReplaced = totalReplaced + ReplaceEverywhere("[[" & CStr(k) & "]]", CStr(dict(k)))
    Next k
    
    UpdateAllFields
    
    Application.ScreenUpdating = True
    undoScope.EndCustomRecord
    
    MsgBox "Done! Replaced " & totalReplaced & " instances.", vbInformation
End Sub

'===============================
' File Picker
'===============================
Private Function PickJsonFilePath() As String
    Dim fd As FileDialog
    Dim res As Integer
    
    Set fd = Application.FileDialog(msoFileDialogFilePicker)
    With fd
        .AllowMultiSelect = False
        .Title = "Select JSON File"
        .Filters.Clear
        .Filters.Add "JSON", "*.json"
        .Filters.Add "Text", "*.txt;*.log"
        .Filters.Add "All", "*.*"
        res = .Show
        If res = -1 Then
            PickJsonFilePath = .SelectedItems(1)
        Else
            PickJsonFilePath = ""
        End If
    End With
End Function

'===============================
' Auto-Encoding File Reader
'===============================
Private Function ReadTextAutoEncoding(ByVal filePath As String) As String
    Dim bytes() As Byte
    Dim fnum As Integer
    Dim txt As String
    
    On Error GoTo FAIL
    
    fnum = FreeFile
    Open filePath For Binary As #fnum
    If LOF(fnum) = 0 Then
        Close #fnum
        ReadTextAutoEncoding = ""
        Exit Function
    End If
    
    ReDim bytes(LOF(fnum) - 1)
    Get #fnum, , bytes
    Close #fnum
    
    ' Check BOM
    If UBound(bytes) >= 2 Then
        If bytes(0) = &HEF And bytes(1) = &HBB And bytes(2) = &HBF Then
            txt = BytesToString_UTF8(bytes, 3)
            ReadTextAutoEncoding = txt
            Exit Function
        End If
    End If
    If UBound(bytes) >= 1 Then
        If bytes(0) = &HFF And bytes(1) = &HFE Then
            txt = BytesToString_UTF16LE(bytes, 2)
            ReadTextAutoEncoding = txt
            Exit Function
        ElseIf bytes(0) = &HFE And bytes(1) = &HFF Then
            txt = BytesToString_UTF16BE(bytes, 2)
            ReadTextAutoEncoding = txt
            Exit Function
        End If
    End If
    
    txt = BytesToString_UTF8(bytes, 0)
    If LenB(txt) > 0 Then
        ReadTextAutoEncoding = txt
        Exit Function
    End If
    
    ReadTextAutoEncoding = BytesToString_ANSI(bytes)
    Exit Function

FAIL:
    On Error Resume Next
    If fnum <> 0 Then Close #fnum
    ReadTextAutoEncoding = ""
End Function

Private Function BytesToString_UTF8(ByRef bytes() As Byte, ByVal offset As Long) As String
    Dim stm As Object
    On Error GoTo FAIL
    Set stm = CreateObject("ADODB.Stream")
    With stm
        .Type = 1
        .Open
        .Write bytes
        .Position = offset
        .Type = 2
        .Charset = "utf-8"
        BytesToString_UTF8 = .ReadText
        .Close
    End With
    Exit Function
FAIL:
    BytesToString_UTF8 = ""
End Function

Private Function BytesToString_UTF16LE(ByRef bytes() As Byte, ByVal offset As Long) As String
    Dim i As Long, cnt As Long
    Dim arr() As Byte
    cnt = UBound(bytes) - offset + 1
    If cnt <= 0 Then BytesToString_UTF16LE = "": Exit Function
    ReDim arr(cnt - 1)
    For i = 0 To cnt - 1
        arr(i) = bytes(offset + i)
    Next
    BytesToString_UTF16LE = arr
End Function

Private Function BytesToString_UTF16BE(ByRef bytes() As Byte, ByVal offset As Long) As String
    Dim i As Long, cnt As Long
    Dim arr() As Byte, tmp As Byte
    cnt = UBound(bytes) - offset + 1
    If cnt <= 0 Then BytesToString_UTF16BE = "": Exit Function
    ReDim arr(cnt - 1)
    For i = 0 To cnt - 1
        arr(i) = bytes(offset + i)
    Next
    For i = 0 To cnt - 1 Step 2
        tmp = arr(i)
        arr(i) = arr(i + 1)
        arr(i + 1) = tmp
    Next
    BytesToString_UTF16BE = arr
End Function

Private Function BytesToString_ANSI(ByRef bytes() As Byte) As String
    BytesToString_ANSI = StrConv(bytes, vbUnicode)
End Function

'===============================
' JSON Parser (flat "key":"value")
'===============================
Private Function ParseFlatJsonToDict(ByVal json As String) As Object
    Dim re As Object, matches As Object, m As Object
    Dim dict As Object
    Dim key As String, val As String
    
    On Error GoTo CleanFail
    Set re = CreateObject("VBScript.RegExp")
    re.Global = True
    re.IgnoreCase = False
    re.MultiLine = True
    re.Pattern = """([^""]+)""\s*:\s*""([^""]*)"""
    
    Set dict = CreateObject("Scripting.Dictionary")
    Set matches = re.Execute(json)
    For Each m In matches
        key = JsonUnescape(CStr(m.SubMatches(0)))
        val = JsonUnescape(CStr(m.SubMatches(1)))
        If Len(key) > 0 Then dict(key) = val
    Next
    Set ParseFlatJsonToDict = dict
    Exit Function
CleanFail:
    Set ParseFlatJsonToDict = Nothing
End Function

Private Function JsonUnescape(ByVal s As String) As String
    s = Replace$(s, "\n", vbLf)
    s = Replace$(s, "\r", vbCr)
    s = Replace$(s, "\t", vbTab)
    s = Replace$(s, "\/", "/")
    s = Replace$(s, "\\", "\")
    s = Replace$(s, "\" & Chr$(34), Chr$(34))
    JsonUnescape = s
End Function

'===============================
' Global Replace (StoryRanges + Headers/Footers + Shapes)
'===============================
Private Function ReplaceEverywhere(ByVal findText As String, ByVal replText As String) As Long
    Dim cnt As Long
    Dim story As Word.Range
    Dim sec As Section
    
    cnt = 0
    
    For Each story In ActiveDocument.StoryRanges
        cnt = cnt + ReplaceInRange(story, findText, replText)
        Do While Not story.NextStoryRange Is Nothing
            Set story = story.NextStoryRange
            cnt = cnt + ReplaceInRange(story, findText, replText)
        Loop
    Next story
    
    cnt = cnt + ReplaceInShapes(ActiveDocument.Shapes, findText, replText)
    
    For Each sec In ActiveDocument.Sections
        cnt = cnt + ReplaceInRange(sec.Headers(wdHeaderFooterFirstPage).Range, findText, replText)
        cnt = cnt + ReplaceInRange(sec.Headers(wdHeaderFooterPrimary).Range, findText, replText)
        cnt = cnt + ReplaceInRange(sec.Headers(wdHeaderFooterEvenPages).Range, findText, replText)
        cnt = cnt + ReplaceInShapes(sec.Headers(wdHeaderFooterFirstPage).Shapes, findText, replText)
        cnt = cnt + ReplaceInShapes(sec.Headers(wdHeaderFooterPrimary).Shapes, findText, replText)
        cnt = cnt + ReplaceInShapes(sec.Headers(wdHeaderFooterEvenPages).Shapes, findText, replText)
        
        cnt = cnt + ReplaceInRange(sec.Footers(wdHeaderFooterFirstPage).Range, findText, replText)
        cnt = cnt + ReplaceInRange(sec.Footers(wdHeaderFooterPrimary).Range, findText, replText)
        cnt = cnt + ReplaceInRange(sec.Footers(wdHeaderFooterEvenPages).Range, findText, replText)
        cnt = cnt + ReplaceInShapes(sec.Footers(wdHeaderFooterFirstPage).Shapes, findText, replText)
        cnt = cnt + ReplaceInShapes(sec.Footers(wdHeaderFooterPrimary).Shapes, findText, replText)
        cnt = cnt + ReplaceInShapes(sec.Footers(wdHeaderFooterEvenPages).Shapes, findText, replText)
    Next sec
    
    ReplaceEverywhere = cnt
End Function

Private Function ReplaceInShapes(ByVal shapesColl As Shapes, _
                                 ByVal findText As String, _
                                 ByVal replText As String) As Long
    Dim shp As Shape, c As Long
    c = 0
    On Error Resume Next
    For Each shp In shapesColl
        If shp.Type = msoGroup Then
            c = c + ReplaceInGroupItems(shp.GroupItems, findText, replText)
        Else
            If shp.TextFrame.HasText Then
                c = c + ReplaceInRange(shp.TextFrame.TextRange, findText, replText)
            End If
            If shp.TextFrame2.HasText Then
                c = c + ReplaceInRange(shp.TextFrame2.TextRange, findText, replText)
            End If
        End If
    Next shp
    On Error GoTo 0
    ReplaceInShapes = c
End Function

Private Function ReplaceInGroupItems(ByVal grp As GroupShapes, _
                                     ByVal findText As String, _
                                     ByVal replText As String) As Long
    Dim i As Long, c As Long
    c = 0
    On Error Resume Next
    For i = 1 To grp.Count
        If grp(i).Type = msoGroup Then
            c = c + ReplaceInGroupItems(grp(i).GroupItems, findText, replText)
        Else
            If grp(i).TextFrame.HasText Then
                c = c + ReplaceInRange(grp(i).TextFrame.TextRange, findText, replText)
            End If
            If grp(i).TextFrame2.HasText Then
                c = c + ReplaceInRange(grp(i).TextFrame2.TextRange, findText, replText)
            End If
        End If
    Next i
    On Error GoTo 0
    ReplaceInGroupItems = c
End Function

Private Function ReplaceInRange(ByVal target As Object, _
                                ByVal findText As String, _
                                ByVal replText As String) As Long
    Dim r As Object
    Dim c As Long
    c = 0
    Set r = target.Duplicate
    
    With r.Find
        .ClearFormatting
        .Replacement.ClearFormatting
        .Text = findText
        .Forward = True
        .Wrap = wdFindStop
        .Format = False
        .MatchCase = False
        .MatchWholeWord = False
        .MatchWildcards = False
        .MatchSoundsLike = False
        .MatchAllWordForms = False
    End With
    
    Do While r.Find.Execute
        r.Text = replText
        c = c + 1
        r.Collapse wdCollapseEnd
        r.Find.Text = findText
    Loop
    
    ReplaceInRange = c
End Function

Private Sub UpdateAllFields()
    Dim s As Section, hf As HeaderFooter
    On Error Resume Next
    ActiveDocument.Fields.Update
    For Each s In ActiveDocument.Sections
        For Each hf In s.Headers
            hf.Range.Fields.Update
        Next hf
        For Each hf In s.Footers
            hf.Range.Fields.Update
        Next hf
    Next s
    On Error GoTo 0
End Sub
