import openai
import os
import json
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

def process_neighbour(i, j, grid, object_cells):
    if i<0 or j<0 or i>=len(grid) or j>=len(grid[0]) or grid[i][j] == "-":
        return

    cell = (len(grid)-1-i)*len(grid[0]) + j  # fixed here

    if cell in object_cells:
        return

    object_cells.append(cell)

    process_neighbour(i+1, j, grid, object_cells)
    process_neighbour(i-1, j, grid, object_cells)
    process_neighbour(i, j+1, grid, object_cells)
    process_neighbour(i, j-1, grid, object_cells)


def create_json_file(env_list):
    grid = [list(row) for row in env_list]
    objects_dict = dict()
    object_counter = 1

    grid_width = len(grid[0])
    grid_height = len(grid)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'H' or grid[i][j] == 'S':
                new_object_indices = []

                process_neighbour(i, j, grid, new_object_indices)

                new_object_types = [1 if grid[(len(grid)-1-idx//grid_width)][idx%grid_width] == 'H' else 2 for idx in new_object_indices]

                new_object = {}
                new_object['indices'] = new_object_indices
                new_object['types'] = new_object_types
                new_object['neighbors'] = {str(idx): [n for n in new_object_indices if (n//grid_width == idx//grid_width and abs(n%grid_width - idx%grid_width) == 1) or (abs(n//grid_width - idx//grid_width) == 1 and n%grid_width == idx%grid_width)] for idx in new_object_indices}

                objects_dict['new_object_' + str(object_counter)] = new_object
                object_counter += 1 

                for idx in new_object_indices:
                    grid[(len(grid)-1-idx//grid_width)][idx%grid_width] = "-"  # fixed here

    return_dict = {}
    return_dict['grid_width'] = grid_width
    return_dict['grid_height'] = grid_height
    return_dict['objects'] = objects_dict

    return return_dict

def generate_env(prompt):
    checked_list = False

    while not checked_list:
        env_list = create_env(prompt)
        fixed_list = adjust_list(env_list)
        checked_list = check_columns(fixed_list)
        try:
            json_env = create_json_file(fixed_list)
        except:
            checked_list = False

    return json_env, fixed_list

def main():
    prompt = "100*20 size Evolution Gym environment that is shaped like a mountain."
    json_env, fixed_list = generate_env(prompt)
    for s in fixed_list:
        print(s)
    print(json_env)
    with open('test.json', 'w') as f:
        json.dump(json_env, f)

if __name__ == "__main__":
    main()
