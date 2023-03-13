import openai
from PIL import Image

openai.api_key = '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'

def replace_with_emoji(input_path, prompt):
  response = openai.Image.create_edit(
    image=open(input_path, "rb"),
    prompt=prompt,
    n=5,
    size="512x512"
  )

  results = []
  for resp in response['data']:
    image_url = resp['url']
    results.append(image_url)
  
  return results