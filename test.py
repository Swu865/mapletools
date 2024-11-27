import pygetwindow as gw

def filter_windows(keywords):
    all_windows = gw.getAllTitles()
    filtered_windows = [title for title in all_windows if any(keyword in title for keyword in keywords)]
    return filtered_windows

# Specify keywords to look for in window titles
keywords = ["Remote Desktop Connection", "远程"]
filtered_titles = filter_windows(keywords)

print(filtered_titles)
