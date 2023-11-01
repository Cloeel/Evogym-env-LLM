import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_env(prompt):
    model_id = "ft:gpt-3.5-turbo-0613:webscience-lab::8DyQDcTj"

    response = openai.ChatCompletion.create(
        model = model_id,
        messages=[
            {"role": "system", "content": "The environment in reinforcement learning, where the agent progresses from left to right, is represented by a list of strings, one character per block. The following conditions are applied: '-' is a blank block, 'H' is a hard block, and 'S' is a soft block. The agent can walk on the 'H' and 'S' blocks and can exist in the '-' area. If there is no 'H' or 'S' block under the agent, it will fall. Please return a list that predicts what kind of environment it is from a prompt that describes the given environment. Please make all elements in the list have the same length. Also, only allow '-' , 'H', and 'S' characters in the elements. Please return with the specified character length. Do not output anything other than a list."},
            {"role": "user", "content": "100*20 size Evolution Gym environment that is simple."},
            {"role": "assistant", "content": "['----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', 'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH------------------------------------------------', '----------------------------------------------------HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------', '----------------------------------------------------------------------------------------------------']"},
            {"role": "user", "content": prompt}
        ]
    )
    env_list = eval(response['choices'][0]['message']['content'])
    return env_list

def adjust_list(lst):
    adjusted_list = []
    for s in lst:
        s = ''.join(c if c in "-HS" else '-' for c in s)
        
        if len(s) == 100:
            adjusted_list.append(s)
        elif len(s) < 100:
            adjusted_list.append(s + '-'*(100 - len(s)))
        else:
            adjusted_list.append(s[:100])
    return adjusted_list

def check_columns(lst):
    num_hyphens = 0
    for i in range(len(lst[0])):
        for j in range(len(lst)):
            if lst[j][i] != '-':
                num_hyphens = 0
                break
        else:
            num_hyphens += 1

        if num_hyphens >= 5:
            return False

    return True

def generate_env(prompt):
    checked_list = False

    while not checked_list:
        env_list = create_env(prompt)
        fixed_list = adjust_list(env_list)
        checked_list = check_columns(fixed_list)

    return fixed_list

def main():
    prompt = "100*20 size Evolution Gym environment that is shaped like a mountain."
    fixed_list = generate_env(prompt)
    for s in fixed_list:
        print(s)

if __name__ == "__main__":
    main()
