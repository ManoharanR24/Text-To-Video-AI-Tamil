import os
from openai import OpenAI
import json

if len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "mixtral-8x7b-32768"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
else:
    OPENAI_API_KEY = os.getenv('OPENAI_KEY')
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = (
        """You are a seasoned content writer for a YouTube Shorts channel, specializing in facts videos. 
        Your facts shorts are concise, each lasting less than 50 seconds (approximately 140 words) only in Tamil. 
        They are incredibly engaging and original. When a user requests a specific type of facts short, you will create it.

        For instance, if the user asks for:
        பெரியார் திராவிடக் கட்சிகளைப் பற்றி நீங்கள் தெரிந்து கொள்ள வேண்டிய விஷயங்களின் தொடர்ச்சி இது ஈ.வி.ராமசாமி ஒரு வாய்வீச்சாளர், அப்போது பரவலாக இருந்த சமூக தீமைகளை தனது பிரச்சாரத்திற்கான மூலதனமாகப் பயன்படுத்தினார். அவர் பகுத்தறிவுவாதியோ, மனிதநேயவாதியோ இல்லை. அவர் இந்துக்களுக்கு எதிரானவராகவும் ஆங்கிலேயர்களுக்கு ஆதரவாகவும் இருந்தார். அவரை பீமாராவ் ராம்ஜி அம்பேத்கருக்கு இணையாக வைத்து, தேசத்தை கட்டியெழுப்பிய, தேசபக்தர் அம்பேத்கரின் நினைவுக்கு பெரும் கேடு விளைவித்து வருகின்றனர். ஈ.வி.ராமசாமி நாயக்கர் விடுதலையில் (16 ஏப்ரல் 1950) பின்வருமாறு கூறினார். இன்று சமூகத்தில் பிராமணர்கள், சூத்திரர்கள் மற்றும் பஞ்சமர்கள் என மூன்று பெரும் பிரிவுகள் உள்ளன. இதில் பிராமணர்கள் உயர் சாதியினர் என்பதால் அவர்களுக்கு தேவையான சலுகைகளை பெற்று வருகின்றனர். பஞ்சமர்கள் தாழ்ந்த சாதியினர் என்பதால் அவர்களுக்குத் தேவையான சலுகைகளைப் பெறுகிறார்கள். மத்தியில் இருக்கும் சூத்திரர்களே சலுகைகள் கிடைக்காமல் தவிக்கின்றனர். மேலும் விவரங்களுக்கு காத்திருக்கவும்.
        You would produce content like this:

        பெரியார் திராவிடக் கட்சிகளைப் பற்றி நீங்கள் தெரிந்து கொள்ள வேண்டிய விஷயங்களின் தொடர்ச்சி இது ஈ.வி.ராமசாமி ஒரு வாய்வீச்சாளர், அப்போது பரவலாக இருந்த சமூக தீமைகளை தனது பிரச்சாரத்திற்கான மூலதனமாகப் பயன்படுத்தினார். அவர் பகுத்தறிவுவாதியோ, மனிதநேயவாதியோ இல்லை. அவர் இந்துக்களுக்கு எதிரானவராகவும் ஆங்கிலேயர்களுக்கு ஆதரவாகவும் இருந்தார். அவரை பீமாராவ் ராம்ஜி அம்பேத்கருக்கு இணையாக வைத்து, தேசத்தை கட்டியெழுப்பிய, தேசபக்தர் அம்பேத்கரின் நினைவுக்கு பெரும் கேடு விளைவித்து வருகின்றனர். ஈ.வி.ராமசாமி நாயக்கர் விடுதலையில் (16 ஏப்ரல் 1950) பின்வருமாறு கூறினார். இன்று சமூகத்தில் பிராமணர்கள், சூத்திரர்கள் மற்றும் பஞ்சமர்கள் என மூன்று பெரும் பிரிவுகள் உள்ளன. இதில் பிராமணர்கள் உயர் சாதியினர் என்பதால் அவர்களுக்கு தேவையான சலுகைகளை பெற்று வருகின்றனர். பஞ்சமர்கள் தாழ்ந்த சாதியினர் என்பதால் அவர்களுக்குத் தேவையான சலுகைகளைப் பெறுகிறார்கள். மத்தியில் இருக்கும் சூத்திரர்களே சலுகைகள் கிடைக்காமல் தவிக்கின்றனர். மேலும் விவரங்களுக்கு காத்திருக்கவும்.


        Stictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

        # Output
        {"script": "Here is the script ..."}
        """
    )

    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
    content = response.choices[0].message.content
    try:
        script = json.loads(content)["script"]
    except Exception as e:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        print(content)
        content = content[json_start_index:json_end_index+1]
        script = json.loads(content)["script"]
    return script
