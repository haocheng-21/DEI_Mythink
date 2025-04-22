import numpy as np
import random
from tqdm import tqdm

def strict_portion(num_A, num_B, selection_n, loc_A, scale_A, loc_B, scale_B):
    # Generate normally distributed scores

    scores_A = np.random.normal(loc=loc_A, scale=scale_A, size=num_A)  # Scores for group A, mean=70, std=10
    scores_B = np.random.normal(loc=loc_B, scale=scale_B, size=num_B)  # Scores for group B, mean=60, std=15

    # Create labels for group A and B
    people_A = [('A', score) for score in scores_A]
    people_B = [('B', score) for score in scores_B]

    # Combine group A and B
    all_people = people_A + people_B

    # Randomly select 200 people
    random.shuffle(all_people)
    selected = all_people[:selection_n]

    # Sort by score in descending order
    selected.sort(key=lambda x: x[1], reverse=True)

    # Select the top 4 A and 1 B from the selected group
    result_A = []
    result_B = []
    for person in selected:
        if person[0] == 'A' and len(result_A) < 4:
            result_A.append(person)
        elif person[0] == 'B' and len(result_B) < 1:
            result_B.append(person)
        if len(result_A) == 4 and len(result_B) == 1:
            break

    # Output results (commented out)
    # print("Top 4 A scores:")
    # for person in result_A:
    #     print(f"Type: {person[0]}, Score: {person[1]:.2f}")
    #
    # print("\nTop 1 B score:")
    # for person in result_B:
    #     print(f"Type: {person[0]}, Score: {person[1]:.2f}")

    # print(scores_A.mean())
    # print(scores_B.mean())

    return result_A, result_B


def monte_carlo_simulation(num_trials,
                           num_A, num_B,
                           selection_n=200,
                           loc_A=70, scale_A=10,
                           loc_B=70, scale_B=10):
    differences = []

    np.random.seed(42)  # Set random seed to ensure reproducibility

    for _ in tqdm(range(num_trials), desc="Monte Carlo Simulation Progress"):
        result_A, result_B = strict_portion(num_A, num_B, selection_n, loc_A, scale_A, loc_B, scale_B)
        avg_score_A = np.mean([score for _, score in result_A])  # Calculate average score of result_A
        score_B = result_B[0][1]  # Get score of the single element in result_B
        difference = avg_score_A - score_B  # Calculate the difference
        differences.append(difference)

    avg_difference = np.mean(differences)  # Calculate the average of all differences
    return avg_difference

# Run Monte Carlo experiment
num_trials = 100000
num_A = 10000
num_B = 1000
avg_difference = monte_carlo_simulation(num_trials, num_A, num_B)
print(f"After {num_trials} Monte Carlo trials, the average difference between result_A's average score and result_B's score is: {avg_difference:.4f}")
