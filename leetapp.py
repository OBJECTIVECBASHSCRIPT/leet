import random

class NumericPatternGame:
    def __init__(self):
        self.difficulty = 1
        self.score = 0

    def generate_pattern(self):
        pattern = [random.randint(1, self.difficulty*9) for _ in range(self.difficulty)]
        return pattern

    def play(self):
        while True:
            print(f"Current difficulty level: {self.difficulty}")
            print(f"Your current score: {self.score}")
            pattern = self.generate_pattern()
            print("Pattern:", pattern)
            user_input = input("Enter the next number in the pattern (or 'q' to quit): ")
            if user_input == "q":
                break
            try:
                user_answer = int(user_input)
                correct_answer = self.calculate_next_number(pattern)
                if user_answer == correct_answer:
                    print("Correct!")
                    self.score += 1
                    self.difficulty = min(self.difficulty + 1, 5) # Max difficulty level is 5
                else:
                    print("Incorrect.")
                    self.difficulty = max(self.difficulty - 1, 1) # Min difficulty level is 1
            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")
        print("Game over. Your final score:", self.score)

    def calculate_next_number(self, pattern):
        if len(pattern) == 1:
            return pattern[0] + random.randint(1, 9)
        elif all(x - y == pattern[1] - pattern[0] for x, y in zip(pattern[1:], pattern)):
            # If the pattern is an arithmetic sequence
            return pattern[-1] + (pattern[1] - pattern[0])
        else:
            # For simplicity's sake, we'll just add a random number for other patterns
            return pattern[-1] + random.randint(1, 9)

if __name__ == "__main__":
    game = NumericPatternGame()
    game.play()
