# parser.py

import os
import zipfile
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from config import UNZIPPED_DIR

def unzip_and_soupify(filepath):
    """Unzip the file and parse the XML."""
    if not os.path.exists(UNZIPPED_DIR):
        os.makedirs(UNZIPPED_DIR)
    
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(UNZIPPED_DIR)
    
    xml_file = next((f for f in os.listdir(UNZIPPED_DIR) if f.endswith('.xml')), None)
    xml_path = os.path.join(UNZIPPED_DIR, xml_file)
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    doc = ET.tostring(root, encoding='unicode')
    
    soup = BeautifulSoup(doc, 'lxml')
    print(f'XML data extracted and parsed from {xml_path}')
    return soup
