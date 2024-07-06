import os
import time
import xml.etree.ElementTree as ET
from typing import List
from xml.dom.minidom import parseString

from odsynth.transformers import XMLTransformer

from ..globals import XML_DOC_ROOT
from .abstract_writer import AbstractWriter


class XMLToDiscWriter(AbstractWriter):
    def __init__(self, base_dir):
        self._base_dir = base_dir
        self._transformer = XMLTransformer()

    def write_data(self, data: List[str]):
        def pretty_xml(element: ET.Element):
            xml_string = ET.tostring(element, encoding="utf-8")
            return parseString(xml_string).toprettyxml(indent=" ")

        file_root = ET.Element(XML_DOC_ROOT)
        xml_str_list = self._transformer.transform(data)

        for xml_string in xml_str_list:
            element = ET.fromstring(xml_string)
            file_root.append(element)

        xml_doc = pretty_xml(file_root)

        os.makedirs(self._base_dir, exist_ok=True)
        timestamp = int(time.time() * 1e6)
        filename = f"{self._base_dir}/odsynth_{timestamp}.xml"
        with open(filename, "w") as file:
            file.write(xml_doc)

    @classmethod
    def get_name(cls) -> str:
        return "xml_to_disc"
