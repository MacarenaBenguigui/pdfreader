import os
from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers import PDFReader
from llama_index.query_engine import PandasQueryEngine
from prompt import new_prompt, instruction_str, context

#Carga de PDFs
def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index


pdf_path = os.path.join("data", "PORTFOLIO INNEVA.pdf")
portfolio_pdf = PDFReader().load_data(file=pdf_path)
portfolio_index = get_index(portfolio_pdf, "portfolio")
portfolio_engine = portfolio_index.as_query_engine()

adjuvant_path = os.path.join("data", "Adjuvant Nivolumab in Resected Esophageal  or Gastroesophageal Junction Cancer.pdf")
adjuvant_pdf = PDFReader().load_data(file=adjuvant_path)
adjuvant_index = get_index(adjuvant_pdf, "adjuvant")
adjuvant_engine = adjuvant_index.as_query_engine()

opdivo_path = os.path.join("data", "FICHA_TÉCNICA__OPDIVO-H-3985-II-117_26_junio_2023_AUTORIZADA.pdf")
opdivo_pdf = PDFReader().load_data(file=opdivo_path)
opdivo_index = get_index(opdivo_pdf, "opdivo")
opdivo_engine = opdivo_index.as_query_engine()

suppplement_path = os.path.join("data", "Supplement to Kelly RJ, Ajani JA, Kuzdzal J, et al. Adjuvant nivolumab in resected esophageal or gastroesophageal junction cancer. N Engl J Med 2021.pdf")
suppplement_pdf = PDFReader().load_data(file=suppplement_path)
suppplement_index = get_index(suppplement_pdf, "suppplement")
suppplement_engine = suppplement_index.as_query_engine()


adjuvant_path = os.path.join("data", "Adjuvant Nivolumab in Resected Esophageal  or Gastroesophageal Junction Cancer.pdf")
adjuvant_df = PDFReader().load_data(file=adjuvant_path)
adjuvant_index = get_index(adjuvant_pdf, "adjuvant")
adjuvant_index = adjuvant_index.as_chat_engine()

