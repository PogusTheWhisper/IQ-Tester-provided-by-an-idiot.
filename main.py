from openai import OpenAI
import gradio as gr
import threading
import pygame

# OpenAI client setup
client = OpenAI(
    api_key="<Typhoon Key>",
    base_url="https://api.opentyphoon.ai/v1",
)

# Function to generate humorous IQ questions
def generate_questions():
    stream = client.chat.completions.create(
        model="typhoon-v1.5-instruct",
        messages=[
            {
                "role": "user",
                "content": """
                คุณคือ AI อัจฉริยะสายขำขันที่มีหน้าที่สร้างคำถาม IQ แบบฮาๆ และไม่คาดคิด เป้าหมายของคุณคือสร้างคำถามเพียง 1 ข้อที่เต็มไปด้วยจินตนาการและตรรกะขำขัน โดยคำถามนี้ต้องทำให้ผู้เล่นหัวเราะหรือคิดอย่างสร้างสรรค์

                แนวทางการสร้างคำถาม:
                - ใช้โทนคำถามที่เบาสมอง สนุก และกระตุ้นจินตนาการ
                - คำถามควรสร้างความประหลาดใจและไม่คาดคิด
                - เน้นให้คำถามเหมือนเป็นเกมมากกว่าการทดสอบ

                ตัวอย่างคำถาม:
                - ถ้าคุณเป็นก้อนชีสที่กลัวโดนขูด คุณจะทำอย่างไรให้รอดพ้นจากเครื่องขูดชีส?
                - ถ้ากาแฟแก้วหนึ่งมีความฝัน อยากจะเป็นอะไรนอกจากกาแฟ?
                - คุณจะตั้งชื่อให้มนุษย์ต่างดาวที่มาถึงโลกแล้วอยากเป็นเชฟว่าอะไร?

                สร้างคำถามใหม่เพียง 1 ข้อ ที่ไม่ซ้ำกับตัวอย่างด้านบนและทำให้ผู้เล่นหัวเราะหรือคิดอย่างคาดไม่ถึง!
                """,
            },
        ],
        max_tokens=512,
        temperature=0.8,
        top_p=0.95,
        stream=True,
    )

    respond = []
    for chunk in stream:
        if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
            choice = chunk.choices[0]
            if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                if choice.delta.content is not None:
                    respond.append(choice.delta.content)
    return ''.join(respond)

# Function to provide humorous, creative answers to questions
def get_correct_answers(question):
    stream = client.chat.completions.create(
        model="typhoon-v1.5-instruct",
        messages=[
            {
                "role": "system",
                "content": """
                คุณคือ AI ที่สร้างคำตอบที่เหมาะสมกับคำถาม IQ แบบขำๆ ที่เน้นจินตนาการและความสนุก
                แนวทางคำตอบ:
                - คำตอบควรมีตรรกะที่เบาสมองและสนุกสนาน
                - ควรสร้างเสียงหัวเราะหรือความประหลาดใจให้กับผู้เล่น
                - คำตอบไม่จำเป็นต้องถูกต้องในเชิงวิทยาศาสตร์ แต่ต้องสร้างความสุข

                ตัวอย่าง:
                - คำถาม: ถ้าคุณเป็นก้อนชีสที่กลัวโดนขูด คุณจะทำอย่างไรให้รอดพ้นจากเครื่องขูดชีส?
                  คำตอบ: แกล้งเป็นนมสด กลับไปเริ่มต้นใหม่!
                - คำถาม: ถ้ากาแฟแก้วหนึ่งมีความฝัน อยากจะเป็นอะไรนอกจากกาแฟ?
                  คำตอบ: อยากเป็นทะเล เพื่อให้คนเติมน้ำใจแทนครีม
                """
            },
            {
                "role": "user",
                "content": f"คำถาม: {question}",
            }
        ],
        max_tokens=512,
        temperature=0.8,
        top_p=0.9,
        stream=True,
    )

    respond = []
    for chunk in stream:
        if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
            choice = chunk.choices[0]
            if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                if choice.delta.content is not None:
                    respond.append(choice.delta.content)
    return ''.join(respond)

# Function to evaluate the user's answers humorously
def evaluate_user(question, user_answer):
    stream = client.chat.completions.create(
        model="typhoon-v1.5-instruct",
        messages=[
            {
                "role": "system",
                "content": """
                คุณคือ AI ที่ต้องประเมินคำตอบของผู้เล่นจากแบบทดสอบ IQ ขำๆ ที่ผ่านมา และให้คะแนนแบบขำๆ เช่น:
                - 'คุณมี IQ 123 ซึ่งเทียบเท่ากับขนมปังที่กำลังพยายามเขียนบทกวี อัจฉริยะ แต่ไม่คาดคิด!'
                - 'คุณมี IQ 99 ที่ใกล้เคียงกับแมวนอนในวันแดดจัด แต่ยังพร้อมผจญภัยในโลกขำขัน!'
                """
            },
            {
                "role": "user",
                "content": f"คำถาม: {question}\nผู้เล่นตอบคำถามเหล่านี้: {user_answer}",
            }
        ],
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
        stream=True,
    )

    respond = []
    for chunk in stream:
        if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
            choice = chunk.choices[0]
            if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                if choice.delta.content is not None:
                    respond.append(choice.delta.content)
    return ''.join(respond)

def play_funny_sound():
    def play_sound():
        pygame.mixer.init()
        pygame.mixer.music.load("WOW.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    threading.Thread(target=play_sound, daemon=True).start()
    
# Gradio UI setup
def interactive_flow():
    question = generate_questions()
    return question

def handle_submission(question, user_answer):
    evaluation = evaluate_user(question, user_answer)
    play_funny_sound()
    correct_answer = get_correct_answers(question)
    return evaluation, correct_answer

with gr.Blocks() as demo:
    gr.Markdown("# 🧠 คำถามวัดไอคิวกับ AI ระดับ 🦾sKyNeT🤖")
    question_display = gr.Textbox(label="คำถาม IQ แบบฮาๆ", interactive=False)
    answer_input = gr.Textbox(label="คำตอบของคุณ", placeholder="พิมพ์คำตอบของคุณที่นี่...")
    submit_button = gr.Button("ส่งคำตอบ")
    evaluation_output = gr.Textbox(label="ผลลัพธ์ IQ ของคุณ", interactive=False)
    correct_answer_output = gr.Textbox(label="คำตอบที่เหมาะสมที่สุดจาก AI", interactive=False)

    submit_button.click(
        handle_submission,
        inputs=[question_display, answer_input],
        outputs=[evaluation_output, correct_answer_output],
    )

    demo.load(interactive_flow, outputs=[question_display])

demo.launch(share=True)
