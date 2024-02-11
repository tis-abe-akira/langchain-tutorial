import os
import langchain
import yaml

from langchain_community.chat_models import BedrockChat
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import pandas as pd
from dotenv import load_dotenv

import langchain
langchain.verbose=True

load_dotenv()
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

# パラメータ
with open('config.yaml') as f:
    config = yaml.safe_load(f)

INPUT_FILE = config['INPUT_FILE']
OUTPUT_FILE = config['OUTPUT_FILE']
TEMPLATE_FILE = config['TEMPLATE_FILE']
CHUNK_SIZE = config['CHUNK_SIZE']
START_POSITION = config['START_POSITION']
MODEL_ID = config['MODEL_ID']
NUMBER_LOC = config['NUMBER_LOC']
VALUE_LOC = config['VALUE_LOC']

# CSVのリスト
csv_data = []

# Excelファイルを読み込む
df = pd.read_excel(INPUT_FILE, header=0)

# dfの中身を確認
print(df.head())

for index, row in df.iterrows():

    if row.iloc[NUMBER_LOC] >= (START_POSITION) and row.iloc[NUMBER_LOC] < (START_POSITION +  CHUNK_SIZE):
        input = row.iloc[VALUE_LOC]
        print(str(row.iloc[NUMBER_LOC]) + " " + input)
    else:
        continue

    if pd.isnull(input) or input == '' or input == ' ':
        continue

    # Create cht_model
    chat_model = BedrockChat(
        model_id=MODEL_ID, 
        streaming=True, 
        model_kwargs={"temperature": 0.0, "max_tokens_to_sample" : 2048}
    )

    # Templateファイルを開く
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()

    # Promptの定義
    prompt = PromptTemplate(
        input_variables=["message"],
        template=template
    )
    # chainの定義
    chain = LLMChain(llm=chat_model, prompt=prompt)
    # run
    result = chain.run(message=input)

    print(result)

    # CSVフォーマットのデータを追加
    formatted_row = f'{row.iloc[NUMBER_LOC]},"{input}","{result}"'
    csv_data.append(formatted_row)

# CSVファイルに書き込む
with open(OUTPUT_FILE, 'w', encoding='cp932', newline='') as f:
    f.write('\n'.join(csv_data))

print("Done!")
