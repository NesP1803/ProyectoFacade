import unittest

from services.factus.credit_note_payload_builder_v2 import build_credit_note_item, build_credit_note_payload
from services.factus.download_adapter import decode_file_payload
from services.factus.endpoints import FactusEndpointRegistry
from services.factus.payload_builder_v2 import build_payment_details, price_net_from_gross
from services.factus.response_mapper_v2 import extract_document_data, map_factus_status


class FactusV2MigrationTests(unittest.TestCase):
    def test_endpoints_default_to_v2(self):
        registry = FactusEndpointRegistry()
        self.assertEqual(registry.resolve("bill_validate"), "/v2/bills/validate")
        self.assertEqual(registry.resolve("credit_note_validate"), "/v2/credit-notes/validate")
        self.assertEqual(registry.resolve("numbering_ranges"), "/v2/numbering-ranges")

    def test_endpoints_allow_v1_fallback(self):
        registry = FactusEndpointRegistry(api_version="v1")
        self.assertEqual(registry.resolve("bill_validate"), "/v1/bills/validate")

    def test_price_net_iva_19(self):
        self.assertEqual(price_net_from_gross("119", "19"), "100.00")

    def test_price_net_iva_5(self):
        self.assertEqual(price_net_from_gross("105", "5"), "100.00")

    def test_price_net_excluded(self):
        self.assertEqual(price_net_from_gross("100", "0"), "100.00")

    def test_payment_details_shape(self):
        details = build_payment_details("1", "10", 25000, reference_code="POS-001")
        self.assertEqual(len(details), 1)
        self.assertIn("payment_form", details[0])
        self.assertIn("payment_method_code", details[0])
        self.assertIn("amount", details[0])

    def test_credit_note_payload(self):
        payload = build_credit_note_payload("NC-1", "FV-100", 10000)
        self.assertEqual(payload["bill_number"], "FV-100")
        self.assertEqual(payload["payment_details"][0]["payment_method_code"], "10")

    def test_credit_note_item_excluded(self):
        item = build_credit_note_item("item", 1, 10000, 0)
        self.assertEqual(item["taxes"], [{"is_excluded": True}])

    def test_download_pdf_base64(self):
        payload = {"data": {"pdf_base_64_encoded": "SG9sYQ=="}}
        self.assertEqual(decode_file_payload(payload, "pdf_base_64_encoded"), b"Hola")

    def test_download_xml_base64(self):
        payload = {"data": {"xml_base_64_encoded": "PHhtbD48L3htbD4="}}
        self.assertEqual(decode_file_payload(payload, "xml_base_64_encoded"), b"<xml></xml>")

    def test_response_mapper_status(self):
        self.assertEqual(map_factus_status("accepted_with_warnings"), "ACEPTADA_CON_OBSERVACIONES")

    def test_response_mapper_extract_data(self):
        payload = {"data": {"bill": {"number": "FV-1"}}}
        self.assertEqual(extract_document_data(payload)["number"], "FV-1")


if __name__ == "__main__":
    unittest.main()
