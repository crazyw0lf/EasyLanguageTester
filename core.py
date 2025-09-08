import json
from PyQt5.QtCore import QObject, pyqtSignal
from groq import Groq
from dotenv import load_dotenv
import random as r
import os

class Core(QObject):
    finished = pyqtSignal(dict)
    evaluated = pyqtSignal(int)
    errored = pyqtSignal(str)

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def run(self, mode):

        try:
            if mode == 'Words and Grammar':
                creator = GramTest(self.owner)
                creator.get_word_list()
                if len(creator.word_list) < creator.size // 2:
                    self.errored.emit("Failed to generate a sufficient vocabulary list. Please try different parameters.")
                    return

                creator.create_light_question()
                creator.create_medium_question()
                creator.create_hard_question()

                if len(creator.test) < creator.size:
                    self.errored.emit("Failed to generate a sufficient number of questions. Please try different parameters.")
                    return

                creator.save_test()

                self.finished.emit(creator.test)

        except Exception as e:
            self.errored.emit(f"{type(e).__name__}: {e}")

    def evaluate(self, ans_sheet):
        try:

            load_dotenv("api_keys.env")
            self.client = Groq(api_key=os.environ["GROQ_API_KEY"][1:-1])
            score_dict = None
            schema = {
            "type": "object",
            "description": "A dictionary of test results indexed by integer IDs",
            "patternProperties": {
                "^[0-9]+$": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "integer",
                            "enum": "from 0 to 10",
                            "description": "given score for the question"
                        },
                        "log": {
                            "type": "string",
                            "description": "explanation of the score"
                        }
                    },
                    "required": ["score","log"]
                }
            },
            "additionalProperties": False
        }
            prompt = f"""
            You are a strict and objective evaluator of language tests.
            Your task is to assess the answers provided in a test and assign a score from 0 to 10 
            for each question based on the accuracy and completeness of the answers.
            As input you are given a JSON object representing the test results.
            Each key in the object is a question ID (an integer as a string), and
            user_answer and right answer. Compare how simular in meaning are results and check
            if grammar and vocabulary in answer are right selected. 
            **Output Format**: The final output must be a single JSON schema: {schema}.
            """

            for i in range(3):
                try:
                    response = self.client.chat.completions.create(model='openai/gpt-oss-120b', messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": json.dumps(ans_sheet)}
                    ])

                    response = response.choices[0].message.content

                    if "```json" in response:
                        start = response.find("```json")
                        end = response.rfind("```")
                        response = response[start + 7:end].strip()

                    score_dict = json.loads(response)
                    print(f'successfully processed score dict with {len(score_dict)} items')
                    break

                except Exception as e:
                    print(f"Error occurred during score dict attempt {i + 1}: {e}")
                    continue

            score = 0
            for k in score_dict:
                score += int(score_dict[k]['score'])

            with open('res.json', 'w') as outfile:
                outfile.write(json.dumps(score_dict, indent=4, ensure_ascii=False))

            self.evaluated.emit(score)

        except Exception as e:
            self.errored.emit(f"{type(e).__name__}: {e}")




class GramTest():

    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.size = int(self.owner.size)
        self.topic = self.owner.topic
        self.language = self.owner.language
        self.level = self.owner.level
        self.test = {}
        self.index = 1
        self.output_schema = {
            "type": "object",
            "description": "A dictionary of quiz questions indexed by integer IDs",
            "patternProperties": {
                "^[0-9]+$": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["light", "medium", "hard"],
                            "description": "Difficulty level of the question"
                        },
                        "question": {
                            "type": "string",
                            "description": "The question text"
                        },
                        "right_answer": {
                            "type": "string",
                            "description": "The correct answer to the question"
                        },
                        "answers": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of possible answers (can be empty if open question) empty for hard questions"
                        }
                    },
                    "required": ["type", "question", "right_answer", "answers"]
                }
            },
            "additionalProperties": False
        }

        self.structure = {}
        self.structure['hard'] = self.size // 10
        self.structure['medium'] = (self.size - self.structure['hard']) // 3
        self.structure['light'] = self.size - self.structure['hard'] - self.structure['medium']

        load_dotenv("api_keys.env")
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"][1:-1])

    def get_word_list(self):

        prompt = f"""
    You are a vocabulary list generator. Your task is to create a JSON object containing a list of about n unique words.
    The words should be in the specified language, suitable for the given proficiency level, and directly related to the provided topic.

    Instructions:
        1.  **Language**: The language is '{self.language}'.
        2.  **Proficiency Level**: The level is '{self.level}'. This can be 'beginner', 'intermediate', or 'advanced'.
        3.  **Topic**: The topic is '{self.topic}'. The words must be semantically relevant to this topic.
        4.  **Word Count**: Provide enough words to cover topic on the given level
        ( 100%-150% from {self.size} in beginner level, 150% - 200% in intermidiate, 200% - 300% for highest).
        5.  **Uniqueness**: All words in the list must be unique
        and keep balance 60% - 70% nouns, 15% - 20% verbs and 15% - 20% adjective.
        6.  **Output Format**: The final output must be a single JSON object.
        The keys must be sequential numbers from '1' to 'n' (as strings), and the values must be the words (as strings).
        Example:
        {{
            "1": "word1",
            "2": "word2",
            ...
            "n": "wordn"
        }}
        7.  **Error Handling**: If it is not possible to generate a list of unique words for the given combination of language, level, and topic, return an empty JSON object: {{}}.
    """

        for i in range(3):
            try:
                response = self.client.chat.completions.create(model='openai/gpt-oss-120b', messages=[
                    {"role": "user", "content": prompt}
                ])

                response = response.choices[0].message.content

                if "```json" in response:
                    start = response.find("```json")
                    end = response.rfind("```")
                    response = response[start + 7:end].strip()

                self.word_list = json.loads(response)
                print(f'successfully processed world list with {len(self.word_list)} items')
                return

            except Exception as e:
                print(f"Error occurred during word_list attempt {i + 1}: {e}")
                continue

    def create_light_question(self):

        light_list = list(self.word_list.values())

        prompt = f"""
        You are multilingual teacher. Create test for level {self.level} student with topic {self.topic} in {self.language} language.
        It should contain of {self.structure['light']} questions. And mostly use words from this list: {light_list}.
        Questions should be design due to following rules:
            1.  **Question Types**: only "light" type questions.
            2.  **Question**: Each question must be a multiple-choice question with four answer options. from such templates:
                1. translate word from target language to english.
                2. translate word from english to target language.
                3. give right article to the noun(if there are such in the language).
                4. choose right synonym/antonym for the word in a target language.
                In all variants question description must be write on english(some part can be write in target language if task needs).
            3.  **Answer Options**: Each question must have one correct answer and three plausible distractors.
            4.  **Output Format**: The final output must be a single JSON object(start from index {self.index}) due to this schema: {self.output_schema}.
    """
        self.index += self.structure['light']

        for i in range(3):
            try:
                response = self.client.chat.completions.create(model='openai/gpt-oss-120b', messages=[
                    {"role": "user", "content": prompt}
                ])

                response = response.choices[0].message.content

                if "```json" in response:
                    start = response.find("```json")
                    end = response.rfind("```")
                    response = response[start + 7:end].strip()

                test = json.loads(response)

                for k, v in test.items():
                    self.test[k] = v

                print(f'successfully processed light questions with {len(test)} items')
                return

            except Exception as e:
                print(f"Error occurred during light question attempt {i + 1}: {e}")
                continue

    def create_medium_question(self):

        med_list = self.word_list.values()
        med_list = r.sample(list(med_list), self.structure['medium'] * 4)

        prompt = f"""
    You are a multilingual teacher. Your task is to generate a test for a student. 
    Details:
    - Student level: {self.level}
    - Topic: {self.topic}
    - Language: {self.language}
    - Number of questions: {self.structure['medium']}
    - Vocabulary focus: Mostly use words from this list → {med_list}
    
    Guidelines for test creation:
    1. **Question Types**: Only "medium" difficulty questions are allowed.
    2. **Question Format**:
       - Each question must be a multiple-choice question with exactly four answer options.
       - The question description must be written in English.
       - Use one of the following templates for the question:
         1. Choose the sentence with a grammar mistake.
         2. Choose the sentence without a grammar mistake.

    3. **Answer Options**:
       - All answers must be written in target language.
       - Each question must have exactly **one correct answer**.
       - Provide **three plausible distractors** that are clearly incorrect.
       - Incorrect answers must not be accidentally correct.
    4. **Output Format**:
       - Return the test as a single JSON object.
       - The first question index must start from {self.index}.
       - Follow this schema strictly: {self.output_schema}.
"""
        self.index += self.structure['medium']

        for i in range(3):
            try:
                response = self.client.chat.completions.create(model='openai/gpt-oss-120b', messages=[
                    {"role": "user", "content": prompt}
                ])

                response = response.choices[0].message.content

                if "```json" in response:
                    start = response.find("```json")
                    end = response.rfind("```")
                    response = response[start + 7:end].strip()

                test = json.loads(response)

                for k, v in test.items():
                    self.test[k] = v

                print(f'successfully processed medium questions with {len(test)} items')
                return

            except Exception as e:
                print(f"Error occurred during medium question attempt {i + 1}: {e}")
                continue

    def create_hard_question(self):

        hard_list = self.word_list.values()
        hard_list = r.sample(list(hard_list), self.structure['hard'] * 4)

        prompt = f"""
        You are multilingual teacher. Create test for level {self.level} student with topic {self.topic} in {self.language} language.
        It should contain of {self.structure['hard']} questions. And mostly use words from this list: {hard_list}.
        Questions should be design due to following rules:
            1.  **Question Types**: only "hard" type questions.
            2.  **Question**: Each question must contain only description and answer, answers is [].
            3.  **Question description**: 
                    Sentence on english language. Sentence must be not very long(5-15 words). Higher level - longer sentence.
            4.  **Answer**: correct answer is sentence translation on target language with correct grammar structures and logic. answers is [].
                    Sentence complexity must relay on the level both in grammar and vocabulary.
                    When level is high use complex grammar structures and less common vocabulary.
                    If there are articles in the language use them correctly. In high level use idioms and phrases.
                    In high level avoid using direct translation from english to target language prefer synonyms.
                    Sentence must be not very long(5-15 words). Higher level - longer sentence.
            5.  **Output Format**: The final output must be a single JSON object(start from index {self.index}) due to this schema: {self.output_schema}.
    """
        self.index += self.structure['hard']

        for i in range(3):
            try:
                response = self.client.chat.completions.create(model='openai/gpt-oss-120b', messages=[
                    {"role": "user", "content": prompt}
                ])

                response = response.choices[0].message.content

                if "```json" in response:
                    start = response.find("```json")
                    end = response.rfind("```")
                    response = response[start + 7:end].strip()

                test = json.loads(response)

                for k, v in test.items():
                    self.test[k] = v

                print(f'successfully processed hard questions with {len(test)} items')
                return

            except Exception as e:
                print(f"Error occurred during hard question attempt {i + 1}: {e}")
                continue

    def save_test(self):
        with open('test.json', 'w') as outfile:
            outfile.write(json.dumps(self.test, indent=4, ensure_ascii=False))