import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from io import BytesIO

def process_pdf(file: bytes) ->str:
    """Extract text from the pdf file

    Args:
        file (bytes): Raw bytes content of the pdf file

    Returns:
        str: Clean text content extracted from the pdf file as a string
    """
    text = ""

    #Create a file-like content object from the byte content
    file_content = BytesIO(file)

    reader = PdfReader(file_content)
    for page in reader.pages:
        text += page.extract_text() or " " # or handles the none case
    print(f"Extracted {len(text)} characters from the pdf document")
    return text


def process_url(url):
    """Scrap and extract clean text from a website

    Args:
        url (str): The url of the website
    Returns:
        str: Clearn text content extracted from the web url
    """
    try:
        response = requests.get(url, headers={"User-Agent": "mozila/5.0"})
        response.raise_for_status() #Raise exception for bad status code
        soup = BeautifulSoup(response.content, "html.parser")

        #Remove scripts or styles
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        text = soup.get_text(separator='', strip=True)
        print(f"Extracted: {len(text)} from the url.")
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetch {url}: {e}")
    return " "
    
def process_csv(csv):
    pass

def process_word_document(document):
    pass
