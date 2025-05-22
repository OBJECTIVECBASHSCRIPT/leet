import random
import sys

class LeetGame:
    def __init__(self):
        self.level = 1
        self.flags = []
        self.lives = 2
        self.multiplier = 1
        self.running = True

    def start(self):
        print("leet: h4x0r edition")
        print("Mode: Survival")
        while self.running:
            self.play_level()

    def play_level(self):
        pattern, answer, idx = self.generate_pattern()
        display = [str(val) if i != idx else "___" for i, val in enumerate(pattern)]

        print(f"\nLevel {self.level} | Lives: {int(self.lives)} | Flags: {len(self.flags)}")
        print("Pattern:", ", ".join(display))

        user_input = input("Your answer (or 'q' to quit): ").strip()
        if user_input.lower() == 'q':
            self.quit_game("Game Quit")
            return

        try:
            if int(user_input) == answer:
                flag = self.generate_flag()
                self.flags.append(flag)
                print(f"✅ Correct! FLAG UNLOCKED: {flag}")
                self.level += 1
                if self.level > 255:
                    self.quit_game("MAX LEVEL REACHED")
            else:
                print(f"❌ Incorrect. The answer was {answer}.")
                self.lives -= 1
                if self.lives <= 0:
                    self.quit_game("Game Over")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

    def generate_pattern(self):
        is_geo = self.level % 2 == 0
        start = random.randint(2, 6)
        step = random.randint(2, 5) + self.level // 10
        length = min(6 + self.level // 10, 10)
        seq = [start]
        for _ in range(1, length):
            seq.append(seq[-1] * step if is_geo else seq[-1] + step)
        idx = random.randint(1, length - 2)
        return seq, seq[idx], idx

    def generate_flag(self):
        suffix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=4))
        return f"FLAG-L{self.level}-{suffix}"

    def quit_game(self, message):
        print(f"\n{message}")
        print(f"Total Flags: {len(self.flags)}")
        print(f"Total Points: {len(self.flags) * 10 * self.multiplier}")
        self.running = False

if __name__ == "__main__":
    game = LeetGame()
    game.start()
