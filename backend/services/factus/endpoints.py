from dataclasses import dataclass


@dataclass(frozen=True)
class FactusEndpointRegistry:
    api_version: str = "v2"
    support_document_version: str = "v1"
    support_adjustment_version: str = "v1"

    def resolve(self, logical_name: str, **path_params: str) -> str:
        template = self._templates().get(logical_name)
        if not template:
            raise KeyError(f"Unknown Factus endpoint: {logical_name}")
        return template.format(**path_params)

    def _templates(self) -> dict[str, str]:
        v = self.api_version
        sdv = self.support_document_version
        sav = self.support_adjustment_version
        return {
            "oauth_token": "/oauth/token",
            "bill_validate": f"/{v}/bills/validate",
            "bill_show": f"/{v}/bills/{{number}}",
            "bill_list": f"/{v}/bills",
            "bill_delete_by_reference": f"/{v}/bills/destroy/reference/{{reference_code}}",
            "bill_download_pdf": f"/{v}/bills/{{number}}/download-pdf",
            "bill_download_xml": f"/{v}/bills/{{number}}/download-xml/",
            "bill_send_email": f"/{v}/bills/{{number}}/send-email",
            "bill_email_content": f"/{v}/bills/{{number}}/email-content",
            "credit_note_validate": f"/{v}/credit-notes/validate",
            "numbering_ranges": f"/{v}/numbering-ranges",
            "numbering_ranges_dian": f"/{v}/numbering-ranges/dian",
            "support_document_validate": f"/{sdv}/support-documents/validate",
            "support_adjustment_validate": f"/{sav}/adjust-notes/validate",
        }
