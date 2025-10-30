from data.dictionary.data_bolivia import PDFConfig
pdf_config = PDFConfig.get_config('2020_EG_CBBA')
pages = pdf_config.get()
print(pages)