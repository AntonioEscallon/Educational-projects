import mdp


"""
Carefully read the Homework 5 Coding pdf to understand what to implement in
this file. Replace the None values with the correct values as per those instructions.

Example of how to construct an MDP object is included at the bottom.
"""
def q1_and_2():
    # TODO: Replace the None values here based on the questions in the PDF.
    #       DO NOT change anything besides these None values when you submit.
    #       However, you may add print statements if it helps.
    gridworld = None
    epsilon = None
    discount_factor = None

    print("\n", '─' * 50, "\n", "Question 1 and 2")
    utilities, policy = mdp.utils_and_policy(gridworld, discount_factor, epsilon)

    # TODO: Fill these in.
    num_convergance_utility = None
    num_convergance_policy = None

    return {"gridworld": gridworld, "epsilon": epsilon,
        "discount_factor": discount_factor, "utilities": utilities,
        "policy": policy, "convergance_utility": num_convergance_utility,
        "convergance_policy": num_convergance_policy}

def q3():
    # TODO: Replace the None values here based on the questions in the PDF.
    #       DO NOT change anything besides these None values when you submit.
    #       However, you may add print statements if it helps.
    gridworld = None
    epsilon = None
    discount_factor = None

    print("\n", '─' * 50, "\n", "Question 3")
    utilities, policy = mdp.utils_and_policy(gridworld, discount_factor, epsilon)

    # TODO: Enter one of the following answer choices below: "a", "b", "c", "d"
    changed_policy_answer = None

    return {"gridworld": gridworld, "epsilon": epsilon,
        "discount_factor": discount_factor,"utilities": utilities,
        "policy": policy, "letter_answer": changed_policy_answer}

def q4():
    # TODO: Replace the None values here based on the questions in the PDF.
    #       DO NOT change anything besides these None values when you submit.
    #       However, you may add print statements if it helps.
    gridworld = None
    epsilon = None
    discount_factor = None

    print("\n", '─' * 50, "\n", "Question 4")
    utilities, policy = mdp.utils_and_policy(gridworld, discount_factor, epsilon)

    # TODO: Enter one of the following answer choices below: "a", "b", "c", "d"
    changed_policy_answer = None

    return {"gridworld": gridworld, "epsilon": epsilon,
        "discount_factor": discount_factor,"utilities": utilities,
        "policy": policy, "letter_answer": changed_policy_answer}

def q5():
    # TODO: Replace the None values here based on the questions in the PDF.
    #       DO NOT change anything besides these None values when you submit.
    #       However, you may add print statements if it helps.
    gridworld = None
    epsilon = None
    discount_factor = None

    print("\n", '─' * 50, "\n", "Question 5")
    utilities, policy = mdp.utils_and_policy(gridworld, discount_factor, epsilon)

    # TODO: Enter one of the following answer choices below: "a", "b", "c", "d"
    changed_policy_answer = None

    return {"gridworld": gridworld, "epsilon": epsilon,
        "discount_factor": discount_factor,"utilities": utilities,
        "policy": policy, "letter_answer": changed_policy_answer}


##########################

if __name__ == "__main__":
    # You may change the code here as the autograder will not run it.
    # We provide an example so you can see the general functionality of the
    # question functions.

    # By default we run all the question functions, so you will get an output even
    # if you haven't started one of them.

    # Usage example
    print("Given Example")
    gridworld_example = mdp.MDP(2, 3,
                    rewards={ (1, 2): -2, (3, 2): 2},
                    terminals=[(1, 2), (3, 2)],
                    prob_forw=0.8)
    epsilon = 0.01
    discount_factor = 0.9
    utilities = mdp.utils_and_policy(gridworld_example, discount_factor, epsilon)

    # Questions
    q1_and_2_results = q1_and_2()
    q3_results = q3()
    q4_results = q4()
    q5_results = q5()

