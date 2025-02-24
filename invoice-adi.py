import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

# Get credentials
load_dotenv()
endpoint = os.environ["ADI_ENDPOINT"]
key = os.environ["ADI_API_KEY"]

# Azure Document Intelligence
adi_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

document_path = "invoices/"

with open(document_path, "rb") as f:
    poller = adi_client.begin_analyze_document(
        "prebuilt-receipt", body=f, locale="en-US"
    )
receipts: AnalyzeResult = poller.result()

if receipts.documents:
    for idx, receipt in enumerate(receipts.documents):
        print(f"--------Analysis of receipt #{idx + 1}--------")
        print(f"Receipt type: {receipt.doc_type if receipt.doc_type else 'N/A'}")
        if receipt.fields:
            print(receipt.fields)
        else:
            print("No fields found.")
