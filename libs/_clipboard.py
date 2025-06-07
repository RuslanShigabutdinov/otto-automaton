import win32clipboard

def getContentFromClipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    
    cleaned = data.strip()
    return cleaned