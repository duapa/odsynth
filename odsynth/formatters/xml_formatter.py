from typing import Any, Dict, List
from xml.etree.ElementTree import Element, tostring

from ..globals import DOM_ROOT_KEY, XML_DOC_ROOT
from .base_formatter import BaseFormatter


class XMLFormatter(BaseFormatter):
    """Takes data generated in odsynth.DataGenerator and
    transforms it to XML."""

    def _dict_to_xml(self, field_name: str, data: Dict[str, Any]) -> str:
        def to_xml_str(element: Element):
            rough_string = tostring(element, "unicode")
            return rough_string

        def build_xml_element(t: str, d: Any):
            element = Element(t)
            if isinstance(d, dict):
                for k, v in d.items():
                    child = build_xml_element(k, v)
                    element.append(child)
            elif isinstance(d, list):
                for item in d:
                    child = build_xml_element(f"{t}_item", item)
                    element.append(child)
            else:
                element.text = str(d)
            return element

        return to_xml_str(build_xml_element(field_name, data))

    def format_data(self, data: List[Dict[str, Any]]):
        """Transforms data from odsynth.DataGenerator to XML.

        Parameters:
        -----------
        - data (list[dict]): Generated data from odsynth.DataGenerator

        Returns:
        --------
        output (list[str]): Data transformed into a list of xml strings.
        """
        xml_objects = []
        for data_point in data:
            xml_objects.append(self._dict_to_xml(DOM_ROOT_KEY, data=data_point))
        return xml_objects

    @classmethod
    def get_name(cls) -> str:
        return "xml"

    def prepare_for_writing(self, data: List[Dict[str, Any]]) -> List[str]:
        xml_reprs = self.format_data(data)
        output_xml = ""
        for xml in xml_reprs:
            output_xml += xml
        return [f"<{XML_DOC_ROOT}>{output_xml}</{XML_DOC_ROOT}>"]

    @property
    def file_extension(self):
        return __class__.get_name()
