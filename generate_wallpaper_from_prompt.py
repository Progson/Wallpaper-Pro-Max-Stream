import sys
from openai import OpenAI
if(len(sys.argv)!=2):
    print("Example usage: python name_of_script.py \"two dogs with a cat on the mountain\"")
    sys.exit(2)

def generate_image_and_url(givenPrompt):
    try:
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=givenPrompt,
            size="1792x1024",
            quality="standard",
            n=1,
        )
        print(response.data[0].url)
        return 0  # Success
    except Exception as e:
        error_message = str(e)
        if "safety" in error_message.lower():
            print("Safety Error: The error is due to safety concerns.")
        else:
            print(f"Other Error: {error_message}")
        return 1  # Error

    
response = generate_image_and_url(sys.argv[1])
sys.exit(response)

        
    