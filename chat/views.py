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




class Chat(APIView):
  def post(self, request):
    
    if not request.body:
      return JsonResponse({'error': 'Empty request body'}, status=400)
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    print(body)
    messagesCliente = body['message']

    openai_wac_chat_api_key = body['openai_wac_chat_api_key']
    openai_wac_chat_model = body['openai_wac_chat_model']
    openai_wac_chat_token_limit = body['openai_wac_chat_token_limit']
    openai_wac_chat_temperature = body['openai_wac_chat_temperature']
    openai_wac_chat_promp = body['openai_wac_chat_promp']

    pinecone_wac_chat_api_key = body['pinecode_wac_chat_api_key']
    pinecode_wac_chat_index=body['pinecode_wac_chat_index']


    
    
    pc = Pinecone(api_key=pinecone_wac_chat_api_key)
    index = pc.Index(pinecode_wac_chat_index) 
    client = OpenAI(api_key=openai_wac_chat_api_key)


    try:
      responseAI = client.embeddings.create(
        input=str(messagesCliente[-1]), 
        model="text-embedding-3-small"
      )
      vector =responseAI.data[0].embedding

      response = index.query(
        namespace='ns1',
        top_k=5,
        include_values=True,
        include_metadata=True,
        vector=vector,
      )
    
      metadata=response['matches'][0]['metadata']
      matches = response['matches']
      # Initialize an empty array to store metadata values
      metadata_values = []

      for match in matches:
          if match['metadata']:
                  metadata_values.append(match['metadata'])

      messagesAPI=[
          {
            "role": "system", 
            "content": str(openai_wac_chat_promp)
          },
          {
            "role": "user",
            "content":str(metadata_values),
          },
      ]
      messagesAPI += messagesCliente
      chat_completion = client.chat.completions.create(
      messages=messagesAPI,
      model="gpt-3.5-turbo",
      temperature=openai_wac_chat_temperature,
      max_tokens=openai_wac_chat_token_limit
      )

      print(chat_completion)
      #return Response({"message":chat_completion.choices[0].message.content,"title":metadata['title'],"url":metadata['url']}, status=status.HTTP_200_OK)
      return Response({"message":chat_completion.choices[0].message.content}, status=status.HTTP_200_OK)
    
    except Exception as e:
        print("An error occurred:", str(e))
        return Response({'status': "error", "error":e}, status=status.HTTP_400_BAD_REQUEST)   
