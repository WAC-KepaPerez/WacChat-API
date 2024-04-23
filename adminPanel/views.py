import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from dotenv import load_dotenv
import uuid





import pandas as pd
import os
load_dotenv()

# Access environment variables
PINECODE_API_KEY = os.getenv("PINECODE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
import openai
from openai import OpenAI,APIConnectionError
from pinecone import Pinecone,ServerlessSpec



@api_view(['GET'])
def pon(request):
         return Response({"pon"})


class SubirPost(APIView):
  def post(self, request):

    if not request.body:
      return JsonResponse({'error': 'Empty request body'}, status=400)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)


    openai_wac_chat_api_key = body['openai_wac_chat_api_key']
    
    pinecone_wac_chat_api_key = body['pinecode_wac_chat_api_key']
    #pinecode_wac_chat_unpload_option = body['pinecode_wac_chat_unpload_option']
    pinecode_wac_chat_index=body['pinecode_wac_chat_index']

    post = body['post']
    vectors=[]


    pc = Pinecone(api_key=pinecone_wac_chat_api_key)
    client = OpenAI(api_key=openai_wac_chat_api_key)
    index = pc.Index(pinecode_wac_chat_index) 

    #Eliminar todos los registros anterirores
    try:
        delete_response=  index.delete(delete_all=True, namespace='ns1')
    except Exception as e:
        print("Error al eliminar index,pueder que no exista") 
    
    #if pinecode_wac_chat_unpload_option == "excel":
    # index.delete(delete_all=True, namespace='ns1')
    try:
      postData=  str(post)
      response = client.embeddings.create(
      input=postData,
      model="text-embedding-3-small"
      )
      #print(response.data[0].embedding)
      vectors.append(
        {
        "id": str(post['id']), 
        "values": response.data[0].embedding, 
        "metadata": post
        },
      )
      response=index.upsert(
          vectors=vectors,
      namespace="ns1"
      )
      print(response)
      return Response({'status': "succes"}, status=status.HTTP_200_OK)
    except Exception as e:
        print("An error occurred:", str(e))
        return Response({'status': "error", "error":e}, status=status.HTTP_400_BAD_REQUEST)   



class BorrarEmbeddings(APIView):
  def post(self, request):
    
    if not request.body:
      return JsonResponse({'error': 'Empty request body'}, status=400)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    pinecone_wac_chat_api_key = body['pinecode_wac_chat_api_key']
    pinecode_wac_chat_index=body['pinecode_wac_chat_index']

    pc = Pinecone(api_key=pinecone_wac_chat_api_key)
    index = pc.Index(pinecode_wac_chat_index) 

    try:
      delete_response=  index.delete(delete_all=True, namespace='ns1')
      return Response({'status': "succes"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': "error", "error":"an error"}, status=status.HTTP_400_BAD_REQUEST)   


class SubirPostExcel(APIView):
    def post(self, request):
      #body_unicode = request.body.decode('utf-8')
      #body = json.loads(body_unicode)
      body = request.data
      
      openai_wac_chat_api_key = body.get('openai_wac_chat_api_key')
      pinecone_wac_chat_api_key = body.get('pinecode_wac_chat_api_key')
      pinecode_wac_chat_index=body.get('pinecode_wac_chat_index')

      excel_file = request.FILES['file']
      pc = Pinecone(api_key=pinecone_wac_chat_api_key)
      client = OpenAI(api_key=openai_wac_chat_api_key)
      indexPC = pc.Index(pinecode_wac_chat_index)



      #Eliminar todos los registros anterirores
      try:
          delete_response=  indexPC.delete(delete_all=True, namespace='ns1')
      except Exception as e:
          print("Error al eliminar index,pueder que no exista") 
      
      #get json
      try:
          df = pd.read_excel(excel_file)
          df.fillna("", inplace=True)
          #json_data = df.to_json(orient='records',force_ascii=False)
          json_data = df.dropna(how='all').to_json(orient='records', force_ascii=False)
          print(df)
          #modified_string = json_data.replace("\\", "")
          #json_data = json.loads(modified_string)
          modified_string = json_data.replace("None", "")
          json_data = json.loads(modified_string)
          vectors=[]
          print(json_data[0])
      except Exception as e:
                print("An error occurred Converting excel to json:", str(e))
                return Response({'status': "error", "error":"An error occurred Converting excel to json:"}, status=status.HTTP_400_BAD_REQUEST)
      

      try:
        for row in json_data:
          postData=  str(row)
          try:
            response = client.embeddings.create(
            input=postData,
            model="text-embedding-3-small"
            )
          except openai.APIConnectionError as e:
              print("The server could not be reached")
              print(e.__cause__)  # an underlying Exception, likely raised within httpx.
          except openai.RateLimitError as e:
              print("A 429 status code was received; we should back off a bit.")
          except openai.APIStatusError as e:
              print("Another non-200-range status code was received")
              print(e.status_code)
              print(e.response)
          
          # Generate a UUID
          new_uuid = str(uuid.uuid4())
          #print(response.data[0].embedding)
          vectors.append(
            {
            "id": new_uuid, 
            "values": response.data[0].embedding, 
            "metadata": row
            },
          )
          response=indexPC.upsert(
              vectors=vectors,
          namespace="ns1"
          )
          print(response)
        return Response({'status': "succes"}, status=status.HTTP_200_OK)
      except Exception as e:
          print("An error occurred:", str(e))
          return Response({'status': "error", "error":e}, status=status.HTTP_400_BAD_REQUEST)   