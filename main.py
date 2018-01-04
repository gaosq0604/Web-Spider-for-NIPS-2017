import re
import requests
import pandas as pd

def main():
    # Get content
    url = "https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017"
    session = requests.Session()
    response = session.get(url)
    content = response.content.decode()
    
    # Regular experssions
    expPaper = '(<li><a href="/paper.*?</li>)'
    expTitle = '">(.*?)</a> '
    expAuthor = 'class="author">(.*?)</a>'
    
    # Get all paper items and initialize memories
    allPapers = list(re.compile(expPaper).findall(content))
    numPapers = len(allPapers)
    titles = [""] * numPapers
    authors = [()] * numPapers
    
    # Get all titles and corresponding authors respectively
    for idxPaper in range(numPapers):
        titles[idxPaper] = re.compile(expTitle).findall(allPapers[idxPaper])[0]
        authors[idxPaper] = list(re.compile(expAuthor).findall(allPapers[idxPaper]))
    
    # Structuring using pandas
    df = pd.DataFrame({"Title": titles, 
                       "Authors": [", ".join(author) for author in authors]})
    df.index.name = "No."
    return df

df = main()
df.head()
df.to_csv("./NIPS2017.txt", sep=",")