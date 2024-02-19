from llama_index import (
   SimpleDirectoryReader,
   GPTDeepLakeIndex,
   GPTSimpleKeywordTableIndex,
   Document,
   LLMPredictor,
   ServiceContext,
   download_loader,
)
from langchain_community.chat_models import ChatOpenAI
from typing import List, Optional, Tuple
import requests
import tqdm
import os
from pathlib import Path

PDFReader = download_loader("PDFReader")

loader = PDFReader()

# financial reports of Amazon, but can be replaced by any URLs of pdfs
urls = ['https://s2.q4cdn.com/299287126/files/doc_financials/Q1_2018_-_8-K_Press_Release_FILED.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/Q2_2018_Earnings_Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_news/archive/Q318-Amazon-Earnings-Press-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_news/archive/AMAZON.COM-ANNOUNCES-FOURTH-QUARTER-SALES-UP-20-TO-$72.4-BILLION.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/Q119_Amazon_Earnings_Press_Release_FINAL.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_news/archive/Amazon-Q2-2019-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_news/archive/Q3-2019-Amazon-Financial-Results.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_news/archive/Amazon-Q4-2019-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2020/Q1/AMZN-Q1-2020-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2020/q2/Q2-2020-Amazon-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2020/q4/Amazon-Q4-2020-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2021/q1/Amazon-Q1-2021-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2021/q2/AMZN-Q2-2021-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2021/q3/Q3-2021-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2021/q4/business_and_financial_update.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2022/q1/Q1-2022-Amazon-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2022/q2/Q2-2022-Amazon-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2022/q3/Q3-2022-Amazon-Earnings-Release.pdf',
        'https://s2.q4cdn.com/299287126/files/doc_financials/2022/q4/Q4-2022-Amazon-Earnings-Release.pdf'
        ]

# hardcoding for now since we're missing q3 2020
years = [
   2018, 2018, 2018, 2018,
   2019, 2019, 2019, 2019,
   2020, 2020, 2020,
   2021, 2021, 2021, 2021,
   2022, 2022, 2022, 2022
]
months = [
   1, 4, 7, 10,
   1, 4, 7, 10,
   1, 4, 10,
   1, 4, 7, 10,
   1, 4, 7, 10
]

zipped_data = list(zip(urls, months, years))


def download_reports(data: List[Tuple[str, int, int]], out_dir: Optional[str] = None) -> List[Document]:
   """Download pages from a list of urls."""
   docs = []
   out_dir = Path(out_dir or ".")
   if not out_dir.exists():
      print(out_dir)
      os.makedirs(out_dir)

   for url, month, year in tqdm.tqdm(data):
      path_base = url.split('/')[-1]
      out_path = out_dir / path_base
      if not out_path.exists():
         r = requests.get(url)
         with open(out_path, 'wb') as f:
            f.write(r.content)
      doc = loader.load_data(file=Path(out_path))[0]

      date_str = f"{month:02d}" + "-01-" + str(year)
      doc.extra_info = {"Date": date_str}

      docs.append(doc)
   return docs


def _get_quarter_from_month(month: int) -> str:
   mapping = {
      1: "Q1",
      4: "Q2",
      7: "Q3",
      10: "Q4"
   }
   return mapping[month]


docs = download_reports(zipped_data, 'data')

llm_predictor = LLMPredictor(
   llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))  # replace with gpt-4 if you have access
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

# build vector index for each quarterly statement, store in dictionary
dataset_root = 'hub://jerryjliu98/amazon_financial_'
vector_indices = {}
for idx, (_, month, year) in enumerate(zipped_data):
   doc = docs[idx]

   dataset_path = dataset_root + f"{month:02d}_{year}"
   vector_index = GPTDeepLakeIndex.from_documents([doc], dataset_path=dataset_path, overwrite=True)
   vector_indices[(month, year)] = vector_index

response = vector_indices[(1, 2018)].query("What is the operating cash flow?")
#Does the sentiment in the earnings from Q1 24 match the market thoughts

print(response)

from gpt_index.indices.composability import ComposableGraph

# set summary text for city
index_summaries = {}
for idx, (_, month, year) in enumerate(zipped_data):
   quarter_str = _get_quarter_from_month(month)
   index_summaries[(month, year)] = f"Amazon Financial Statement, {quarter_str}, {year}"

graph = ComposableGraph.from_indices(
   GPTSimpleKeywordTableIndex,
   [index for _, index in vector_indices.items()],
   [summary for _, summary in index_summaries.items()],
   max_keywords_per_chunk=50
)

from gpt_index.indices.query.query_transform.base import DecomposeQueryTransform
decompose_transform = DecomposeQueryTransform(
   llm_predictor,
   verbose=True
)

# set query config
query_configs = [
   {
       "index_struct_type": "deeplake",
       "query_mode": "default",
       "query_kwargs": {
           "similarity_top_k": 1
       },
       # NOTE: set query transform for subindices
       "query_transform": decompose_transform
   },
   {
       "index_struct_type": "keyword_table",
       "query_mode": "simple",
       "query_kwargs": {
           "response_mode": "tree_summarize",
           "verbose": True
       },
   },
]